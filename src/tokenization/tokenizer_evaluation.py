"""Evaluate tokenization behavior on actual text records."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def evaluate_tokenizer(tokenizer: Any, texts: Iterable[str]) -> dict[str, float | int]:
    """Measure lengths, unknowns, Fidel coverage, and code-switch examples."""

    values = list(texts)
    encoded = [tokenizer.encode(text) for text in values]
    lengths = [len(item.ids) for item in encoded]
    unknown_id = tokenizer.token_to_id("[UNK]")
    unknowns = sum(token == unknown_id for item in encoded for token in item.ids)
    total_tokens = sum(lengths)
    return {
        "records": len(values),
        "vocabulary_size": tokenizer.get_vocab_size(),
        "average_sequence_length": sum(lengths) / max(len(lengths), 1),
        "unknown_token_frequency": unknowns / max(total_tokens, 1),
        "fidel_records": sum(any("\u1200" <= char <= "\u137f" for char in text) for text in values),
        "english_code_switch_records": sum(any("a" <= char.lower() <= "z" for char in text) for text in values),
    }