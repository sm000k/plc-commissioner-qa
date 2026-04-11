# PLC Commissioner Q&A — Kompendium wiedzy

Baza wiedzy Q&A dla inżyniera PLC/Commissioner przygotowującego się do rozmowy kwalifikacyjnej.

**Zakres:** Siemens TIA Portal (V16–V19), SIMATIC Safety Integrated, ET200 SP/MP, SINAMICS G120/S120/V90, Robot ABB IRC5, SICAR@GST, PROFINET

**Wersja:** v12.4 | **159 pytań** | **21 sekcji** | [Otwórz online](https://sm000k.github.io/plc-commissioner-qa/)

---

## Struktura projektu

```
docs/
  LATEST.md                   ← GŁÓWNY DOKUMENT Q&A (v12.4, 159 pytań) ✅ AKTYWNY
  qa_draft_v12.md             ← Aktualny draft (= LATEST.md, scalany z chapters)
  chapters/                   ← Rozdziały źródłowe (21 plików, edytujesz TU)
    00_header.md … 21_sicar.md
  kb/                         ← Baza wiedzy per sekcja (14 plików)
  images/safety/              ← 45 diagramów PNG z dokumentacji Siemens
  images/electrical/          ← 9 schematów elektrycznych
  sections_manifest.json      ← Indeks sekcji (auto-generowany)
  QA_LOG.md                   ← Historia zmian i wersji
  REFERENCE.md                ← Mapa źródeł PDF i braków
  knowledge_base_controlbyte.md ← Baza wiedzy z transkrypcji YouTube
  _config.yml                 ← Konfiguracja Jekyll (GitHub Pages)

scripts/
  publish.ps1                 ← Pipeline: TOC → merge → manifest → git push
  merge_chapters.py           ← Scala chapters → qa_draft_v12.md
  build_toc.py                ← Generuje spis treści w 00_header.md
  build_manifest.py           ← Generuje sections_manifest.json
  egzaminator.py              ← Bot przepytujący (Anthropic API)
  validate_qa.py              ← Walidacja jakości Q&A
  split_chapters.py           ← Rozdziela draft → chapters
  extract_pdfs.py             ← Ekstrakcja tekstu z PDF
  split_knowledge_base.py     ← Podział KB na sekcje
  archive/                    ← Stare/jednorazowe skrypty

sources/
  pdfs/                       ← Dokumentacja Siemens (PDFy źródłowe)
    extracted/                ← Pre-wyekstrahowany tekst (grep_search)
  books/                      ← Materiały edukacyjne
  sicar/                      ← Dokumentacja SICAR@TIA

archive/                      ← Stare wersje (v7–v11, docx v3–v7)

transcripts/
  controlbyte/                ← Transkrypcje @controlbytepl (52 filmy)

.github/
  copilot-instructions.md     ← Instrukcje dla GitHub Copilot
  prompts/                    ← Prompty workflow
```

---

## Publikacja (GitHub Pages)

```powershell
.\scripts\publish.ps1 -Message "Opis zmiany"
```
Pipeline automatycznie: generuje TOC → scala chapters → kopiuje LATEST.md → buduje manifest → kopiuje index.md → git push.

Strona: https://sm000k.github.io/plc-commissioner-qa/

---

## Sekcje Q&A (21 sekcji, 159 pytań)

1. Podstawy PLC i automatyki (16)
2. Architektura SIMATIC Safety Integrated (9)
3. Moduły F-DI / F-DO — okablowanie i parametry (10)
4. Struktury głosowania 1oo1/1oo2/2oo2/2oo3 (8)
5. Passivation, Reintegration, ACK (4)
6. Safe State — bezpieczny stan (5)
7. PROFIsafe — komunikacja Safety (4)
8. Napędy Safety — SINAMICS z wbudowanym Safety (8)
9. TIA Portal — Safety praktyka (8)
10. Robot ABB IRC5 — integracja z PLC (8)
11. Commissioning i diagnostyka (10)
12. Napędy SINAMICS (2)
13. E-Stop — normy, implementacja i obliczenia (5)
14. PROFINET — topologia, diagnostyka (8)
15. Kurtyny bezpieczeństwa i Muting (6)
16. Motion Control i SINAMICS — praktyka commissioning (15)
17. Realne scenariusze commissioning (9)
18. TIA Portal — zaawansowane funkcje (4)
19. Commissioning — dodawanie stacji (3)
20. Schematy elektryczne (7)
21. SICAR@TIA — standard automatyki automotive (10)
