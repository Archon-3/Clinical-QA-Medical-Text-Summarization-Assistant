"""Deterministic empty-record and duplicate detection."""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from typing import Any


def normalized_key(text: str) -> str:
    return hashlib.sha256(text.strip().casefold().encode("utf-8")).hexdigest()


def deduplicate_records(
    records: Iterable[dict[str, Any]],
    text_field: str = "normalized_text",
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    """Drop empty and exact normalized duplicates, retaining the first record."""

    kept: list[dict[str, Any]] = []
    seen: set[str] = set()
    stats = {"input": 0, "empty_removed": 0, "duplicates_removed": 0, "kept": 0}
    for record in records:
        stats["input"] += 1
        text = str(record.get(text_field) or "").strip()
        if not text:
            stats["empty_removed"] += 1
            continue
        key = normalized_key(text)
        if key in seen:
            stats["duplicates_removed"] += 1
            continue
        seen.add(key)
        kept.append(record)
    stats["kept"] = len(kept)
    return kept, stats