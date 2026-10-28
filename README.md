# Group 04: Amharic Clinical QA and Medical Text Summarization Assistant

This repository prepares public Amharic medical text for future clinical question
answering and summarization experiments. The current scope is limited to data
collection, normalization and cleaning, and tokenizer evaluation.

## Status

Phase 1 source investigation is recorded in [docs/data-sources.md](docs/data-sources.md).
No dataset is treated as approved merely because it is discoverable: the source
registry records license evidence and the collection code refuses sources that are
not explicitly approved.

## Planned layout

- `data/raw/`: downloaded source data and collection manifests
- `data/interim/`: intermediate files
- `data/processed/`: records with original and normalized text
- `data/tokenized/`: tokenizer artifacts and evaluation reports
- `src/`: collection, preprocessing, tokenization, and utility modules
- `tests/`: unit tests

The implementation will not fine-tune a model or deploy Gradio in this scope.

## Development

Use Python 3.10+ and install the pinned dependency ranges:

```powershell
python -m pip install -r requirements.txt
```

Run the tests:

```powershell
pytest -q
```

Once a registry source has both explicit license approval and a retrievable data
file, collect a bounded sample before scaling:

```python
from src.collection.dataset_loader import collect_huggingface_dataset
from src.collection.source_registry import load_sources

sources = load_sources("configs/sources.json")
collect_huggingface_dataset(
		sources["<approved-source-id>"],
		"data/raw",
		max_records=25,
)
```

Process a collected JSONL file:

```python
import json
from src.preprocessing.pipeline import process_jsonl

config = json.load(open("configs/normalization.json", encoding="utf-8"))
process_jsonl("data/raw/source.jsonl", "data/processed/source.jsonl", config)
```

Train a custom tokenizer only after real processed text exists. Do not substitute
it into mT5 or Llama-3 without adapting the model embeddings and validating the
resulting architecture.

## Current status

- Completed: Phase 1 source registry and architecture.
- Completed: license and approval gates, schema mapping, provenance manifests, and
	robots-aware web collector.
- Completed: conservative NFC/Fidel normalization, HTML/noise cleaning, duplicate
	handling, original-text preservation, and unit tests.
- Completed: BPE and WordPiece training modules plus tokenizer metrics and comparison
	support.
- Blocked: raw and processed medical datasets, tokenizer artifacts, and empirical
	tokenizer comparison. The verified medical QA repository currently has no data
	files, and held sources lack sufficient license evidence.
