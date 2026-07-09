from pathlib import Path
import chromadb


def get_chroma_client():
    """
    Create or connect to the persistent ChromaDB database.
    """

    current_dir = Path.cwd().resolve()

    candidate_paths = [
        current_dir / "data" / "chroma_db",
        current_dir.parent / "data" / "chroma_db",
        current_dir.parent.parent / "data" / "chroma_db",
    ]

    chroma_path = None

    for path in candidate_paths:
        if path.exists():
            chroma_path = path
            break

    if chroma_path is None:
        chroma_path = candidate_paths[0]
        chroma_path.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(chroma_path))

    return client


def create_collection(collection_name="studybuddy_rag"):
    """
    Create or connect to the ChromaDB collection.
    """

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=collection_name
    )

    return collection


def store_embeddings(chunks, embeddings):
    """
    Store chunk embeddings in ChromaDB.
    """

    collection = create_collection()

    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        embeddings=embeddings.tolist(),
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_id": chunk["chunk_id"],
            }
            for chunk in chunks
        ],
    )

    return collection