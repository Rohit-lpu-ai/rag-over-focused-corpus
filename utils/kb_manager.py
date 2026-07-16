"""
Knowledge-base management bridge.

IMPORTANT: This module does NOT modify pyfiles/ (the existing backend).
It builds new, additive orchestration on top of it so the Streamlit
frontend can support incremental document upload and deletion.

Why this exists instead of reusing pyfiles.vector_db.store_embeddings:
That function assigns chunk ids as str(0), str(1), str(2)... starting
from zero on every call. Calling it a second time (e.g. after a user
uploads a second document) would overwrite the first document's
vectors in ChromaDB, because Chroma treats matching ids as upserts.
That behavior is left untouched in pyfiles/ as instructed. Instead,
add_document_to_kb() below inserts with globally-unique ids so
multiple uploads can coexist safely.
"""

import uuid
from pathlib import Path

from pypdf import PdfReader

from pyfiles.chunking import create_chunks
from pyfiles.embedding import generate_embeddings
from pyfiles.vector_db import create_collection

from utils import metadata_store


def _read_pdf(file_path: Path):
    """Extract text and page count from a PDF, matching pyfiles/ingestion.py style."""
    reader = PdfReader(str(file_path))

    pages_text = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages_text)

    return text, len(reader.pages)


def add_document_to_kb(file_path: Path, file_bytes: bytes) -> dict:
    """
    Ingest a single uploaded PDF into the existing ChromaDB collection
    without disturbing previously stored vectors.

    Returns a summary dict: {filename, num_pages, num_chunks}.
    """
    filename = file_path.name

    text, num_pages = _read_pdf(file_path)

    if not text.strip():
        raise ValueError(
            f"No extractable text found in '{filename}'. "
            "It may be a scanned/image-only PDF."
        )

    document = {"filename": filename, "text": text}
    chunks = create_chunks([document])

    if not chunks:
        raise ValueError(f"'{filename}' produced no chunks after splitting.")

    texts = [c["text"] for c in chunks]
    embeddings = generate_embeddings(texts)

    collection = create_collection()

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=[
            {"source": chunk["source"], "chunk_id": chunk["chunk_id"]}
            for chunk in chunks
        ],
    )

    metadata_store.add_entry(
        filename=filename,
        size_bytes=len(file_bytes),
        num_pages=num_pages,
        num_chunks=len(chunks),
        file_bytes=file_bytes,
    )

    return {
        "filename": filename,
        "num_pages": num_pages,
        "num_chunks": len(chunks),
    }


def delete_document_from_kb(source_name: str) -> int:
    """
    Remove all chunks belonging to `source_name` from ChromaDB and
    from the metadata store. Returns the number of chunks removed.
    """
    collection = create_collection()

    results = collection.get(where={"source": source_name})
    ids = results.get("ids", [])

    if ids:
        collection.delete(ids=ids)

    metadata_store.remove_entry(source_name)

    return len(ids)


def list_kb_documents() -> list[dict]:
    """
    List every document currently present in the vector store, merging
    in richer metadata where available (uploads made through this app)
    and falling back gracefully for documents that were ingested
    another way (e.g. the original notebook pipeline).
    """
    collection = create_collection()

    all_meta = collection.get(include=["metadatas"])
    metadatas = all_meta.get("metadatas", []) or []

    chunk_counts: dict[str, int] = {}
    for meta in metadatas:
        if not meta:
            continue
        source = meta.get("source", "Unknown")
        chunk_counts[source] = chunk_counts.get(source, 0) + 1

    stored_metadata = metadata_store.load_metadata()

    documents = []
    for source, chunk_count in sorted(chunk_counts.items()):
        entry = stored_metadata.get(source, {})
        documents.append({
            "filename": source,
            "num_chunks": chunk_count,
            "size_bytes": entry.get("size_bytes"),
            "upload_date": entry.get("upload_date"),
            "num_pages": entry.get("num_pages"),
        })

    return documents


def get_kb_stats() -> dict:
    """High-level stats for the dashboard."""
    collection = create_collection()

    total_chunks = collection.count()
    documents = list_kb_documents()

    return {
        "total_documents": len(documents),
        "total_chunks": total_chunks,
        "total_embeddings": total_chunks,
    }
