"""Apply cleaning and deduplication to collected JSONL records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .deduplication import deduplicate_records
from .text_cleaner import clean_text


def process_jsonl(
    input_path: str | Path,
    output_path: str | Path,
    config: dict[str, object],
) -> dict[str, int]:
    """Create processed JSONL while retaining each record's original text."""

    records: list[dict[str, Any]] = []
    with Path(input_path).open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            cleaned = clean_text(str(record.get("original_text") or ""), config)
            record["original_text"] = cleaned.original_text
            record["normalized_text"] = cleaned.normalized_text
            record["normalization_operations"] = list(cleaned.operations)
            record["preprocessing_status"] = "normalized"
            records.append(record)

    kept, stats = deduplicate_records(records)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in kept:
            handle.write(json.dumps(record, ensure_ascii=False))
            handle.write("\n")
    return stats