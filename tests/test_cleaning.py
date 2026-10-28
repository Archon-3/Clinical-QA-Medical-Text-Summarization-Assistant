from src.preprocessing.deduplication import deduplicate_records


def test_deduplication_removes_empty_and_duplicate_records():
    records = [
        {"id": "1", "normalized_text": "አንድ"},
        {"id": "2", "normalized_text": ""},
        {"id": "3", "normalized_text": " አንድ "},
    ]

    kept, stats = deduplicate_records(records)

    assert [record["id"] for record in kept] == ["1"]
    assert stats == {"input": 3, "empty_removed": 1, "duplicates_removed": 1, "kept": 1}