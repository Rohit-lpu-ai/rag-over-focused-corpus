# Document Q&A — RAG over a Focused Corpus

## Problem Statement

**I2 — Document Q&A: RAG over a Focused Corpus**

## Segment

**Foundations of Applied Machine Learning**

## Author

**Rohit Sharma**
B.Tech AI & Data Engineering
Lovely Professional University

---

## 📖 Project Overview

This project implements a Retrieval-Augmented Generation (RAG) based Question Answering system over a focused collection of documents.

The system allows users to upload and query documents in natural language and receive context-aware answers generated using Large Language Models (LLMs) and semantic search.

---

## Problem Statement

Traditional LLMs suffer from hallucination and lack access to domain-specific knowledge.

This project solves this problem by:

* Retrieving relevant information from a focused corpus.
* Providing grounded answers based on retrieved context.
* Displaying source citations for transparency.

---

## 🚀 Features

* PDF document ingestion
* Automatic text extraction
* Intelligent chunking strategy
* Semantic search using embeddings
* Vector database storage
* Context-aware answer generation
* Source citation support
* User-friendly interface
* Evaluation pipeline

---

## Architecture

Documents
↓
Document Loader
↓
Text Chunking
↓
Embedding Generation
↓
Vector Database
↓
Retriever
↓
LLM
↓
Answer Generation

---

## Tech Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| Framework            | LangChain             |
| Embedding Model      | Sentence Transformers |
| Vector Database      | ChromaDB              |
| LLM                  | OpenAI GPT            |
| Frontend             | Streamlit             |
| PDF Processing       | PyMuPDF               |
| Deployment           | Streamlit Cloud       |

---

## 🏗️ Project Structure

```text
rag-over-focused-corpus/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── ingest.py
│   ├── chunk.py
│   ├── embed.py
│   ├── retrieve.py
│   └── generate.py
│
├── docs/
│   ├── adr/
│   ├── design_doc.md
│   └── architecture.png
│
├── tests/
│
├── evaluation/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Current Progress

### Completed
- Project setup and repository creation
- PDF ingestion pipeline using PyPDF
- Document loading from local corpus
- Text chunking using RecursiveCharacterTextSplitter
- Embedding generation using BGE Small (`BAAI/bge-small-en-v1.5`)
- Created 103 semantic chunks from the document corpus
- Generated embeddings of shape `(103, 384)`

### In Progress
- Vector database integration using ChromaDB
- Semantic retrieval pipeline

### Upcoming
- LLM integration
- Citation support
- Streamlit UI
- Evaluation framework
- Compare Two Documents feature
---

# Week 2 Learning Summary

- Learned the fundamentals of Retrieval-Augmented Generation (RAG).
- Explored PDF parsing and document ingestion using PyPDF.
- Implemented text chunking using LangChain text splitters.
- Generated semantic embeddings using the BGE embedding model.
- Learned the difference between keyword search and semantic search.
- Gained hands-on experience with Git, GitHub, and Jupyter notebooks.
- Successfully processed documents into 103 chunks with 384-dimensional embeddings.
- Adopted a modular notebook-based workflow for building the RAG pipeline.
## Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/rag-over-focused-corpus.git
cd rag-over-focused-corpus
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/MacOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

---

## Data Source

The project uses a focused corpus of documents for retrieval and question answering.

Corpus:

* To be finalized.

---

## Example Questions

* What are the deliverables for Week 2?
* What is the late submission policy?
* How many ADRs are required?
* What are the requirements for Milestone 1?

---

## Evaluation

The system will be evaluated using:

* Retrieval accuracy
* Answer relevance
* Context precision
* Context recall
* Faithfulness

---

## Mini Extension

Planned extension:

* Multi-document comparison support
* Comparative answers across multiple PDFs

---

## Tests

Run tests using:

```bash
pytest
```

---

## Known Limitations

* Supports English documents only.
* Performance may decrease for extremely large corpora.
* Currently optimized for PDF documents.

---

## Future Work

* Hybrid search (BM25 + Dense Retrieval)
* Re-ranking
* Multi-modal support
* Agentic workflows

---

## ADRs

Architecture Decision Records are stored in:

```text
docs/adr/
```

---

## 3rd Year Extension Plan

This project will be extended in third year by:

* Adding enterprise-scale document ingestion
* Supporting multiple data sources
* Adding fine-tuning
* Introducing agentic retrieval pipelines

---

## License

MIT License

---

## Acknowledgements

* Futurense Technologies Internship Program
* Open Source Community
* LangChain Community
