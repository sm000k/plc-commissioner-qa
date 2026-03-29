"""
Merge-KnowledgeBase.py
Scala wiedzę z knowledge_base_controlbyte.md do qa_draft_v7.md
przy użyciu Gemini jako inteligentnego redaktora.
"""

import os
import re
import sys
import time
from pathlib import Path

QA_DRAFT = Path("docs/qa_draft_v7.md")
KNOWLEDGE_BASE = Path("docs/knowledge_base_controlbyte.md")
OUTPUT_FILE = Path("docs/qa_draft_v8.md")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash"

PROMPT = """Jesteś redaktorem kompendium Q&A dla inżyniera PLC/Commissioner (Siemens TIA Portal, Safety, SINAMICS, PROFINET).

ZADANIE: Połącz dwa dokumenty w jeden zaktualizowany plik.

DOKUMENT A — "qa_draft_v7.md" (istniejące kompendium, ~120 pytań):
{qa_draft}

---

DOKUMENT B — "knowledge_base_controlbyte.md" (nowa wiedza z transkrypcji YouTube):
{knowledge_base}

---

INSTRUKCJE SCALANIA:

1. **Zachowaj całą treść DOKUMENTU A bez zmian** — nie usuwaj, nie skracaj, nie przerabiaj istniejących pytań.

2. **Dodaj nowe pytania z DOKUMENTU B** do odpowiednich sekcji w DOKUMENCIE A.
   - Sekcja 1 (Podstawy PLC) ← pytania z sekcji 1 dokumentu B (rodziny CPU, pamięć, hardware S7-1200, IEC 61131-3)
   - Sekcja 3 (Moduły F-DI/F-DO) ← pytania z sekcji 3 dokumentu B (awarie wejść 1oo2, parametry rozbieżności)
   - Sekcja 4 (Struktury głosowania) ← pytania z sekcji 4 dokumentu B
   - Sekcja 5 (Passivation/Reintegration) ← pytania z sekcji 5 dokumentu B
   - Sekcja 6 (Safe State) ← pytanie STO z dokumentu B
   - Sekcja 11 (Commissioning/diagnostyka) ← pytania z sekcji 11 dokumentu B (V-Assistant, Python/OPC UA)
   - Sekcja 14 (PROFINET) ← pytania z sekcji 14 dokumentu B (switche przemysłowe, ISO on TCP)
   - Sekcja 15 (Kurtyny) ← pytania z sekcji 15 dokumentu B
   - Sekcja 16 (Motion Control) ← pytania z sekcji 16 dokumentu B (typy silników)
   - Sekcja 2 (Architektura Safety) ← pytanie o Pilz PNOZmulti z dokumentu B

3. **Format pytań z DOKUMENTU B** — przetłumacz na format DOKUMENTU A:
   - Nagłówek: `### S.N. Pytanie?` gdzie S = numer sekcji, N = kolejny numer pytania w sekcji
   - Definicja (1-2 zdania) + szczegóły w bullet pointach
   - Zachowaj adnotacje *Praktyk:* jako dodatkową sekcję "Praktyczne wskazówki:" lub włącz w istniejące punkty
   - Zachowaj tagi [Safety], [Sinamics], [TIA Portal] jako *Źródło: transkrypcje ControlByte*

4. **Pomijaj** pytania z DOKUMENTU B które są:
   - Oczywistymi duplikatami pytań już istniejących w DOKUMENCIE A
   - Zbyt ogólne, bez konkretnych danych technicznych
   - O produktach poza zakresem (Pilz PNOZmulti — dodaj tylko jeśli wnosi coś nowego do sekcji 2)

5. **Numeracja** — kontynuuj istniejące numery. Np. jeśli sekcja 1 ma pytania 1.1–1.6, nowe pytania to 1.7, 1.8 itd.

6. **Na końcu** — zaktualizuj nagłówek dokumentu, zmieniając "v7" na "v8" i dodając wzmiankę o transkrypcjach ControlByte.

Zwróć TYLKO treść zaktualizowanego pliku Markdown, bez żadnych komentarzy czy wyjaśnień.
"""


def load_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def generate_with_gemini(qa_draft: str, knowledge_base: str) -> str:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[ERROR] Brak google-genai. Uruchom: pip install google-genai")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = PROMPT.format(qa_draft=qa_draft, knowledge_base=knowledge_base)

    chars = len(prompt)
    print(f"  Prompt: ~{chars // 1000}K znaków (~{chars // 4000}K tokenów)")
    print(f"  Model: {GEMINI_MODEL}")
    print(f"  Wysyłanie...")

    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=32000,
                    temperature=0.1,
                )
            )
            return response.text
        except Exception as e:
            err_str = str(e)
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
        print("[ERROR] Brak GEMINI_API_KEY.")
        sys.exit(1)

    print("\n[1/3] Ładowanie dokumentów...")
    qa_draft = load_file(QA_DRAFT)
    knowledge_base = load_file(KNOWLEDGE_BASE)
    print(f"  qa_draft_v7.md: {len(qa_draft) // 1000}K znaków")
    print(f"  knowledge_base: {len(knowledge_base) // 1000}K znaków")

    print("\n[2/3] Scalanie przez Gemini...")
    result = generate_with_gemini(qa_draft, knowledge_base)

    print("\n[3/3] Zapisywanie...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(result, encoding="utf-8")

    lines = result.count("\n")
    questions = result.count("### ")
    print(f"  Zapisano: {OUTPUT_FILE}")
    print(f"  ~{lines} linii, ~{questions} pytań/nagłówków")

    # Statystyki przyrostu
    orig_q = qa_draft.count("### ")
    new_q = questions - orig_q
    print(f"  Przyrost: +{new_q} nowych pytań (było {orig_q}, teraz {questions})")
    print("\nGotowe! Zaktualizowane kompendium: docs/qa_draft_v8.md")


if __name__ == "__main__":
    main()
