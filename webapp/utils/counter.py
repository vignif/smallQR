"""File-based persistent counter utilities."""
from __future__ import annotations
import threading
from pathlib import Path

_lock = threading.Lock()


def get_counter(path: str | Path) -> int:
    p = Path(path)
    try:
        return int(p.read_text().strip())
    except Exception:
        return 0


def increment_counter(path: str | Path) -> int:
    with _lock:
        value = get_counter(path) + 1
        Path(path).write_text(str(value))
        return value
