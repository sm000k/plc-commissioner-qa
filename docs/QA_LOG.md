# QA_LOG — Historia wersji PLC Commissioner Q&A

Każda wersja dokumentu jest opisana: co dodano, co poprawiono, z jakich źródeł korzystano.

---

## qa_draft_v12 — 2026-04-01 (aktualizacja) ✅ AKTYWNA WERSJA

### Stan: 155 pytań, 20 sekcji — +9 nowych pytań (schematy elektryczne) vs poprzedniego stanu

### Nowa sekcja 20 — Schematy elektryczne | Silniki i aparatura łączeniowa (+9 pytań, 2026-04-01)
- **Q20.1** Silnik Dahlander (6 wyprowadzeń) — przełączanie biegunów Δ→YY, aparatura (KM_L/KM2/KM3)
- **Q20.2** Rozruch gwiazda-trójkąt Y/Δ — parametry elektryczne, aparatura, sekwencja, kiedy NIE stosować
- **Q20.3** Zmiana kierunku obrotów — zamiana faz, 3-warstwowa blokada (mech.+el.+PLC), czas martwy
- **Q20.4** Przekaźnik termiczny 3RU2 — zasada, dobór I_set, klasy 10/20/30, sygnał do PLC
- **Q20.5** Aparat różnicowoprądowy RCD — zasada, typy A/B/F, progi 30/300 mA, problem z VFD
- **Q20.6** Blokada elektryczna i mechaniczna — interlocking 3-warstwowy, Siemens 3RA1934-1A
- **Q20.7** Wyłącznik silnikowy 3RV2 vs bezpiecznik topikowy — tabela porównawcza, klasy gG/aM
- **Q20.8** Układ samopodtrzymania — schemat NC/NO, STOP musi być NC (fail-safe), realizacja LAD
- **Q20.9** Schemat Y/Δ sterowany PLC — kompletna sekwencja SCL z timerami, tabela diagnostyczna

### Źródła nowej wiedzy:
- Transkrypcje ControlByte: rygle bezpieczeństwa, PackML/OOP, radar Safety, HMI Template Suite
- Priorytetowe tematy (PLAN NAUKI): IO-Link, S7-1500H, PROFINET TSN, IE5 silniki
- Ręczna edycja (Copilot Agent)

### Nowe pytania wg sekcji:
| Sekcja | v11 | v12 | +Δ | Dodane tematy |
|--------|-----|-----|-----|--------------|
| **1** Podstawy PLC | 15 | 16 | +1 | Q1.16 IO-Link — Data Storage, tryby AI/IO-Link |
| **2** Architektura Safety | 8 | 9 | +1 | Q2.9 S7-1500H Hot Standby — sync link, bumpless switchover |
| **14** PROFINET zaawansowane | 7 | 8 | +1 | Q14.8 PROFINET TSN — IEEE 802.1Qbv, preemption, porównanie z IRT |
| **15** Kurtyny i Muting | 4 | 6 | +2 | Q15.5 Elektrorygiel (PSENmlock/PSENslock 2), Q15.6 Czujnik radarowy PSEN RD 1.2 |
| **16** Motion Control | 13 | 14 | +1 | Q16.14 Silniki IE5/IPM — p0300, klasy sprawności IEC 60034-30-1 |
| **17** Realne scenariusze | 8 | 9 | +1 | Q17.9 Diagnostyka legacy projektu TIA Portal |
| **18** TIA Portal adv. | 5 | 7 | +2 | Q18.6 PackML standard ISA-88, Q18.7 HMI Template Suite |

### Kluczowe dodane treści:
- Tabele porównawcze: IE3 vs IE5, IRT vs TSN, PSENmlock vs PSENslock, radar vs laser
- Nowe parametry: `p0300`, `p1910`, `p1960` (typ silnika w SINAMICS)
- Nowe normy: IEC 60034-30-1 (klasy sprawności silników), ISA-88 (PackML)
- Nowe urządzenia: PSEN RD 1.2 (radar), PSENmlock mini/PSENslock 2, SIMOTICS GP 1LA (IE5)

---

## qa_draft_v11 — 2026-03-30

### Stan: 134 pytań, 19 sekcji — +21 nowych pytań vs v10

### Źródła nowej wiedzy:
- 5 transkrypcji ControlByte (serwonapędy V90, ABB TCP/XML, Safety 1oo2)
- Targetowane rozszerzenie sekcji 4, 6, 17, 18
- Skrypt: `scripts/patch_v11.py` (Gemini 2.5 Flash, 2 wywołania)

### Nowe pytania wg sekcji:
| Sekcja | v10 | v11 | +Δ | Dodane tematy |
|--------|-----|-----|-----|--------------|
| **4** Struktury głosowania | 3 | 8 | +5 | Discrepancy time, cross-circuit detection, reintegration po błędzie, scenariusze awaryjne 1oo2 |
| **6** Safe State | 3 | 5 | +2 | STO vs OFF1/OFF2, konfiguracja substitute values per urządzenie |
| **8** SINAMICS Safety | 7 | 8 | +1 | Parametry Safety V90 |
| **10** Robot ABB | 5 | 8 | +3 | Komunikacja TCP/XML PLC↔ABB IRC5, format XML, obsługa błędów |
| **16** Motion Control | 5 | 11 | +6 | Hardware V90, Startdrive, tryby sterowania, One-Button Tuning, MC_MoveJog praktyka |
| **17** Realne scenariusze | 6 | 8 | +2 | FAT checklist Safety, SAT Site Acceptance Test |
| **18** TIA Portal adv. | 3 | 5 | +2 | ProDiag konfiguracja, Compare online/offline |

### Pliki pomocnicze:
- `docs/knowledge_base_delta_v11.md` — delta KB z 5 transkrypcji (podgląd)

---

## qa_draft_v10 — edycja ciągła (backup)

### Stan: 113 pytań, 19 sekcji — po sesjach redakcyjnych 2026-03-30 i późniejszych

### Zmiany redakcyjne (sesja formatowania):
- **Global reformat:** `•` → `-` bullets, blank lines przed/po nagłówkach `###`, collapse 3+ blank lines, strip trailing whitespace (1287 → 1394 linii)
- **Sekcja 5** (Passivation/Reintegration/ACK): pełny enriched reformat — tabele, blockquotes `> ⚠️` / `> 💡`, checklisty `- [ ]`, color spans, backtick zmienne
- **Sekcja 6** (Safe State): dodano tabelę urządzenie→Safe State, blockquotes, backtick dla `substitute value`
- **Sekcja 7** (PROFIsafe): dodano tabelę pakiet PROFIsafe, tabelę F-peripheral IP/montaż, blockquotes dla F-Address warning i F-monitoring time
- **Sekcja 4** (Struktury głosowania): przepisano na tabelę XooY + blockquoty z pułapkami
- **Sekcja 8.1–8.4** (SINAMICS Safety): Q8.1 color span STO + różnica od OFF, Q8.2 tabela STO vs wyłączenie programowe, Q8.3 color span SS1, Q8.4 przepisano na tabelę SS2/SOS/SLS/SDI/SBC
- **Sekcja 2.1** (Safety arch): color span SIMATIC Safety Integrated, bullet list korzyści
- **Sekcja 13.1**: przepisano na tabelę Kat.0/1/2 → STO/SS1/SS2; blockquote norma EN 60204-1
- **Sekcja 13.2**: przepisano LSafe_EStop — rozdzielono wejścia/wyjścia, dodano blockquote
- **Naprawiono**: obraz `06d_wiring_et200mp_p9.png` → `06e_wiring_et200mp_p10.png` (Q3.8 — właściwy schemat Figure 3-1)

### Dodane pytania:
- **Q17.6** „Po czym poznajesz że projekt TIA Portal jest skalowalny?" — dodane do sekcji 17 (Realne scenariusze)

### Poprzedni stan vs v9:
- Brak nowych pytań przy pierwszej promocji — wersja stabilna po sesji redakcyjnej 2026-03-30
- **112 pytań, 19 sekcji** — identyczna treść z v9 po wszystkich poprawkach
- Plik roboczy przeniesiony do `qa_draft_v10.md`

---

## qa_draft_v9 — edycja 2026-03-30 — Redukcja i korekta pytań

### Zmiany 2026-03-30:
- **112 pytań** (było 115) — usunięto 6 pytań, przepisano 1
- **Usunięte pytania (zbyt ogólne / poza zakresem PLC Commissioner):**
  - `1.11` Warianty CPU S7-1200 i rozbudowa (SM/CM/SB) — zbyt sprzętowe/katalogowe
  - `1.12` Co to jest HMI — zbyt podstawowe
  - `1.13` Co to jest SCADA / WinCC — zbyt ogólne
  - `13.5` Łańcuch Safety PFH: Detection→Evaluation→Reaction — zbędna duplikacja
  - `18.1` Know-How Protection vs Copy Protection — poza zakresem core Safety/Commissioning
  - `18.5` Access levels S7-1500 — poza zakresem core Safety/Commissioning
- **Przepisane pytania:**
  - `11.8` — zmieniono z V90/V-Assistant na **SINAMICS G120** (Quick Commissioning, p0010, p0304-p0311, p3900, p0922, p1910, p1960, p0970, r0945/r0947/r0949, FB SINA_SPEED)
- **Przenumerowania:** 1.14→1.11 | 13.6+→13.5+ | 18.2→18.1, 18.3→18.2, 18.4→18.3

---

## qa_draft_v9 — 2026-03-29 — Obrazy, System Nauki, Tagi Priorytetów

### Zmiany vs v8:
- **+5 nowych pytań** (łącznie 115 pytań)
- **9 obrazów embedded** z dokumentacji Siemens (diagramy cross-circuit, PM/PP-switching, passivation, E-Stop, ISO 13849-1)
- **PLAN NAUKI** dodany na początku dokumentu — 3-fazowy system (Faza 1→2→3: 2–3 dni każda)
  - Faza 1 FUNDAMENT (12 pytań 🔴): architektura Safety, F-CPU, F-DI, PROFIsafe, E-Stop
  - Faza 2 PRAKTYKA (14 pytań 🟡): discrepancy time, F-signature, komisjonowanie, diagnostyka
  - Faza 3 SENIOR LEVEL (10 pytań 🟢): ISO 13849-1, PFHD, Safety Matrix, FAT/SAT, ProDiag
- **36 pytań otagowanych** inline: 🔴 (17) / 🟡 (15) / 🟢 (13)
- **Mapa tematyczna** (Safety/Napędy/Commissioning/Robot/PROFINET/TIA)
- **Technika Feynman** — procedura szybkiej nauki

### Obrazy embedded (docs/images/safety/):
| Pytanie | Obraz | Opis |
|---------|-------|------|
| 2.1 | `01b_simatic_safety_overview_p2.png` | Safety Integrated — przegląd systemu |
| 3.2 | `01d_safety_brochure_p4.png` | Cross-circuit, wire break, short-circuit |
| 3.6 | `06a_wiring_pm_switching_p6.png` | PM-switching |
| 3.6 | `06b_wiring_pp_switching_p7.png` | PP-switching |
| 3.8 | `06d_wiring_et200mp_p9.png` | ET200MP okablowanie |
| 5.1 | `05a_passivation_p189.png` | Passivation — diagram czasowy |
| 13.2 | `07b_estop_mode_of_op_p6.png` | E-Stop tryby pracy |
| 13.2 | `07c_estop_hw_setup_p10.png` | E-Stop hardware setup |
| 13.5 | `07d_estop_iso13849_p21.png` | ISO 13849-1 PFHD tabela |

### Katalog obrazów:
- `docs/images/safety/` — 45 plików PNG, ~11.4 MB
- Renderowane z: `21064024_E-Stop`, `39198632_Wiring`, `SIMATIC Safety` (Konfiguracja+Broszura), `safety_getting_started`

---

## qa_draft_v8 — 2026-03-29 — Integracja transkrypcji ControlByte

### Źródło danych:
- **51 transkrypcji** z kanału YouTube `@controlbytepl` (pobrane przez Gemini 2.5 Flash)
- Filmy z zakresu: Safety PLC (Pilz), TIA Portal S7-1200/1500, Sinamics V90, Motion Control, PROFINET, HMI, Python/OPC UA, normy PN-EN 60204, schematy elektryczne
- Plik pośredni: `docs/knowledge_base_controlbyte.md` (37K znaków, 22 Q&A)

### Nowe pytania dodane do qa_draft_v8.md (+12 pytań, łącznie 109):

| Sekcja | Nowe pytania | Temat |
|--------|-------------|-------|
| **1** (1.9–1.11) | +3 | Rodziny CPU Siemens (LOGO!/S7-1200/S7-1500), Pamięć sterownika (Load/Work/Retentive), Hardware S7-1200 (złącza, moduły, DIN) |
| **3** (3.9) | +1 | Reakcja F-modułu na awarie wejść 1oo2: zwarcie do 0V, zwarcie międzykanałowe, discrepancy failure — błędy z bufora diagnostycznego |
| **11** | szczegóły | V-Assistant dla SINAMICS V90 (etapy komisjonowania, Control Mode, AutoTuning), Python + OPC UA (testy automatyczne PLC) |
| **14** | szczegóły | Przemysłowe switche PROFINET (zarządzalne vs niezarządzalne, QoS, ERPS G.8032), ISO on TCP (GET/PUT) |
| **15** | szczegóły | Wyjścia tranzystorowe z czujników Safety podłączone do F-DI |
| **16** | szczegóły | Typy silników w Motion Control: DC szczotkowe, asynchroniczne klatkowe z enkoderem, synchroniczne servo, liniowe |

### Pliki wygenerowane:
- `scripts/Build-KnowledgeBase.py` — ekstrakcja wiedzy z transkrypcji (Gemini, batch 46 plików)
- `scripts/Merge-KnowledgeBase.py` — scalanie knowledge_base → qa_draft
- `docs/knowledge_base_controlbyte.md` — surowy wynik ekstrakcji

---

## Analiza nowych materiałów źródłowych — 2026-03-29

Dodano 5 nowych plików do workspace. Przeprowadzono ekstrakcję i porównanie z qa_draft_v7.md.

### Nowe materiały:
| Plik | Zakres | Przydatność |
|------|--------|-------------|
| `siemens SCL.PDF` (109s) | SCL dla S7-300/400 (STEP 7), praca dyplomowa | Historyczne tło; SKŁAdnia inna niż TIA Portal |
| `Sterowniki_PLC.pdf` (96s) | Podręcznik akademicki S7-300, STEP 7 | Ogólne koncepcje; UWAŻAJ: błąd klasyfikacji sprzętu |
| `btc.pl SCL S7-1200` (566s) | Programowanie S7-1200 w SCL, TIA Portal V13 | Potwierdza typy danych, struktury bloków |
| `Simatic-s7-1200-w-zadaniach.pdf` (171s) | Ćwiczenia praktyczne S7-1200 | Potwierdza OB/FB/FC, operacje bitowe, timery |
| `Simatic-s7-1200-w-zadaniach_LAD_Zaawansowany.pdf` | Zaawansowane LAD + FactoryIO | Ćwiczeniowy, bez wpływu na fakty |

### ⚠️ BŁĄD ZNALEZIONY W ŹRÓDLE:
- `Sterowniki_PLC.pdf` str.3 klasyfikuje **S7-1200 jako "sterowniki duże"** — **BŁĄD**.
  - Prawidłowa klasyfikacja Siemens: S7-1200 = Basic/Compact (zastępca S7-200), S7-1500 = Advanced (zastępca S7-300/400).
  - Q&A NIE było dotknięte tym błędem (prawidłowa klasyfikacja w Q 2.3).
  - **Nie używać `Sterowniki_PLC.pdf` jako referencji dla klasyfikacji sprzętu.**

### Poprawki wprowadzone do qa_draft_v7.md (2026-03-29):
1. **Q 1.3 (OB blocks)** — Rozbudowano o diagnostyczne OB wymagane przy commissioning: OB80 (cycle time exceeded), OB82 (diagnostic error), OB86 (rack/station failure), OB121/122 (program errors). Potwierdzono z obu książek S7-1200.
2. **Q 1.4 (FB/FC/DB)** — Dodano rozróżnienie VAR_TEMP vs VAR_STAT (potwierdzone w siemens SCL.PDF i btc.pl). Dodano wzmiankę o multi-instance DB i Optimized Block Access.
3. **Q 1.6 (Języki SCL)** — Wzbogacono o przykłady składni SCL (IF/FOR/WHILE/CASE), dodano STL jako przestarzały, wyjaśniono różnicę TIA Portal SCL vs STEP 7 SCL (symboliczne adresowanie). Dodano uwagę że Safety F-bloki używają LAD/FBD, nie SCL.

---

## Audit merytoryczny v7 — 2026-03-28

Przeprowadzono pełny przegląd dokumentu `qa_draft_v7.md` pod kątem prawdziwości odpowiedzi. Zweryfikowano treść z:
- Siemens Application Note **21064024 V7.0.1** (E-Stop SIL3, PDF odczytany bezpośrednio)
- Normy EN ISO 13849-1, IEC 62061, EN 60204-1, IEC 61496, IEC 61800-5-2
- Specyfikacja PROFINET MRP (IEC 61158)

### Potwierdzone jako POPRAWNE (z PDF):
- ✅ Nazwa bloku `LSafe_EStop` — potwierdzona w PDF str. 6-7 (V7.0.1 zastąpiło stary blok ESTOP)
- ✅ Wartości PFH (Detection 9.06×10⁻¹⁰, Evaluation 5.00×10⁻⁹, Reaction 1.45×10⁻⁹, Total 7.35×10⁻⁹) — identyczne z Tabelą 3-8 w PDF
- ✅ ACK_GL z STEP 7 Safety Advanced — potwierdzone w PDF str. 7-8
- ✅ Feedback circuit, CCF, discrepancy time, passivation — zgodne ze źródłami
- ✅ Kategorie zatrzymania EN 60204-1 ↔ STO/SS1/SS2 — poprawne

### Błędy NAPRAWIONE w tym przeglądzie:
1. **F30001** — błędny opis „DC link undervoltage". POPRAWIONO na: „Ground fault — błąd doziemny wyjścia". DC link undervoltage to F30002. Dodano ostrzeżenie o weryfikacji w Parameter Manual dla konkretnego firmware.
2. **p2051** — błędny parametr dla selekcji telegramu PROFIdrive. POPRAWIONO na `p0922` (właściwy parametr w SINAMICS G120).
3. **„Fast-MRP"** — nieistniejący termin PROFINET. POPRAWIONO na MRPD (Media Redundancy with Planned Duplication). Dodano ostrzeżenie.
4. **SICAR acronym** — „Siemens Industry Automotive Reference" → POPRAWIONO na „Siemens Automation Platform for CAR Plants" (zgodnie z dokumentacją SICAR_Conventions.pdf).
5. **Kurtyna Type 2 max PL** — zbyt konserwatywne „PL c / SIL 1". POPRAWIONO: Type 2 może osiągnąć PL d / SIL 2 przy 2-kanałowej architekturze.
6. **SIL zakresy w Słowniku** — niepełna definicja (tylko górne granice). POPRAWIONO na pełne zakresy PFHD per SIL.
7. **SICAR w Słowniku** — jak punkt 4 (spójność).

---

## v6 — (wersja bieżąca)
- **Plik**: `PLC_Commissioner_QA_v6.docx`
- **Sekcje**: 19
- **Pytań szacunkowo**: ~120
- **Nowe w v6**:
  - Sekcja 13: E-Stop — normy, implementacja i obliczenia PFH/PL
  - Sekcja 14: PROFINET zaawansowane (MRP, IRT, Shared Device)
  - Sekcja 15: Kurtyny bezpieczeństwa i Muting
  - Sekcja 16: Motion Control i SINAMICS commissioning
  - Sekcja 17: Elektrotechnika praktyczna *(usunięta w v7 — sekcja renamed)*
  - Sekcja 18: Realne scenariusze commissioning
  - Sekcja 19: TIA Portal zaawansowane funkcje
  - Rozszerzona Ściąga terminologiczna
- **Źródła użyte**: Siemens doc. 21064024 (E-Stop SIL3 V7.0.1), Siemens doc. 39198632 (Wiring Examples), SIMATIC Safety Integrated dokumentacja
- **Zmiany strukturalne w v7**:
  - Sekcja 17 „Elektrotechnika praktyczna" — **usunięta** (zakres zbyt ogólny)
  - Sekcje przemianowane: 18→17 (Realne scenariusze), 19→18 (TIA Portal zaawansowane)
  - Sekcja 19 — nowa: **Słownik pojęć** (PLC / Safety / PROFINET / Napędy) z pełnymi definicjami zamiast ściągi jednozdaniowej
- **Brakuje** (wejście do v7):
  - TIA Portal V19 — nowe funkcje
  - SINAMICS S210 / V90 komisjonowanie
  - ProDiag — diagnostyka inline
  - S7-1500R/H — redundancja CPU
  - IO-Link — smart sensors
  - Safety door interlock z RFID
  - Two-hand control (blok LSafe_TwoHand)
  - Proof test interval — obliczenia
  - PROFINET TSN

---

## v5 — (poprzednia wersja)
- **Plik**: `PLC_Commissioner_QA_v5.docx`
- **Nowe w v5**:
  - Sekcja 10: Robot ABB IRC5 — integracja z PLC
  - Sekcja 11: Commissioning i diagnostyka
  - Sekcja 12: SICAR i Napędy SINAMICS

---

## v4 — (wersja historyczna)
- **Plik**: `PLC_Commissioner_QA_v4.docx`
- **Nowe w v4**:
  - Rozbudowane Safety i commissioning
  - Napędy SINAMICS Safety (STO, SS1, SLS, SDI, SBC)

---

## v3 — (wersja historyczna)
- **Plik**: `PLC_Commissioner_QA_v3.docx`
- Pierwsza obszerna wersja kompendium

---

<!-- Nowe wpisy dodawane przez skrypt New-QADocument.ps1 -->

## v7 — 2026-03-26 13:11
- Plik: PLC_Commissioner_QA_v7.docx
- Wygenerowano z: $InputFile
- Rozmiar: 56.6 KB

