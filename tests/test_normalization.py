from src.preprocessing.text_cleaner import clean_text


def test_cleaner_preserves_medical_numbers_and_latin_terms():
    config = {"fidel_map": {"ሃ": "ሀ"}, "remove_control_characters": True}
    result = clean_text("<p>ሃኪም 500 mg HIV</p>\u200b", config)

    assert result.original_text == "<p>ሃኪም 500 mg HIV</p>\u200b"
    assert result.normalized_text == "ሀኪም 500 mg HIV"
    assert "fidel_homophone_normalization" in result.operations
    assert "html_removed" in result.operations


def test_cleaner_keeps_code_switched_words():
    config = {"fidel_map": {}, "remove_control_characters": True}
    result = clean_text("የ patient ምልክቶች", config)

    assert result.normalized_text == "የ patient ምልክቶች"