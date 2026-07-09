from sentence_transformers import SentenceTransformer

# Load the embedding model once
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def generate_embeddings(texts):
    """
    Generate embeddings for a list of text chunks.

    Args:
        texts (list[str]): List of text strings.

    Returns:
        numpy.ndarray: Embedding vectors.
    """

    embeddings = embedding_model.encode(
        texts,
        show_progress_bar=True,
    )

    return embeddings