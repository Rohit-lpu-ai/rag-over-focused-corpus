# StudyBuddy AI — Document Q&A: RAG over a Focused Corpus

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

Users upload PDF documents through a Streamlit application, ask questions in natural language, and receive context-aware answers grounded in the uploaded content, with every answer traceable back to the exact source chunk it came from.

---

## Problem Statement (Detail)

Traditional LLMs suffer from hallucination and lack access to domain-specific knowledge.

This project addresses that by:

* Retrieving relevant information from a focused corpus using semantic search.
* Providing grounded answers based only on retrieved context.
* Displaying source citations — document, chunk number, and similarity score — for transparency.

---

## 🚀 Features

* Multi-document PDF ingestion via drag-and-drop upload
* Automatic text extraction and duplicate-file detection
* Recursive-character chunking with configurable overlap
* Semantic search using sentence-transformer embeddings
* Persistent vector storage via ChromaDB (documents can be added/removed incrementally)
* Context-aware answer generation via Google Gemini
* Source citation cards (document, chunk #, similarity score, preview)
* Document manager: rename, delete (with confirmation), multi-select bulk delete
* Dashboard with live knowledge-base metrics (documents, chunks, storage used, success rate, avg. response time)
* Configurable generation model and temperature from the Settings page
* Knowledge-base maintenance: rebuild index, clear cache, reset chat, export data
* Light/dark theme with a persistent, app-wide toggle
* Chat history, favorited answers, and full-conversation export
* Evaluation pipeline *(in progress — see Current Progress)*

---

## Architecture

```
Documents
  ↓
Document Loader (pypdf)
  ↓
Text Chunking (LangChain text splitters)
  ↓
Embedding Generation (Sentence-Transformers)
  ↓
Vector Database (ChromaDB)
  ↓
Retriever (semantic similarity search)
  ↓
LLM (Google Gemini)
  ↓
Answer Generation + Source Citations
```

The Streamlit frontend (`app.py` + `pages/`) sits on top of this pipeline and never modifies the core retrieval/generation logic in `pyfiles/` — all document-management, stats, and UI orchestration lives in `utils/` as an additive layer.

---

## Tech Stack

| Component             | Technology                                  |
| ---------------------- | -------------------------------------------- |
| Programming Language   | Python                                       |
| Frontend               | Streamlit (native multipage navigation)      |
| PDF Processing         | pypdf                                        |
| Text Chunking          | LangChain text splitters                     |
| Embedding Model        | Sentence-Transformers (`BAAI/bge-small-en-v1.5`) |
| Vector Database        | ChromaDB (persistent, local)                 |
| LLM                    | Google Gemini (`gemini-2.5-flash`, configurable) |
| Deployment              | Local (Streamlit Cloud planned)              |

---

## 🏗️ Project Structure

```text
RAG focused corpus/
│
├── app.py                       # Streamlit entry point (page config, theme, navigation)
│
├── pages/                       # One file per app page (native st.navigation)
│   ├── chat.py                  # Chat interface, source citations, favorites, export
│   ├── dashboard.py             # Live KB metrics, gauges, response-time trend
│   ├── documents.py             # Document manager: upload, rename, delete
│   ├── settings.py              # Theme, model/temperature, KB maintenance
│   └── about.py                 # Project overview, pipeline diagram, roadmap
│
├── components/                  # Shared UI building blocks
│   ├── styles.py                 # Design system: theme tokens, CSS, animated background
│   └── sidebar.py                # Sidebar: branding, KB status, theme toggle, quick actions
│
├── utils/                        # Additive orchestration layer (does not modify pyfiles/)
│   ├── kb_manager.py              # Multi-document add/delete/rename/rebuild against ChromaDB
│   ├── metadata_store.py          # JSON-backed file metadata + duplicate detection
│   ├── stats_tracker.py           # Query counts, response times, success rate
│   ├── constants.py               # Shared display constants (model names, version)
│   └── html.py                    # Safe HTML injection helper for st.markdown
│
├── pyfiles/                     # Core RAG pipeline (backend — not modified by the frontend)
│   ├── __init__.py
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── vector_db.py
│   ├── retrieval.py
│   └── generation.py
│
├── src/                          # Original Jupyter notebooks (pipeline prototyping)
│   ├── ingest.ipynb
│   ├── chunking.ipynb
│   ├── Embedding.ipynb
│   ├── vector.ipynb
│   ├── retrieval.ipynb
│   ├── generation.ipynb
│   ├── evaluation.ipynb
│   └── ingest.py
│
├── data/
│   ├── raw/                      # Uploaded source PDFs
│   ├── processed/                # chunks.pkl, embeddings.pkl (notebook pipeline artifacts)
│   ├── chroma_db/                 # Persistent ChromaDB store
│   ├── doc_metadata.json          # Per-document metadata (size, pages, upload date, hash)
│   └── usage_stats.json           # Query counts, response times, success rate
│
├── evaluation/                   # Evaluation outputs
├── docs/                         # Project documentation
├── tests/                        # Testing scripts (optional)
│
├── README.md
├── requirements.txt
└── test_imports.py
```

---

## Current Progress

### Completed
- Project setup and repository creation
- PDF ingestion pipeline using pypdf
- Text chunking using `RecursiveCharacterTextSplitter`
- Embedding generation using BGE Small (`BAAI/bge-small-en-v1.5`)
- ChromaDB vector database integration, with support for incremental multi-document add/delete/rename
- Semantic retrieval pipeline
- LLM integration (Google Gemini) with configurable model and temperature
- Source citation support (document, chunk, similarity score)
- Full Streamlit UI: chat, dashboard, document manager, settings, about — with light/dark theming

### In Progress
- Evaluation framework (retrieval accuracy, answer relevance, faithfulness)
- True token-by-token streaming responses

### Upcoming
- In-app PDF preview / page-level citation jump
- Compare Two Documents feature
- Multi-user knowledge bases

---

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

> On Windows, if `python` isn't recognized, use `py -m venv venv` instead.

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

---

## Running the Application

Run from the project root (not from inside `pages/` or `pyfiles/`, since ChromaDB and `data/raw/` paths are resolved relative to the working directory):

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## Data Source

The project uses a focused corpus of PDF documents for retrieval and question answering, uploaded directly through the app's Document Manager. Two sample documents are included under `data/raw/` for testing.

---

## Example Questions

* What is Retrieval-Augmented Generation?
* What are the deliverables for Week 2?
* What is the late submission policy?
* What does the AI/ML report conclude?

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
* Currently optimized for text-based (non-scanned) PDF documents.
* No true token-by-token streaming yet — answers appear once fully generated.

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