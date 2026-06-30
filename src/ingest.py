from pathlib import Path
from pypdf import PdfReader


def resolve_data_path() -> Path:
    current_dir = Path.cwd().resolve()
    candidates = [
        current_dir / "data" / "Raw",
        current_dir / "data" / "raw",
        current_dir.parent / "data" / "Raw",
        current_dir.parent / "data" / "raw",
        current_dir.parent.parent / "data" / "Raw",
        current_dir.parent.parent / "data" / "raw",
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "No PDF data folder found. Checked: " + ", ".join(str(p) for p in candidates)
    )


def load_documents():
    data_path = resolve_data_path()
    documents = []

    for pdf_path in sorted(data_path.glob("*.pdf")):
        reader = PdfReader(str(pdf_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        documents.append({"filename": pdf_path.name, "text": text})

    return documents
