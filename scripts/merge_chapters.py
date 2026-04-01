#!/usr/bin/env python3
"""
Scala rozdziały z docs/chapters/ z powrotem w jeden plik qa_draft.

Kolejność: 00_header.md, potem pliki N_*.md posortowane numerycznie.
Między sekcjami wstawia separator ---

Użycie:
  python scripts/merge_chapters.py                          → docs/qa_draft_v12.md
  python scripts/merge_chapters.py docs/qa_draft_v13.md     → podany plik
"""

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = WORKSPACE / "docs" / "chapters"
DEFAULT_OUTPUT = WORKSPACE / "docs" / "qa_draft_v12.md"

def sort_key(path: Path) -> tuple[int, str]:
    """00_header → (0, 'header'), 01_xxx → (1, 'xxx'), etc."""
    name = path.stem
    m = re.match(r"^(\d+)_(.+)$", name)
    if m:
        return (int(m.group(1)), m.group(2))
    return (999, name)


def merge(output: Path) -> None:
    if not CHAPTERS_DIR.exists():
        print(f"ERROR: Nie znaleziono katalogu {CHAPTERS_DIR}")
        sys.exit(1)

    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"), key=sort_key)

    if not chapter_files:
        print(f"ERROR: Brak plików .md w {CHAPTERS_DIR}")
        sys.exit(1)

    print(f"Źródło:  {CHAPTERS_DIR}/")
    print(f"Cel:     {output}")
    print(f"Plików:  {len(chapter_files)}")
    print()

    parts: list[str] = []
    for f in chapter_files:
        content = f.read_text(encoding="utf-8")
        parts.append(content)
        print(f"  + {f.name}")

    # Proste połączenie — każdy plik zachowuje swoje separatory
    merged = "".join(parts)

    output.write_text(merged, encoding="utf-8")

    line_count = merged.count("\n")
    print(f"\nZapisano: {output} ({line_count} linii)")


def main():
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUTPUT
    merge(output)


if __name__ == "__main__":
    main()
