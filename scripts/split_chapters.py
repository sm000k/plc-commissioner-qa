#!/usr/bin/env python3
"""
Rozdziela qa_draft_v12.md na osobne pliki rozdziałów w docs/chapters/.

Struktura wyjściowa:
  docs/chapters/00_header.md      — nagłówek, spis treści, plan nauki
  docs/chapters/01_podstawy_plc.md
  docs/chapters/02_architektura_safety.md
  ...
  docs/chapters/20_schematy_elektryczne.md

Użycie:
  python scripts/split_chapters.py
  python scripts/split_chapters.py docs/qa_draft_v12.md
"""

import re
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = WORKSPACE / "docs" / "qa_draft_v12.md"
CHAPTERS_DIR = WORKSPACE / "docs" / "chapters"

# Mapowanie numeru sekcji → nazwa pliku (slug)
SECTION_SLUGS = {
    1:  "01_podstawy_plc",
    2:  "02_architektura_safety",
    3:  "03_moduly_fdi_fdo",
    4:  "04_struktury_glosowania",
    5:  "05_passivation_reintegration",
    6:  "06_safe_state",
    7:  "07_profisafe",
    8:  "08_napedy_safety",
    9:  "09_tia_portal_safety",
    10: "10_robot_abb_irc5",
    11: "11_commissioning_diagnostyka",
    12: "12_sicar_napedy",
    13: "13_estop_normy",
    14: "14_profinet",
    15: "15_kurtyny_muting",
    16: "16_motion_control",
    17: "17_scenariusze_commissioning",
    18: "18_tia_portal_zaawansowane",
    19: "19_commissioning_stacje",
    20: "20_schematy_elektryczne",
}

SECTION_RE = re.compile(r"^## (\d+)\.\s")


def split(source: Path) -> dict[str, str]:
    """Rozdziela plik na słownik {nazwa_pliku: treść}."""
    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)

    # Znajdź linie z nagłówkami sekcji
    section_starts: list[tuple[int, int]] = []  # (line_index, section_number)
    for i, line in enumerate(lines):
        m = SECTION_RE.match(line)
        if m:
            section_starts.append((i, int(m.group(1))))

    if not section_starts:
        print("ERROR: Nie znaleziono żadnych sekcji (## N. ...)")
        sys.exit(1)

    chapters: dict[str, str] = {}

    # Nagłówek (00_header.md) — wszystko przed pierwszą sekcją
    header_end = section_starts[0][0]
    header_text = "".join(lines[:header_end])
    chapters["00_header.md"] = header_text

    # Każda sekcja — zachowaj dokładną treść, łącznie z --- na końcu
    for idx, (start_line, sec_num) in enumerate(section_starts):
        if idx + 1 < len(section_starts):
            end_line = section_starts[idx + 1][0]
        else:
            end_line = len(lines)

        slug = SECTION_SLUGS.get(sec_num, f"{sec_num:02d}_section_{sec_num}")
        filename = f"{slug}.md"

        section_text = "".join(lines[start_line:end_line])
        chapters[filename] = section_text

    return chapters


def write_chapters(chapters: dict[str, str]) -> None:
    """Zapisuje rozdziały do docs/chapters/."""
    CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, content in chapters.items():
        path = CHAPTERS_DIR / filename
        path.write_text(content, encoding="utf-8")
        lines_count = content.count("\n")
        print(f"  {filename:<45s} {lines_count:>5d} linii")


def main():
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.exists():
        print(f"ERROR: Plik nie istnieje: {source}")
        sys.exit(1)

    print(f"Źródło: {source}")
    print(f"Cel:    {CHAPTERS_DIR}/")
    print()

    chapters = split(source)
    write_chapters(chapters)

    print(f"\nGotowe! Rozdzielono na {len(chapters)} plików.")


if __name__ == "__main__":
    main()
