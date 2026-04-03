# PLC Commissioner Q&A — Instrukcje dla Copilot

## Cel workspace
Generowanie i utrzymanie kompendium **Q&A** dla inżyniera PLC/Commissioner przygotowującego się do rozmowy kwalifikacyjnej z zakresu automatyki Siemens.

## Kontekst merytoryczny
Technologie: **Siemens TIA Portal** (V16–V19), **SIMATIC Safety Integrated**, **ET200 SP/MP**, **SINAMICS G120/S120/V90**, **Robot ABB IRC5**, **SICAR@GST**

## Struktura projektu

```
docs/                                ← Aktywne dokumenty
  LATEST.md                          ← GŁÓWNY DOKUMENT Q&A (v12, 155 pytań, 20 sekcji) ✅
  qa_draft_v12.md                    ← Aktualny draft
  qa_draft_v11.md                    ← Poprzednia wersja
  chapters/                          ← Rozdziały Q&A (po 1 pliku na sekcję)
    00_header.md … 20_schematy_elektryczne.md
  knowledge_base_controlbyte.md      ← Baza wiedzy: transkrypcje ControlByte (52 filmy)
  knowledge_base_delta_v11.md        ← Delta wiedzy: patch v11
  images/safety/                     ← 45 PNG z dokumentacji Siemens
  QA_LOG.md                          ← Log zmian
  slownik_v7.md
scripts/                             ← Skrypty produkcyjne
  egzaminator.py                     ← Bot przepytujący (Anthropic API)
  merge_chapters.py / split_chapters.py
  Get-YouTubeTranscripts.py
  Build-KnowledgeBase.py
  Merge-KnowledgeBase.py
  New-QADocument.ps1
  Read-DocxText.ps1
  _build_selection.py
sources/pdfs/                        ← Dokumentacja Siemens (PDFy)
sources/books/                       ← Materiały edukacyjne
archive/docx/                        ← Stare wersje .docx (v3–v7)
archive/old-docs/                    ← Stare pliki robocze
transcripts/controlbyte/             ← Transkrypcje YouTube (52 filmy)
```

## Źródła wiedzy (PDFy w sources/pdfs/)

| Plik | Zawartość |
|------|-----------|
| `21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en.pdf` | Application Example: E-Stop SIL3, klasy zatrzymania, PFH, obliczenia ISO 13849-1 |
| `39198632_Wiring_Example_en.pdf` | Przykłady okablowania F-DI/F-DO, PM-switching, PP-switching, relay |
| `safety_getting_started_en-US.pdf` | Podstawy SIMATIC Safety — pierwsze kroki, architektura |
| `SIMATIC Safety - Konfiguracja i programowanie (2).pdf` | Zaawansowana konfiguracja Safety, programowanie F-bloków |
| `SIMATIC Safety Integrated – wszystko w jednym sterowniku PLC.pdf` | Koncepcja Safety Integrated, F-CPU, PROFIsafe |
| `btc.pl-SCL-S7-1200.pdf` | Programowanie S7-1200 w SCL (TIA Portal V13+) |
| `Sterowniki_PLC.pdf` | Ogólne informacje o sterownikach PLC |
| `siemens SCL.PDF` | Programowanie w SCL — uzupełnienie |

## Aktywny dokument Q&A
- **Bieżący**: `docs/LATEST.md` = `docs/qa_draft_v12.md` — **155 pytań, 20 sekcji** (2026-04-01)
  - Zawiera PLAN NAUKI z tagami 🔴🟡🟢
  - Rozdziały jako osobne pliki: `docs/chapters/00_header.md` … `20_schematy_elektryczne.md`
  - Bazy wiedzy: `docs/knowledge_base_controlbyte.md`, `docs/knowledge_base_delta_v11.md`
  - Embedded: obrazy z `docs/images/safety/` (45 PNG łącznie)
- **Poprzedni**: `docs/qa_draft_v11.md` — backup
- **Historia**: `archive/docx/` — wersje v3–v7 .docx

Następna wersja: `docs/qa_draft_v13.md`

## Format dokumentu Q&A

**Struktura pliku Markdown (wejście dla skryptu):**
```
# KOMPENDIUM Q&A
## Podtytuł i źródła
---
## 1. NAZWA SEKCJI
### 1. Pytanie w formie pełnego zdania?
Treść odpowiedzi — definicja + szczegóły.
- Punkt kluczowy 1
- Punkt kluczowy 2
Źródło/uwaga praktyczna.

### 2. Kolejne pytanie?
...
```

**Reguły jakości odpowiedzi:**
- **MAX 30 zdań na odpowiedź** — zwięzłe, konkretne, bez lania wody. Definicja (1-2 zd.) + bullet list (3-6 pkt) + praktyka (3-5 kroków)
- Podawaj numery parametrów Siemens (np. `p0840`, `r0945`) **tylko gdy znasz je ze źródeł**
- Podawaj normy (EN ISO 13849-1, IEC 61508, IEC 62061, EN 60204-1)
- **NIGDY** nie fabrykuj danych technicznych — źródłem są pliki w workspace (PDFs, chapters, knowledge base)
- Używaj terminologii Siemens (nie generycznej) — patrz tabela terminologii poniżej
- Każda odpowiedź MUSI zawierać min. 1 element praktyczny: procedura krok-po-kroku / scenariusz z obiektu / co sprawdzasz w TIA Portal / komenda diagnostyczna
- Język: **polski**
- Poziom: szczegółowy, techniczny, gotowy do rozmowy kwalifikacyjnej

## Zakres tematyczny — 20 sekcji

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
19. Commissioning — dodawanie stacji i urządzeń do projektu
20. Schematy elektryczne — silniki i aparatura łączeniowa

**Tematy priorytetowe do rozszerzenia w kolejnych wersjach:**
- TIA Portal V19 — nowe funkcje
- SINAMICS S210 / V90 z PROFINET
- ProDiag — diagnostyka online
- S7-1500 R/H — redundancja CPU
- IO-Link — czujniki inteligentne
- OPC UA — integracja MES/SCADA
- PROFINET TSN (Time Sensitive Networking)

## Terminologia Siemens (używaj ZAWSZE zamiast odpowiedników generycznych)

| ✅ Termin Siemens | ❌ NIE używaj | Kontekst |
|-------------------|---------------|----------|
| F-CPU | sterownik bezpieczeństwa | Failsafe CPU z dual-channel processing |
| passivation | wyłączenie/blokada modułu | Stan błędu F-I/O → substitute values |
| reintegration | resetowanie/restart modułu | Ręczne potwierdzenie powrotu po passivation |
| F-signature | suma kontrolna programu | Podpis jednego bloku Safety |
| collective signature | podpis całości | Podpis CAŁEGO programu Safety |
| substitute value | wartość domyślna / zastępcza | Wartość wyjścia podczas passivation (zwykle 0) |
| F-monitoring time | timeout komunikacji | Czas nadzoru PROFIsafe |
| value status | bit jakości | Kwalifikator poprawności sygnału F-I/O |
| discrepancy time | czas rozbieżności | Max dozwolona różnica między kanałami 1oo2 |
| F-address | adres Safety / PROFIsafe | Unikalny adres urządzenia w sieci PROFIsafe |
| STO / SS1 / SS2 / SOS / SLS / SDI / SBC | bezpieczne zatrzymanie / ograniczenie | Funkcje Safety napędów wg IEC 61800-5-2 |
| PROFIdrive | protokół napędowy | Standard komunikacji napędów przez PROFINET |
| telegram (1/20/105/111) | ramka / pakiet danych | Struktura danych PROFIdrive |
| CU (Control Unit) | jednostka sterująca | Moduł sterujący napędu SINAMICS |
| AOP / BOP / IOP | panel operatorski napędu | Advanced/Basic/Intelligent Operator Panel |
| isochronous mode | tryb synchroniczny | Synchronizacja cyklu PLC z cyklem PROFINET |
| GSDML | plik opisowy urządzenia | GSD Markup Language dla urządzeń PROFINET |

## Polityka anty-halucynacji

> ⛔ **KRYTYCZNE** — te zasady obowiązują przy KAŻDYM generowaniu treści Q&A.

1. **NIGDY nie wymyślaj** numerów parametrów (pXXXX/rXXXX), adresów, zakresów wartości, wersji firmware.
   - Nie znasz numeru parametru? → napisz `pXXXX (sprawdź w dokumentacji SINAMICS)` zamiast zgadywać.
   - Nie znasz zakresu wartości? → podaj tylko kierunek (np. „kilkadziesiąt ms", „rzędu sekund") zamiast wymyślać konkretne liczby.
2. **NIGDY nie fabrykuj** numerów norm, klauzul, artykułów. Podawaj tylko normy z listy poniżej lub znalezione w źródłach.
3. **Oznaczaj poziom pewności** przy niepewnych faktach:
   - `[ZWERYFIKOWANE]` — fakt znaleziony w pliku źródłowym workspace (PDF, chapter, knowledge base)
   - `[PRAWDOPODOBNE]` — fakt z ogólnej wiedzy domenowej, spójny ze źródłami ale nie potwierdzony dosłownie
   - `⚠️ DO WERYFIKACJI` — fakt niepewny, wymaga sprawdzenia w dokumentacji Siemens
4. Gdy nie wiesz → powiedz **„Nie znalazłem w źródłach — wymaga weryfikacji w dokumentacji Siemens"** zamiast generować wiarygodnie brzmiącą odpowiedź.
5. **Normy dozwolone** (nie wymyślaj innych):
   - Bezpieczeństwo maszyn: EN ISO 13849-1 (PL a–e), IEC 62061 (SIL CL), EN ISO 12100 (ocena ryzyka)
   - Napędy Safety: IEC 61800-5-2 (STO/SS1/SS2/SOS/SLS/SDI/SBC)
   - Systemy Safety: IEC 61508 (SIL 1–3), EN 60204-1 (kategorie zatrzymania 0/1/2)
   - E-Stop: EN ISO 13850, przekaźniki: EN 60947-5-1
   - Kurtyny: IEC 61496, EN ISO 13855 (odległości bezpieczeństwa)
   - PLC ogólne: IEC 61131-3 (języki programowania)

## Workflow „source-first" — obowiązkowa kolejność

> Przed wygenerowaniem lub zmodyfikowaniem JAKIEJKOLWIEK odpowiedzi Q&A, ZAWSZE wykonaj:

1. **Odczytaj rozdział** — `docs/chapters/XX_*.md` odpowiadający sekcji pytania
2. **Sprawdź bazy wiedzy** — `docs/knowledge_base_controlbyte.md` i `docs/knowledge_base_delta_v11.md` (szukaj słów kluczowych z pytania)
3. **Jeśli brakuje informacji** — dopiero wtedy sięgnij do `sources/pdfs/` (ekstrakcja tekstu z PDF)
4. **Generuj odpowiedź** — dopiero po zebraniu materiału źródłowego
5. **Self-check** — sprawdź odpowiedź wg Quality Checklist poniżej

## Quality Checklist — każda odpowiedź musi przejść

- [ ] ✅ **Definicja** — czy odpowiedź zaczyna się od 1-2 zdań definiujących pojęcie?
- [ ] ✅ **Bullet list** — czy zawiera min. 3 punkty kluczowe ze szczegółami technicznymi?
- [ ] ✅ **Praktyka** — czy zawiera min. 1 element praktyczny (procedura / scenariusz / diagnostyka / konfiguracja TIA Portal)?
- [ ] ✅ **Parametry** — czy numery parametrów Siemens (pXXXX) pochodzą ze źródeł, nie są wymyślone?
- [ ] ✅ **Terminologia** — czy używa terminów Siemens z tabeli powyżej (nie generycznych)?
- [ ] ✅ **Źródło** — czy podano źródło (PDF, norma, knowledge base) lub oznaczono `⚠️ DO WERYFIKACJI`?

## Skrypty automatyzacji

| Skrypt | Opis |
|--------|------|
| `scripts/Get-YouTubeTranscripts.py` | Pobiera transkrypcje YouTube przez Gemini API |
| `scripts/Build-KnowledgeBase.py` | Generuje bazę wiedzy Q&A z transkrypcji |
| `scripts/Merge-KnowledgeBase.py` | Scala nową wiedzę do dokumentu Q&A |
| `scripts/New-QADocument.ps1` | Generuje .docx z pliku Markdown |
| `scripts/Read-DocxText.ps1` | Wyciąga tekst z .docx do analizy |
| `scripts/_build_selection.py` | Filtruje listę filmów YouTube do pobrania |

## Workflow generowania (3 fazy)

Używaj promptów z `.github/prompts/`:
1. `1-zbierz-zrodla.prompt.md` — Faza 1: ekstrakcja informacji z PDF i analiza braków
2. `2-formuluj-pytania.prompt.md` — Faza 2: formułowanie nowych pytań
3. `3-generuj-dokument.prompt.md` — Faza 3: generowanie odpowiedzi i .docx

## Polityka dokumentacji
- Log zmian: `docs/QA_LOG.md`
- Roboczy draft nowej wersji: `docs/qa_draft_v{n}.md`
- Aktualny dokument zawsze w: `docs/LATEST.md`
- Rozdziały: `docs/chapters/XX_*.md` (scalane przez `scripts/merge_chapters.py`)
