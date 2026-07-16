"""
Lightweight JSON-backed metadata store for uploaded documents.

This module is purely additive: it does not modify any existing
backend logic in pyfiles/. It exists to track presentation-layer
metadata (file size, upload date, page count, dedupe hash) that the
original backend has no concept of.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

METADATA_PATH = Path("data") / "doc_metadata.json"


def _ensure_parent():
    METADATA_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_metadata() -> dict:
    """Load the full metadata dict, keyed by filename."""
    _ensure_parent()

    if not METADATA_PATH.exists():
        return {}

    try:
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_metadata(data: dict) -> None:
    _ensure_parent()

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def file_hash(file_bytes: bytes) -> str:
    """Content hash used for duplicate-file detection."""
    return hashlib.md5(file_bytes).hexdigest()


def is_duplicate(file_bytes: bytes) -> str | None:
    """
    Return the filename of an existing document with identical content,
    or None if no duplicate exists.
    """
    h = file_hash(file_bytes)
    data = load_metadata()

    for filename, entry in data.items():
        if entry.get("file_hash") == h:
            return filename

    return None


def add_entry(filename: str, size_bytes: int, num_pages: int,
              num_chunks: int, file_bytes: bytes) -> None:
    data = load_metadata()

    data[filename] = {
        "size_bytes": size_bytes,
        "upload_date": datetime.now(timezone.utc).isoformat(),
        "num_pages": num_pages,
        "num_chunks": num_chunks,
        "file_hash": file_hash(file_bytes),
    }

    save_metadata(data)


def remove_entry(filename: str) -> None:
    data = load_metadata()

    if filename in data:
        del data[filename]
        save_metadata(data)


def get_entry(filename: str) -> dict | None:
    return load_metadata().get(filename)
