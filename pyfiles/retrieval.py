from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model once
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def get_collection():
    """
    Connect to the persistent ChromaDB collection.
    """

    candidate_paths = [
        Path.cwd() / "data" / "chroma_db",
        Path.cwd().parent / "data" / "chroma_db",
        Path.cwd().parent.parent / "data" / "chroma_db",
    ]

    chroma_path = next(
        (path for path in candidate_paths if path.exists()),
        candidate_paths[0],
    )

    client = chromadb.PersistentClient(path=str(chroma_path))

    collection = client.get_or_create_collection(
        name="studybuddy_rag"
    )

    return collection


def retrieve_documents(query, n_results=3):
    """
    Retrieve the most relevant documents from ChromaDB.
    """

    collection = get_collection()

    query_embedding = embedding_model.encode(
        query,
        convert_to_tensor=False,
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = []

    for doc, meta, distance in zip(
        results.get("documents", [[]])[0],
        results.get("metadatas", [[]])[0],
        results.get("distances", [[]])[0],
    ):
        documents.append(
            {
                "text": doc,
                "metadata": meta or {},
                "distance": distance,
            }
        )

    return documents