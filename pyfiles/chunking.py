from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents, chunk_size=500, chunk_overlap=100):
    """
    Split loaded documents into overlapping chunks.

    Args:
        documents (list): Output from load_documents().
        chunk_size (int): Maximum characters per chunk.
        chunk_overlap (int): Overlap between consecutive chunks.

    Returns:
        list: List of chunk dictionaries.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    chunks = []

    for doc in documents:
        split_chunks = text_splitter.split_text(doc["text"])

        for idx, chunk in enumerate(split_chunks):
            chunks.append(
                {
                    "source": doc["filename"],
                    "chunk_id": idx,
                    "text": chunk,
                }
            )

    return chunks