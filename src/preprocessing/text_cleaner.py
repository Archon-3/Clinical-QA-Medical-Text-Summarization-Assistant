"""Conservative cleaning that preserves clinically meaningful content."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from bs4 import BeautifulSoup

from .unicode_normalizer import normalize_unicode_and_fidel

CONTROL_CHARACTERS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
WHITESPACE = re.compile(r"\s+")


@dataclass(frozen=True)
class CleanedText:
    """Original text, cleaned text, and reproducible operation names."""

    original_text: str
    normalized_text: str
    operations: tuple[str, ...]


def clean_text(text: str, config: dict[str, object]) -> CleanedText:
    """Clean markup and noise without transliterating or deleting medical terms."""

    original = text
    operations: list[str] = []
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(" ")
    if text != original:
        operations.append("html_removed")

    if config.get("remove_control_characters", True):
        cleaned = CONTROL_CHARACTERS.sub("", text)
        if cleaned != text:
            operations.append("control_characters_removed")
        text = cleaned

    normalized = normalize_unicode_and_fidel(text, config)
    operations.extend(normalized.operations)
    compact = WHITESPACE.sub(" ", normalized.text).strip()
    if compact != normalized.text:
        operations.append("whitespace_normalized")

    compact = "".join(
        character for character in compact if unicodedata.category(character) != "Cf"
    )
    if compact != normalized.text and "format_characters_removed" not in operations:
        operations.append("format_characters_removed")
    compact = WHITESPACE.sub(" ", compact).strip()
    return CleanedText(original, compact, tuple(dict.fromkeys(operations)))