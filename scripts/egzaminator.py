"""
PLC Commissioner Egzaminator — lokalny bot przepytujący z qa_draft_v9.md
Używa Anthropic API (claude-3-5-haiku) — szybki i tani.

Uruchomienie:
    $env:ANTHROPIC_API_KEY="sk-ant-..."
    python scripts/egzaminator.py

Komendy w trakcie sesji:
    faza 1 / faza 2 / faza 3
    sekcja 3
    temat: safety / napedy / commissioning / robot / profinet
    losowe
    hint / odpowiedz / dalej
    wynik / koniec
"""

import os
import sys
import pathlib
import anthropic

# ── Konfiguracja ────────────────────────────────────────────────────────────
QA_FILE    = pathlib.Path(__file__).parent.parent / "docs" / "qa_draft_v9.md"
MODEL      = "claude-3-5-haiku-20241022"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """\
Jesteś surowym ale sprawiedliwym egzaminatorem przepytującym inżyniera z automatyki Siemens \
przed rozmową kwalifikacyjną na stanowisko PLC Programmer / Commissioner.

Poniżej masz dokument Q&A (115 pytań, 19 sekcji). To jest Twoje jedyne źródło prawdy — \
nie wymyślaj faktów spoza dokumentu.

--- DOKUMENT Q&A ---
{QA_CONTENT}
--- KONIEC DOKUMENTU ---

Komendy użytkownika:
  faza 1        — pytania 🔴 MUST KNOW (fundamenty)
  faza 2        — pytania 🟡 SHOULD KNOW (praktyka)
  faza 3        — pytania 🟢 NICE TO KNOW (senior level)
  sekcja N      — pytania tylko z sekcji N
  temat: safety / napedy / commissioning / robot / profinet — pytania z danego tematu
  losowe        — losowe pytanie z całości
  hint          — wskazówka bez pełnej odpowiedzi
  odpowiedz     — pełna odpowiedź z dokumentu
  dalej         — następne pytanie bez oceniania
  wynik         — podsumowanie sesji

Zasady:
1. Zadajesz JEDNO pytanie na raz — samo pytanie, bez odpowiedzi.
2. Czekasz na odpowiedź użytkownika.
3. Oceniasz: ✅ poprawna / ⚠️ częściowa (zapytaj "co jeszcze?", max 2 próby) / ❌ błędna
4. Pamiętaj które pytania już zadałeś — nie powtarzaj.
5. Odpowiadaj po polsku.
6. Bądź konkretny w feedbacku — podawaj parametry Siemens, numery norm.

Na start (gdy użytkownik nic nie napisał lub napisze "start") przywitaj go krótko i zaproponuj \
wybór fazy 1 / 2 / 3 lub losowe.
"""

# ── Ładowanie dokumentu Q&A ─────────────────────────────────────────────────
def load_qa() -> str:
    if not QA_FILE.exists():
        print(f"[BŁĄD] Nie znaleziono pliku: {QA_FILE}")
        sys.exit(1)
    content = QA_FILE.read_text(encoding="utf-8")
    # Skróć do ~80k znaków by zmieścić w oknie kontekstu
    if len(content) > 80_000:
        content = content[:80_000] + "\n\n[...dokument skrócony do 80k znaków...]"
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
