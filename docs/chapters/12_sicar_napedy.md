## 12. NAPĘDY SINAMICS

### 12.1. Co to jest SINAMICS Startdrive w TIA Portal?

**SINAMICS Startdrive** to wtyczka do TIA Portal do parametryzacji, uruchamiania i diagnostyki napędów SINAMICS (G120, S120, V90) bezpośrednio z TIA Portal — bez osobnego oprogramowania STARTER.

**Możliwości:**
- Konfiguracja napędu i autotuning
- Monitoring parametrów online
- Diagnostyka błędów (fault codes)
- Konfiguracja Safety Integrated (STO, SS1, SLS przez PROFIsafe)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 12.2. Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?  🟡

**Konfiguracja SINAMICS G120 z Safety (w SINAMICS Startdrive):**

1. Dodaj napęd G120 do projektu (`CU240E-2 PN` lub `CU250S-2 PN`) — ustaw adres PROFINET i telegram (`p0922`)
2. Zakładka `Safety Integrated` → włącz PROFIsafe, ustaw `F-Address`
3. Wybierz funkcje Safety: `STO`, `SS1` (`p9560` = ramp time ⚠️ DO WERYFIKACJI w SINAMICS G120 Safety Function Manual), `SLS` (`p9531` = max prędkość ⚠️ DO WERYFIKACJI)
4. Autotuning: Static motor identification → Speed controller optimization
5. Weryfikacja Safety: test STO → accept safety settings → Safety checksum/Safety ID

Po stronie F-CPU: blok Safety dla napędu (F-FB dla G120 z biblioteki) odbiera/wysyła telegram PROFIsafe.

> ⚠️ `F-Address` musi być **identyczny** w TIA Portal i na fizycznym napędzie — inaczej Safety nie uruchomi się.

> 💡 Pełna procedura krok po kroku: → Sekcja 19 *(Commissioning — Dodawanie napędu G120)*.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*

### 12.3. Z jakich komponentów składa się napęd SINAMICS G120 i jaką rolę pełni każdy z nich?

**SINAMICS G120** to modułowy przemiennik częstotliwości Siemens składający się z dwóch głównych komponentów: Control Unit (CU) i Power Module (PM), które dobieramy niezależnie.

- **Control Unit (CU)** — moduł sterujący odpowiedzialny za regulację napędu, komunikację sieciową (PROFINET/PROFIBUS) oraz realizację funkcji Safety Integrated. Warianty:
  - `CU240E-2` — podstawowa wersja z interfejsem Ethernet/PROFINET
  - `CU250S-2` — wersja z Safety Integrated (STO, SS1, SLS, SDI przez PROFIsafe) i wejściami/wyjściami Safety
- **Power Module (PM)** — moduł mocy zasilający silnik. Warianty obejmują PM240-2 (standardowy), PM230 (bez hamowania DC), PM250 (z wbudowanym hamowaniem regeneracyjnym)
- **Panel operatorski (opcja)** — BOP-2 (Basic Operator Panel — wyświetlacz segmentowy, ustawianie parametrów ręcznie), IOP-2 (Intelligent Operator Panel — graficzny wyświetlacz LCD, kopiowanie parametrów między napędami)
- **Karta pamięci SD** — na CU, przechowuje parametryzację napędu (backup/restore — wymiana CU bez ponownej parametryzacji)

**Praktyka commissioning:** Przy wymianie CU w terenie — karta SD z parametrami pozwala na szybką wymianę bez Startdrive. Wyjmij kartę ze starego CU → włóż w nowy → napęd startuje z zapisaną konfiguracją.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens, warianty CU/PM mogą się różnić w zależności od generacji*

### 12.4. Czym są telegramy PROFIdrive i jakie telegramy stosuje się w SINAMICS G120?

**PROFIdrive** to standard komunikacji napędów przez PROFINET/PROFIBUS, definiujący strukturę danych wymienianych cyklicznie między PLC a napędem. Wybór telegramu determinuje jakie dane sterujące i statusowe są przesyłane.

- **Telegram 1** — sterowanie prędkościowe podstawowe: słowo sterujące STW1 + zadana prędkość NSOLL_A → słowo statusowe ZSW1 + aktualna prędkość NIST_A. Najczęściej stosowany w prostych aplikacjach transporterów i wentylatorów
- **Telegram 20** — rozszerzony telegram prędkościowy z dodatkowymi słowami sterującymi (STW2) i procesowymi (PZD). Umożliwia przesyłanie dodatkowych parametrów (np. moment, prąd)
- **Telegram 352/353** — telegramy z danymi Safety (PROFIsafe) — dla CU250S-2 z Safety Integrated, łączy sterowanie standardowe z danymi failsafe
- **p0922** — parametr w napędzie, który określa numer aktywnego telegramu. Zmiana telegramu wymaga restartu napędu

**Słowo sterujące STW1 (Control Word)** — kluczowe bity:
- Bit 0: ON/OFF1 (włącz/wyłącz napęd z wyhamowaniem po rampie)
- Bit 1: OFF2 (wyłącz — wybieg naturalny)
- Bit 3: Enable operation (zezwolenie na pracę)
- Bit 7: Acknowledge fault (kasowanie błędu — zbocze narastające)

**Praktyka commissioning:** Po dodaniu G120 do projektu TIA Portal → w konfiguracji sprzętowej wybierz telegram (zakładka „Telegram configuration") → w programie PLC mapuj STW1/ZSW1 do odpowiednich adresów procesowych.

*[PRAWDOPODOBNE] — struktura telegramów zgodna z profilem PROFIdrive V4; numery telegramów Safety (352/353) ⚠️ DO WERYFIKACJI w dokumentacji SINAMICS G120*

### 12.5. Jak wygląda procedura pierwszego uruchomienia (commissioning) SINAMICS G120 przez Startdrive?

**Procedura pierwszego uruchomienia G120** w TIA Portal ze Startdrive obejmuje konfigurację podstawowych parametrów silnika, identyfikację i optymalizację regulatorów.

**Krok po kroku:**

1. **Dodaj napęd do projektu** — wstaw CU (np. CU240E-2 PN) z katalogu sprzętowego, przypisz adres PROFINET i nazwę urządzenia
2. **Konfiguracja silnika (dane z tabliczki znamionowej):**
   - Moc znamionowa, napięcie, prąd, częstotliwość, prędkość obrotowa — Startdrive prowadzi przez wizard „Motor data"
   - Tryb sterowania: V/f (skalarny — proste aplikacje) lub Vector (wektorowy — precyzyjna regulacja momentu)
3. **Identyfikacja silnika:**
   - „Stationary motor identification" — pomiar parametrów silnika bez obrotu wału (rezystancja, indukcyjność, stała czasowa). Bezpieczna — silnik się nie kręci
   - „Rotating motor identification" — pomiar z obrotem wału (momenty bezwładności, optymalizacja regulatora prędkości). Uwaga: silnik się obraca — odłącz mechanikę!
4. **Autotuning regulatorów** — na podstawie identyfikacji Startdrive proponuje nastawy regulatora prądowego i prędkościowego
5. **Test w trybie Jog** — ręczny obrót silnika z Startdrive (przycisk Jog w panelu commissioning) → weryfikacja kierunku obrotu, płynności pracy
6. **Download do napędu** — „Download to device" → parametry zapisywane w CU (EEPROM)

**Praktyka:** Zawsze wykonaj identyfikację silnika — bez niej regulator pracuje na parametrach domyślnych, co prowadzi do oscylacji, przegrzewania i faultów (np. overcurrent). Po identyfikacji napęd pracuje stabilnie od pierwszego startu.

*[PRAWDOPODOBNE] — procedura ogólna Startdrive commissioning wizard, nazwy parametrów mogą się różnić między wersjami Startdrive*

### 12.6. Czym różnią się napędy SINAMICS G120, S120 i V90 i kiedy stosuje się każdy z nich?

**Rodzina SINAMICS** obejmuje trzy główne serie napędów, dobierane w zależności od wymagań aplikacji: prostota (G120), wydajność wieloosiowa (S120) lub precyzja serwo (V90).

- **SINAMICS G120** — modułowy przemiennik częstotliwości do silników asynchronicznych. Zastosowanie: transportery, pompy, wentylatory, proste napędy w liniach produkcyjnych. Moc: 0,37 kW – 250 kW. Sterowanie: V/f lub wektorowe. Safety opcjonalnie (CU250S-2)
- **SINAMICS S120** — wieloosiowy system napędowy do wymagających aplikacji Motion Control. Architektura: wspólna szyna DC (Active/Smart Line Module) + pojedyncze Motor Modules dla każdej osi. Zastosowanie: maszyny wieloosiowe (CNC, pakowanie, handling), linie produkcyjne automotive. Pełna integracja Safety Integrated (STO, SS1, SS2, SOS, SLS, SDI, SBC). Wymaga CU310-2 PN lub CU320-2 PN
- **SINAMICS V90** — kompaktowy serwonapęd do prostych aplikacji pozycjonowania. Sterowanie: PTI (Pulse Train Input) lub PROFINET (telegram 1/2/3/102). Wbudowane STO (hardwired, dwukanałowe). Zastosowanie: małe maszyny, proste osie pozycjonujące, podajniki. Komisjonowanie przez V-Assistant (dedykowane narzędzie) lub Startdrive

**Kryterium wyboru na commissioning:**
| Kryterium | G120 | S120 | V90 |
|-----------|------|------|-----|
| Typ silnika | Asynchroniczny | Synchroniczny/Asynchroniczny | Serwo (1FL6) |
| Liczba osi | Jednoosiowy | Wieloosiowy (wspólna DC bus) | Jednoosiowy |
| Safety Integrated | Opcja (CU250S-2) | Pełna (CU310/320) | Tylko STO hardwired |
| Narzędzie | Startdrive | Startdrive/STARTER | V-Assistant/Startdrive |

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens i źródeł workspace (kb_S16, kb_S08)*

### 12.7. Jak wygląda diagnostyka napędu SINAMICS G120 — fault codes, ostrzeżenia i kasowanie błędów?

**Diagnostyka napędów SINAMICS** opiera się na kodach błędów (fault/alarm) wyświetlanych na BOP/IOP, w Startdrive online lub odczytywanych z PLC przez słowo statusowe ZSW1 i bufor diagnostyczny.

- **Fault (Fxxxx)** — błąd krytyczny, napęd zatrzymuje się. Wymaga usunięcia przyczyny i skasowania (acknowledge). Przykłady typowych faultów:
  - `F07011` — Motor blocked / zablokowany silnik (przeciążenie mechaniczne)
  - `F07801` — Motor overtemperature / przegrzanie silnika (KTY/PTC)
  - `F30001` — Power module overcurrent / przetężenie modułu mocy
  - `F30003` — DC-link overvoltage / przepięcie na szynie DC (hamowanie bez rezystora hamującego)
  - `F01000` — Internal software error (często po aktualizacji firmware — reset do factory)
  ⚠️ DO WERYFIKACJI — numery faultów mogą się różnić między generacjami firmware G120
- **Alarm (Axxxx)** — ostrzeżenie, napęd kontynuuje pracę. Np. `A07900` — motor overtemperature warning (zbliżanie się do limitu)
- **Kasowanie błędu z PLC** — zbocze narastające na bicie 7 słowa STW1 (Acknowledge fault). Z BOP: przytrzymanie przycisku `FN`
- **Bufor diagnostyczny** — Startdrive → „Diagnostics" → „Fault buffer" / „Alarm buffer" — historia ostatnich błędów z timestampem

**Praktyka commissioning:** Przy pierwszym uruchomieniu najczęstsze faultdy to: overcurrent (źle dobrana identyfikacja silnika), DC-link overvoltage (brak rezystora hamującego przy szybkim hamowaniu), motor overtemperature (niepodłączony czujnik PTC/KTY). Zawsze sprawdź fault buffer po pierwszym starcie — nawet jeśli napęd działa, mogły wystąpić alarmy.

*[PRAWDOPODOBNE] — typowe faultcodes SINAMICS, numery konkretnych faultów ⚠️ DO WERYFIKACJI w dokumentacji SINAMICS G120 Faults and Alarms*

### 12.8. Czym jest sterowanie wektorowe (Vector Control) vs skalarne (V/f) w SINAMICS G120 i kiedy stosujesz każdy tryb?

**Tryb sterowania** w napędzie SINAMICS G120 określa sposób regulacji prędkości/momentu silnika asynchronicznego. Wybór trybu wpływa na dynamikę, precyzję i zachowanie napędu.

- **V/f (skalarny)** — utrzymuje stały stosunek napięcia do częstotliwości. Prosty, nie wymaga identyfikacji silnika. Zastosowanie: proste aplikacje bez wymagań dynamicznych — pompy, wentylatory, transportery. Nie kontroluje momentu bezpośrednio
- **Vector (wektorowy, SLVC — Sensorless Vector Control)** — rozdziela prąd silnika na składową momentotwórczą i magnesującą, regulując moment niezależnie od prędkości. Wymaga identyfikacji silnika (motor identification). Zastosowanie: precyzyjna regulacja prędkości/momentu, aplikacje z dynamicznym obciążeniem (wciągarki, nawijarki, prasy)
- **Vector z enkoderem (VC — Vector Control with Encoder)** — jak SLVC, ale z enkodem na wale silnika — najlepsza precyzja. Pozwala na pełny moment przy 0 Hz (holding torque). Wymaga fizycznego enkodera i karty enkoderowej na CU

**Kiedy co wybrać:**
| Aspekt | V/f | SLVC | VC (z enkoderem) |
|--------|-----|------|-------------------|
| Precyzja prędkości | ±2-3% | ±0,5% | ±0,01% |
| Moment przy 0 Hz | Brak | Ograniczony | Pełny |
| Identyfikacja silnika | Nie wymagana | Wymagana | Wymagana |
| Koszt wdrożenia | Najniższy | Średni | Najwyższy |

**Praktyka commissioning:** Domyślny tryb przy dodaniu G120 do projektu to V/f. Jeśli aplikacja wymaga dynamiki (szybkie przyspieszanie/hamowanie, trzymanie pozycji) — przełącz na Vector i wykonaj identyfikację silnika. Bez identyfikacji tryb wektorowy generuje faultdy.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens, wartości precyzji są orientacyjne*

### 12.9. Czym różni się architektura SINAMICS S120 od G120 i jak wygląda jej konfiguracja w TIA Portal?

**SINAMICS S120** to wieloosiowy system napędowy z centralną szyną DC, przeznaczony do maszyn o wielu osiach (CNC, handling, automotive). W odróżnieniu od G120 (samodzielny napęd jednoosiowy), S120 składa się z wielu modułów współdzielących zasilanie.

- **Architektura S120:**
  - **Active/Smart Line Module (ALM/SLM)** — prostownik sieciowy zasilający wspólną szynę DC. ALM umożliwia zwrot energii do sieci (regeneracja), SLM jest prostszy (bez regeneracji)
  - **Motor Module (MM)** — falownik dla pojedynczej osi, zasilany z szyny DC. Jeden Motor Module na jedną oś/silnik
  - **Control Unit (CU310-2 PN / CU320-2 PN)** — sterownik napędu. CU310-2 steruje jedną osią, CU320-2 steruje wieloma osiami (do 6 Motor Modules). CU320-2 jest typowy dla aplikacji wieloosiowych
  - **Sensor Module (SMC/SME)** — moduł do podłączenia enkodera silnika
- **Konfiguracja w TIA Portal:**
  1. Wstaw Line Module + CU + Motor Modules z katalogu sprzętowego → automatycznie tworzą się połączenia po szynie DRIVE-CLiQ (wewnętrzna magistrala między modułami S120)
  2. Każdy Motor Module konfiguruj osobno: dane silnika, telegram PROFIdrive, identyfikacja
  3. Safety: każda oś S120 ma pełen zestaw Safety Integrated (STO, SS1, SS2, SOS, SLS, SDI, SBC) — konfiguracja przez PROFIsafe telegram (np. telegram 30/54/902)
- **Tryb izochroniczny** — S120 obsługuje synchronizację cyklu napędu z cyklem PROFINET IRT (Isochronous Real-Time), co jest wymagane w aplikacjach Motion Control z wieloma zsynchronizowanymi osiami

**Praktyka commissioning:** Przy S120 kluczowe jest DRIVE-CLiQ topology — fizyczne połączenie kablami DRIVE-CLiQ między CU, Motor Modules i Sensor Modules musi odpowiadać topologii w projekcie TIA Portal. Błędna topologia → napęd nie startuje i zgłasza fault.

> Źródło: SIMATIC Safety - Konfiguracja i programowanie (2), s. 62 — konfiguracja PROFIsafe telegram 902 dla SINAMICS S120 CU310-2 PN V5.1 w trybie izochronicznym [ZWERYFIKOWANE]

### 12.10. Jak wyglądają typowe scenariusze wymiany napędu SINAMICS G120 na obiekcie (service/replacement)?

**Wymiana napędu G120** na działającej linii produkcyjnej to częsta procedura serwisowa. Kluczowe jest szybkie przywrócenie pracy bez ponownej pełnej parametryzacji.

**Scenariusz 1 — Wymiana Power Module (PM) przy sprawnym CU:**
1. Odłącz zasilanie → wymień PM na identyczny typ
2. CU rozpoznaje nowy PM automatycznie → parametryzacja pozostaje w CU
3. Włącz zasilanie → napęd powinien wystartować bez zmian. Jeśli PM jest innego typu → fault incompatibility

**Scenariusz 2 — Wymiana Control Unit (CU) z kartą SD:**
1. Wyjmij kartę SD ze starego CU → włóż w nowy CU tego samego typu
2. Przy starcie nowy CU ładuje parametry z karty SD automatycznie
3. Ustaw nazwę PROFINET i adres IP identycznie jak poprzedni CU (przez Startdrive online lub BOP)
4. Weryfikacja: Startdrive online → porównaj parametry → test Jog

**Scenariusz 3 — Wymiana CU bez karty SD (brak backupu):**
1. Skonfiguruj napęd od zera w Startdrive (wizard commissioning)
2. Jeśli masz backup projektu TIA Portal → „Download to device" przywraca pełną konfigurację
3. Jeśli nie masz backupu → ręczna parametryzacja z dokumentacji maszyny + identyfikacja silnika

**Praktyka commissioning:** ZAWSZE rób backup parametrów na kartę SD po komisjonowaniu. Na każdej linii powinien być dostępny backup projektu TIA Portal z aktualną konfiguracją napędów. Brak backupu + padnięty CU = wielogodzinny przestój.

*[PRAWDOPODOBNE] — procedura standardowa wymiany SINAMICS G120, zgodna z praktyką serwisową*
