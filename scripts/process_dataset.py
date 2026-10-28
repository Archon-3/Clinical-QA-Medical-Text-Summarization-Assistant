"""Normalize and deduplicate one collected JSONL file."""

from __future__ import annotations

import argparse
import json

from src.preprocessing.pipeline import process_jsonl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Collected JSONL path under data/raw")
    parser.add_argument("output", help="Processed JSONL path under data/processed")
    args = parser.parse_args()
    with open("configs/normalization.json", encoding="utf-8") as handle:
        config = json.load(handle)
    print(process_jsonl(args.input, args.output, config))


if __name__ == "__main__":
    main()