## 16. MOTION CONTROL I SINAMICS — PRAKTYKA COMMISSIONING


### 16.1. Co to jest Technology Object (TO) w TIA Portal i jak go używasz?

**Technology Object** to abstrakcja osi w TIA Portal dla motion control *(dostępna w S7-1500, ET200SP CPU)*. TO enkapsuluje napęd + enkoder + parametry osi jako jeden obiekt z gotowym API w SCL.

| Typ TO | Opis | Typowe zastosowanie |
|--------|------|---------------------|
| `TO_SpeedAxis` | Tylko prędkość | Napędy bez pozycjonowania |
| `TO_PositioningAxis` | Pozycjonowanie absolutne/względne | Przenośniki z pozycją |
| `TO_SynchronousAxis` | Synchronizacja do osi master | Systemy wieloosiowe, cam profiles |
| `TO_ExternalEncoder` | Zewnętrzny enkoder bez napędu | Monitoring pozycji, wałek wirtualny |

**API Motion Control (bloki MC_):**
`MC_Power`, `MC_Home`, `MC_MoveAbsolute`, `MC_MoveVelocity`, `MC_Halt`, `MC_Stop`

**Konfiguracja:** TIA Portal → `Add new object` → `Technology object` → wybierz typ → przypisz napęd SINAMICS przez telegram PROFIdrive `105` / `111`.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 16.2. Jak robisz autotuning napędu G120/V90 w Startdrive?

**Startdrive:** Online → wybierz napęd → `Commissioning` → `Motor identification`

**1. Motor identification (statyczna — silnik stoi):**
- `Motor identification → Static → Start`
- Trwa ~30 s, napęd mierzy rezystancję i induktancję uzwojeń
- Wymagane: uziemienie silnika, napęd w stanie Ready

**2. Speed controller optimization (dynamiczna — silnik się obraca):**
- `Motor identification → Speed controller optimization → Start`
- Silnik wykonuje sekwencję ruchów testowych — **odblokuj strefę bezpieczeństwa**
- Wyznacza `Kp` (wzmocnienie) i `Ti` (czas całkowania) regulatora prędkości

**3. Weryfikacja:** `r0047` (status identyfikacji) = `0` → brak błędu, parametry zapisane

> 💡 Jeśli napęd jest mechatronicznie połączony z ciężką maszyną: uruchom identyfikację na **biegu jałowym** lub przy odłączonej mechanice, a potem ręcznie dostraj `Kp`.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 16.3. Jakie są najważniejsze parametry SINAMICS G120 które musisz znać?

| Parametr | Opis | Uwaga |
|----------|------|-------|
| `p0840` | ON/OFF1 — źródło sygnału start/stop | Bit z telegramu PROFIdrive lub terminal |
| `p1120` | Czas rampy rozruchu [s] | Od 0 do max prędkości |
| `p1121` | Czas rampy hamowania [s] | |
| `p0922` | Telegram PROFIdrive | Musi zgadzać się z konfiguracją TIA Portal! |
| `r0002` | Aktualny status napędu (bitmapa) | Gotowy / praca / błąd / alarm |
| `r0945[0..7]` | Kody błędów (fault codes) | Pierwsze miejsce diagnostyki po F-alarm |
| `r2110` | Aktualny kod alarmu (warning) | ⚠️ DO WERYFIKACJI — sprawdź w Parameter Manual |
| `p9501` / `p9601` | Parametry Safety (STO enable, SS1) | ⚠️ DO WERYFIKACJI — zakres p95xx/p96xx poprawny, dokładne numery sprawdź w SINAMICS Safety Function Manual |

> ⚠️ Błędny `p0922` (telegram) = brak komunikacji lub brak danych Safety — **zawsze weryfikuj po podłączeniu** nowego napędu.

### 16.4. Jak interpretujesz i kasujesz fault F30001 i F07801 w SINAMICS?

| Fault | Znaczenie | Najczęstsza przyczyna | Diagnoza |
|-------|-----------|----------------------|---------|
| **F30001** | Power unit: Ground fault — błąd doziemny wyjścia | Uszkodzona izolacja kabla silnikowego, zwarcie w uzwojeniu | Megaomomierz 500V DC między żyłami a PE — powinno być >10 MΩ |
| **F07801** | Motor overtemperature (model termiczny) | Przeciążenie, zatkany filtr chłodzenia, za długie rozruchy | Sprawdź `p0335` (klasa izolacji) i wentylację silnika |

> ⚠️ W starszych wersjach firmware G120 `F30001` może oznaczać różne usterki Power Unit — zawsze weryfikuj w Parameter Manual dla konkretnej wersji firmware (`r0018` = wersja firmware).

**Kasowanie faultów:**
- Programowo: `p2103 = 1` lub bit 7 słowa sterowania `STW1` w telegramie PROFIdrive
- Na panelu BOP-2: długie wciśnięcie ESC/OK
- Historia faultów: `r0945[0..7]`

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 16.5. Czym jest SINAMICS G120 i do jakich silników oraz aplikacji jest przeznaczony? 🔴

**SINAMICS G120** to rodzina przemysłowych przemienników częstotliwości (falowników) firmy Siemens przeznaczonych do regulacji prędkości silników indukcyjnych (asynchronicznych) klatkowych w aplikacjach ogólnoprzemysłowych.

**Podstawowe dane:**
- Zakres mocy: 0,37 kW – 250 kW (napięcie 3×400V AC / 3×690V AC)
- Topologia: modułowa — Control Unit (CU) + Power Module (PM) + opcjonalnie BOP (panel operatorski)
- Komunikacja: PROFINET, PROFIBUS, USS, Modbus RTU (zależy od wersji CU)

**Stosowane silniki:**
| Typ silnika | Tryb sterowania G120 | Typowe zastosowanie |
|-------------|---------------------|-------------------|
| Silnik indukcyjny klatkowy (IM) | V/f, Vector (VVC+) | Wentylatory, pompy, przenośniki |
| Silnik indukcyjny z enkoderem | Vector closed-loop | Wciągarki, prasy, mieszalniki |
| PMSM / IPM (IE4/IE5) | Vector PMSM | Sprężarki, pompy wysokosprawne |

**Typowe aplikacje G120:**
- Wentylatory i pompy (redukcja zużycia energii przez regulację prędkości)
- Przenośniki taśmowe i rolkowe
- Mieszalniki, ekstruktory, wciągarki
- Sprężarki powietrza

> ⚠️ **G120 ≠ serwonapęd** — G120 nie jest przeznaczony do precyzyjnego pozycjonowania (brak sprzężenia zwrotnego pozycji w standardzie). Do servo używaj SINAMICS S120 lub V90.

*Źródło: Siemens SINAMICS G120 Getting Started / transkrypcje ControlByte*

### 16.6. Jakie są podstawowe komponenty układu napędowego z SINAMICS G120 i sterownikiem Siemens? 🔴

Kompletny układ z G120 składa się z kilku modułów, które można dobierać niezależnie.

**Architektura modułowa G120:**

| Komponent | Opis | Przykładowe typy |
|-----------|------|-----------------|
| **Control Unit (CU)** | "Mózg" napędu — sterowanie, komunikacja, Safety | CU240E-2 PN, CU250S-2 PN, CU230P-2 |
| **Power Module (PM)** | Przekształtnik mocy — prostownik + falownik IGBT | PM240-2, PM250, PM330 |
| **BOP-2 / IOP** | Panel operatorski — parametryzacja, diagnostyka | BOP-2 (basic), IOP-2 (graficzny) |
| **Silnik** | Silnik indukcyjny klatkowy 3-fazowy | SIMOTICS GP, SD, DP |
| **Sterownik PLC** | Wydaje rozkazy przez PROFINET/PROFIBUS | S7-1200, S7-1500 |

**Połączenia:**
- CU ↔ PM: złącze wewnętrzne (snap-in) lub kabel adaptera
- PLC ↔ CU: PROFINET lub PROFIBUS — telegramy standardowe (1, 20, 352)
- Czujnik temperatury silnika: PTC/KTY84 do wejścia CU (ochrona termiczna)

> 💡 **PM250** ma funkcję odzysku energii (regeneracja do sieci) — stosowany przy wciągarkach i aplikacjach z hamowaniem.

*Źródło: Siemens SINAMICS G120 Getting Started / transkrypcje ControlByte*

### 16.7. Jakie oprogramowanie służy do konfiguracji i uruchomienia SINAMICS G120? 🔴

Do uruchomienia G120 dostępne są trzy narzędzia — wybór zależy od zakresu prac.

| Narzędzie | Zastosowanie | Kiedy używać |
|-----------|-------------|-------------|
| **Startdrive** *(wtyczka TIA Portal)* | Pełna konfiguracja, parametryzacja, diagnostyka online, Safety | Nowe projekty, integracja z PLC |
| **STARTER** *(standalone)* | Parametryzacja offline/online, oscyloskop, Drive Control Chart | Starsze projekty, poza TIA |
| **BOP-2 / IOP** | Parametryzacja ręczna na panelu napędu | Szybki serwis w terenie bez laptopa |
| **SINAMICS Smart Access Module** | Parametryzacja przez Wi-Fi z przeglądarki | Uruchomienie mobilne |

**Startdrive — kluczowe kroki commission:**
1. TIA Portal → Add new device → Drives → SINAMICS G120 → wybierz CU i PM
2. Konfiguracja silnika: `p0304` (napięcie), `p0305` (prąd), `p0307` (moc), `p0310` (częstotliwość), `p0311` (prędkość znamionowa)
3. Identyfikacja silnika: `p1910 = 1` (pomiar stojana w stanie spoczynku) lub `p1960 = 1` (obracająca się identyfikacja)
4. Wybór metody sterowania: `p1300` (0 = V/f, 20 = Vector bez enkodera, 21 = Vector z enkoderem)
5. Download → Compile → Go online → Test Jog

*Źródło: Siemens SINAMICS G120 Getting Started / transkrypcje ControlByte*

### 16.8. Jakie tryby sterowania oferuje SINAMICS G120 i czym się różnią? 🟡

G120 obsługuje kilka metod sterowania silnikiem — dobór zależy od wymagań aplikacji.

| Tryb (`p1300`) | Nazwa | Enkoder | Dokładność prędkości | Zastosowanie |
|----------------|-------|---------|---------------------|-------------|
| **0** | V/f (liniowy) | Nie | ±3–5% | Wentylatory, pompy, proste przenośniki |
| **2** | V/f z FCC (Flux Current Control) | Nie | ±2–3% | Wyższy moment przy małych prędkościach |
| **20** | Vector (bez enkodera) | Nie | ±0,5% | Wymagania na moment, bez czujnika |
| **21** | Vector (z enkoderem) | Tak | ±0,01% | Wciągarki, precyzyjne prędkości |
| **22** | PMSM Vector (bez enk.) | Nie | ±0,5% | Silniki IE4/IE5 bez enkodera |
| **23** | PMSM Vector (z enk.) | Tak | ±0,01% | Silniki IE4/IE5 z enkoderem |

**Telegramy PROFINET dla G120:**
- **Telegram 1** (standardowy): słowo sterujące STW1 + prędkość zadana (16-bit)
- **Telegram 20**: rozszerzony — dodaje prąd, moment, status
- **Telegram 352** (Safety): zawiera PROFIsafe — dla wersji CU z Safety Integrated

> ⚠️ **p1300 = 0 (V/f)** nie reguluje momentu — przy przeciążeniu prędkość spada. Do stałego momentu niezależnego od obciążenia → Vector (p1300 = 20/21).

*Źródło: Siemens SINAMICS G120 Getting Started / transkrypcje ControlByte*

### 16.9. Jak przebiega procedura identyfikacji silnika (Motor ID) w SINAMICS G120 i dlaczego jest niezbędna? 🟡

**Identyfikacja silnika** to pomiar elektrycznych parametrów podłączonego silnika przez napęd G120. Bez niej regulator wektorowy nie działa poprawnie — używa jedynie wartości tabliczkowych, które nie uwzględniają rzeczywistego okablowania i stanu silnika.

**Dwa rodzaje identyfikacji:**

| Parametr | Typ | Opis | Warunek |
|----------|-----|------|---------|
| `p1910 = 1` | **Stojanova (statyczna)** | Pomiar rezystancji stojana R1, indukcyjności rozproszenia — silnik stoi | Silnik może być połączony z maszyną |
| `p1960 = 1` | **Wirująca (dynamiczna)** | Pomiar R1 + R2, indukcyjności magnesującej Lm — silnik obraca się | Silnik musi móc się obracać swobodnie |

**Procedura `p1910` (statyczna) krok po kroku:**
1. Podaj dane tabliczkowe silnika: `p0304`, `p0305`, `p0307`, `p0310`, `p0311`
2. Ustaw `p1910 = 1` → przy następnym rozruchu napęd przeprowadzi pomiar
3. Daj rozkaz RUN (Enable) → napęd wykonuje pomiar (~10–30 s), silnik może lekko drżeć
4. Po zakończeniu `p1910` wraca do 0, parametry `p0350` (R1), `p0356` (Ls) są zapisane
5. Zapisz parametry: `p0971 = 1` (zapis do ROM) lub przez Startdrive → Download

**Dlaczego toważne:**
- Zbyt wysokie R1 (długi kabel) → regulator wektorowy kompensuje automatycznie po ID
- Silnik inny niż w danych tabliczkowych (np. przewinięty) → ID wykryje różniące się R1
- Brak ID przy `p1300 = 20/21` → moment może być niedokładny o 20–40%

> ⚠️ **Najczęstszy błąd na komisjoningu:** download projektu, pierwsze uruchomienie → silnik wibruje lub nie osiąga zadanej prędkości → przyczyną brak identyfikacji lub błędne dane tabliczkowe.

*Źródło: Siemens SINAMICS G120 Getting Started / transkrypcje ControlByte*

### 16.10. Jak wygląda pełna procedura commissioning SINAMICS G120 z TIA Portal krok po kroku? 🔴

Procedura uruchomienia G120 (CU240E-2 PN + PM240-2) z silnikiem indukcyjnym przez PROFINET.

**Faza 1 — Przygotowanie sprzętowe:**
1. Zamontuj CU na PM (snap-in), podłącz 3×400V AC do PM, silnik do U2/V2/W2
2. Podłącz PTC/KTY84 do CU, kabel PROFINET do switcha/PLC
3. Jeśli Safety: podłącz E-Stop do zacisków STO (DI4/DI5)
4. Włącz zasilanie — BOP-2 pokaże `o` lub alarm A07991 (brak konfiguracji)

**Faza 2 — Konfiguracja w Startdrive:**
1. TIA Portal → `Add new device` → `SINAMICS G120` → wybierz CU i PM
2. Commissioning wizard: dane tabliczkowe silnika (`p0304`–`p0311`), metoda sterowania (`p1300`)
3. Network view: połącz z PLC, ustaw nazwę PROFINET i IP
4. Wybierz telegram `p0922` (1 = standardowy, 20 = rozszerzony, 352 = Safety)
5. Compile + Download HW do PLC

**Faza 3 — Identyfikacja silnika:**
1. Statyczna (`p1910 = 1`): pomiar R1, Lσ przy stojącym silniku (~30s)
2. Opcjonalnie wirująca (`p1960 = 1`): silnik musi się obracać swobodnie — **zabezpiecz strefę**
3. Sprawdź `r0047 = 0` (brak błędów po identyfikacji)

**Faza 4 — Test Jog i weryfikacja:**
1. Startdrive → Control panel → Jog: ustaw 300 rpm, kliknij JOG+
2. Monitoruj `r0021` (prędkość), `r0027` (prąd) — porównaj z tabliczkowymi
3. Kierunek odwrotny? → zamień fazy lub `p1821 = 1`
4. Test STO: aktywuj → `r9722.0 = 1` (STO_Active) → napęd nie generuje momentu

**Faza 5 — Uruchomienie z PLC przez PROFINET:**
1. STW1 = `16#047F` (Enable + RUN), HSW = `16384` → 100% prędkości `p2000`
2. Monitoruj ZSW1 (`r0052`): bit 2 = gotowy, bit 4 = w ruchu
3. Zapisz do ROM: `p0971 = 1`

**Faza 6 — Safety komisjonowanie (jeśli dotyczy):**
1. Startdrive → Safety Integrated → Start safety commissioning
2. Test STO z podpisem → Safety checksum (Safety ID) → zmień hasło

| Parametr diagnostyczny | Opis |
|----------------------|------|
| `r0945` | Kod ostatniego faultu |
| `r0021` | Prędkość aktualna [rpm] |
| `r0027` | Prąd aktualny [A] |
| `r0052` | Słowo statusowe ZSW1 |

> ⚠️ **Telegram `p0922`** musi być identyczny w napędzie i DB PLC. Niezgodność = pozornie poprawna komunikacja, ale bity na złych pozycjach.

> ⚠️ Po zmianie parametrów Safety obowiązkowy **Safety Acceptance Test** z raportem.

> 💡 `Take online device as preset` — TIA Portal wczyta konfigurację z istniejącego napędu jako punkt startowy.

*Źródło: Siemens SINAMICS G120 Getting Started, Startdrive commissioning guide*

### 16.11. Do czego służy blok funkcyjny MC_MoveJog w TIA Portal i jakie są jego podstawowe parametry wejściowe?
Blok funkcyjny MC_MoveJog w TIA Portal służy do sterowania osią z zadaną prędkością, najczęściej wykorzystywany jest do ruchu w trybie ręcznym (JOG), ale może być również używany w normalnym cyklu pracy maszyny.
- Jest to blok typu Enable, co oznacza, że działa tak długo, dopóki na jego wejściu `JogForward` lub `JogBackward` podany jest stan wysoki.
- **`Axis`:** Referencja do obiektu technologicznego (SpeedAxis, PositioningAxis, SynchronousAxis).
- **`JogForward` (BOOL):** Aktywuje ruch osi do przodu.
- **`JogBackward` (BOOL):** Aktywuje ruch osi do tyłu (jednoczesne aktywowanie obu powoduje błąd).
- **`Velocity` (Long Real):** Bezwzględna wartość prędkości, z jaką oś ma się poruszać (np. w mm/s); wartość ujemna jest traktowana jako bezwzględna, a kierunek nadaje `JogForward`/`JogBackward`.
- **`Acceleration`, `Deceleration`, `Jerk` (Long Real):** Parametry dynamiki ruchu; wartość -1 powoduje użycie parametrów skonfigurowanych w obiekcie technologicznym.
- **`PositionControl` (BOOL):** Aktywuje regulator pozycji (domyślnie True).
*Źródło: transkrypcje ControlByte*

### 16.12. Jakie są kluczowe cechy i zachowania bloku MC_MoveJog podczas pracy?
Blok MC_MoveJog charakteryzuje się specyficznymi zachowaniami i wyjściami statusowymi, które informują o jego działaniu i umożliwiają dynamiczną kontrolę ruchu.
- Po aktywacji ruchu (np. `JogForward` = True), na wyjściu `Busy` pojawia się stan True, a po osiągnięciu zadanej prędkości, bit `InVelocity` również przyjmuje wartość True.
- W przypadku błędnej parametryzacji (np. nieodpowiednie przyspieszenie), na wyjściu `Error` pojawia się True, a `ErrorID` wskazuje kod błędu (np. 8004h dla "Illegal acceleration specification").
- Podczas trwania ruchu możliwe jest dynamiczne zmienianie parametrów `Velocity`, `Acceleration`, `Deceleration` i `Jerk` "w locie", co jest przydatne w aplikacjach wymagających adaptacji prędkości.
- Podanie wartości 0 dla `Velocity` podczas aktywnego bloku spowoduje zahamowanie osi i utrzymanie prędkości zerowej.
*Źródło: transkrypcje ControlByte*

### 16.13. Jakie są parametry enkoderów inkrementalnych i absolutnych — rozdzielczość, co mogą i czego nie mogą?  🟡

**Enkoder inkrementalny — kluczowe parametry:**

| Parametr | Typowe wartości | Opis |
|----------|----------------|------|
| **PPR** *(Pulses Per Revolution)* | 100 / 512 / 1024 / 2048 / 4096 / 8192 | Impulsy na jeden pełny obrót osi enkodera |
| **Napięcie zasilania** | 5 V DC (TTL) / 12–24 V DC (HTL) | TTL = linie różnicowe, HTL = sygnał push-pull |
| **Sygnały** | A, B (faza 90°), Z (indeks/zerowy) | A+B → kierunek i liczba impulsów; Z → punkt odniesienia |
| **Max częstotliwość** | do 500 kHz (HTL) / do 1 MHz (TTL) | Limit dla modułu licznikowego lub wejścia HSC |
| **Ochrona** | IP54–IP67 | Zależnie od producenta i montażu |

**Enkoder absolutny — kluczowe parametry:**

| Parametr | Typowe wartości | Opis |
|----------|----------------|------|
| **Rozdzielczość single-turn** | 12–25 bit | 17 bit = 131 072 pozycji/obrót (typowy HIPERFACE/EnDat) |
| **Rozdzielczość multi-turn** | 12 bit dodatkowe | 4096 pełnych obrotów liczonych niezależnie |
| **Interfejs** | SSI, EnDat 2.1/2.2, HIPERFACE, HIPERFACE DSL | Patrz Q16.13 |
| **Czas odpowiedzi** | do 8 µs (EnDat 2.2) | Limit dla krótkiego czasu cyklu napędu |
| **Diagnostyka** | temperatura, błędy wewnętrzne | Dostępna przez EnDat 2.2 i HIPERFACE DSL |

**Co mogą:**
- Precyzyjne pozycjonowanie do ±1 impulsu (inkrementalny) lub ±0.003° przy 17 bit (absolutny)
- Pomiar prędkości: $n = (f 	imes 60) / PPR$ [rpm]
- Multi-turn absolutny: śledzenie pozycji przez wiele obrotów bez zasilania bateryjnego
- Diagnostyka wewnętrzna (temperatura, błędy — EnDat 2.2, HIPERFACE DSL)
- Synchronizacja osi (`TO_ExternalEncoder` w TIA Portal) — wałek wirtualny, master-slave

**Czego nie mogą:**
- **Inkrementalny:** nie pamięta pozycji po zaniku zasilania → **zawsze wymaga homing** po resecie
- **Inkrementalny:** nie ma jednoznacznej pozycji absolutnej → niebezpieczne przy osiach pionowych z obciążeniem
- **Absolutny single-turn:** zlicza tylko jeden obrót → po >360° traci pozycję absolutną
- **Standard enkodery:** nie są certyfikowane Safety → **nie można ich używać dla SLS/SDI** (wymagają enkoder Safety: HIPERFACE Safety lub EnDat Safety)
- **HTL przy dużej prędkości:** ograniczona częstotliwość (~500 kHz) → przy dużej prędkości i wysokim PPR może dochodzić do utraty impulsów

> ⚠️ **Safety funkcje SLS/SDI:** SINAMICS wymaga enkodera certyfikowanego Safety (HIPERFACE Safety lub EnDat Safety) wbudowanego w silnik — standardowy enkoder przemysłowy nie spełnia wymagań IEC 61800-5-2 dla „safe encoder feedback".

> 💡 **Przelicznik rozdzielczości:** enkoder 1024 PPR z interpolacją ×4 (A, /A, B, /B) daje **4096 kroków/obrót** — to standardowe zachowanie modułu HSC lub SINAMICS przy zliczaniu czterech zboczy.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 16.14. Jakie są interfejsy enkoderów i jak konfigurujesz enkoder w SINAMICS i TIA Portal?  🟡

**Przegląd interfejsów:**

| Interfejs | Typ sygnału | Napięcie | Kierunek | Typowe zastosowanie |
|-----------|------------|----------|----------|---------------------|
| **TTL (A/B/Z)** | Cyfrowy różnicowy | 5 V DC | Jednostronny | S7-1200 HSC, proste osi, tanie aplikacje |
| **HTL (A/B/Z)** | Cyfrowy push-pull | 12–24 V DC | Jednostronny | Środowisko przemysłowe, odporność na EMC |
| **Sin/Cos 1 Vpp** | Analogowy sinusoidalny | 5 V / 12 V | Jednostronny | G120 z CU240E, wysoka rozdzielczość przez interpolację |
| **SSI** | Szeregowy synchroniczny | 5 V / 12 V | Jednostronny | Absolutne enkoderzy starszej generacji |
| **EnDat 2.1/2.2** | Szeregowy, dwukierunkowy | 5 V DC | Dwukierunkowy | S120, SIMOTION, nowoczesne SINAMICS — wysoka dynamika |
| **HIPERFACE** | Sin/Cos + RS-485 | 7–12 V DC | Dwukierunkowy | Silniki Siemens 1FK7/1FT7 (classic) |
| **HIPERFACE DSL** | Cyfrowy, tylko 2 żyły | 5 V DC | Dwukierunkowy | V90 z 1FG/1FK7 — kabel enkodera = kabel mocy |

**Konfiguracja w SINAMICS Startdrive:**

| Parametr | Opis | Przykładowe wartości |
|----------|------|---------------------|
| `p0400` | Typ enkodera | 0=brak, 1=TTL/HTL inkr., 4=SSI, 9=EnDat 2.2, 11=HIPERFACE sin/cos |
| `p0404` | Liczba PPR (impulsy/obrót) | 1024, 2048, 4096, 8192 |
| `p0406` | Napięcie zasilania enkodera | 0=5V, 1=12V, 2=24V |
| `p0408` | Liczba bitów SSI | 10–30 bit |
| `p0418` | Współczynnik interpolacji sin/cos | 1024 lub 2048 |
| `p0431` | Korekta offsetu enkodera (fine adjust) | Wartość w impulsach |

**Konfiguracja Technology Object (TIA Portal Motion Control):**
1. TIA Portal → Technology objects → wybrany TO (`TO_PositioningAxis` lub `TO_ExternalEncoder`)
2. Zakładka `Encoder` → `Encoder type`: Incremental / Absolute
3. Ustaw: `Data exchange type` (np. PROFIdrive, analog sin/cos, HSC module)
4. `Encoder resolution`: podaj PPR lub ilość bitów
5. Dla `TO_ExternalEncoder`: wskaż moduł HSC (S7-1200) lub interfejs sieciowy enkodera (ET200S counting module)

**Wejście HSC (High Speed Counter) w S7-1200/S7-1500 dla enkoderów TTL/HTL:**
- S7-1200: wbudowane HSC (`HSC1–HSC6`) — max **100 kHz** na kanał; moduł SB 1221 High Speed zwiększa do **200 kHz**
- S7-1500T: moduł TM PosInput (6ES7138-6AA01) dla enkoderów sin/cos / TTL do 1 MHz

> ⚠️ **PROFINET enkoder z Technology Object:** telegram `102` (z enkoderem) wymaga że SINAMICS odbiera pozycję z wbudowanego enkodera przez Startdrive, następnie przesyła ją do CPU przez PROFINET jako część PZD telegramu. Telegramy `1` i `20` **nie zawierają** danych enkodera — tylko prędkość!

> 💡 **HIPERFACE DSL:** jeden kabel do serwosilnika zawiera jednocześnie zasilanie silnika (3 fazy + PE) i sygnał enkodera DSL — brak osobnego kabla enkodera. Stosowany w Sinamics V90 z silnikami 1FK7. Upraszcza montaż ale wymaga specjalnego kabla (Siemens Motion Connect 500).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 16.15. Czym są silniki IE5 (IPM / synchroniczne z magnesami trwałymi) i dlaczego zastępują klasyczne silniki indukcyjne w nowych projektach?  🟢

**Silniki IE5** *(Ultra-Premium Efficiency)* to silniki synchroniczne z magnesami trwałymi wbudowanymi w wirnik (IPM — Interior Permanent Magnet). Są najwyższą klasą sprawności według IEC 60034-30-1.

**Klasy sprawności silników (IEC 60034-30-1):**

| Klasa | Opis | Sprawność (4-bieg., 11 kW) |
|-------|------|---------------------------|
| IE1 | Standard | ~89% |
| IE2 | High Efficiency | ~91% |
| IE3 | Premium | ~92% |
| IE4 | Super Premium | ~94% |
| **IE5** | **Ultra Premium** | **≥ 96%** |

**Dlaczego IE5 / IPM zastępuje silnik indukcyjny klatkowy:**
- **Sprawność:** IE5 = ≥96% vs IE3 = ~92% → mniejszy pobór prądu, oszczędność energii
- **Regulator:** PMSM wymaga enkodera i wektorowego sterowania (FOC) — nie można go uruchomić przez prosty V/f; wymaga SINAMICS z silnikowym modułem
- **Wygląd:** silnik IE5 (np. SIMOTICS GP 1LA, seria 1PH PMSM) wygląda identycznie jak klasyczny silnik indukcyjny — tylko tabliczka znamionowa zdradza różnicę
- **Wymaganie unijne:** od 2023 roku w EU obowiązkowy IE3 dla silników ≥750W; nowe projekty kierują się w stronę IE4/IE5

**IE5 w praktyce commissioning:**
- Tabliczka znamionowa: `IPM` lub `PMSM` zamiast `IM` (Induction Motor)
- Parametryzacja napędu: `p0300 = 2` *(PMSM)* zamiast `p0300 = 1` *(IM)*
- Enkoder obowiązkowy (inkrementalny lub absolutny wbudowany) — nie ma pola magnetycznego wirnika bez magnesów = brak synchronizacji
- Identyfikacja silnika (p1910/p1960) przebiega inaczej niż dla IM — uwzględnia magnetyzację stałą magnesów

> ⚠️ **Najczęstszy błąd:** operator wymienia silnik IE3 (IM) na IE5 (IPM) i pozostawia `p0300 = 1` — napęd próbuje magnetyzować silnik synchroniczny jak indukcyjny → natychmiastowy fault lub zniszczenie uzwojeń.

> 💡 **Na rozmowie:** pytanie *"co zrobisz gdy dostajesz silnik który wygląda jak standardowy trójfazowy ale napęd nie chce się uruchomić?"* → sprawdź typ: `IM` vs `PMSM/IPM` na tabliczce → ustaw `p0300` odpowiednio.

*Źródło: transkrypcja ControlByte — przegląd silników w aplikacjach Motion Control*

---

