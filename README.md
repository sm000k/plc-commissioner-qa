# PLC Commissioner Q&A — Kompendium wiedzy

Baza wiedzy Q&A dla inżyniera PLC/Commissioner przygotowującego się do rozmowy kwalifikacyjnej.

**Zakres:** Siemens TIA Portal (V16–V19), SIMATIC Safety Integrated, ET200 SP/MP, SINAMICS G120/S120/V90, Robot ABB IRC5, SICAR@GST, PROFINET

---

## Struktura projektu

```
docs/
  qa_draft_v9.md              ← GŁÓWNY DOKUMENT Q&A (115 pytań, 19 sekcji) ✅ AKTYWNY
  qa_draft_v8.md              ← Poprzednia wersja (110 pytań) — backup
  images/safety/              ← 45 diagramów PNG z dokumentacji Siemens
  knowledge_base_controlbyte.md ← Baza wiedzy z transkrypcji YouTube
  QA_LOG.md                   ← Historia zmian i wersji
  slownik_v7.md               ← Słownik pojęć PLC/Safety/Napędy

scripts/
  Get-YouTubeTranscripts.py   ← Pobieranie transkrypcji z YouTube (Gemini API)
  Build-KnowledgeBase.py      ← Ekstrakcja Q&A z transkrypcji (Gemini)
  Merge-KnowledgeBase.py      ← Scalanie nowej wiedzy do dokumentu Q&A
  New-QADocument.ps1          ← Generowanie .docx z pliku Markdown
  Read-DocxText.ps1           ← Ekstrakcja tekstu z .docx do analizy
  _build_selection.py         ← Filtr filmów YouTube do pobrania

sources/
  pdfs/                       ← Dokumentacja Siemens (PDFy źródłowe)
  books/                      ← Materiały edukacyjne S7-1200

archive/
  docx/                       ← Stare wersje dokumentu Q&A (v3–v7)
  old-docs/                   ← Stare pliki robocze

transcripts/
  controlbyte/                ← Transkrypcje z kanału @controlbytepl (52 filmy)

.github/
  copilot-instructions.md     ← Instrukcje dla GitHub Copilot
  prompts/                    ← Prompty workflow (zbierz→formułuj→generuj)
```

---

## Źródła wiedzy (PDFy)

| Plik | Zawartość |
|------|-----------|
| `21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en.pdf` | E-Stop SIL3, klasy zatrzymania, PFH, ISO 13849-1 |
| `39198632_Wiring_Example_en.pdf` | Okablowanie F-DI/F-DO, PM/PP-switching |
| `safety_getting_started_en-US.pdf` | SIMATIC Safety — podstawy, architektura |
| `SIMATIC Safety - Konfiguracja i programowanie (2).pdf` | Zaawansowana konfiguracja Safety, F-bloki |
| `SIMATIC Safety Integrated – wszystko w jednym sterowniku PLC.pdf` | Koncepcja Safety Integrated, F-CPU, PROFIsafe |
| `btc.pl-SCL-S7-1200.pdf` | Programowanie S7-1200 w SCL |
| `siemens SCL.PDF` | SCL S7-300/400, historyczne tło |
| `Sterowniki_PLC.pdf` | Podręcznik akademicki (⚠️ błędna klasyfikacja sprzętu) |

---

## Workflow generowania

### Aktualizacja Q&A z nowych transkrypcji:
```powershell
# 1. Pobierz transkrypcje (wymaga GEMINI_API_KEY)
$env:GEMINI_API_KEY="..."
python scripts/Get-YouTubeTranscripts.py --selection

# 2. Wyciągnij wiedzę z transkrypcji
python scripts/Build-KnowledgeBase.py

# 3. Scal z dokumentem Q&A
python scripts/Merge-KnowledgeBase.py
```

### Generowanie .docx z Markdown:
```powershell
.\scripts\New-QADocument.ps1 docs/qa_draft_v9.md
```

---

## Sekcje Q&A (19 sekcji, 110 pytań)

1. Podstawy PLC i automatyki (14 pyt.)
2. Architektura SIMATIC Safety Integrated (8 pyt.)
3. Moduły F-DI / F-DO (10 pyt.)
4. Struktury głosowania 1oo1/1oo2/2oo3 (3 pyt.)
5. Passivation, Reintegration, ACK (4 pyt.)
6. Safe State (3 pyt.)
7. PROFIsafe (4 pyt.)
8. Napędy Safety — SINAMICS (6 pyt.)
9. TIA Portal — Safety praktyka (6 pyt.)
10. Robot ABB IRC5 (5 pyt.)
11. Commissioning i diagnostyka (9 pyt.)
12. SICAR i Napędy SINAMICS (4 pyt.)
13. E-Stop — normy i obliczenia (6 pyt.)
14. PROFINET — topologia i diagnostyka (7 pyt.)
15. Kurtyny bezpieczeństwa i Muting (4 pyt.)
16. Motion Control i SINAMICS (5 pyt.)
17. Realne scenariusze commissioning (5 pyt.)
18. TIA Portal — zaawansowane funkcje (4 pyt.)
19. Słownik pojęć (2 pyt.)
