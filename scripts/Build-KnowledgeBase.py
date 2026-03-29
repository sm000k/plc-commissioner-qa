"""
Build-KnowledgeBase.py
Wysyła transkrypcje do Gemini, który generuje ustrukturyzowaną bazę wiedzy
mapowaną na sekcje Q&A do rozmowy kwalifikacyjnej PLC/Commissioner.
"""

import os
import re
import sys
import time
from pathlib import Path

TRANSCRIPTS_DIR = Path("transcripts/controlbyte")
OUTPUT_FILE = Path("docs/knowledge_base_controlbyte.md")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

# Słowa kluczowe wyeliminowanych plików (Finder, CodeSys, Beckhoff, Lenze, Wago etc.)
EXCLUDE_KEYWORDS = [
    "codesys", "codedsys", "codeys",
    "finder opta", "finder_opta",
    "beckhoff",
    "lenze",
    "wago",
    "home assistant", "homeassistant",
    "scada",
]

QA_SECTIONS = """
1. Podstawy PLC i automatyki
2. Architektura SIMATIC Safety Integrated
3. Moduły F-DI / F-DO — okablowanie i parametry
4. Struktury głosowania (1oo1 / 1oo2 / 2oo2 / 2oo3)
5. Passivation, Reintegration, ACK
6. Safe State — bezpieczny stan
7. PROFIsafe — komunikacja Safety
8. Napędy Safety — SINAMICS z wbudowanym Safety
9. TIA Portal — Safety praktyka
10. Robot ABB IRC5 — integracja z PLC
11. Commissioning i diagnostyka
12. SICAR i Napędy SINAMICS
13. E-Stop — normy, implementacja i obliczenia bezpieczeństwa
14. PROFINET — topologia, diagnostyka i zaawansowane funkcje
15. Kurtyny bezpieczeństwa i Muting
16. Motion Control i SINAMICS — praktyka commissioning
17. Realne scenariusze commissioning
18. TIA Portal — zaawansowane funkcje
19. Słownik pojęć
"""

PROMPT = """Jesteś ekspertem automatyki przemysłowej Siemens. Poniżej znajdziesz transkrypcje filmów edukacyjnych z kanału ControlByte z zakresu PLC, Safety, napędów i TIA Portal.

ZADANIE: Na podstawie tych transkrypcji wygeneruj ustrukturyzowaną bazę wiedzy do rozmowy kwalifikacyjnej dla stanowiska PLC Commissioner / Automatyk. 

FORMAT WYJŚCIOWY: Plik Markdown z sekcjami mapowanymi do poniższych obszarów tematycznych. Dla każdej sekcji generuj pytania+odpowiedzi w formacie:

### Pytanie w formie pełnego zdania?
Odpowiedź — definicja (1-2 zdania) + szczegółowe punkty + praktyczny przykład.
- Punkt kluczowy 1 (z parametrami, numerami alarmów, krokami procedury)
- Punkt kluczowy 2
*Praktyk: [obserwacja z filmów, konkretny przykład z pola]*

ZASADY:
- Język: POLSKI
- Uwzględniaj tylko wiedzę faktycznie wspomnianą w transkrypcjach
- Podawaj konkretne szczegóły: numery błędów diagnostycznych, parametry, nazwy funkcji TIA Portal, nazwy bloków
- Priorytetyzuj wiedzę praktyczną (jak to wygląda na żywo, co widać w diagnostyce)
- Pomijaj ogólniki bez treści technicznej
- Oznaczaj skąd pochodzi wiedza: [Safety], [Sinamics], [TIA Portal], [HMI], [normy], [Motor Control], [ABB]
- Generuj MINIMUM 3-5 pytań na sekcję, tylko dla sekcji gdzie transkrypcje zawierają odpowiednie treści
- Skup się na sekcjach: 1, 2, 3, 4, 5, 6, 9, 11, 14, 15, 16, 17, 18 (to są obszary poruszane na filmach)

SEKCJE DO WYPEŁNIENIA:
{sections}

--- TRANSKRYPCJE DO ANALIZY ---
{transcripts}
--- KONIEC TRANSKRYPCJI ---

Teraz wygeneruj bazę wiedzy. Zacznij od: # BAZA WIEDZY — CONTROLBYTE TRANSKRYPCJE
"""


def should_exclude(filename: str) -> bool:
    name_lower = filename.lower()
    for kw in EXCLUDE_KEYWORDS:
        if kw in name_lower:
            return True
    return False


def load_transcripts() -> tuple[list[dict], int]:
    files = sorted(TRANSCRIPTS_DIR.glob("*.txt"))
    
    # Pomijamy pliki meta
    files = [f for f in files if not f.name.startswith("_")]
    
    included = []
    excluded = []
    
    for f in files:
        if should_exclude(f.name):
            excluded.append(f.name)
        else:
            included.append(f)
    
    print(f"  Transkrypcje: {len(included)} załadowanych, {len(excluded)} pominiętych")
    if excluded:
        print(f"  Pominięte (off-topic):")
        for name in excluded:
            print(f"    - {name[:80]}")
    
    docs = []
    total_chars = 0
    for f in included:
        try:
            text = f.read_text(encoding="utf-8")
            # Wyciągamy tytuł z pierwszej linii
            title = text.split("\n")[0].lstrip("# ").strip()
            docs.append({"title": title, "text": text})
            total_chars += len(text)
        except Exception as e:
            print(f"  [WARN] Błąd czytania {f.name}: {e}")
    
    return docs, total_chars


def build_combined_text(docs: list[dict]) -> str:
    parts = []
    for i, doc in enumerate(docs, 1):
        parts.append(f"\n{'='*60}")
        parts.append(f"FILM {i}/{len(docs)}: {doc['title']}")
        parts.append(f"{'='*60}")
        parts.append(doc["text"])
    return "\n".join(parts)


def generate_with_gemini(combined: str) -> str:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[ERROR] Brak google-genai. Uruchom: pip install google-genai")
        sys.exit(1)
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = PROMPT.format(
        sections=QA_SECTIONS,
        transcripts=combined
    )
    
    prompt_chars = len(prompt)
    prompt_tokens_est = prompt_chars // 4
    print(f"  Rozmiar promptu: ~{prompt_chars // 1000}K znaków (~{prompt_tokens_est // 1000}K tokenów)")
    print(f"  Wysyłanie do Gemini ({GEMINI_MODEL})...")
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=16000,
                    temperature=0.2,
                )
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            # Rate limit handling
            wait_match = re.search(r"Retry-After[:=\s]+(\d+)", err_str, re.IGNORECASE)
            if "429" in err_str or "quota" in err_str.lower() or "rate" in err_str.lower():
                wait = int(wait_match.group(1)) if wait_match else 60
                print(f"  [429] Rate limit. Czekam {wait}s... (próba {attempt}/{max_retries})")
                time.sleep(wait + 2)
                continue
            raise
    
    raise RuntimeError("Przekroczono liczbę prób — rate limit nieustępliwy.")


def main():
    if not GEMINI_API_KEY:
        print("[ERROR] Brak klucza API. Ustaw zmienną środowiskową GEMINI_API_KEY.")
        sys.exit(1)
    
    print("\n[1/3] Ładowanie transkrypcji...")
    docs, total_chars = load_transcripts()
    print(f"  Łącznie: ~{total_chars // 1000}K znaków z {len(docs)} filmów")
    
    print("\n[2/3] Łączenie transkrypcji i generowanie bazy wiedzy przez Gemini...")
    combined = build_combined_text(docs)
    
    result = generate_with_gemini(combined)
    
    print("\n[3/3] Zapisywanie wyniku...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(result, encoding="utf-8")
    
    lines = result.count("\n")
    sections = result.count("## ")
    questions = result.count("### ")
    print(f"  Zapisano: {OUTPUT_FILE}")
    print(f"  Rozmiar: {len(result) // 1000}K znaków, ~{lines} linii")
    print(f"  Sekcji: {sections}, Pytań/tematów: {questions}")
    print("\nGotowe! Baza wiedzy: docs/knowledge_base_controlbyte.md")


if __name__ == "__main__":
    main()
