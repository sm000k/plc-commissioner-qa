---
mode: agent
description: "Faza 3: Generuj kompletne odpowiedzi Q&A i utwórz gotowy dokument .docx"
tools: ['read_file', 'file_search', 'run_in_terminal', 'create_file', 'replace_string_in_file']
---

# Faza 3 — Generowanie odpowiedzi i dokumentu .docx

## Twój cel
Na podstawie pytań z `docs/pytania_draft_v{n}.md` wygeneruj kompletne odpowiedzi, złóż z istniejącym Q&A i uruchom skrypt tworzący `.docx`.

## Krok 1 — Odczytaj pytania

```
#file:docs/pytania_draft_v7.md
```

## Krok 2 — Format odpowiedzi (template obligatoryjny)

Każda odpowiedź **musi** składać się z trzech bloków:

```
### [numer]. [Pytanie w formie pełnego zdania?]

[DEFINICJA — 1-2 zdania wyjaśniające czym jest X i jak działa]

- [Kluczowy fakt / właściwość 1]
- [Kluczowy fakt / właściwość 2]
- [Kluczowy fakt / właściwość 3 — z numerem parametru Siemens jeśli dotyczy]

[PRAKTYKA — procedura krok po kroku LUB przykład z TIA Portal LUB realny scenariusz]

> Źródło: [nazwa dokumentu / numer Siemens / norma IEC lub EN] *(opcjonalne, gdy znane)*
```

### Przykład dobrej odpowiedzi:

```
### 3. Co to jest SS1 (Safe Stop 1) i kiedy go używasz zamiast STO?

SS1 (Safe Stop 1) to funkcja Safety napędu SINAMICS która hamuje oś wzdłuż 
zaprogramowanej rampy prędkości do zatrzymania, a następnie aktywuje STO 
(Safe Torque Off). Certyfikowana wg IEC 61800-5-2.

- Czas hamowania monitorowany przez napęd — przekroczenie limitu = natychmiastowe STO
- Skonfigurowana rampa SS1 musi być krótsza niż czas reakcji Safety wynikający z analizy ryzyka
- Realizowana przez PROFIsafe (zaawansowana) lub zaciski hardwarowe (prostsza)
- Parametr p9652 (G120) — czas SS1 ramp, zakres 0–300s

Używasz SS1 zamiast STO gdy natychmiastowe odcięcie momentu (STO) jest niebezpieczne:
obrabiarka z dużą masą bezwładnościową, winda, dźwig, robot z ciężkim ładunkiem — 
nagłe odcięcie powoduje zderzenie lub uszkodzenie mechaniki.

Procedura testowania SS1 podczas commissioning:
1. Aktywuj SS1 przez PROFIsafe lub zacisk STO
2. Zmierz czas hamowania stopwatchem
3. Zweryfikuj że napęd się zatrzymał przed aktywacją STO (status r9722.3=1)
4. Sprawdź czy napęd nie może ruszyć bez cofnięcia SS1

> Źródło: IEC 61800-5-2, Siemens SINAMICS G120 Safety Integrated Function Manual
```

## Krok 3 — Zasady merytoryczne dla generowania odpowiedzi

### Numery parametrów SINAMICS (używaj gdy pewny)
| Parametr | Opis |
|----------|------|
| `p0840` | ON/OFF1 — źródło sygnału start napędu |
| `p1120` | Ramp-up time [s] |
| `p1121` | Ramp-down time [s] |
| `r0002` | Status napędu (bitmapa) |
| `r0945[0..7]` | Kody błędów (fault codes) |
| `r2110` | Aktualny kod alarmu (warning) |
| `p2051` | Telegram PROFIdrive (1/20/105) |
| `p9501` | Safety STO enable |
| `p9601` | Safety SS1 ramp time |
| `p9652` | SS1 timeout |

### Normy — używaj właściwych oznaczeń
- Bezpieczeństwo maszyn: **EN ISO 13849-1** (PL a-e), **IEC 62061** (SIL)
- Napędy Safety: **IEC 61800-5-2** (STO/SS1/SS2/SOS/SLS/SDI/SBC)
- Systemy Safety: **IEC 61508** (SIL 1-3), **EN 60204-1** (kategorie zatrzymania 0/1/2)
- E-Stop: **EN ISO 13850**, przekaźniki bezpieczeństwa: **EN 60947-5-1**

### Terminologia Siemens (używaj ZAWSZE)
| ✅ Poprawnie | ❌ Niepoprawnie |
|-------------|----------------|
| F-CPU | sterownik bezpieczeństwa |
| passivation | wyłączenie/blokada modułu |
| F-signature | suma kontrolna programu |
| collective signature | podpis całości |
| reintegration | resetowanie modułu |
| substitute value | wartość domyślna |
| F-monitoring time | timeout komunikacji |
| value status | bit jakości |

## Krok 4 — Złóż pełne Q&A

Weź istniejące pytania i odpowiedzi z v6 + nowe pytania z `docs/pytania_draft_v7.md` i złóż kompletny draft w `docs/qa_draft_v7.md`.

Struktura pliku `docs/qa_draft_v7.md`:

```markdown
# KOMPENDIUM Q&A
### PLC Programmer / Commissioner / Automatyk
### Siemens TIA Portal · Safety PLC · ET200 · Napędy SINAMICS · Robot ABB · SICAR
### Pytania + odpowiedzi zweryfikowane pod kątem rozmów kwalifikacyjnych.
### Źródła: Siemens Application Example 21064024 (E-Stop SIL3 V7.0.1), Wiring Examples 39198632, SIMATIC Safety Integrated dokumentacja.
---

## 1. PODSTAWY PLC I AUTOMATYKI
### 1. Co to jest PLC i czym różni się od zwykłego komputera?
[treść odpowiedzi]

[... dalsze sekcje 2–18 ...]

---

## 19. SŁOWNIK POJĘĆ — PLC / Safety / PROFINET / Napędy

Słownik zawiera **pełne definicje** (2–4 zdania) wszystkich kluczowych pojęć
używanych w komisjonowaniu systemów Siemens. W odróżnieniu od ściągi — każde
hasło wyjaśnia kontekst użycia i praktyczne znaczenie.

### Podstawy PLC

**Scan cycle** — jeden pełny cykl wykonania programu CPU: odczyt wejść →
wykonanie programu → zapis wyjść → obsługa komunikacji. Czas cyklu wynosi
typowo 1–20 ms; przy dużych projektach Safety może wzrosnąć do 50–100 ms.
Zbyt długi scan cycle = opóźniona reakcja na sygnały bezpieczeństwa.

**OB (Organization Block)** — blok organizacyjny w TIA Portal definiujący
punkt wywołania programu. OB1 = główny cykl, OB35 = przerwanie cykliczne
(np. co 100 ms), OB100 = zimny start, F_MAIN = Safety OB.

**FB (Function Block)** — blok funkcjonalny z własną pamięcią instancji (IDB).
Zachowuje stan między wywołaniami — używany dla silników, sekwencji, timerów.
Każde wywołanie FB wymaga odrębnej instancji DB.

**FC (Function)** — blok bez pamięci własnej. Używany dla obliczeń
jednorazowych, konwersji sygnałów, logiki bezstanowej. Tańszy pamięciowo
niż FB.

**DB (Data Block)** — blok danych. Globalny DB: dostępny z całego programu.
Instancja DB: dedykowana pamięć jednego FB, tworzona automatycznie.

**UDT (User Data Type)** — użytkowniczy typ złożony (np. `Motor_t` z polami
Speed:REAL, Fault:BOOL). Wymusza spójną strukturę dla wielu identycznych
urządzeń; jeden FB + UDT zastępuje N osobnych bloków.

**Tag (zmienna PLC)** — nazwy symboliczne adresów I/O, DB, merkerów
w tablicy tagów TIA Portal. Tagi globalne dostępne z całego projektu;
lokalne tylko w bloku.

---

### Architektura Safety

**F-CPU (Fail-safe CPU)** — sterownik Siemens z certyfikowanym podwójnym
kanałem obliczeniowym (dual-channel processing). Oba kanały wykonują te same
obliczenia równolegle; rozbieżność wyników → przejście w bezpieczny stan.
Certyfikat TÜV: SIL 3 / PL e.

**F-signature** — kryptograficzny podpis jednego bloku Safety generowany
przez TIA Portal podczas kompilacji. Zmienia się przy każdej modyfikacji kodu.
Przechowywany w F-DB — nie można go edytować ręcznie.

**Collective signature (podpis zbiorczy)** — unikalny podpis całego programu
Safety złożony ze wszystkich F-signatur. Widoczny na wyświetlaczu CPU.
Niezgodność collective signature po wgraniu → Safety nie uruchamia się.

**F-DB (Fail-safe Data Block)** — blok danych generowany automatycznie przez
TIA Portal dla każdego bloku Safety. Zawiera CRC, F-signature i parametry
czasowe. Ręczna edycja zniszczyłaby spójność i uniemożliwiłaby uruchomienie
Safety.

**Safety Integrated** — koncepcja Siemens: funkcje bezpieczeństwa (failsafe)
i funkcje standardowe w jednym fizycznym CPU, jednym projekcie TIA Portal,
przez jedną sieć PROFINET/PROFIsafe.

**LOCK / RUN (Safety CPU)** — tryby pracy Safety runtime. LOCK: program
Safety zablokowany, wyjścia Safety → wartości zastępcze. RUN: Safety wykonuje
się normalnie. Zmiana trybu wymaga hasła Safety i jest logowana.

**F-OB (Safety Main OB)** — organizacyjny blok Safety wywoływany osobnym
cyklem F-CPU. Odpowiednik OB1 dla programu failsafe. W TIA Portal widoczny
jako np. `Main_Safety_RTG1`.

---

### Moduły F-DI / F-DO

**Passivation** — stan błędu modułu F-I/O: wyjścia przyjmują substitute value
(zwykle 0), wejścia raportowane są do F-CPU jako 0. Wyzwalana przez: urwanie
kabla, discrepancy timeout, utratę PROFIsafe, błąd wewnętrzny modułu.

**Reintegration** — ręczne potwierdzenie (ACK) powrotu modułu do normalnej
pracy po usunięciu błędu i passivation. Wymaga impulsu ACK_NEC — moduł nie
wraca automatycznie (zasada „no silent recovery").

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
