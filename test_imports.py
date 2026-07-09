from pyfiles.ingestion import *
from pyfiles.chunking import *
from pyfiles.embedding import *
from pyfiles.vector_db import *
from pyfiles.retrieval import *
from pyfiles.generation import *

print("✅ All imports successful!")

from pyfiles.retrieval import retrieve_documents

question = "What is Dynamic CRM Personalization?"

docs = retrieve_documents(question)

print("Retrieved:", len(docs))

for i, doc in enumerate(docs, 1):
    print(f"\nDocument {i}")
    print(doc)