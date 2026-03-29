---
mode: agent
description: "Faza 1: Zbierz informacje z PDF i istniejących Q&A, zidentyfikuj braki tematyczne"
tools: ['read_file', 'run_in_terminal', 'file_search', 'create_file', 'replace_string_in_file']
---

# Faza 1 — Zbieranie informacji i analiza braków

## Twój cel
Przeanalizuj dostępne materiały źródłowe i istniejące dokumenty Q&A, a następnie zapisz raport braków do `docs/analiza_zrodel.md`.

## Krok 1 — Wyodrębnij tekst z istniejącego Q&A

Uruchom skrypt, który wyciągnie tekst z najnowszej wersji dokumentu:

```powershell
cd "c:\automation\rozmowa_kwal"
# Znajdź najnowszą wersję
$latest = Get-ChildItem "PLC_Commissioner_QA_v*.docx" | Sort-Object Name | Select-Object -Last 1
Write-Host "Analizuję: $($latest.Name)"

# Wyciągnij tekst przez skrypt pomocniczy
& "scripts\Read-DocxText.ps1" -Path $latest.FullName -OutputFile "docs\existing_qa_text.txt"
```

## Krok 2 — Wyciągnij kluczowe tematy z PDF

Dla każdego pliku PDF wyciągnij główne koncepcje używając PowerShell i .NET iTextSharp lub przez rozpakowanie tekstu:

```powershell
# Lista PDFs do analizy
$pdfs = @(
    "21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en.pdf",
    "39198632_Wiring_Example_en.pdf",
    "safety_getting_started_en-US.pdf",
    "SIMATIC Safety - Konfiguracja i programowanie (2).pdf",
    "SIMATIC Safety Integrated – wszystko w jednym sterowniku PLC.pdf"
)

foreach ($pdf in $pdfs) {
    Write-Host "PDF: $pdf"
}
```

## Krok 3 — Analiza pokrycia tematycznego

Sprawdź które z poniższych tematów są już pokryte i oceń jakość pokrycia:

### Tematy do weryfikacji

| # | Sekcja | Pytania min | Status |
|---|--------|-------------|--------|
| 1 | Podstawy PLC i automatyki | 10 | ? |
| 2 | Architektura SIMATIC Safety Integrated | 8 | ? |
| 3 | Moduły F-DI / F-DO | 8 | ? |
| 4 | Struktury głosowania | 4 | ? |
| 5 | Passivation, Reintegration, ACK | 5 | ? |
| 6 | Safe State | 3 | ? |
| 7 | PROFIsafe | 5 | ? |
| 8 | Napędy Safety — SINAMICS | 6 | ? |
| 9 | TIA Portal Safety praktyka | 6 | ? |
| 10 | Robot ABB IRC5 | 5 | ? |
| 11 | Commissioning i diagnostyka | 6 | ? |
| 12 | SICAR i Napędy SINAMICS | 4 | ? |
| 13 | E-Stop — normy i obliczenia | 6 | ? |
| 14 | PROFINET zaawansowane | 5 | ? |
| 15 | Kurtyny bezpieczeństwa i Muting | 3 | ? |
| 16 | Motion Control | 4 | ? |
| 17 | Realne scenariusze commissioning | 5 | ? |
| 18 | TIA Portal zaawansowane funkcje | 4 | ? |
| 19 | Słownik pojęć (PLC / Safety / PROFINET / Napędy) | 80+ haseł | ? |

### Tematy priorytetowe (brakujące lub słabe w v6)

Sprawdź czy następujące tematy są pokryte w istniejącym Q&A:
- [ ] **TIA Portal V19** — nowe funkcje (AI assistant, ulepszone debugowanie)
- [ ] **SINAMICS S210** — servo z PROFIdrive na PROFINET
- [ ] **V90 + V-ASSISTANT** — parametryzacja serwo
- [ ] **ProDiag** — diagnostyka inline w TIA Portal
- [ ] **S7-1500R/H** — redundancja CPU, switchover time
- [ ] **IO-Link** — czujniki smart, parametryzacja przez PLC
- [ ] **OPC UA** — serwer w S7-1500, klient w WinCC/Python
- [ ] **PROFINET TSN** — Time Sensitive Networking
- [ ] **Safety w robotach** — PROFIsafe do IRC5 safety controller
- [ ] **Siemens TIA Selection Tool** — obliczenia PL/SIL online
- [ ] **Proof test interval** — MT_PFH i TTF
- [ ] **SINAMICS G120X / G120C** — różnice od G120
- [ ] **Safety door interlock** — RFID safety switches
- [ ] **Two-hand control** — implementacja bloku LSafe_TwoHand

## Krok 4 — Zapisz raport do docs/analiza_zrodel.md

Utwórz plik `docs/analiza_zrodel.md` z następującą strukturą:

```markdown
# Analiza Źródeł — [DATA]

## Wersja bieżąca
Najnowszy plik: PLC_Commissioner_QA_vX.docx
Liczba sekcji: 19
Liczba pytań: ~XXX

## Pokrycie tematyczne

### Dobrze pokryte sekcje
- Sekcja X: [ocena i uwagi]

### Sekcje wymagające rozszerzenia
- Sekcja X: [co brakuje]

### Brakujące tematy priorytetowe
1. [temat] — [dlaczego ważny]

## Informacje z PDF

### 21064024_E-Stop_SIL3_1500F
Kluczowe tematy:
- [temat 1]
- [temat 2]

### 39198632_Wiring_Example
...

## Zalecenia do Fazy 2
- Priorytet 1: [co dodać]
- Priorytet 2: [co poprawić]
```

## Po wykonaniu
Plik `docs/analiza_zrodel.md` jest gotowy → przejdź do Fazy 2 (`2-formuluj-pytania.prompt.md`).
