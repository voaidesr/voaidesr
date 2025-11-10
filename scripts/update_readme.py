#!/usr/bin/env python3
"""Update the README refresh marker with the current UTC timestamp."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
START = "<!--stats-update-->"
END = "<!--/stats-update-->"
REMOTE_IMG_PATTERN = re.compile(
    r'(https://(?:github-readme-stats\.vercel\.app|streak-stats\.demolab\.com|'
    r'github-profile-summary-cards\.vercel\.app)[^\s"]*)'
)


def main() -> None:
    timestamp = datetime.now(timezone.utc)
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M UTC")
    cache_bust = timestamp.strftime("%Y%m%d%H%M%S")
    replacement = f"{START}\n_Last updated: {timestamp_str}_\n{END}"

    text = README.read_text()
    text = _refresh_cache_busters(text, cache_bust)
    pattern = re.compile(
        rf"{re.escape(START)}.*?{re.escape(END)}", flags=re.DOTALL
    )

    if pattern.search(text):
        updated = pattern.sub(replacement, text)
    else:
        updated = text.rstrip() + "\n\n" + replacement + "\n"

    README.write_text(updated)


def _refresh_cache_busters(text: str, cache_bust: str) -> str:
    def replace_url(match: re.Match[str]) -> str:
        url = match.group(1)
        url = re.sub(r'([?&])cache_bust=\d+', r'\1', url)
        url = url.replace('?&', '?').replace('&&', '&')
        url = re.sub(r'[?&]+$', '', url)
        sep = '&' if '?' in url else '?'
        return f"{url}{sep}cache_bust={cache_bust}"

    return REMOTE_IMG_PATTERN.sub(replace_url, text)


if __name__ == "__main__":
    main()
