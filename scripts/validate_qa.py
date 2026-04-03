#!/usr/bin/env python3
"""
Walidacja jakości dokumentu Q&A — sprawdza wszystkie rozdziały pod kątem:
  1. Terminologia Siemens (zakazane terminy generyczne)
  2. Długość odpowiedzi (max 30 zdań)
  3. Brak źródła (tag ZWERYFIKOWANE/PRAWDOPODOBNE/DO WERYFIKACJI/Źródło)
  4. Brak elementu praktycznego
  5. Błędy numeracji
  6. Literówki (znane patterns)

Użycie:
  python scripts/validate_qa.py              # waliduj wszystko
  python scripts/validate_qa.py 14           # waliduj rozdział 14
  python scripts/validate_qa.py 01-05        # waliduj rozdziały 1-5
  python scripts/validate_qa.py --fix        # napraw automatycznie co się da

Exit code: 0 = OK, 1 = znaleziono problemy
"""

import re
import sys
import glob
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

WORKSPACE = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = WORKSPACE / "docs" / "chapters"

# ── Terminologia ────────────────────────────────────────────────────────────

FORBIDDEN_TERMS = {
    r"\bsterownik bezpieczeństwa\b": "F-CPU",
    r"\bsterownik safety\b": "F-CPU / moduł F-DI",
    r"\bmoduł safety\b": "moduł F-DI / moduł F-DO",
    r"\bukład bezpieczeństwa\b": "system Safety / F-CPU",
    r"\bsuma kontrolna\b": "F-signature / collective signature",
    r"\bwartość domyślna\b": "substitute value",
    r"\bwartość zastępcza\b": "substitute value",
    r"\btimeout komunikacji\b": "F-monitoring time",
    r"\bczas rozbieżności\b": "discrepancy time",
    r"\badres [Ss]afety\b": "F-address",
    r"\bbezpieczne zatrzymanie\b": "STO / SS1 / SS2 (konkretna funkcja)",
    r"\b= master\b": "IO-Controller",
    r"\b= slave\b": "IO-Device",
}

# ── Źródła ──────────────────────────────────────────────────────────────────

SOURCE_PATTERN = re.compile(
    r"[Źź]ródło:|knowledge.base|transkrypcje|ZWERYFIKOWANE|PRAWDOPODOBNE|DO WERYFIKACJI",
    re.IGNORECASE,
)

# ── Praktyka ────────────────────────────────────────────────────────────────

PRACTICE_KEYWORDS = re.compile(
    r"TIA Portal|krok po kroku|procedura|diagnostyk|konfigur|commissioning|"
    r"na obiekcie|Watch Table|Go online|Startdrive|online →|Force Value|"
    r"sprawdź|monitoruj|F-DB|BOP-2|Jog|Download to device|"
    r"checklista|\- \[ \]|Pułapka|PLC (zamknij|otwórz)|Sekwencja|"
    r"podłącz(enie|yć)|PRONETA|Praktyczne wskazówk|drag-and-drop",
    re.IGNORECASE,
)

# Pytania WYMAGAJĄCE elementu praktycznego (akcja/konfiguracja/diagnostyka)
ACTIONABLE_QUESTION = re.compile(
    r"jak\s+(konfigurujesz|robisz|wgrywasz|testujesz|dodajesz|generujesz|"
    r"sprawdzasz|diagnostykujesz|debugujesz|interpretujesz|kasujesz|"
    r"reagować|postępujesz|przekazujesz|czytasz|realizujesz|podejść)|"
    r"co\s+(sprawdzasz|robisz)|"
    r"krok po kroku|commissioning|"
    r"pierwsze \d+ krok|lista kroków|"
    r"nie (pojawia się|wychodzi|wraca|kasuje)|"
    r"świeci.*(led|błęd|czerwon)|"
    r"startuje sam|alarm którego",
    re.IGNORECASE,
)

# Pytania DEFINICYJNE — element praktyczny opcjonalny
DEFINITIONAL_QUESTION = re.compile(
    r"^### \d+\.\d+\.\s*(co to jest|czym jest|czym różni się|"
    r"jaka jest różnica|jakie są (główne|kluczowe|warianty|rodzaj|typy|kategori)|"
    r"wyjaśnij|dlaczego|na czym polega|jakie (protokoły|funkcje|elementy|oprogramowanie)|"
    r"do czego służy|kiedy (wybierasz|stosujesz)|"
    r"czy można)",
    re.IGNORECASE,
)

# ── Znane literówki ─────────────────────────────────────────────────────────

KNOWN_TYPOS = {
    "styling i demagnetyzacj": "stykach i demagnetyzacj",
    "odebrана": "odebrana",
    "Zastazpuje": "Zastępuje",
    "przesuznite": "przesunięte",
}


@dataclass
class Issue:
    chapter: str
    question: str
    severity: str  # ERROR, WARN, INFO
    category: str
    message: str
    line_hint: int = 0
    auto_fixable: bool = False


def parse_questions(text: str) -> list[tuple[str, str, int]]:
    """Return list of (question_id, body, approx_line)."""
    results = []
    parts = re.split(r"(^### .+$)", text, flags=re.MULTILINE)
    line_num = 0
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        # Extract question number from header
        m = re.match(r"### (\d+\.\d+)\.", header)
        qid = m.group(1) if m else header[:40]
        line_num = text[: text.index(header)].count("\n") + 1
        results.append((qid, header + "\n" + body, line_num))
    return results


def count_sentences(text: str) -> int:
    """Approximate sentence count (skip code blocks, tables, images)."""
    lines = []
    in_code = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if stripped.startswith("|") or stripped.startswith("!["): 
            continue
        if stripped.startswith("---"):
            continue
        if stripped:
            lines.append(stripped)
    body = " ".join(lines)
    return len(re.findall(r"[.?!](?:\s|$)", body))


def validate_chapter(filepath: Path, section_num: int) -> list[Issue]:
    """Validate a single chapter file."""
    issues: list[Issue] = []
    chapter_name = filepath.stem
    text = filepath.read_text(encoding="utf-8")
    questions = parse_questions(text)

    for qid, body, line_num in questions:
        # 1. Terminology
        for pattern, replacement in FORBIDDEN_TERMS.items():
            matches = list(re.finditer(pattern, body, re.IGNORECASE))
            for m in matches:
                context = body[max(0, m.start() - 80) : m.end() + 50]
                # Skip if inside a quote about what NOT to use
                if "nie:" in context.lower() or "NIE używaj" in context or "zamiast" in context:
                    continue
                # Skip Polish term in parentheses after Siemens term, e.g. "Discrepancy time (czas rozbieżności)"
                pre = body[max(0, m.start() - 2) : m.start()]
                if pre.endswith("("):
                    continue
                # Skip when describing non-Siemens products (Pilz, ABB, KUKA, etc.)
                ctx_lower = context.lower()
                if any(brand in ctx_lower for brand in ("pilz", "pnoz", "abb", "kuka", "fanuc")):
                    continue
                issues.append(Issue(
                    chapter=chapter_name,
                    question=qid,
                    severity="ERROR",
                    category="TERMINOLOGY",
                    message=f'„{m.group()}" → {replacement}',
                    line_hint=line_num,
                    auto_fixable=True,
                ))

        # 2. Sentence count
        sents = count_sentences(body)
        if sents > 30:
            issues.append(Issue(
                chapter=chapter_name,
                question=qid,
                severity="WARN",
                category="LENGTH",
                message=f"{sents} zdań (max 30)",
                line_hint=line_num,
            ))

        # 3. Source tag
        if not SOURCE_PATTERN.search(body):
            issues.append(Issue(
                chapter=chapter_name,
                question=qid,
                severity="ERROR",
                category="NO_SOURCE",
                message="Brak tagu źródła",
                line_hint=line_num,
                auto_fixable=True,
            ))

        # 4. Practical element — context-aware
        if not PRACTICE_KEYWORDS.search(body):
            # Extract the question header line
            header_line = body.split("\n")[0] if body else ""
            is_actionable = ACTIONABLE_QUESTION.search(header_line)
            is_definitional = DEFINITIONAL_QUESTION.search(header_line)

            if is_actionable and not is_definitional:
                # Actionable question WITHOUT practice → ERROR
                issues.append(Issue(
                    chapter=chapter_name,
                    question=qid,
                    severity="ERROR",
                    category="NO_PRACTICE",
                    message="Pytanie akcyjne bez elementu praktycznego!",
                    line_hint=line_num,
                ))
            elif not is_definitional:
                # Ambiguous question → WARN
                issues.append(Issue(
                    chapter=chapter_name,
                    question=qid,
                    severity="WARN",
                    category="NO_PRACTICE",
                    message="Brak elementu praktycznego (procedura/TIA Portal/diagnostyka)",
                    line_hint=line_num,
                ))
            # Definitional questions → no warning

        # 5. Numbering
        m_num = re.match(r"### (\d+)\.(\d+)\.", body)
        if m_num:
            sec = int(m_num.group(1))
            if sec != section_num:
                issues.append(Issue(
                    chapter=chapter_name,
                    question=qid,
                    severity="ERROR",
                    category="NUMBERING",
                    message=f"Numer sekcji {sec} ≠ oczekiwany {section_num}",
                    line_hint=line_num,
                    auto_fixable=True,
                ))

    # 6. Known typos (whole file)
    for typo, fix in KNOWN_TYPOS.items():
        if typo in text:
            issues.append(Issue(
                chapter=chapter_name,
                question="(cały plik)",
                severity="ERROR",
                category="TYPO",
                message=f'„{typo}" → „{fix}"',
                auto_fixable=True,
            ))

    return issues


def get_chapter_files(scope: Optional[str] = None) -> list[tuple[Path, int]]:
    """Return list of (filepath, section_number) for scope."""
    all_files = sorted(CHAPTERS_DIR.glob("[0-2]*.md"))
    all_files = [(f, int(re.match(r"(\d+)", f.stem).group(1)))
                 for f in all_files
                 if "desktop" not in f.name and "00_header" not in f.name]

    if not scope or scope == "all":
        return all_files

    # Range: "01-05"
    m = re.match(r"(\d+)-(\d+)", scope)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        return [(f, n) for f, n in all_files if lo <= n <= hi]

    # Single: "14"
    if scope.isdigit():
        n = int(scope)
        return [(f, num) for f, num in all_files if num == n]

    # Named groups
    groups = {
        "safety": range(2, 10),
        "napedy": [8, 12, 16],
        "commissioning": [11, 17, 19],
        "profinet": [14],
        "tia": [9, 18],
    }
    if scope in groups:
        nums = groups[scope]
        return [(f, n) for f, n in all_files if n in nums]

    print(f"⚠️  Nieznany zakres: {scope}")
    return all_files


def print_report(all_issues: list[Issue]) -> None:
    """Print formatted report."""
    if not all_issues:
        print("\n✅ Brak problemów — wszystkie rozdziały przeszły walidację.")
        return

    errors = [i for i in all_issues if i.severity == "ERROR"]
    warns = [i for i in all_issues if i.severity == "WARN"]
    auto = [i for i in all_issues if i.auto_fixable]

    print(f"\n{'='*80}")
    print(f"  RAPORT WALIDACJI Q&A")
    print(f"{'='*80}")
    print(f"  ❌ Błędy:      {len(errors)}")
    print(f"  ⚠️  Ostrzeżenia: {len(warns)}")
    print(f"  🔧 Auto-fixable: {len(auto)}")
    print(f"{'='*80}\n")

    # Group by category
    by_cat: dict[str, list[Issue]] = {}
    for issue in all_issues:
        by_cat.setdefault(issue.category, []).append(issue)

    cat_names = {
        "TERMINOLOGY": "Terminologia Siemens",
        "LENGTH": "Przekroczona długość (>30 zdań)",
        "NO_SOURCE": "Brak tagu źródła",
        "NO_PRACTICE": "Brak elementu praktycznego",
        "NUMBERING": "Błąd numeracji",
        "TYPO": "Literówka",
    }

    for cat, issues in by_cat.items():
        print(f"## {cat_names.get(cat, cat)} ({len(issues)})")
        for i in issues:
            fix = " [AUTO]" if i.auto_fixable else ""
            print(f"  {i.severity} {i.chapter} Q{i.question}: {i.message}{fix}")
        print()


def main():
    scope = None
    do_fix = False
    for arg in sys.argv[1:]:
        if arg == "--fix":
            do_fix = True
        else:
            scope = arg

    files = get_chapter_files(scope)
    if not files:
        print("Brak plików do sprawdzenia.")
        sys.exit(0)

    print(f"Sprawdzam {len(files)} rozdziałów...")

    all_issues: list[Issue] = []
    for filepath, section_num in files:
        issues = validate_chapter(filepath, section_num)
        all_issues.extend(issues)

    print_report(all_issues)

    errors = [i for i in all_issues if i.severity == "ERROR"]
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
