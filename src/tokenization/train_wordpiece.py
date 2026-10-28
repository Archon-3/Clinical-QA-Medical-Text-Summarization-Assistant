"""Train a custom WordPiece tokenizer from processed UTF-8 text."""

from __future__ import annotations

from pathlib import Path

from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, trainers


def train_wordpiece(
    text_files: list[str | Path], output_path: str | Path, vocab_size: int = 8000
) -> Path:
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    tokenizer.normalizer = normalizers.NFC()
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.WordPieceTrainer(
        vocab_size=vocab_size,
        min_frequency=2,
        special_tokens=["[UNK]", "[PAD]", "[BOS]", "[EOS]"],
    )
    tokenizer.train([str(path) for path in text_files], trainer)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(destination))
    return destination