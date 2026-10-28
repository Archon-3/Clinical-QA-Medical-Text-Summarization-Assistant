"""Load comparable pretrained tokenizers without changing model embeddings."""

from __future__ import annotations

from typing import Any


def compare_pretrained_tokenizers(texts: list[str], model_names: list[str]) -> list[dict[str, Any]]:
    """Return measured counts for each tokenizer; downloads are caller-controlled."""

    from transformers import AutoTokenizer

    results: list[dict[str, Any]] = []
    for model_name in model_names:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        encoded = tokenizer(texts, add_special_tokens=True, truncation=False)
        token_counts = [len(ids) for ids in encoded["input_ids"]]
        words = sum(len(text.split()) for text in texts)
        results.append(
            {
                "tokenizer": model_name,
                "vocabulary_size": len(tokenizer),
                "average_sequence_length": sum(token_counts) / len(token_counts),
                "average_tokens_per_word": sum(token_counts) / max(words, 1),
                "unknown_token_frequency": sum(
                    token == tokenizer.unk_token_id
                    for ids in encoded["input_ids"]
                    for token in ids
                )
                / max(sum(token_counts), 1),
            }
        )
    return results