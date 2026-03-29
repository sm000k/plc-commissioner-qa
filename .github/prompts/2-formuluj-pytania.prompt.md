---
mode: agent
description: "Faza 2: Sformułuj nowe pytania Q&A na podstawie analizy braków z Fazy 1"
tools: ['read_file', 'file_search', 'create_file', 'replace_string_in_file']
---

# Faza 2 — Formułowanie pytań Q&A

## Twój cel
Na podstawie `docs/analiza_zrodel.md` (wynik Fazy 1) sformułuj nowe pytania dla brakujących tematów i zapisz je do `docs/pytania_draft_v{n}.md`.

## Krok 1 — Odczytaj analizę braków

```
#file:docs/analiza_zrodel.md
```

## Krok 2 — Zasady formułowania pytań

Każde pytanie musi być jednego z 5 typów — zaplanuj mix dla każdego tematu:

| Typ | Format | Przykład |
|-----|--------|---------|
| **Definicja** | "Co to jest X i jak działa?" | "Co to jest PROFIsafe i co zawiera jego pakiet?" |
| **Konfiguracja** | "Jak konfigurujesz X w TIA Portal?" | "Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?" |
| **Diagnostyka** | "Co sprawdzasz gdy X nie działa?" | "Moduł nie wychodzi z passivation — co sprawdzasz?" |
| **Obliczenia** | "Jak obliczasz / dobierasz X?" | "Jak wygląda łańcuch Safety i co liczy się do PFH?" |
| **Scenariusz** | "Masz sytuację X — co robisz?" | "CPU przeszło w STOP podczas produkcji — pierwsze 3 kroki" |

**Reguła 3x3**: każdy nowy temat powinien mieć min. 3 pytania, w tym min. 1 praktyczne (konfiguracja/diagnostyka/scenariusz).

## Krok 3 — Generuj pytania dla brakujących tematów

### TIA Portal V19 (priorytet WYSOKI)
Zaproponuj min. 5 pytań:
1. Co nowego w TIA Portal V19 w porównaniu do V18?
2. Jak działa AI-Assisted Engineering w TIA V19?
3. ...

### SINAMICS S210 / Servo komisjonowanie
Zaproponuj min. 4 pytania:
1. Czym różni się SINAMICS S210 od G120 i kiedy wybierasz który?
2. Jak konfigurujesz V90 z PROFIdrive przez PROFINET?
3. ...

### ProDiag — diagnostyka inline
Zaproponuj min. 3 pytania:
1. Co to jest ProDiag i czym różni się od standardowej diagnostyki?
2. ...

### S7-1500R/H — redundancja
Zaproponuj min. 4 pytania:
1. Co to jest S7-1500R i kiedy go używasz?
2. Co się dzieje podczas switchover w S7-1500H?
3. ...

### IO-Link
Zaproponuj min. 3 pytania:
1. Co to jest IO-Link i jakie ma zalety nad standardowym 24VDC?
2. Jak konfigurujesz IO-Link Master w TIA Portal?
3. ...

### Safety — tematy zaawansowane
Zaproponuj pytania dla:
- Safety door interlock z RFID (Siemens 3SE6/3SE7)
- Two-hand control — blok LSafe_TwoHand
- Safety z robotem ABB przez PROFIsafe
- Proof test interval — obliczenia i praktyka

## Krok 4 — Formatuj pytania do draftu

Zapisz pytania do `docs/pytania_draft_v7.md` w formacie:

```markdown
# Pytania do Q&A — wersja 7

## NOWE pytania — priorytet WYSOKI

### Sekcja: TIA Portal V19
Q1. Co nowego wprowadza TIA Portal V19 w stosunku do V18?
Q2. Jak działa AI-Assisted Engineering w TIA Portal V19?
Q3. Co to jest Unified Engineering i jak wpływa na workflow?
Q4. Jak konfigurujesz PROFINET TSN w TIA Portal V19?
Q5. Co to są Smart Objects w TIA V19?

### Sekcja: SINAMICS S210 / Servo
Q6. Czym różni się SINAMICS S210 od G120?
...

## ROZSZERZENIA istniejących sekcji

### Sekcja 8: Napędy Safety — SINAMICS
Q_ext1. Jak konfigurujesz SLS (Safely Limited Speed) w SINAMICS G120 przez PROFIsafe?
...

### Sekcja 11: Commissioning i diagnostyka  
Q_ext2. Jak korzystasz z ProDiag podczas commissioning?
...

## POPRAWKI ISTNIEJĄCYCH ODPOWIEDZI

### Sekcja 3, P5 (substitute value)
Problem: brakuje opisu jak ustawić substitute value dla grupy F-DO
Poprawka: [opisz co dodać]
```

## Krok 5 — Weryfikacja kompletności

Przed przejściem do Fazy 3 upewnij się że:
- [ ] Każda priorytetowa luka z analizy ma min. 3 nowe pytania
- [ ] Mix typów pytań (definicja/konfiguracja/diagnostyka/scenariusz)
- [ ] Pytania są sformułowane jak na rozmowie kwalifikacyjnej (pełne zdania)
- [ ] Brak duplikatów z istniejącymi pytaniami Q&A
- [ ] Numery pytań są ciągłe w obrębie każdej sekcji

## Po wykonaniu
`docs/pytania_draft_v7.md` jest gotowy → przejdź do Fazy 3 (`3-generuj-dokument.prompt.md`).
