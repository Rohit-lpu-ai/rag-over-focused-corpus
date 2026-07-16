"""
Simple JSON-backed usage stats tracker (query count, response times).

Additive only -- does not touch pyfiles/ backend logic.
"""

import json
from pathlib import Path
from datetime import datetime, timezone

STATS_PATH = Path("data") / "usage_stats.json"

_DEFAULT_STATS = {
    "query_count": 0,
    "total_response_time_sec": 0.0,
    "last_updated": None,
}


def _ensure_parent():
    STATS_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_stats() -> dict:
    _ensure_parent()

    if not STATS_PATH.exists():
        return dict(_DEFAULT_STATS)

    try:
        with open(STATS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            merged = dict(_DEFAULT_STATS)
            merged.update(data)
            return merged
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT_STATS)


def save_stats(data: dict) -> None:
    _ensure_parent()

    with open(STATS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def record_query(response_time_sec: float) -> None:
    data = load_stats()

    data["query_count"] += 1
    data["total_response_time_sec"] += response_time_sec
    data["last_updated"] = datetime.now(timezone.utc).isoformat()

    save_stats(data)


def get_summary() -> dict:
    data = load_stats()

    count = data["query_count"]
    avg = (data["total_response_time_sec"] / count) if count else 0.0

    return {
        "query_count": count,
        "avg_response_time_sec": avg,
        "last_updated": data["last_updated"],
    }
