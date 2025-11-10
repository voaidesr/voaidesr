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


def main() -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    replacement = f"{START}\n_Last updated: {timestamp}_\n{END}"

    text = README.read_text()
    pattern = re.compile(
        rf"{re.escape(START)}.*?{re.escape(END)}", flags=re.DOTALL
    )

    if pattern.search(text):
        updated = pattern.sub(replacement, text)
    else:
        updated = text.rstrip() + "\n\n" + replacement + "\n"

    README.write_text(updated)


if __name__ == "__main__":
    main()
