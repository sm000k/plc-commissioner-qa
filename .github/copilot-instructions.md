# PLC Commissioner Q&A — Instrukcje dla Copilot

## Cel workspace
Generowanie i utrzymanie kompendium **Q&A** dla inżyniera PLC/Commissioner przygotowującego się do rozmowy kwalifikacyjnej z zakresu automatyki Siemens.

## Kontekst merytoryczny
Technologie: **Siemens TIA Portal** (V16–V19), **SIMATIC Safety Integrated**, **ET200 SP/MP**, **SINAMICS G120/S120/V90**, **Robot ABB IRC5**, **SICAR@GST**

## ⚡ Strategia pracy — automatyczne dzielenie zadań

> **OBOWIĄZKOWE** — stosuj ZAWSZE, niezależnie od tego czy użytkownik o to prosi.

### Zasada: max 3 pytania Q&A na jeden krok
Przy generowaniu/edycji dokumentu Q&A **NIGDY** nie przetwarzaj więcej niż **3 pytania naraz**. Po każdej partii:
1. Zapisz wynik do pliku (chapter lub draft)
2. Podsumuj co zrobiłeś (1 linia)
3. Przejdź do następnej partii

### Zasada: 1 sekcja = 1 krok
Przy pracy z wieloma sekcjami — przetwarzaj **jedną sekcję na raz**. Workflow:
1. Odczytaj chapter danej sekcji
2. Zbierz źródła (knowledge base, PDF)
3. Wygeneruj/edytuj pytania dla TEJ sekcji
4. Zapisz → przejdź do kolejnej sekcji

### Zasada: używaj todo list
Przy zadaniach obejmujących >1 sekcję lub >3 pytania — **ZAWSZE** utwórz todo list na początku i aktualizuj postęp po każdym kroku. Użytkownik musi widzieć co jest zrobione, a co jeszcze przed nim.

### Zasada: duży plik = czytaj fragmentami
Nie czytaj `LATEST.md` ani `qa_draft_v*.md` w całości. Czytaj tylko potrzebną sekcję (po numerze linii lub przez grep). Bazy wiedzy przeszukuj po słowach kluczowych, nie ładuj w całości.

### Zasada: aktualizuj nagłówek z datą i wersją
Przy KAŻDEJ edycji dokumentu Q&A → zaktualizuj nagłówek w `docs/chapters/00_header.md`:
- Tytuł: `# KOMPENDIUM Q&A — v{WERSJA}`
- Linia wersji: `### Wersja: v{WERSJA} | Data: {RRRR-MM-DD HH:MM} | Pytania: {LICZBA}`
- Data+godzina = moment ostatniej edycji (pobierz przez `[DateTime]::Now.ToString("yyyy-MM-dd HH:mm")`), wersja = bieżąca wersja z QA_LOG.md
- **NIE edytuj ręcznie spisu treści** — `build_toc.py` generuje go automatycznie w pipeline

### Zasada: ZAWSZE publikuj na GitHub Pages po edycji Q&A
Po KAŻDEJ zmianie w dokumencie Q&A (dodanie/edycja pytań, merge chapters) → uruchom:
```powershell
.\scripts\publish.ps1 -Message "Opis zmiany"
```
Skrypt wykonuje **cały pipeline automatycznie**:
1. `build_toc.py` — generuje TOC z chapter files → aktualizuje `00_header.md`
2. `merge_chapters.py` — scala chapters → `qa_draft_v12.md`
3. Kopiuje draft → `LATEST.md`
4. `build_manifest.py` — aktualizuje `sections_manifest.json`
5. Kopiuje `LATEST.md` → `index.md` (GitHub Pages)
6. `git add + commit + push`

**NIE trzeba** odpalać osobno `merge_chapters.py`, `build_toc.py`, `build_manifest.py` — `publish.ps1` robi wszystko.
Strona: https://sm000k.github.io/plc-commissioner-qa/

## Struktura projektu

```
docs/                                ← Aktywne dokumenty
  LATEST.md                          ← GŁÓWNY DOKUMENT Q&A (v12.4, 159 pytań, 21 sekcji) ✅
  sections_manifest.json             ← Indeks sekcji: zakresy linii, liczba pytań → CZYTAJ ZAMIAST LATEST.md
  qa_draft_v12.md                    ← Aktualny draft (= LATEST.md)
  chapters/                          ← Rozdziały Q&A (po 1 pliku na sekcję)
    00_header.md … 21_sicar.md
  kb/                                ← ⚡ Knowledge base podzielona per sekcja (14 plików, avg 40 linii)
    kb_S01_podstawy_plc.md … kb_S16_motion_control.md
  knowledge_base_controlbyte.md      ← MONOLIT — nie czytaj w całości → używaj docs/kb/
  knowledge_base_delta_v11.md        ← MONOLIT — nie czytaj w całości → używaj docs/kb/
  images/safety/                     ← 45 PNG z dokumentacji Siemens
  images/electrical/                 ← 9 schematów elektrycznych
  REFERENCE.md                       ← Mapa źródeł PDF i braków
  QA_LOG.md                          ← Log zmian
scripts/
  publish.ps1                        ← ⚡ Pipeline: TOC → merge → manifest → index.md → git push
  build_toc.py                       ← Generuje spis treści z chapters
  merge_chapters.py / split_chapters.py
  build_manifest.py                  ← Update sections_manifest.json
  egzaminator.py                     ← Bot przepytujący (Anthropic API)
  validate_qa.py                     ← Walidacja jakości Q&A
  extract_pdfs.py                    ← Ekstrakcja tekstu z PDF-ów (jednorazowo)
  split_knowledge_base.py            ← Podział KB per sekcja
  archive/                           ← Stare/jednorazowe skrypty
sources/pdfs/
  extracted/                         ← ⚡ Pre-wyekstrahowane teksty PDF (grep_search!)
  pdf_manifest.json                  ← Indeks PDF-ów: keywords, mapa sekcji
sources/sicar/                       ← Dokumentacja SICAR@TIA (72 PDF + extracted)
transcripts/controlbyte/             ← 52 transkrypcje YouTube
archive/                             ← Stare drafty v8–v11, slownik_v7
```

## Źródła wiedzy (PDFy w sources/pdfs/)

> Pełna lista źródeł, mapa pokrycia sekcji i lista brakujących PDF-ów do pobrania:
> **`docs/REFERENCE.md`** — otwórz gdy potrzebujesz dodać/znaleźć źródło.

Pre-wyekstrahowany tekst wszystkich PDF-ów: `sources/pdfs/extracted/*.txt` — szukaj przez `grep_search`.
Indeks PDF-ów z keywords i mapą sekcji: `sources/pdfs/pdf_manifest.json`.

## Aktywny dokument Q&A
- **Bieżący**: `docs/LATEST.md` = `docs/qa_draft_v12.md` — **159 pytań, 21 sekcji** (2026-04-11)
  - Zawiera PLAN NAUKI z tagami 🔴🟡🟢
  - Rozdziały jako osobne pliki: `docs/chapters/00_header.md` … `21_sicar.md`
  - Bazy wiedzy: `docs/knowledge_base_controlbyte.md`, `docs/knowledge_base_delta_v11.md`
  - Embedded: obrazy z `docs/images/safety/` (45 PNG), `docs/images/electrical/` (9 PNG)
- **Archiwum**: `archive/` — stare drafty v8–v11, slownik_v7

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
12. Napędy SINAMICS
13. E-Stop — normy, implementacja i obliczenia bezpieczeństwa
14. PROFINET — topologia, diagnostyka i zaawansowane funkcje
15. Kurtyny bezpieczeństwa i Muting
16. Motion Control i SINAMICS — praktyka commissioning
17. Realne scenariusze commissioning
18. TIA Portal — zaawansowane funkcje
19. Commissioning — dodawanie stacji i urządzeń do projektu
20. Schematy elektryczne — silniki i aparatura łączeniowa
21. SICAR@TIA — standard automatyki automotive

**Tematy priorytetowe do rozszerzenia w kolejnych wersjach:**
- §12 Napędy SINAMICS — rozbudowa parametryzacji G120/S120, faultcodes (+8 pytań)
- §7 PROFIsafe — telegramy Safety 30/54/900 w napędach (+4 pytania)
- §13 E-Stop — obliczenia PFH/DC z Application Example (+3 pytania)
- §19 Commissioning stacje — dodawanie ET200/napędów do istniejącej linii (+4 pytania)
- §21 SICAR — Safety w SICAR, sequencing, diagnostyka (+5 pytań)
- ProDiag — diagnostyka online
- PROFINET TSN (Time Sensitive Networking)

**Tematy WYKLUCZONE (poza zakresem kompendium):**
- ~~HMI / WinCC~~ — poza zakresem stanowiska
- ~~PID regulacja~~ — poza zakresem
- ~~SCL wzorce praktyczne~~ — poza zakresem
- ~~Backup/restore TIA Portal~~ — poza zakresem

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

1. **Sprawdź manifest** — `docs/sections_manifest.json` → znajdź zakres linii sekcji (start/end)
2. **Odczytaj rozdział** — `docs/chapters/XX_*.md` odpowiadający sekcji pytania
3. **Sprawdź knowledge base per sekcja** — `docs/kb/kb_SXX_*.md` (tylko plik dla TEJ sekcji, nie monolity!)
4. **Jeśli brakuje informacji** — `grep_search` po `sources/pdfs/extracted/*.txt` (pre-wyekstrahowany tekst)
5. **Generuj odpowiedź** — dopiero po zebraniu materiału źródłowego
6. **Self-check** — sprawdź odpowiedź wg Quality Checklist poniżej

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
