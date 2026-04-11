"""
patch_v11.py
Generuje docs/qa_draft_v11.md na podstawie:
  1. docs/qa_draft_v10.md        — dokument bazowy (113 pytań)
  2. 5 wybranych transkrypcji   — nowa wiedza (serwony, ABB TCP, Safety 1oo2)
  3. Celowane rozszerzenie sekcji 4, 6, 17, 18 o brakujące pytania

Wymagania:
  pip install google-genai
  $env:GEMINI_API_KEY="AIzaSy..."
  $env:PYTHONUTF8=1
  python scripts/patch_v11.py

Plik wyjściowy: docs/qa_draft_v11.md
"""

import os
import re
import sys
import time
import pathlib

# ── Konfiguracja ─────────────────────────────────────────────────────────────
GEMINI_API_KEY  = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL    = "gemini-2.5-flash"
TRANSCRIPTS_DIR = pathlib.Path("transcripts/controlbyte")
QA_DRAFT        = pathlib.Path("docs/qa_draft_v10.md")
OUTPUT          = pathlib.Path("docs/qa_draft_v11.md")

TARGET_TRANSCRIPTS = [
    "NA_Jak działa PLC Safety - Wykrywanie zwarć do 0V, rozbieżności w ocenie 1oo2.txt",
    "NA_Komunikacja TCP – PLC Siemens a Robotem ABB z wykorzystaniem standardu XML.txt",
    "NA_Minikurs Programowania Napędów Serwo - Lekcja #1 Hardware serwonapędu Sinamics V.txt",
    "NA_Minikurs Programowania Napędów Serwo - Lekcja #2 Konfiguracja serwonapędu Sinami.txt",
    "NA_Podstawy Programowania Serwonapędów - Jak sterować napędem w trybie JOG z wykorz.txt",
]

# ── Prompt — Faza 1: Delta Knowledge Base z transkrypcji ────────────────────
PROMPT_DELTA = """\
Jesteś ekspertem automatyki przemysłowej Siemens. Poniżej znajdziesz 5 transkrypcji filmów \
edukacyjnych z kanału ControlByte PL.

ZADANIE: Wyciągnij z transkrypcji KONKRETNĄ WIEDZĘ TECHNICZNĄ i sformułuj nowe pytania Q&A \
mappowane na sekcje dokumentu kompendium PLC Commissioner.

FORMAT WYJŚCIOWY — użyj dokładnie tego formatu dla każdego nowego pytania:

## SEKCJA: <numer i nazwa sekcji>

### <Pytanie w formie pełnego zdania?>
<Definicja — 1-2 zdania techniczne>
- <punkt 1 z konkretnymi parametrami, numerami, procedurami>
- <punkt 2>
- <punkt 3>
*Źródło: transkrypcje ControlByte*

ZASADY:
- Język: POLSKI
- TYLKO wiedza faktycznie wspomniana w transkrypcjach — zero fabrykacji
- Podawaj konkretne szczegóły: parametry SINAMICS (p0304, p1900 itd.), nazwy funkcji TIA Portal
- MINIMUM 3 pytania z każdej transkrypcji zawierającej treść techniczną
- Skupiaj się na sekcjach: 4, 8, 10, 16 — to obszary z tych transkrypcji

SEKCJE DOCELOWE:
4. Struktury głosowania (1oo1 / 1oo2 / 2oo2 / 2oo3)
6. Safe State — bezpieczny stan
8. Napędy Safety — SINAMICS z wbudowanym Safety
10. Robot ABB IRC5 — integracja z PLC
16. Motion Control i SINAMICS — praktyka commissioning

--- TRANSKRYPCJE ---
{transcripts}
--- KONIEC TRANSKRYPCJI ---

Wygeneruj teraz delta bazę wiedzy. Zacznij od: # DELTA KNOWLEDGE BASE — PATCH V11
"""

# ── Prompt — Faza 2: Merger + Sekcje 4/6/17/18 ─────────────────────────────
PROMPT_MERGE = """\
Jesteś redaktorem technicznego kompendium Q&A dla inżyniera PLC/Commissioner Siemens.

ZADANIE: Wygeneruj pełny plik qa_draft_v11.md łącząc:
1. DOKUMENT BAZOWY: qa_draft_v10.md (113 pytań, 19 sekcji)
2. DELTA KB: nowe pytania z 5 transkrypcji ControlByte
3. TARGETOWANE ROZSZERZENIE: dodaj brakujące pytania do sekcji 4, 6, 17, 18

══════════════════════════════════════════
DOKUMENT BAZOWY — qa_draft_v10.md:
{qa_draft}
══════════════════════════════════════════

DELTA KNOWLEDGE BASE (z 5 transkrypcji):
{delta_kb}
══════════════════════════════════════════

INSTRUKCJE SZCZEGÓŁOWE:

### A. ZACHOWANIE ISTNIEJĄCEJ TREŚCI
- Każde istniejące pytanie (1.1–19.3) ZACHOWUJESZ bez zmian
- Nie skracaj, nie parafrazuj istniejących odpowiedzi
- Zachowaj wszystkie obrazy embedded (![...](docs/images/safety/...))
- Zachowaj tagi 🔴🟡🟢 przy pytaniach
- Zachowaj formatowanie: tabele, blockquoty, backticki

### B. DODAJ PYTANIA Z DELTA KB
Zintegruj pytania z Delta KB do odpowiednich sekcji — kontynuuj numerację.
- Sekcja 4: pytania z Safety 1oo2 transkrypcji
- Sekcja 8: pytania o SINAMICS Safety z transkrypcji serwo
- Sekcja 10: pytania ABB + TCP/XML z transkrypcji
- Sekcja 16: pytania o hardware i konfigurację V90/Startdrive

### C. TARGETOWANE ROZSZERZENIE (obowiązkowe — te pytania MUSZĄ pojawić się w v11)

**Sekcja 4 — dodaj te pytania jeśli nie ma ich w Delta KB:**

**4.X. Co to jest czas rozbieżności (discrepancy time) w F-DI 1oo2 i co się dzieje gdy zostanie przekroczony?** 🔴
Czas rozbieżności (Discrepancy Time) to maksymalny czas, przez jaki oba kanały 1oo2 mogą mieć różne wartości logiczne bez wywołania błędu. Parametr konfigurowany w TIA Portal dla każdego F-DI z oceną 1oo2.
- Domyślnie: 100 ms — oba sygnały muszą zmienić stan w tym oknie
- Przekroczenie → F-DI przechodzi w stan pasywny (passivation), wyjście F-DO = substitute value
- Typowa przyczyna: mechaniczne opóźnienie styku bezpieczeństwa lub błąd okablowania
- Konfiguracja: właściwości modułu F-DI → zakładka „Input" → „Discrepancy time [ms]"
- W diagnostyce: alarm „1001: Discrepancy error channel 1/2" w F_LADDR.DIAG

**4.X. Jak moduł F-DI ET200SP wykrywa zwarcie między kanałami (cross-circuit detection) w obwodzie 1oo2?** 🟡
Detekcja cross-circuit (zwarcia między kanałami) to mechanizm pozwalający wykryć zwarcie przewodu kanału 1 do kanału 2 dzięki testowym impulsom wyjść testowych (T-signal).
- T1 i T2 generują impulsy testowe z różną fazą (wzajemnie rozłączne)
- Wejścia odczytują sygnał z powrotem przez czujnik
- Zwarcie między kanałami = impuls T1 pojawia się na wejściu kanału 2 → błąd cross-circuit
- Wymaga okablowania z wyjść testowych (T1, T2) przez czujnik do wejść (DI0.0, DI0.1)
- Nie działa przy PM-switching bez wyjść testowych (wtedy cross-circuit wykrywany ograniczenie)

**Sekcja 6 — dodaj te pytania jeśli nie ma ich w Delta KB:**

**6.X. Czym różni się STO jako Safe State napędu SINAMICS od zatrzymania programowego (OFF1/OFF2)?** 🔴
STO (Safe Torque Off) jako Safe State napędu oznacza zablokowanie impulsów bramkowania tranzystorów — napęd nie może generować momentu obrotowego, nawet przy zasilaniu energetycznym. Zatrzymanie OFF1/OFF2 to kontrolowane wyhamowanie przez falownik z możliwością ponownego załączenia bez potwierdzenia.
- STO: brak momentu → wolne wybieganie jeśli nie ma hamulca mechanicznego (niebezpieczne na siłowniku pionowym!)
- OFF1: hamowanie po rampie (p1121), potem wyłączenie impulsów — napęd można ponownie uruchomić sygnałem ON
- OFF2: natychmiastowe wyłączenie impulsów (jak STO, ale sterowane programem, nie Safety)
- Safe State = STO → w konfiguracji F-DO parametr „substitute value" = 0 dla wyjścia STO
- Dla osi pionowych (roboty, podnośniki): jako Safe State użyj SS1 (Stop + STO po rampie) lub SBC

**6.X. Jak konfigurujesz substitute values dla F-DO i jaką wartość wybrać dla zaworu, siłownika i napędu?** 🟡
Substitute value to wartość logiczna wyjścia F-DO nadawana automatycznie podczas passivacji lub gdy F-CPU akceptuje błąd bezpieczeństwa. Konfigurowana w TIA Portal → właściwości modułu F-DO → „Substitute value for outputs".
- Domyślnie: 0 (false) dla wszystkich kanałów — to zazwyczaj poprawne
- Zawór bezpieczeństwa (NC — normalnie zamknięty): substitute value = 0 → zawór zamknięty ✓
- Siłownik pneumatyczny: zależy od logiki bezpiecznej pozycji — z reguły 0 = bezpieczna
- Napęd STO: substitute value = 0 → sygnał STO_active = false = brak momentu ✓
- WYJĄTEK: zawór NO (normalnie otwarty) — substitute value = 0 → zawór OTWARTY (niespójne z intencją)
- Ważna zasada: Zawsze weryfikuj że substitute value 0 odpowiada fizycznie bezpiecznemu stanowi urządzenia

**Sekcja 17 — dodaj te pytania:**

**17.X. Co sprawdzasz na FAT (Factory Acceptance Test) dla instalacji z Safety?** 🟡
FAT (Factory Acceptance Test) to weryfikacja systemu u producenta maszyny przed wysyłką do klienta. Dla Safety obejmuje funkcjonalne testy każdej funkcji bezpieczeństwa zgodnie z wymaganiami normy EN ISO 13849-1 i dokumentacją techniczną.
- Weryfikacja F-Signatures (F-DB i F-CPU): sprawdź match między TIA Portal a CPU → F-Program → Signature Comparison
- Test każdego E-Stop fizycznie: wciśnij → CPU pasywuje → wyjścia = substitute values → zwolnij → ACK → restart
- Test discrepancy: symuluj opóźnienie jednego kanału 1oo2 > discrepancy time → passivation
- Test muting: aktywuj oba czujniki muting w oknie czasowym → kurtyna działa → odblokowanie
- Test napędów Safety: sprawdź STO, SS1, SLS każdej osi — porównaj z Safety Matrix
- Documented: każdy test zapisany w protokole FAT z datą, podpisem, numerem PO
- Checklista: F-Version, F-Address, F-Monitoring Time, passivation time, substitute values

**17.X. Jak realizujesz SAT (Site Acceptance Test) po dostarczeniu maszyny do klienta?** 🟡
SAT (Site Acceptance Test) to weryfikacja systemu na miejscu klienta po instalacji. Różni się od FAT tym, że uwzględnia rzeczywiste środowisko: okablowanie obiektowe, medium procesowe, warunki bezpieczeństwa operacyjnego.
- Krok 1: Upload projektu z CPU i porównaj z referencją z FAT (Project → Compare)
- Krok 2: Sprawdź F-Signature CPU vs wartość zapisana w FAT-protokole — muszą być identyczne
- Krok 3: Fizyczny test E-Stop i kurtyn w normalnych warunkach pracy maszyny
- Krok 4: Próba produkcyjna z rzeczywistym materiałem (opcjonalnie)
- Krok 5: Przeszkolenie operatorów i techników serwisu
- Dokumentacja: protokół SAT + podpis inżyniera Safety i przedstawiciela klienta
- Jeśli F-Signature różni się od FAT → STOP — ktoś zmienił program po FAT, eskalacja

**Sekcja 18 — dodaj te pytania:**

**18.X. Czym jest SIMATIC ProDiag i jak konfigurujesz pierwsze monitory diagnostyczne?** 🟡
ProDiag (Process Diagnostics) to narzędzie TIA Portal do tworzenia automatycznej diagnostyki maszynowej generując alarmy HMI wprost z warunków logicznych PLC bez programowania w blokach.
- Dostępny od: TIA Portal V14 SP1, dla S7-1500 i ET200SP z CPU
- Konfiguracja: Devices & Networks → CPU → ProDiag → Add monitor
- Monitor = warunek logiczny (np. „siłownik nie dosunął się w 5s") → automatyczny alarm HMI + log
- Typy monitorów: Supervision (stan), Process Monitor (czas reakcji), Travel movement (pozycja)
- Krok 1: Zdefiniuj warunek triggering (bool z programu PLC)
- Krok 2: Przypisz tekst alarmu (wielojęzyczny) i kategorie (Error, Warning, Info)
- Krok 3: Skompiluj → alarmy automatycznie pojawiają się w HMI bez dodatkowej konfiguracji WinCC
- Korzyść: czas od awarii do diagnozy przyczyny bez przeglądania kodu — operator widzi kontekst

**18.X. Jak używasz funkcji Compare (porównywanie) w TIA Portal i co konkretnie porównujesz?** 🟢
Compare to narzędzie TIA Portal umożliwiające porównanie projektu online (CPU) z projektem offline (plik), wykrywające różnice w logice, konfiguracji sprzętu i danych — kluczowe przy commissioning i utrzymaniu.
- Dostęp: Menu Project → Compare → Online/Offline
- Kolory wyników: identyczne (biały), zmienione (żółty), tylko offline (niebieski), tylko online (czerwony)
- Co porównujesz: bloki programu, konfigurację HW, DB — osobno lub wszystko naraz
- Przy SAT: porównaj CPU (online) vs referencja FAT (offline) → sprawdź zero czerwonych/żółtych różnic
- Przy serwisie: sprawdź czy serwisant nie zmienił czegoś bez dokumentacji
- F-Program: po porównaniu sprawdź F-Signature — zmiana dowolnego F-bloku zmienia signature
- Export: wynik porównania możesz drukować do PDF jako dowód zgodności

### D. AKTUALIZACJA NAGŁÓWKA
Zmień w pierwszych liniach pliku:
- `v10` → `v11`
- `Pytania: 113` → `Pytania: <policz nowe pytania>`
- Data: `2026-03-30`

### E. ZASADY FORMATU
- Zachowaj istniejący format pytań: `### N.M. Treść pytania?  [emoji]`
- Nowe pytania: kontynuuj numerację w sekcji (np. jeśli sekcja 4 ma 4.3, nowe to 4.4, 4.5...)
- Nowe odpowiedzi: definicja + bullet list + praktyczny przykład
- NIE zmieniaj kolejności sekcji ani istniejących Q

Zwróć TYLKO kompletny plik Markdown — bez komentarzy, bez wyjaśnień, bez ```markdown wrappera.
"""

# ── Gemini helper ────────────────────────────────────────────────────────────
def gemini_generate(prompt: str, max_tokens: int, label: str) -> str:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[ERROR] Brak google-genai. Uruchom: pip install google-genai")
        sys.exit(1)

    client = genai.Client(api_key=GEMINI_API_KEY)

    chars = len(prompt)
    print(f"  [{label}] Prompt: ~{chars // 1000}K znaków (~{chars // 4000}K tokenów)")
    print(f"  [{label}] Wysyłanie do {GEMINI_MODEL}...")

    for attempt in range(1, 4):
        try:
            resp = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.15,
                )
            )
            return resp.text
        except Exception as e:
            err = str(e)
            wait_m = re.search(r"Retry-After[:=\s]+(\d+)", err, re.IGNORECASE)
            if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                wait = int(wait_m.group(1)) if wait_m else 60
                print(f"  [429] Rate limit. Czekam {wait}s... (próba {attempt}/3)")
                time.sleep(wait + 2)
                continue
            raise
    raise RuntimeError("Przekroczono liczbę prób Gemini — rate limit.")


# ── Ładowanie plików ──────────────────────────────────────────────────────────
def load_transcripts() -> str:
    parts = []
    for name in TARGET_TRANSCRIPTS:
        path = TRANSCRIPTS_DIR / name
        if not path.exists():
            print(f"  [WARN] Nie znaleziono transkrypcji: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        title = text.split("\n")[0].lstrip("# ").strip()
        parts.append(f"\n{'='*60}\nFILM: {title}\n{'='*60}\n{text}")
        print(f"  Załadowano: {name[:70]}")
    return "\n".join(parts)


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    if not GEMINI_API_KEY:
        print("[ERROR] Brak GEMINI_API_KEY.")
        sys.exit(1)

    # ── Faza 1: Delta KB z 5 transkrypcji ────────────────────────────────────
    print("\n" + "="*60)
    print(" FAZA 1 — Delta Knowledge Base z 5 transkrypcji")
    print("="*60)
    transcripts_text = load_transcripts()
    print(f"  Łącznie: ~{len(transcripts_text) // 1000}K znaków z {len(TARGET_TRANSCRIPTS)} filmów")

    delta_kb = gemini_generate(
        prompt=PROMPT_DELTA.format(transcripts=transcripts_text),
        max_tokens=16000,
        label="DELTA",
    )

    delta_lines = delta_kb.count("\n")
    delta_q = delta_kb.count("###")
    print(f"  Delta KB: ~{delta_lines} linii, {delta_q} pytań/nagłówków")

    # Opcjonalnie zapisz delta KB do podglądu
    delta_path = pathlib.Path("docs/knowledge_base_delta_v11.md")
    delta_path.write_text(delta_kb, encoding="utf-8")
    print(f"  Zapisano podgląd delta KB: {delta_path}")

    # ── Faza 2: Merge → qa_draft_v11.md ──────────────────────────────────────
    print("\n" + "="*60)
    print(" FAZA 2 — Merge z qa_draft_v10.md → qa_draft_v11.md")
    print("="*60)

    qa_draft = QA_DRAFT.read_text(encoding="utf-8")
    print(f"  Bazowy dokument: {QA_DRAFT.name} ({len(qa_draft) // 1000}K znaków)")
    print(f"  Delta KB: {len(delta_kb) // 1000}K znaków")

    result = gemini_generate(
        prompt=PROMPT_MERGE.format(qa_draft=qa_draft, delta_kb=delta_kb),
        max_tokens=65000,
        label="MERGE",
    )

    # Usuń ewentualny ```markdown wrapper jeśli model go dodał
    result = re.sub(r"^```(?:markdown)?\s*\n", "", result.strip())
    result = re.sub(r"\n```\s*$", "", result.strip())

    # ── Zapis ────────────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print(" FAZA 3 — Zapis wyników")
    print("="*60)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(result, encoding="utf-8")

    new_q = result.count("### ")
    orig_q = qa_draft.count("### ")
    lines = result.count("\n")
    print(f"  Zapisano: {OUTPUT}")
    print(f"  Rozmiar: ~{lines} linii, {new_q} pytań/nagłówków")
    print(f"  Przyrost: +{new_q - orig_q} nowych pytań (było {orig_q})")

    # ── Weryfikacja integralności ────────────────────────────────────────────
    sections_in = len(re.findall(r"^## \d+\.", qa_draft, re.MULTILINE))
    sections_out = len(re.findall(r"^## \d+\.", result, re.MULTILINE))
    print(f"\n  Sekcje: {sections_in} → {sections_out} (oczekiwane: {sections_in})")
    if sections_out != sections_in:
        print("  [UWAGA] Liczba sekcji zmieniła się — sprawdź plik ręcznie!")
    else:
        print("  [OK] Struktura sekcji zachowana")

    # Sprawdź czy obrazy nadal są
    imgs_in  = len(re.findall(r"!\[", qa_draft))
    imgs_out = len(re.findall(r"!\[", result))
    print(f"  Obrazy embedded: {imgs_in} → {imgs_out}")
    if imgs_out < imgs_in:
        print(f"  [UWAGA] Utracono {imgs_in - imgs_out} obrazów!")
    else:
        print(f"  [OK] Wszystkie obrazy zachowane")

    print("\n  GOTOWE → docs/qa_draft_v11.md")
    print("  Następny krok: sprawdź plik, następnie uruchom New-QADocument.ps1")


if __name__ == "__main__":
    main()
