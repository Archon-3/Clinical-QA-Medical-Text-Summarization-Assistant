"""Unicode and configurable Fidel normalization."""

from __future__ import annotations

import json
import unicodedata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class NormalizationResult:
    """Normalized text with an audit trail of applied operations."""

    text: str
    operations: tuple[str, ...]


def load_normalization_config(path: str | Path) -> dict[str, object]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_unicode_and_fidel(
    text: str,
    config: dict[str, object],
) -> NormalizationResult:
    """Apply NFC and explicitly configured character substitutions."""

    normalized = unicodedata.normalize("NFC", text)
    operations: list[str] = []
    if normalized != text:
        operations.append("unicode_nfc")

    fidel_map = config.get("fidel_map", {})
    if not isinstance(fidel_map, dict):
        raise ValueError("fidel_map must be an object")
    mapped = "".join(str(fidel_map.get(character, character)) for character in normalized)
    if mapped != normalized:
        operations.append("fidel_homophone_normalization")
    return NormalizationResult(mapped, tuple(operations))