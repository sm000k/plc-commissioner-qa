# REFERENCE — Źródła wiedzy projektu Q&A

> Plik pomocniczy dla `copilot-instructions.md`. Otwórz gdy potrzebujesz:
> - sprawdzić jakie PDFy są dostępne i co pokrywają
> - znaleźć brakujące źródła do pobrania
> - dodać nowy PDF do projektu

---

## Obecne źródła PDF (`sources/pdfs/`)

Pre-wyekstrahowany tekst: `sources/pdfs/extracted/*.txt` → szukaj przez `grep_search`.  
Indeks maszynowy: `sources/pdfs/pdf_manifest.json`.

| Plik | Zawartość | Pokrywa sekcje |
|------|-----------|----------------|
| `21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en.pdf` | Application Example: E-Stop SIL3, klasy zatrzymania, PFH, obliczenia ISO 13849-1 | §13 |
| `39198632_Wiring_Example_en.pdf` | Przykłady okablowania F-DI/F-DO, PM-switching, PP-switching, relay | §3 |
| `safety_getting_started_en-US.pdf` | Podstawy SIMATIC Safety — pierwsze kroki, architektura | §2, §6 |
| `SIMATIC Safety - Konfiguracja i programowanie (2).pdf` | Zaawansowana konfiguracja Safety, programowanie F-bloków | §2, §4, §5, §7, §9 |
| `SIMATIC Safety Integrated – wszystko w jednym sterowniku PLC.pdf` | Koncepcja Safety Integrated, F-CPU, PROFIsafe | §2, §7 |
| `btc.pl-SCL-S7-1200.pdf` | Programowanie S7-1200 w SCL (TIA Portal V13+) | §1 |
| `Sterowniki_PLC.pdf` | Ogólne informacje o sterownikach PLC | §1 |
| `siemens SCL.PDF` | Programowanie w SCL — uzupełnienie | §1 |

---

## Mapa pokrycia sekcji

| § | Sekcja | Ma źródło? | Brak |
|---|--------|------------|------|
| 1 | Podstawy PLC | ✅ PDF + books | — |
| 2 | Architektura Safety | ✅ 3 PDFy | — |
| 3 | Moduły F-DI/F-DO | ✅ Wiring Example | — |
| 4 | Struktury głosowania | ✅ Safety Konfig. | — |
| 5 | Passivation/Reintegration | ✅ Safety Konfig. | — |
| 6 | Safe State | ✅ Safety Getting Started | — |
| 7 | PROFIsafe | ✅ Safety Konfig./Integrated | — |
| 8 | Napędy Safety | ❌ | SINAMICS Safety Integrated FM |
| 9 | TIA Portal Safety | ✅ Safety Konfig. | — |
| 10 | Robot ABB IRC5 | ❌ | ABB IRC5 Application Manual |
| 11 | Commissioning i diagnostyka | ⚠️ knowledge base only | S7-1500 Diagnostics Manual |
| 12 | SICAR i Napędy SINAMICS | ❌ | SINAMICS G120 Commissioning, SICAR Conventions |
| 13 | E-Stop | ✅ Application Example | — |
| 14 | PROFINET | ❌ | PROFINET System Description |
| 15 | Kurtyny/Muting | ❌ | Light Curtains App. Example |
| 16 | Motion Control | ❌ | SINAMICS S120/V90 Manual |
| 17 | Scenariusze commissioning | ⚠️ knowledge base only | — |
| 18 | TIA Portal zaawansowane | ❌ | TIA Portal V19 What's New |
| 19 | Commissioning stacje | ❌ | ET200SP/MP System Manual |
| 20 | Schematy elektryczne | ❌ | EN 60204-1, schematy katalogowe |

---

## 🔴 Brakujące źródła — do pobrania z Siemens SIOS

> `support.industry.siemens.com` → szukaj po tytule. Wszystkie są darmowe.

### Priorytet 1 — krytyczne luki

| Dokument | Szukaj na SIOS | Dla sekcji |
|----------|----------------|------------|
| SINAMICS G120 — Getting Started | "SINAMICS G120 getting started" | §12, §16 |
| SINAMICS G120 — List Manual (parametry) | "SINAMICS G120 list manual" | §8, §12, §16 |
| SINAMICS S120 — Safety Integrated Function Manual | "SINAMICS S120 safety integrated function manual" | §8 |
| PROFINET System Description | "PROFINET system description" | §14 |
| S7-1500 / ET200SP System Manual | "ET200SP system manual" | §11, §19 |
| S7-1500 Diagnostics Manual | "S7-1500 diagnostics" | §11 |
| Light Curtains with SIMATIC Safety — Application Example | "safety light curtain muting application example" | §15 |

### Priorytet 2 — wzmocnienie istniejących sekcji

| Dokument | Szukaj na SIOS | Dla sekcji |
|----------|----------------|------------|
| SINAMICS V90 — Getting Started | "SINAMICS V90 getting started PROFINET" | §16 |
| TIA Portal V19 — What's New | "TIA Portal V19 innovations" | §18 |
| PROFIsafe — System Description | "PROFIsafe system description" (PI International) | §7 |
| SIMATIC Safety — Application Examples Collection | "SIMATIC safety application examples" | §4, §5, §6 |

### Priorytet 3 — źródła zewnętrzne

| Dokument | Źródło | Dla sekcji |
|----------|--------|------------|
| ABB IRC5 — Application Manual PROFINET | library.abb.com → "IRC5 PROFINET" | §10 |
| SICAR@GST Conventions | Wewnętrzny Siemens (jeśli masz dostęp) | §12 |
| EN 60204-1 | Norma płatna; app. notes Siemens jako substytut | §20 |

---

## Konwencja nazw nowych PDF-ów

```
sources/pdfs/{temat_krótki}_{lang}.pdf
```
Przykłady: `sinamics_g120_getting_started_en.pdf`, `profinet_system_description_en.pdf`

Po dodaniu nowego PDF-a:
1. Uruchom `python scripts/extract_pdfs.py` → odświeży `extracted/` i `pdf_manifest.json`
2. Zaktualizuj tabelę "Obecne źródła" powyżej
