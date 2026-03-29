# PLC Commissioner Q&A — Instrukcje dla Copilot

## Cel workspace
Generowanie i utrzymanie kompendium **Q&A** dla inżyniera PLC/Commissioner przygotowującego się do rozmowy kwalifikacyjnej z zakresu automatyki Siemens.

## Kontekst merytoryczny
Technologie: **Siemens TIA Portal** (V16–V19), **SIMATIC Safety Integrated**, **ET200 SP/MP**, **SINAMICS G120/S120/V90**, **Robot ABB IRC5**, **SICAR@GST**

## Struktura projektu

```
docs/                          ← Aktywne dokumenty
  qa_draft_v9.md               ← GŁÓWNY DOKUMENT Q&A (bieżący) ✅
  qa_draft_v8.md               ← Poprzednia wersja (backup)
  images/safety/               ← 45 PNG z dokumentacji Siemens
  knowledge_base_controlbyte.md
  QA_LOG.md
  slownik_v7.md
scripts/                       ← Skrypty produkcyjne
  Get-YouTubeTranscripts.py
  Build-KnowledgeBase.py
  Merge-KnowledgeBase.py
  New-QADocument.ps1
  Read-DocxText.ps1
  _build_selection.py
sources/pdfs/                  ← Dokumentacja Siemens (PDFy)
sources/books/                 ← Materiały edukacyjne
archive/docx/                  ← Stare wersje .docx (v3–v7)
archive/old-docs/              ← Stare pliki robocze
transcripts/controlbyte/       ← Transkrypcje YouTube (52 filmy)
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

## Aktywny dokument Q&A
- **Bieżący**: `docs/qa_draft_v9.md` — **115 pytań, 19 sekcji, ~115 KB**
  - Zawiera PLAN NAUKI (linie 7–85) z tagami 🔴🟡🟢
  - Embedded: 9 obrazów z `docs/images/safety/` (45 PNG łącznie)
- **Poprzedni**: `docs/qa_draft_v8.md` — 110 pytań (backup)
- **Historia**: `archive/docx/` — wersje v3–v7 .docx

Następna wersja: `docs/qa_draft_v10.md`

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
- Odpowiedź = **definicja** (1-2 zdania) + **szczegóły** (bullet list) + **praktyczny przykład** lub **procedura**
- Podawaj numery parametrów Siemens (np. `p0840`, `r0945`) tam gdzie możliwe
- Podawaj normy (EN ISO 13849-1, IEC 61508, IEC 62061, EN 60204-1)
- Nie fabrykuj danych technicznych — źródłem są PDFs w workspace
- Używaj terminologii Siemens (nie generycznej): F-CPU, passivation, F-signature, collective signature
- Język: **polski**
- Poziom: szczegółowy, techniczny, gotowy do rozmowy kwalifikacyjnej

## Zakres tematyczny — 19 sekcji

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
19. Słownik pojęć (PLC / Safety / PROFINET / Napędy)

> ⚠️ Sekcja **Elektrotechnika praktyczna** usunięta — zbyt ogólna, wykracza poza zakres rozmowy kwal. PLC/Commissioner.

**Tematy priorytetowe do rozszerzenia w kolejnych wersjach:**
- TIA Portal V19 — nowe funkcje
- SINAMICS S210 / V90 z PROFINET
- ProDiag — diagnostyka online
- S7-1500 R/H — redundancja CPU
- IO-Link — czujniki inteligentne
- OPC UA — integracja MES/SCADA
- PROFINET TSN (Time Sensitive Networking)

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
