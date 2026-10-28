# Phase 1: Data Source Investigation

Investigation date: 2026-11-08

## Verified candidates

| Source | Intended use | License evidence | Collection decision |
| --- | --- | --- | --- |
| [Walelign/Amharic_STI_QA_Dataset](https://huggingface.co/datasets/Walelign/Amharic_STI_QA_Dataset) | Amharic health question-answer data | Hugging Face API reports `CC-BY-NC-4.0` | Blocked: collection attempt found no data files in the repository |
| [EthioNLP/Amharic_Instruction_dataset](https://huggingface.co/datasets/EthioNLP/Amharic_Instruction_dataset) | EthioNLP discovery candidate | Dataset is public, but the API result did not expose a license tag | Hold; do not collect until the dataset card states usable terms |
| [rasyosef/xlsum_amharic_summarization](https://huggingface.co/datasets/rasyosef/xlsum_amharic_summarization) | Summarization benchmark candidate | Public dataset found, but license evidence requires dataset-card review | Hold until license and redistribution terms are verified |
| WHO Ethiopia publications | Official health advisories and publications | WHO site is authoritative, but each publication can have its own reuse terms | Discovery source; collect only pages whose terms permit the intended use |
| Ethiopian Ministry of Health | Official Ethiopian health information | Copyright and reuse terms vary by page | Discovery source; respect robots.txt and page-specific terms |

The Hugging Face search endpoint also returned datasets with missing, unclear, or
non-medical licensing metadata. They are intentionally not included as approved
sources. A public URL is not equivalent to permission to redistribute or train on
the material.

## Collection result

On 2026-11-08, the collector attempted a bounded retrieval from
`Walelign/Amharic_STI_QA_Dataset`. Hugging Face returned `EmptyDatasetError`: the
repository revision contained no data files. Therefore `data/raw/` contains no
claimed dataset records. The registry was changed from `approved_research_only`
to `blocked_empty_repository` until the dataset owner publishes a usable file or
an alternative licensed source is verified.

## Collection architecture

1. `configs/sources.json` is the auditable registry. Each source includes an
   identifier, URL, language, document type, license evidence, and approval state.
2. `src/collection/dataset_loader.py` loads approved Hugging Face datasets through
   the `datasets` library, limits records explicitly, normalizes them into the
   project schema, and writes JSONL plus a manifest under `data/raw/`.
3. `src/collection/web_scraper.py` fetches only explicitly registered web pages,
   checks `robots.txt`, uses a descriptive user agent, and stores page metadata and
   extracted text without silently claiming a license.
4. Every run writes a manifest containing collection time, source identifier,
   record count, file checksum, license evidence, and method. Failed or held
   sources produce no raw dataset.

## Limitations and compliance gates

- No private patient data, Telegram private chats, or confidential conversations
  are collected.
- Telegram collection is not enabled by default; it requires a legally permitted
  public channel and a separately reviewed API configuration.
- The first collection run should begin with a small explicit record limit so the
  dataset card, schema, and license are manually inspected before scaling.
- Medical text is research data, not medical advice. The future model must not be
  presented as a clinical decision-maker without separate safety validation.