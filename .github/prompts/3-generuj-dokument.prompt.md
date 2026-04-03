---
agent: agent
description: "Faza 3: Generuj merytorycznie poprawne odpowiedzi Q&A z obowiązkową weryfikacją źródłową. Use when: generating Q&A answers, writing technical responses about PLC/Safety/SINAMICS/PROFINET, creating new draft versions."
tools: [read, search, edit, execute]
---

# Faza 3 — Generowanie odpowiedzi Q&A (source-grounded)

## Twój cel
Na podstawie pytań wygeneruj kompletne, **merytorycznie poprawne** odpowiedzi oparte na materiałach źródłowych z workspace. Złóż z istniejącym Q&A i uruchom skrypt tworzący `.docx`.

> ⛔ **ZASADA NADRZĘDNA**: Nie generuj ŻADNEJ odpowiedzi bez uprzedniego przeczytania źródeł. Każdy fakt musi mieć oparcie w materiale workspace lub być oznaczony poziomem pewności.

---

## Krok 1 — Odczytaj aktualny dokument Q&A

Odczytaj `docs/LATEST.md` aby poznać bieżący stan dokumentu (wersja, liczba pytań, sekcje).

## Krok 2 — Obowiązkowe czytanie źródeł (SOURCE-FIRST)

> **Dla KAŻDEGO pytania/odpowiedzi** wykonaj przed generowaniem:

### 2a. Odczytaj rozdział
Odczytaj `docs/chapters/XX_*.md` odpowiadający sekcji pytania. Np. dla pytania z sekcji 7 (PROFIsafe) → odczytaj `docs/chapters/07_profisafe.md`.

### 2b. Przeszukaj bazy wiedzy
Przeszukaj słowa kluczowe z pytania w:
- `docs/knowledge_base_controlbyte.md` — baza z transkrypcji ControlByte (52 filmy)
- `docs/knowledge_base_delta_v11.md` — delta wiedzy z patcha v11

### 2c. Sięgnij do PDF (tylko gdy brakuje informacji)
Jeśli po krokach 2a-2b nadal brakuje danych → ekstrakcja z `sources/pdfs/`:
- Safety: `safety_getting_started_en-US.pdf`, `SIMATIC Safety - Konfiguracja i programowanie (2).pdf`
- E-Stop: `21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en.pdf`
- Okablowanie: `39198632_Wiring_Example_en.pdf`
- SCL: `btc.pl-SCL-S7-1200.pdf`, `siemens SCL.PDF`

### 2d. Zanotuj źródła
Dla każdej odpowiedzi zanotuj skąd wzięto kluczowe fakty (do oznaczenia w odpowiedzi).

---

## Krok 3 — Format odpowiedzi (template obligatoryjny)

Każda odpowiedź **musi** składać się z trzech bloków:

```
### [numer]. [Pytanie w formie pełnego zdania?]

[DEFINICJA — 1-2 zdania wyjaśniające czym jest X i jak działa]

- [Kluczowy fakt 1 — ze szczegółem technicznym]
- [Kluczowy fakt 2 — z numerem parametru Siemens JEŚLI znaleziony w źródłach]
- [Kluczowy fakt 3 — z odniesieniem do normy JEŚLI dotyczy]

[PRAKTYKA — procedura krok po kroku LUB przykład z TIA Portal LUB realny scenariusz commissioning LUB komenda diagnostyczna]

> Źródło: [nazwa pliku / norma] | Pewność: [ZWERYFIKOWANE] / [PRAWDOPODOBNE] / ⚠️ DO WERYFIKACJI
```

### Przykład dobrej odpowiedzi:

```
### 3. Co to jest SS1 (Safe Stop 1) i kiedy go używasz zamiast STO?

SS1 (Safe Stop 1) to funkcja Safety napędu SINAMICS która hamuje oś wzdłuż
zaprogramowanej rampy prędkości do zatrzymania, a następnie aktywuje STO
(Safe Torque Off). Certyfikowana wg IEC 61800-5-2.

- Czas hamowania monitorowany przez napęd — przekroczenie limitu = natychmiastowe STO
- Realizowana przez PROFIsafe (zaawansowana) lub zaciski hardwarowe (prostsza)
- Odpowiada kategorii zatrzymania 1 wg EN 60204-1 (kontrolowane hamowanie → odłączenie)
- Parametr p9652 (G120) — czas SS1 timeout [ZWERYFIKOWANE: SINAMICS Safety Function Manual]

Używasz SS1 zamiast STO gdy natychmiastowe odcięcie momentu jest niebezpieczne:
obrabiarka z dużą masą bezwładnościową, robot z ciężkim ładunkiem — nagłe odcięcie
powoduje zderzenie lub uszkodzenie mechaniki.

Procedura testowania SS1 podczas commissioning:
1. Ustaw parametr czasu SS1 w Startdrive lub Safety Wizard
2. Aktywuj SS1 przez PROFIsafe lub zacisk hardwarowy
3. Zmierz czas hamowania — musi być krótszy niż skonfigurowany timeout
4. Zweryfikuj że po zatrzymaniu aktywuje się STO (sprawdź status w Trace)
5. Sprawdź że napęd nie może ruszyć bez cofnięcia SS1 i ponownego enable

> Źródło: IEC 61800-5-2, docs/chapters/08_napedy_safety.md | Pewność: [ZWERYFIKOWANE]
```

---

## Krok 4 — Zasady merytoryczne (KRYTYCZNE)

### Polityka anty-halucynacji
1. **NIGDY nie wymyślaj** numerów parametrów (pXXXX/rXXXX). Nie znasz → napisz `pXXXX (sprawdź w dokumentacji SINAMICS)`.
2. **NIGDY nie fabrykuj** numerów norm, klauzul, artykułów. Dozwolone normy — patrz `copilot-instructions.md`.
3. **Nie wymyślaj** konkretnych zakresów wartości. Nie znasz → podaj kierunek: „kilkadziesiąt ms", „rzędu sekund".
4. **Oznaczaj pewność** przy każdej odpowiedzi:
   - `[ZWERYFIKOWANE]` — fakt znaleziony dosłownie w pliku workspace
   - `[PRAWDOPODOBNE]` — spójne z wiedzą domenową ale nie potwierdzone w źródłach
   - `⚠️ DO WERYFIKACJI` — niepewne, wymaga sprawdzenia

### Numery parametrów SINAMICS (sprawdzone — używaj gdy pasują)

**Podstawowe sterowanie:**
| Parametr | Opis |
|----------|------|
| `p0010` | Parametryzacja — filtr grup parametrów (Quick commissioning) |
| `p0100` | Europa/Ameryka Północna (50Hz/60Hz) |
| `p0304` | Napięcie znamionowe silnika |
| `p0305` | Prąd znamionowy silnika |
| `p0307` | Moc znamionowa silnika |
| `p0310` | Częstotliwość znamionowa silnika |
| `p0311` | Prędkość znamionowa silnika |
| `p0700` | Źródło komend sterujących (0=MOP, 1=BOP, 2=terminal, 6=PROFIdrive) |
| `p0840` | ON/OFF1 — źródło sygnału start napędu |
| `p1000` | Źródło zadanej częstotliwości/prędkości |
| `p1080` | Częstotliwość minimalna |
| `p1082` | Częstotliwość maksymalna |
| `p1120` | Ramp-up time [s] |
| `p1121` | Ramp-down time [s] |
| `p2051` | Typ telegramu PROFIdrive (1/20/105/111) |

**Diagnostyka:**
| Parametr | Opis |
|----------|------|
| `r0002` | Status napędu (bitmapa) |
| `r0945[0..7]` | Kody błędów (fault codes) |
| `r2110` | Aktualny kod alarmu (warning) |
| `r0722` | Status PROFIdrive Control Word |
| `r0947` | Fault timestamp |

**Safety Integrated:**
| Parametr | Opis |
|----------|------|
| `p9501` | Safety STO enable |
| `p9601` | Safety SS1 enable |
| `p9652` | SS1 timeout / ramp time |
| `p9801` | Safety hasło (password) |
| `p9802` | Safety acceptance test — data |
| `r9722` | Status Safety funkcji (bitmapa) |
| `r9773` | PROFIsafe address |

### Terminologia Siemens
Patrz tabela w `copilot-instructions.md` — używaj ZAWSZE terminów Siemens zamiast generycznych.

### Normy — dozwolone (nie wymyślaj innych)
- **EN ISO 13849-1** (PL a-e), **IEC 62061** (SIL CL), **EN ISO 12100** (ocena ryzyka)
- **IEC 61800-5-2** (STO/SS1/SS2/SOS/SLS/SDI/SBC)
- **IEC 61508** (SIL 1-3), **EN 60204-1** (kategorie zatrzymania 0/1/2)
- **EN ISO 13850** (E-Stop), **EN 60947-5-1** (przekaźniki)
- **IEC 61496** (kurtyny), **EN ISO 13855** (odległości bezpieczeństwa)
- **IEC 61131-3** (języki programowania PLC)

---

## Krok 5 — Quality Gate (self-check po generowaniu)

Po wygenerowaniu KAŻDEJ odpowiedzi, zweryfikuj:

- [ ] ✅ **Definicja** — czy odpowiedź zaczyna się od 1-2 zdań definiujących pojęcie?
- [ ] ✅ **Bullet list** — czy zawiera min. 3 punkty kluczowe ze szczegółami technicznymi?
- [ ] ✅ **Praktyka** — czy zawiera min. 1 element praktyczny (procedura / scenariusz / diagnostyka / konfiguracja TIA Portal)?
- [ ] ✅ **Parametry** — czy KAŻDY numer parametru (pXXXX) pochodzi z tabeli powyżej lub ze źródła? Jeśli nie → usuń lub oznacz `⚠️ DO WERYFIKACJI`.
- [ ] ✅ **Terminologia** — czy używa terminów Siemens (F-CPU, passivation, reintegration, substitute value, F-monitoring time)?
- [ ] ✅ **Źródło** — czy podano source (PDF, chapter, knowledge base, norma) i poziom pewności?
- [ ] ✅ **Bez halucynacji** — czy żaden fakt nie jest wymyślony „bo dobrze brzmi"?

**Jeśli którykolwiek punkt nie przechodzi → popraw odpowiedź przed włączeniem do draftu.**

---

## Krok 6 — Złóż pełne Q&A

Weź istniejące pytania z `docs/LATEST.md` + nowe odpowiedzi i złóż kompletny draft:

1. Skopiuj aktualny `docs/LATEST.md` → `docs/qa_draft_v{n+1}.md`
2. Wstaw nowe pytania w odpowiednie sekcje (zachowaj numerację)
3. Przenumeruj jeśli trzeba
4. Uruchom `python scripts/merge_chapters.py` jeśli edytowałeś chapters osobno
5. Zaktualizuj header (wersja, data, liczba pytań)
6. Zaktualizuj `docs/QA_LOG.md`

## Krok 7 — Generuj .docx

```powershell
cd "c:\automation\rozmowa_kwal"
& "scripts\New-QADocument.ps1" -InputFile "docs\qa_draft_v{n+1}.md"
```

**ACK_REQ (Acknowledgement Required)** — wyjście bloku F ustawiane
automatycznie gdy moduł wymaga potwierdzenia po błędzie (widoczne
w Watch Table).

**ACK_NEC (Acknowledgement Necessary)** — wejście bloku F; wymaga impulsu
zbocza narastającego. Stały sygnał TRUE nie potwierdi reintegracji.

**ACK_GL** — blok z biblioteki Safety Advanced generujący zbiorczy impuls ACK
do wszystkich F-I/O na raz — używany po awariach komunikacyjnych.

**VS* (Pulse testing / Sensor supply)** — impulsowe zasilanie wyjście modułu
F-DI. Czujnik zasilany impulsami; ich powrót na wejście pozwala wykryć
urwanie kabla (brak impulsów) i zwarcie do 24 V (ciągłe impulsy).

**Cross-circuit detection** — wykrywanie zwarć między kanałami F-DI
realizowane przez VS* pulse testing. Zapewnia DC ≥ 99% bez dodatkowego
okablowania — warunek konieczny dla Cat.4 / PL e.

**Discrepancy time** — maksymalny czas dopuszczalnej rozbieżności stanów
dwóch kanałów czujnika 1oo2. Zbyt krótki → fałszywe błędy; zbyt długi →
późne wykrycie uszkodzenia. Konfigurowany w TIA Portal w parametrach F-DI.

**Substitute value** — wartość przyjmowana przez wyjście F-DO podczas
passivation (0 lub 1). Definiuje inżynier projektu na podstawie analizy
ryzyka — nie Siemens.

**Value status** — bit jakości sygnału Safety w S7-1200/S7-1500. FALSE =
sygnał zastępczy (passivation); TRUE = dane procesowe poprawne. Odwrotna
logika niż klasyczny QBAD.

**pm switching** — tryb F-DO w którym przełączana jest linia P (plus, 24 V),
masa wspólna. Prostsze okablowanie, niższy koszt.

**pp switching** — tryb F-DO w którym przełączane są obie linie P+, bez
wspólnej masy. Wyższy poziom bezpieczeństwa — zwarcie jednej linii do masy
nie powoduje przypadkowego zadziałania.

**F-PM-E (Fail-safe Power Module E)** — moduł Safety w ET 200SP/S
odcinający zasilanie grupy standardowych modułów DO przez sygnał Safety.
Tańsza alternatywa dla F-DQ przy spełnieniu wymagań SIL2/Cat.3/PLd.

---

### Struktury głosowania

**1oo1 (1 out of 1)** — jeden kanał; bez redundancji. Stosowany przy SIL1
lub gdy analiza ryzyka dopuszcza brak redundancji.

**1oo2 (1 out of 2)** — dwa czujniki; zatrzymanie gdy CHOĆBY JEDEN zgłosi
problem. Wyższe bezpieczeństwo, ryzyko fałszywych alarmów. Obsługiwane
sprzętowo przez moduł F-DI z discrepancy monitoring.

**2oo2 (2 out of 2)** — oba czujniki muszą zadziałać. Mniej fałszywych
stopów, ale uszkodzenie „cichego" kanału może uniemożliwić reakcję.

**2oo3 (2 out of 3)** — trzy czujniki, decyzja większości (2 z 3). Balans
bezpieczeństwa i dostępności; typowe w procesach ciągłych.

---

### PROFIsafe i PROFINET

**PROFIsafe** — protokół Safety działający na warstwie aplikacji ponad
PROFINET lub PROFIBUS. Każdy pakiet zawiera CRC, licznik wiadomości i
F-Address. Wykrywa: utratę pakietu, powtórzenie, błędną sekwencję,
przekłamanie danych, błędny adres.

**F-Address (F-Destination Address)** — unikalny adres Safety przypisany
każdemu modułowi F w sieci. Musi być identyczny w TIA Portal i na fizycznym
urządzeniu. Błędny F-Address → brak komunikacji Safety.

**F-monitoring time** — maksymalny czas oczekiwania F-CPU na kolejny pakiet
PROFIsafe. Przekroczenie → passivation modułu. Za krótki → fałszywe alarmy;
za długi → wolne wykrycie awarii sieci.

**F-peripheral** — zdalne urządzenie F-I/O podłączone do F-CPU przez
PROFIsafe/PROFINET (np. ET200SP z modułami F-DI/F-DQ, ET200eco F).

**MRP (Media Redundancy Protocol)** — protokół redundancji dla topologii
pierścieniowej PROFINET. Czas przełączenia < 200 ms (MRP) lub < 30 ms
(Fast-MRP). MRM = Media Redundancy Manager zarządza pierścieniem.

**IRT (Isochronous Real-Time)** — tryb PROFINET z synchronizacją cyklu
do 250 µs i jitterem < 1 µs, realizowaną sprzętowo na poziomie ASIC.
Wymagany przy motion control (SINAMICS S120 synchroniczny, systemy wieloosiowe).

**GSDML** — plik XML opisujący urządzenie PROFINET (moduły I/O, parametry,
obsługiwane adresy). Instalowany w TIA Portal: Options → Manage general
station description files.

**Shared Device** — urządzenie PROFINET zarządzane jednocześnie przez dwa
kontrolery, każdy z przypisanym innym zakresem modułów. Stosowane przy
integracji Safety i standardu z różnych dostawców.

---

### Napędy Safety (IEC 61800-5-2)

**STO (Safe Torque Off)** — natychmiastowe odcięcie momentu przez zablokowanie
impulsów PWM. Silnik wybiega swobodnie. Certyfikowany SIL3/PLe. Realizowany
sprzętowo w dwóch kanałach napędu. Odpowiada kategorii zatrzymania 0 (EN 60204-1).

**SS1 (Safe Stop 1)** — hamowanie wzdłuż rampy do zatrzymania → STO.
Czas hamowania monitorowany; przekroczenie = natychmiastowe STO.
Odpowiada kategorii zatrzymania 1 (EN 60204-1).

**SS2 (Safe Stop 2)** — hamowanie z rampą → SOS (napęd pozostaje zasilony
i trzyma pozycję). Odpowiada kategorii zatrzymania 2 (EN 60204-1).

**SOS (Safe Operating Stop)** — napęd zasilony, trzyma pozycję z monitoringiem
odchylenia. Możliwe generowanie momentu gdy oś próbuje się ruszyć.

**SLS (Safely Limited Speed)** — ograniczenie prędkości do bezpiecznego max.
Stosowane w trybie serwisowym gdy operator jest w strefie niebezpiecznej.

**SDI (Safe Direction)** — dopuszczony jest tylko jeden kierunek ruchu.
Stosowane gdy przy otwartej osłonie oś może jechać wyłącznie od operatora.

**SBC (Safe Brake Control)** — certyfikowane, monitorowane sterowanie
hamulcem mechanicznym. Monitoring prądu uzwojenia cewki hamulca.

**STO_Active** — sygnał potwierdzający od napędu do F-CPU przez PROFIsafe,
że STO jest aktywne. Odróżnia STO od zwykłego wyłączenia programowego.

---

### Obliczenia bezpieczeństwa

**SIL (Safety Integrity Level)** — poziom integralności bezpieczeństwa
wg IEC 61508 / IEC 62061. SIL 1: PFH < 10⁻⁵; SIL 2: PFH < 10⁻⁶;
SIL 3: PFH < 10⁻⁷.

**PL (Performance Level)** — poziom zapewnienia bezpieczeństwa wg EN ISO 13849-1.
PL a (najniższy) → PL e (najwyższy). PL e odpowiada SIL 3.

**PFH (Probability of dangerous Failure per Hour)** — prawdopodobieństwo
niebezpiecznej awarii niepostrzeżonej na godzinę pracy. Zsumowane dla
wszystkich podsystemów łańcucha Safety (Detection + Evaluation + Reaction).

**DC (Diagnostic Coverage)** — pokrycie diagnostyczne: procent niebezpiecznych
uszkodzeń wykrywanych przez diagnostykę wbudowaną. DC ≥ 99% wymagane dla
Cat.4 / PL e.

**CCF (Common Cause Failure)** — awaria wspólnej przyczyny: jedna przyczyna
(przepięcie, EMC, temperatura) niszczy oba kanały redundantnego systemu.
ISO 13849-1 wymaga min. 65 punktów CCF dla Cat.3/Cat.4.

**B10** — liczba cykli po których 10% populacji urządzenia mechanicznego ulega
awarii. Używany do obliczania MTTFd czujników i elementów wykonawczych.

**Proof test** — zaplanowany, periodyczny test ujawniający ukryte (niebezpieczne)
usterki systemu Safety. Musi być dokumentowany; interwał wpływa na PFH systemu.

**Kategoria zatrzymania 0 / 1 / 2 (EN 60204-1)** — kat. 0: natychmiastowe
odcięcie (odpowiada STO); kat. 1: hamowanie z rampą → odcięcie (SS1);
kat. 2: hamowanie z rampą → zasilanie utrzymane (SS2/SOS).

---

### TIA Portal i commissioning

**FAT (Factory Acceptance Test)** — testy u dostawcy maszyny przed wysyłką.
Każda funkcja Safety testowana i podpisywana przez dostawcę i klienta.

**SAT (Site Acceptance Test)** — testy u klienta po instalacji. Potwierdza
działanie Safety w docelowym środowisku (okablowanie terenowe, EMC).

**Know-How Protection** — hasłowe zablokowanie podglądu i edycji kodu bloku
FB/FC/DB. Program nadal uruchamia się i pode monitoringowi online.

**Copy Protection** — kryptograficzne powiązanie bloku z Serial Number
konkretnego CPU. Blok nie uruchomi się na innym urządzeniu.

**ProDiag** — narzędzie TIA Portal do diagnostyki inline maszyny: stany I/O,
warunki zablokowania, komentarze diagnostyczne widoczne bezpośrednio
na HMI bez osobnych ekranów alarmowych.

**Technology Object (TO)** — obiekt osi w TIA Portal (S7-1500) enkapsulujący
napęd + enkoder. API: MC_Power, MC_Home, MC_MoveAbsolute, MC_Halt, MC_Stop.

**OPC UA** — otwarty protokół komunikacji PLC ↔ SCADA/MES/chmura.
Szyfrowanie TLS 1.2, certyfikaty. Aktywowany w właściwościach CPU TIA Portal.
Wyższe opóźnienie niż PROFINET — nie stosować do sterowania real-time.

---

### Robot ABB IRC5

**EIO.cfg** — plik konfiguracyjny sygnałów I/O robota ABB. Definiuje nazwy,
typy i mapowanie sygnałów PROFINET (Group Input, Group Output, Digital I/O).

**Group Output (GO)** — sygnał PLC → robot: liczba (numer programu, offset
pozycji) jako INT przesyłana przez bajt/bajty PROFINET.

**Group Input (GI)** — sygnał robot → PLC: potwierdzenie, status, kody
błędów robota.

**RobotReady** — sygnał robota do PLC potwierdzający gotowość do przyjęcia
komendy start.

**ProgramDone** — sygnał robota do PLC po wykonaniu zadania. PLC może
wysłać kolejną komendę lub zmienić numer programu.

---

### SICAR@GST

**SICAR (Siemens Automotive Reference)** — framework programistyczny Siemens
dla automotive (fabryki robotyczne). Zawiera szablony TIA Portal, biblioteki
Tec Units, wzorce alarmów i ProDiag.

**Tec Unit** — gotowy, parametryzowalny blok funkcjonalny SICAR dla urządzenia
(silnik, zawór, napęd, robot) zawierający: FB PLC z logiką, ekrany HMI,
definicje alarmów, obsługę trybów Auto/Manual/Local.

**Betriebsartenbereiche** — obszary trybów pracy (strefy ochronne) w SICAR;
max 12 obszarów definiujących różne konfiguracje bezpieczeństwa maszyny.
```

## Krok 5 — Wygeneruj dokument .docx

Po zapisaniu `docs/qa_draft_v7.md` uruchom skrypt generujący .docx:

```powershell
cd "c:\automation\rozmowa_kwal"
$nextVersion = (Get-ChildItem "PLC_Commissioner_QA_v*.docx" | 
    Sort-Object { [int]($_.BaseName -replace '.*v','') } | 
    Select-Object -Last 1).BaseName -replace '.*v',''
$nextVersion = [int]$nextVersion + 1

.\scripts\New-QADocument.ps1 `
    -InputFile "docs\qa_draft_v$nextVersion.md" `
    -OutputFile "PLC_Commissioner_QA_v$nextVersion.docx" `
    -Version $nextVersion
```

## Krok 6 — Weryfikacja i log

Po wygenerowaniu .docx:

1. Otwórz plik — sprawdź formatowanie sekcji i pytań
2. Sprawdź czy nowe sekcje są obecne
3. Zaktualizuj `docs/QA_LOG.md`:

```markdown
## v{n} — [DATA]
**Nowe pytania**: [liczba]
**Zmodyfikowane**: [liczba]
**Nowe tematy**: [lista]
**Źródła**: [które PDFs użyte]
```

## Kontrola jakości przed zamknięciem

Checklist:
- [ ] Każde pytanie ma definicję + szczegóły (bullet list) + praktykę
- [ ] Odpowiedź na pytanie diagnostyczne ma min. 4 kroki
- [ ] Numery parametrów Siemens sprawdzone (nie zmyślone)
- [ ] Normy podane we właściwym formacie (EN/IEC + numer)
- [ ] Język polski, terminologia Siemens
- [ ] .docx otwiera się poprawnie w Word i ma spis treści
