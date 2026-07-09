from pyfiles.ingestion import load_documents
from pyfiles.chunking import create_chunks
from pyfiles.embedding import generate_embeddings
from pyfiles.vector_db import store_embeddings
from pyfiles.retrieval import retrieve_documents
from pyfiles.generation import generate_answer

print("=" * 60)
print("Testing Ingestion...")
docs = load_documents()
print(f"Loaded {len(docs)} documents")

print("=" * 60)
print("Testing Chunking...")
chunks = create_chunks(docs)
print(f"Created {len(chunks)} chunks")

print("=" * 60)
print("Testing Embeddings...")
texts = [chunk["text"] for chunk in chunks]
embeddings = generate_embeddings(texts)
print(f"Generated {len(embeddings)} embeddings")

print("=" * 60)
print("Testing Vector DB...")
collection = store_embeddings(chunks, embeddings)
print(f"Collection Count: {collection.count()}")

print("=" * 60)
print("Testing Retrieval...")
results = retrieve_documents(
    "What is Retrieval-Augmented Generation?"
)

print(f"Retrieved {len(results)} chunks")

print("=" * 60)
print("Testing Generation...")
answer = generate_answer(
    "What is Retrieval-Augmented Generation?",
    results,
)

print(answer)

print("=" * 60)
print("All tests completed.")