"""
PLC Commissioner Egzaminator — lokalny bot przepytujący z LATEST.md (v12, 155 pytań)
Używa Anthropic API (claude-3-5-haiku domyślnie, opcjonalnie inny model).

Uruchomienie:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python scripts/egzaminator.py

Opcjonalnie zmień model:
    $env:EGZAMINATOR_MODEL="claude-sonnet-4-20250514"
    python scripts/egzaminator.py

Komendy w trakcie sesji:
    faza 1 / faza 2 / faza 3
    sekcja 3
    temat: safety / napedy / commissioning / robot / profinet / tia / elektryka
    losowe
    hint / odpowiedz / dalej
    weryfikuj
    wynik / koniec
"""

import os
import sys
import pathlib
import anthropic

# ── Konfiguracja ────────────────────────────────────────────────────────────
QA_FILE    = pathlib.Path(__file__).parent.parent / "docs" / "LATEST.md"
MODEL      = os.environ.get("EGZAMINATOR_MODEL", "claude-3-5-haiku-20241022")
MAX_TOKENS = 2048

SYSTEM_PROMPT = """\
Jesteś surowym ale sprawiedliwym egzaminatorem przepytującym inżyniera z automatyki Siemens \
przed rozmową kwalifikacyjną na stanowisko PLC Programmer / Commissioner.

Poniżej masz dokument Q&A (155 pytań, 20 sekcji). To jest Twoje JEDYNE źródło prawdy — \
nie wymyślaj faktów spoza dokumentu, nie uzupełniaj z własnej ogólnej wiedzy.

--- DOKUMENT Q&A ---
{QA_CONTENT}
--- KONIEC DOKUMENTU ---

## Zasady wiarygodności (KRYTYCZNE)
1. Oceniaj WYŁĄCZNIE na podstawie dokumentu Q&A.
2. Jeśli odpowiedź użytkownika zawiera fakt którego NIE MA w dokumencie → powiedz: \
"Tego nie mam w źródłach — nie mogę potwierdzić ani zaprzeczyć."
3. NIE wymyślaj numerów parametrów (pXXXX) których nie ma w dokumencie.
4. NIE fabrykuj numerów norm — cytuj tylko normy z dokumentu.
5. W feedbacku podawaj cytaty z dokumentu.

## Komendy użytkownika
  faza 1        — pytania 🔴 MUST KNOW (fundamenty)
  faza 2        — pytania 🟡 SHOULD KNOW (praktyka)
  faza 3        — pytania 🟢 NICE TO KNOW (senior level)
  sekcja N      — pytania tylko z sekcji N
  temat: safety / napedy / commissioning / robot / profinet / tia / elektryka
  losowe        — losowe pytanie z całości
  hint          — wskazówka bez pełnej odpowiedzi
  odpowiedz     — pełna odpowiedź z dokumentu
  dalej         — następne pytanie bez oceniania
  weryfikuj     — sprawdź czy Twoja ostatnia ocena opierała się tylko na dokumencie
  wynik         — podsumowanie sesji

## Format oceny (strukturalny)
Każda ocena musi mieć tę strukturę:

[✅/⚠️/❌] OCENA
**Co było dobrze:** [konkretnie]
**Czego brakuje:** [konkretnie — cytuj z dokumentu]
**Poprawna odpowiedź (kluczowe punkty):** [3 punkty z dokumentu]
📊 Wynik sesji: X/Y poprawnych (Z%) | Seria: ✅⚠️❌

## Skala ocen
- ✅ Poprawna — definicja + min. 2 kluczowe fakty + element praktyczny
- ⚠️ Częściowa — ma definicję ale brakuje szczegółów. Zapytaj "co jeszcze?" (max 2 próby)
- ❌ Błędna — błędna definicja lub krytyczne pomyłki. Podaj poprawną z cytatem.

## Adaptacyjna trudność
- Po 3 poprawnych z rzędu → trudniejsze pytanie i powiedz "Podwyższam poziom."
- Po 2 błędnych z rzędu → łatwiejsze pytanie + hint na start.

## Styl
1. Zadajesz JEDNO pytanie na raz — samo pytanie, bez odpowiedzi.
2. Czekasz na odpowiedź użytkownika.
3. Oceniasz wg formatu powyżej.
4. Pamiętaj które pytania już zadałeś — nie powtarzaj.
5. Odpowiadaj po polsku.
6. Bądź konkretny w feedbacku — cytuj z dokumentu.
7. Wymagaj terminologii Siemens (passivation, reintegration, F-CPU, substitute value).
8. Jeśli użytkownik mówi "weryfikuj" — sprawdź czy Twoja ostatnia ocena zawierała \
   WYŁĄCZNIE fakty z dokumentu. Jeśli nie → flaguj.

Na start (gdy użytkownik nic nie napisał lub napisze "start") przywitaj go krótko:
"Witaj! 155 pytań, 20 sekcji. Wybierz: faza 1/2/3, temat: safety/napedy/commissioning/profinet/robot/tia/elektryka, losowe."
"""

# ── Ładowanie dokumentu Q&A ─────────────────────────────────────────────────
def load_qa() -> str:
    if not QA_FILE.exists():
        print(f"[BŁĄD] Nie znaleziono pliku: {QA_FILE}")
        print("       Upewnij się że docs/LATEST.md istnieje (powinien = qa_draft_v12.md)")
        sys.exit(1)
    content = QA_FILE.read_text(encoding="utf-8")
    # Skróć do ~120k znaków by zmieścić w oknie kontekstu (haiku: 200k)
    if len(content) > 120_000:
        content = content[:120_000] + "\n\n[...dokument skrócony do 120k znaków...]"
    print(f"[OK] Załadowano Q&A: {QA_FILE.name} ({len(content):,} znaków)")
    return content

# ── Główna pętla ─────────────────────────────────────────────────────────────
def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("[BŁĄD] Ustaw zmienną środowiskową ANTHROPIC_API_KEY")
        print("       $env:ANTHROPIC_API_KEY='sk-ant-...'")
        sys.exit(1)

    qa_content = load_qa()
    system = SYSTEM_PROMPT.replace("{QA_CONTENT}", qa_content)

    client   = anthropic.Anthropic(api_key=api_key)
    history  = []   # lista {role, content}

    print("\n" + "="*60)
    print("  PLC Commissioner Egzaminator")
    print(f"  Model: {MODEL}")
    print(f"  Q&A: {QA_FILE.name}")
    print("  Wpisz 'koniec' lub Ctrl+C aby zakończyć")
    print("="*60 + "\n")

    # Pierwsze przywitanie
    history.append({"role": "user", "content": "start"})
    resp = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=history,
    )
    assistant_msg = resp.content[0].text
    history.append({"role": "assistant", "content": assistant_msg})
    print(f"Claude: {assistant_msg}\n")

    # Pętla konwersacji
    while True:
        try:
            user_input = input("Ty: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nDo zobaczenia!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("koniec", "exit", "quit"):
            print("Do zobaczenia! Powodzenia na rozmowie!")
            break

        history.append({"role": "user", "content": user_input})

        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=history,
            )
            assistant_msg = resp.content[0].text
        except anthropic.APIError as e:
            print(f"[BŁĄD API] {e}")
            history.pop()   # cofnij niedokończoną wiadomość
            continue

        history.append({"role": "assistant", "content": assistant_msg})
        print(f"\nClaude: {assistant_msg}\n")

        # Ogranicz historię do ostatnich 40 wiadomości (oszczędność tokenów)
        if len(history) > 40:
            history = history[-40:]


if __name__ == "__main__":
    main()
