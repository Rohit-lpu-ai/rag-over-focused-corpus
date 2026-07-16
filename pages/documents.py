"""Document manager: upload, inspect, and remove PDFs from the knowledge base."""

import time
from pathlib import Path

import streamlit as st

from utils import kb_manager, metadata_store
from utils.constants import APP_NAME

UPLOAD_DIR = Path("data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _format_size(num_bytes) -> str:
    if not num_bytes:
        return "n/a"
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.0f} {unit}" if unit == "B" else f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


def _format_date(iso_str) -> str:
    if not iso_str:
        return "n/a"
    return iso_str.split("T")[0]


@st.dialog("Confirm deletion")
def _confirm_delete(filenames: list) -> None:
    label = filenames[0] if len(filenames) == 1 else f"{len(filenames)} documents"
    st.write(f"Are you sure you want to delete **{label}**?")
    st.caption("This removes the file, its chunks, and its embeddings from the knowledge base.")
    c1, c2 = st.columns(2)
    if c1.button("Cancel", use_container_width=True):
        st.rerun()
    if c2.button("Delete", type="primary", use_container_width=True):
        for name in filenames:
            kb_manager.delete_document_from_kb(name)
            local_path = UPLOAD_DIR / name
            if local_path.exists():
                local_path.unlink()
        st.session_state.selected_docs = []
        st.toast(f"Deleted {label}.", icon="🗑️")
        st.rerun()


st.markdown(
    f"""
    <div class="page-hero">
        <div class="eyebrow">Knowledge base</div>
        <div class="brand-title">📂 Document Manager</div>
        <div class="brand-subtitle">Upload, inspect, and manage the PDFs {APP_NAME} learns from.</div>
        <div class="pill-row">
            <span class="score-pill">PDF ingestion</span>
            <span class="score-pill">Chunked indexing</span>
            <span class="score-pill">Quick cleanup</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# Upload
# -------------------------------------------------
st.markdown("#### Upload a document")
uploaded_file = st.file_uploader("Drag and drop a PDF here, or click to browse", type=["pdf"])

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    duplicate_of = metadata_store.is_duplicate(file_bytes)

    if duplicate_of:
        st.warning(f"This file matches an already-indexed document: **{duplicate_of}**. Skipped.", icon="⚠️")
    elif st.session_state.get("last_uploaded") == uploaded_file.name:
        st.info("Already processed in this session.")
    else:
        steps = ["Uploading...", "Reading PDF...", "Creating chunks...", "Generating embeddings...",
                 "Updating vector database...", "Knowledge base updated"]
        progress = st.progress(0, text=steps[0])
        try:
            file_path = UPLOAD_DIR / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(file_bytes)
            progress.progress(20, text=steps[1])
            time.sleep(0.15)
            progress.progress(40, text=steps[2])

            progress.progress(60, text=steps[3])
            summary = kb_manager.add_document_to_kb(file_path, file_bytes)

            progress.progress(85, text=steps[4])
            time.sleep(0.15)
            progress.progress(100, text=steps[5])

            st.session_state.last_uploaded = uploaded_file.name
            st.toast(f"{summary['filename']} indexed ({summary['num_chunks']} chunks).", icon="✅")
            st.success(
                f"✅ **{summary['filename']}** uploaded and indexed "
                f"({summary['num_pages']} pages · {summary['num_chunks']} chunks)."
            )
        except Exception as e:
            st.error(f"Failed to process {uploaded_file.name}: {e}")

st.divider()

# -------------------------------------------------
# Document list
# -------------------------------------------------
st.markdown("#### Indexed documents")

try:
    documents = kb_manager.list_kb_documents()
except Exception as e:
    documents = []
    st.error(f"Could not load the knowledge base: {e}")

if "selected_docs" not in st.session_state:
    st.session_state.selected_docs = []

if not documents:
    st.info("No documents indexed yet. Upload a PDF above to get started.")
else:
    header = st.columns([0.5, 3, 1.3, 1.3, 1, 1])
    for col, label in zip(header, ["", "Document", "Size", "Uploaded", "Pages", ""]):
        col.markdown(f"**{label}**")

    for doc in documents:
        c0, c1, c2, c3, c4, c5 = st.columns([0.5, 3, 1.3, 1.3, 1, 1])
        checked = c0.checkbox("", key=f"chk_{doc['filename']}", label_visibility="collapsed")
        if checked and doc["filename"] not in st.session_state.selected_docs:
            st.session_state.selected_docs.append(doc["filename"])
        if not checked and doc["filename"] in st.session_state.selected_docs:
            st.session_state.selected_docs.remove(doc["filename"])

        c1.write(f"📄 {doc['filename']}")
        c2.write(_format_size(doc.get("size_bytes")))
        c3.write(_format_date(doc.get("upload_date")))
        c4.write(doc.get("num_pages") if doc.get("num_pages") is not None else "n/a")
        if c5.button("🗑️", key=f"del_{doc['filename']}"):
            _confirm_delete([doc["filename"]])

    if st.session_state.selected_docs:
        st.write("")
        if st.button(
            f"🗑️ Delete {len(st.session_state.selected_docs)} selected",
            type="primary",
        ):
            _confirm_delete(list(st.session_state.selected_docs))
