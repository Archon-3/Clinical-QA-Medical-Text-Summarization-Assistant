"""Small, robots-aware collector for explicitly approved public web pages."""

from __future__ import annotations

import json
import logging
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .source_registry import Source, require_approved

LOGGER = logging.getLogger(__name__)
USER_AGENT = "Group04-AmharicMedicalNLP/0.1 (academic research; contact repository owner)"


def fetch_public_page(source: Source, output_dir: str | Path, timeout: int = 20) -> Path:
    """Fetch one approved public page after checking its site's robots.txt."""

    require_approved(source)
    if source.source_type != "web":
        raise ValueError(f"Source {source.id} is not a web page")

    parsed = urlparse(source.source_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    robots = urllib.robotparser.RobotFileParser(robots_url)
    robots.read()
    if not robots.can_fetch(USER_AGENT, source.source_url):
        raise PermissionError(f"robots.txt disallows collection: {source.source_url}")

    response = requests.get(
        source.source_url,
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "noscript"]):
        element.decompose()
    text = " ".join(soup.stripped_strings)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    path = output_path / f"{source.id}.json"
    path.write_text(
        json.dumps(
            {
                "source_id": source.id,
                "source_url": source.source_url,
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "license": source.license,
                "text": text,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    LOGGER.info("Fetched public page %s", source.source_url)
    return path