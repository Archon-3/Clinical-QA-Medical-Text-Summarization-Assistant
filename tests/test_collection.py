import pytest

from src.collection.source_registry import load_sources, require_approved


def test_registry_rejects_sources_without_license_approval():
    sources = load_sources("configs/sources.json")

    with pytest.raises(PermissionError):
        require_approved(sources["ethionlp_amharic_instruction"])