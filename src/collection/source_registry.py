"""Load and validate the auditable data source registry."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


APPROVED_STATES = {"approved_research_only"}


@dataclass(frozen=True)
class Source:
    """A registered external data source and its license decision."""

    id: str
    name: str
    source_type: str
    source_identifier: str
    source_url: str
    language: str
    document_type: str
    license: str | None
    license_evidence: str
    approval: str
    collection_method: str

    @property
    def is_approved(self) -> bool:
        return self.approval in APPROVED_STATES and bool(self.license)


def load_sources(path: str | Path) -> dict[str, Source]:
    """Load sources keyed by registry id and reject malformed duplicates."""

    records = json.loads(Path(path).read_text(encoding="utf-8"))
    sources: dict[str, Source] = {}
    for record in records:
        source = Source(**record)
        if source.id in sources:
            raise ValueError(f"Duplicate source id: {source.id}")
        sources[source.id] = source
    return sources


def require_approved(source: Source) -> None:
    """Raise unless a source has an explicit license and approval decision."""

    if not source.is_approved:
        raise PermissionError(
            f"Source {source.id!r} is not approved for collection; "
            "review its license and registry approval first."
        )