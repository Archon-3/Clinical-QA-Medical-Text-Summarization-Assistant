"""Collect a bounded sample from an approved registry source."""

from __future__ import annotations

import argparse

from src.collection.dataset_loader import collect_huggingface_dataset
from src.collection.source_registry import load_sources


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id", help="ID from configs/sources.json")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--split", default="train")
    args = parser.parse_args()

    sources = load_sources("configs/sources.json")
    if args.source_id not in sources:
        raise SystemExit(f"Unknown source ID: {args.source_id}")
    path = collect_huggingface_dataset(
        sources[args.source_id],
        "data/raw",
        max_records=args.limit,
        split=args.split,
    )
    print(f"Saved collected records to {path}")


if __name__ == "__main__":
    main()