"""Download approved Hugging Face datasets into the project schema."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .source_registry import Source, require_approved

LOGGER = logging.getLogger(__name__)


def _first_value(record: dict[str, Any], names: tuple[str, ...]) -> str:
    for name in names:
        value = record.get(name)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def _to_schema(record: dict[str, Any], source: Source, index: int) -> dict[str, Any]:
    """Map common QA, instruction, and text columns without inventing content."""

    question = _first_value(record, ("question", "query", "prompt"))
    answer = _first_value(record, ("answer", "response", "completion", "output"))
    context = _first_value(record, ("context", "passage", "document"))
    text = context or question or _first_value(record, ("text", "document", "instruction"))
    return {
        "id": f"{source.id}-{index:08d}",
        "source": source.name,
        "source_url": source.source_url,
        "language": source.language,
        "document_type": source.document_type,
        "original_text": text,
        "normalized_text": None,
        "collection_date": datetime.now(timezone.utc).date().isoformat(),
        "license": source.license,
        "preprocessing_status": "raw",
        "question": question or None,
        "context": context or None,
        "answer": answer or None,
        "raw_record": record,
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_huggingface_dataset(
    source: Source,
    output_dir: str | Path,
    max_records: int | None = None,
    split: str = "train",
) -> Path:
    """Collect a bounded approved dataset and write JSONL plus a manifest."""

    require_approved(source)
    if source.source_type != "huggingface":
        raise ValueError(f"Source {source.id} is not a Hugging Face dataset")

    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError("Install requirements.txt before collecting datasets") from exc

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    dataset = load_dataset(source.source_identifier, split=split, streaming=True)
    limit = max_records if max_records is not None else float("inf")
    dataset_path = output_path / f"{source.id}.jsonl"
    count = 0
    with dataset_path.open("w", encoding="utf-8") as handle:
        for record in dataset:
            handle.write(json.dumps(_to_schema(dict(record), source, count), ensure_ascii=False))
            handle.write("\n")
            count += 1
            if count >= limit:
                break

    manifest = {
        "source_id": source.id,
        "source_identifier": source.source_identifier,
        "source_url": source.source_url,
        "language": source.language,
        "document_type": source.document_type,
        "license": source.license,
        "collection_method": source.collection_method,
        "collection_date": datetime.now(timezone.utc).isoformat(),
        "records_collected": count,
        "file": dataset_path.name,
        "sha256": _sha256(dataset_path),
    }
    manifest_path = output_path / f"{source.id}.manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    LOGGER.info("Collected %s records from %s", count, source.source_identifier)
    return dataset_path