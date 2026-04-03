---
agent: qa-expert
description: "Quality pass: audit + fix chapters automatically. Run with: @qa-expert /4-quality-pass [chapters]"
---

# Quality Pass — Automatyczny przegląd i poprawa rozdziałów

## Cel
Przeprowadź kompletny przegląd jakości wskazanych rozdziałów i **napraw problemy bezpośrednio w plikach**.

## Parametry

Użytkownik podaje zakres, np.:
- `all` — wszystkie rozdziały 01-20
- `01-05` — rozdziały 1 do 5
- `14` — pojedynczy rozdział
- `safety` — rozdziały 02, 03, 04, 05, 06, 07, 08, 09 (Safety-related)
- `napedy` — rozdziały 08, 12, 16 (SINAMICS/drives)
- `commissioning` — rozdziały 11, 17, 19

Jeśli nie podano zakresu, zapytaj użytkownika.

## Workflow

### Krok 1 — Walidacja (read-only)

Dla każdego rozdziału w zakresie, przeczytaj plik `docs/chapters/XX_*.md` i sprawdź:

| # | Kryterium | Jak sprawdzić | Naprawa |
|---|-----------|---------------|---------|
| 1 | **Terminologia Siemens** | Szukaj: "sterownik bezpieczeństwa", "sterownik safety", "moduł safety", "suma kontrolna", "wartość domyślna", "timeout komunikacji", "adres Safety", "master/slave" | Zamień na: F-CPU, moduł F-DI, F-signature, substitute value, F-monitoring time, F-address, IO-Controller/IO-Device |
| 2 | **Długość ≤30 zdań** | Policz zdania (przybliżenie: `.?!` + spacja/koniec) | Skróć: usuń powtórzenia, kompresuj listy, ogranicz do: definicja 1-2zd + 4-6 bulletów + praktyka 3-5 kroków |
| 3 | **Źródło** | Szukaj: `Źródło:`, `transkrypcje`, `ZWERYFIKOWANE`, `PRAWDOPODOBNE`, `DO WERYFIKACJI` | Dodaj `*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*` |
| 4 | **Element praktyczny** | Szukaj: procedura, krok po kroku, TIA Portal, diagnostyka, konfiguracja, commissioning | Dodaj min. 1 scenariusz: "W TIA Portal: ...", "Na obiekcie: ...", "Diagnostyka: ..." |
| 5 | **Numeracja** | Sprawdź `### N.M.` — N musi = nr sekcji | Popraw numery |
| 6 | **Podejrzane parametry** | pXXXX/rXXXX — sprawdź czy występują w knowledge_base lub PDF | Oznacz `⚠️ DO WERYFIKACJI` |

### Krok 2 — Raport

Wypisz znalezione problemy w formacie:
```
## Raport — rozdziały [zakres]
| Rozdział | Problem | Linia | Naprawa |
|----------|---------|-------|---------|
| 04 | "sterownik safety" → "F-CPU" | Q4.4 tytuł | AUTO |
| 07 | brak źródła | Q7.1 | AUTO |
| 12 | za krótkie (3 zd.) | Q12.1 | MANUAL |
```

### Krok 3 — Automatyczna naprawa

Dla problemów oznaczonych `AUTO`:
1. Edytuj plik `docs/chapters/XX_*.md` bezpośrednio
2. Po zakończeniu wszystkich edycji uruchom merge:
   ```
   python scripts/merge_chapters.py docs/qa_draft_v12.md
   Copy-Item docs/qa_draft_v12.md docs/LATEST.md -Force
   ```

Dla problemów `MANUAL` — wypisz co trzeba zrobić ręcznie (np. rozbudowa odpowiedzi wymaga źródeł).

### Krok 4 — Podsumowanie

```
✅ Naprawiono automatycznie: X problemów
⚠️ Wymaga ręcznej interwencji: Y problemów
📊 Statystyki: Z rozdziałów sprawdzonych, N pytań przejrzanych
```

## Ograniczenia

- NIE dodawaj nowych pytań — tylko poprawiaj istniejące
- NIE usuwaj treści merytorycznej — tylko kompresuj/przeformatuj
- NIE zmieniaj kolejności pytań
- Przy skracaniu zachowaj: definicję + kluczowe fakty + element praktyczny
