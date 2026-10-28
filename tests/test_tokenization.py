from tokenizers import Tokenizer

from src.tokenization.train_bpe import train_bpe
from src.tokenization.tokenizer_evaluation import evaluate_tokenizer


def test_custom_bpe_handles_amharic_and_code_switching(tmp_path):
    corpus = tmp_path / "corpus.txt"
    corpus.write_text("የጤና መረጃ HIV 500 mg\nየጤና ጥያቄ", encoding="utf-8")
    path = train_bpe([corpus], tmp_path / "tokenizer.json", vocab_size=64)
    tokenizer = Tokenizer.from_file(str(path))

    metrics = evaluate_tokenizer(tokenizer, ["የጤና መረጃ HIV 500 mg"])

    assert metrics["records"] == 1
    assert metrics["vocabulary_size"] > 4
    assert metrics["fidel_records"] == 1
    assert metrics["english_code_switch_records"] == 1