## 1. PODSTAWY PLC I AUTOMATYKI

### 1.1. Co to jest PLC i czym różni się od zwykłego komputera?  🔴

PLC (Programmable Logic Controller) to przemysłowy komputer czasu rzeczywistego do sterowania maszynami. Kluczowe różnice:
- Deterministyczny scan cycle — program wykonywany cyklicznie z przewidywalnym czasem (ms)
- Odporność na EMI, drgania, temperatury, wilgoć przemysłową
- Dedykowane moduły I/O (DI, DO, AI, AO) bezpośrednio do czujników i aktuatorów
- Watchdog timer — CPU restartuje się przy zawieszeniu zamiast „wisieć"
- Brak systemu plików jak Windows — działa natychmiast po włączeniu zasilania

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.2. Co to jest scan cycle i ile trwa?  🔴

Scan cycle to jeden pełny cykl pracy CPU: odczyt wejść → wykonanie programu → zapis wyjść → komunikacja.
Typowy czas: 1–20ms dla prostych programów. Przy dużych projektach lub Safety może wzrosnąć do 50–100ms.
W S7-1500 monitorujesz czas cyklu online (Cycle time w diagnostyce CPU). Zbyt długi scan = wolna reakcja na sygnały.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.3. Co to jest OB1, OB35, OB100 — kiedy każdego używasz?

Bloki organizacyjne (OB) to punkt wejścia do programu wywoływany przez system operacyjny CPU w ściśle określonych warunkach.

**Podstawowe OB:**
- OB1 — główny cykl programu, wykonywany ciągle. Tutaj trafia główna logika maszyny. Przerwany przez OB o wyższym priorytecie.
- OB35 — przerwanie cykliczne (np. co 100ms). Używasz dla PID, komunikacji z napędami, obliczeń niezależnych od obciążenia OB1. Wyższy priorytet niż OB1.
- OB100 — zimny start (Startup OB), wykonywany raz po przejściu CPU z STOP→RUN. Inicjalizacja zmiennych, reset stanu maszyny, wyzerowanie wyjść. W TIA Portal S7-1200/1500: jedyny OB startu (nie ma OB101/OB102 jak w starym S7-300).
- F_MAIN — Safety OB, oddzielny cykl dla programu failsafe, chroniony przez F-CPU.

**Diagnostyczne OB — ważne przy commissioning:**
- OB80 — cycle time exceeded (czas cyklu przekroczył watchdog). Sygnalizuje zbyt wolną logikę.
- OB82 — diagnostic error: moduł I/O zgłosił błąd diagnostyczny (np. zerwanie kabla, przegrzanie modułu F). W TIA Portal: blok RALRM lub ProDiag odbiera dane.
- OB86 — rack failure / PROFINET station failure. Wywołany gdy zdalna stacja (ET200SP, napęd) znika z sieci.
- OB121 / OB122 — błędy programistyczne (np. dostęp do nieistniejącej zmiennej) — ważne przy uruchamianiu nowego kodu.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.4. Co to jest FB, FC, DB — kiedy używasz każdego?  🔴
- FC (Function) — blok bez pamięci własnej (brak sekcji VAR_STAT). Używasz dla prostych obliczeń, konwersji sygnałów, logiki bez stanu. Może zwracać wartość (Return Value). Ma tylko VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT i VAR_TEMP.
- FB (Function Block) — ma instancję DB z pamięcią stanu między wywołaniami (sekcja VAR_STAT). Używasz dla sterowania silnikiem, sekwencji, timerów — wszędzie gdzie blok musi "pamiętać". Multi-instance: jeden FB może zawierać instancje innych FB bez osobnych DB.
- DB (Data Block) — blok danych. Globalny DB: dostęp z całego programu. Instancja DB: dedykowana pamięć jednego FB.

**Typy zmiennych w blokach (ważne rozróżnienie):**
- `VAR_TEMP` — tymczasowe, przechowywane na stosie CPU. Tracą wartość po zakończeniu wywołania. Dostępne we wszystkich blokach (FB, FC, OB).
- `VAR_STAT` — statyczne, zachowują wartość między wywołaniami. Tylko w FB, przechowywane w instancji DB.
- `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` — parametry interfejsu bloku.

W TIA Portal: bloki z włączonym *Optimized Block Access* używają wyłącznie nazw symbolicznych — brak adresowania absolutnego (%.0, %DB1.DBX0.0). Standardowe ustawienie dla nowych projektów.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.5. Co to jest UDT i po co go używasz?

UDT (User Data Type) to własny złożony typ danych definiowany raz i wielokrotnie używany w całym projekcie. Przykład: typ `Motor_t` z polami `Speed:REAL`, `Current:REAL`, `Fault:BOOL`, `Running:BOOL`.

**Kiedy używasz UDT:**
- Masz wiele identycznych urządzeń (np. 20 silników) — definiujesz FB jeden raz z parametrem `VAR_IN_OUT: Motor_t`, tworzysz 20 instancji. Zmiana struktury UDT → automatyczna propagacja do wszystkich instancji.
- Chcesz wymusić spójną strukturę danych między PLC, HMI i DB.
- Przekazujesz zestaw powiązanych danych jako jeden parametr `VAR_IN_OUT`.

**UDT vs STRUCT:**
- `STRUCT` to typ anonimowy (inline) — definiujesz go bezpośrednio w bloku, bez nazwy globalnej, nie możesz go reużyć w innych blokach.
- `UDT` ma nazwę globalną (np. `"Motor_t"`) — reużywany w całym projekcie i w Project Library.

**Wersjonowanie:** W TIA Portal można przypisać UDT do Project Library i wersjonować. Przy zmianie struktury UDT TIA Portal ostrzega o niespójnych instancjach — musisz je zaktualizować (`Update instances`). Ważne w dużych projektach — jedna zmiana UDT bez aktualizacji instancji = błąd kompilacji.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.6. Co to są języki programowania PLC — LAD, FBD, SCL, GRAPH?
- LAD (Ladder) — graficzny, podobny do schematów przekaźnikowych. Dobry dla logiki binarnej, łatwy dla elektryków. Najczęściej używany.
- FBD (Function Block Diagram) — bloki połączone liniami. Dobry dla logiki kombinacyjnej i programów Safety w TIA Portal.
- SCL (Structured Control Language) — tekstowy, składnia podobna do Pascala (wysokopoziomowy). Używasz dla algorytmów, pętli, obliczeń matematycznych, obsługi tablic, przetwarzania STRING.
- GRAPH (SFC) — sekwencyjny, kroki i przejścia. Idealny dla sekwencji technologicznych (napełnianie, obróbka, mycie). Certyfikowany wg IEC 61131-3.
- STL (Statement List) — niskopoziomowy, lista instrukcji podobna do asemblera. Dostępny w TIA Portal ale uznawany za przestarzały — nie stosuj w nowych projektach.

**Kluczowe konstrukcje SCL w TIA Portal:**
```
IF warunek THEN        // instrukcja warunkowa
  ...
ELSIF warunek2 THEN    // opcjonalne
  ...
ELSE
  ...
END_IF;

FOR i := 1 TO 10 DO    // pętla zliczająca
  array[i] := 0;
END_FOR;

WHILE warunek DO       // pętla warunkowa
  ...
END_WHILE;

CASE zmienna OF        // instrukcja wyboru
  1: akcja1;
  2: akcja2;
  ELSE: domyslna;
END_CASE;
```

**TIA Portal SCL vs klasyczny STEP 7 SCL:**
- TIA Portal: zmienne wyłącznie symboliczne, brak tablicy symboli (Symbol Table), *Optimized Block Access* domyślnie włączony.
- Stary STEP 7 (S7-300/400): mieszanie adresów absolutnych (I0.0, DB1.DBX0.0) i nazw symbolicznych; osobna tablica symboli.
- W Safety: program F_MAIN w TIA Portal **V18 i starszych** wymaga FBD lub LAD — SCL nie jest certyfikowany dla F-bloków Safety. Od TIA Portal **V19** SCL jest obsługiwany jako język F-bloków Safety. Zawsze sprawdź dopuszczalne języki dla swojej wersji portalu przed użyciem SCL w logice Safety.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.7. Co to jest sygnał 4-20mA i dlaczego nie 0-20mA?

4-20mA to standardowy sygnał analogowy dla czujników przemysłowych. Zakres 4mA (min) do 20mA (max).
Dlaczego 4 a nie 0: sygnał 0mA jednoznacznie oznacza zerwanie kabla lub awarię zasilania czujnika — łatwa diagnostyka. Przy 0-20mA nie da się odróżnić minimalnej wartości od awarii.
Sygnał prądowy ma też przewagę nad napięciowym (0-10V): nie spada na rezystancji kabla — można przesyłać na duże odległości bez strat.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.8. Co to jest PROFINET i czym różni się od PROFIBUS?  🔴

PROFINET: Ethernet-based, 100Mbit/s (gigabit w nowych instalacjach), elastyczna topologia (gwiazdka, linia, pierścień), plug-and-play z GSDML, obsługuje PROFIsafe i IRT (250µs, jitter <1µs). Nowy standard dla wszystkich nowych projektów.
PROFIBUS: RS-485, max 12Mbit/s, liniowa topologia z terminatorami na obu końcach kabla, starszy standard. Nadal spotykany w modernizacjach i instalacjach sprzed 2010.

**Role urządzeń PROFINET — kluczowe na rozmowie:**
- **IO-Controller**: sterownik nadrzędny zarządzający cyklem wymiany danych — to jest CPU (np. S7-1500F). Jeden IO-Controller obsługuje do 512 IO-Devices (S7-1500).
- **IO-Device**: urządzenie peryferyjne oddające/przyjmujące dane — ET200SP, ET200MP, SINAMICS G120, robot ABB IRC5, kurtyna PROFINET. Każde opisane przez plik GSDML.
- **IO-Supervisor**: urządzenie diagnostyczne i konfiguracyjne (laptop z TIA Portal, panel HMI) — odczytuje dane, nie uczestniczy w cyklu produkcyjnym.

Jeden CPU może być jednocześnie IO-Controller swojej sieci i IO-Device w sieci nadrzędnej (np. S7-1500 jako slave do głównego systemu SCADA).

PROFIBUS analogicznie: DP-Master Class 1 (CPU) → DP-Slave (ET200M/S, napęd z CB DP) → DP-Master Class 2 (PG/PC diagnostyczny).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.9. Jakie są główne rodziny sterowników PLC Siemens i do jakich zastosowań są dedykowane?

Siemens oferuje różne rodziny sterowników PLC, dostosowane do aplikacji o różnej skali i złożoności, od prostych zadań po najbardziej wymagające systemy.
- **LOGO!**: Najmniejszy sterownik, nazywany przekaźnikiem programowalnym lub modułem logicznym.
  - **Zastosowanie:** Proste maszyny, nieskomplikowana automatyka procesowa (przepompownie, oczyszczalnie), automatyka budynkowa.
  - **Możliwości:** Możliwość rozszerzania o wejścia/wyjścia cyfrowe i analogowe, ale nie do zaawansowanych aplikacji napędowych czy kompletnych regulatorów PID.
- **S7-1200**: Kompaktowe sterowniki ze zintegrowanymi wejściami i wyjściami.
  - **Zastosowanie:** Małe i średnie aplikacje, łączące dobrą wydajność z niską ceną.
  - **Możliwości:** Modułowa konstrukcja, port PROFINET, płytka sygnałowa, moduły rozszerzeń DI/DO/AI/AO, moduły technologiczne (np. wagowe), moduły komunikacyjne (RS232, RS485, PROFIBUS, AS-i, IO-Link, GSM), wbudowane szybkie wejścia/wyjścia (do enkoderów, silników krokowych/serwo), wersje failsafe.
- **S7-1500**: Dedykowane do najbardziej wymagających aplikacji.
  - **Zastosowanie:** Charakteryzują się największą mocą obliczeniową, zaawansowanymi funkcjami technologicznymi i komunikacyjnymi.
Praktyczne wskazówki:
- Dla początkujących w programowaniu PLC, S7-1200 jest polecany ze względu na niższą cenę. Po opanowaniu S7-1200, przejście na S7-1500 nie powinno stanowić problemu.
- Sterowniki S7-1200 posiadają wbudowany serwer WWW do diagnostyki i wyświetlania własnych stron.
*Źródło: transkrypcje ControlByte*

### 1.10. Jakie są kluczowe aspekty pamięci sterownika PLC Siemens S7-1200/1500?

Pamięć sterownika PLC jest podzielona na obszary o różnych właściwościach, co pozwala na efektywne zarządzanie programem i danymi, uwzględniając trwałość i szybkość dostępu.
- **Pamięć ładowania (Load Memory):**
  - **Typ:** Pamięć trwała (nieulotna), np. karta pamięci typu Flash lub wbudowana kość pamięci (S7-1200).
  - **Zawartość:** Skompilowane bloki programowe (kod maszynowy), bloki danych, konfiguracja sprzętowa.
  - **Działanie:** Dane są kopiowane z pamięci ładowania do pamięci roboczej podczas fazy startupu sterownika.
- **Pamięć robocza (Work Memory):**
  - **Typ:** Pamięć ulotna (RAM).
  - **Działanie:** Sterownik wykonuje większość działań w tym obszarze. Dane są tracone po zdjęciu zasilania.
- **Pamięć systemowa:**
  - **Typ:** Część pamięci roboczej.
  - **Zawartość:** Pamięć bitowa M (zmienne z tablicy tagów), timery i liczniki systemowe, lokalna pamięć tymczasowa L (zmienne tymczasowe), aktualny obraz procesu wejść i wyjść.
- **Pamięć Retentive (nieulotna):**
  - **Typ:** Specjalny obszar pamięci nieulotnej w sterowniku.
  - **Działanie:** W przypadku utraty zasilania, sterownik przez chwilę podtrzymuje pracę i przepisuje część danych z pamięci roboczej do pamięci Retentive, co pozwala na zachowanie wybranych danych (np. parametry, aktualny stan maszyny).
Praktyczne wskazówki:
- Ważne jest, aby świadomie decydować, które dane mają być retentywne, aby zachować stan maszyny po zaniku zasilania.
- Ograniczona żywotność pamięci trwałej i długi czas zapisu/odczytu sprawiają, że pamięć RAM jest preferowana do bieżących operacji.
*Źródło: transkrypcje ControlByte*

### 1.11. Jakie są warianty CPU S7-1200 i jakie mają możliwości rozbudowy?

Rodzina S7-1200 to kompaktowe sterowniki montowane na szynie DIN, programowane w TIA Portal. Wiedza o limitach rozbudowy jest ważna przy doborze do projektu.

**Warianty CPU S7-1200:**
| CPU | Wbudowane I/O | Max SM (prawo) | Max CM (lewo) | SB (front) | Uwagi |
|-----|---------------|---------------|--------------|------------|-------|
| 1211C | 6DI/4DO/2AI | brak | 3 | 1 | Brak rozbudowy SM |
| 1212C | 8DI/6DO/2AI | 2 SM | 3 | 1 | |
| 1214C | 14DI/10DO/2AI | 8 SM | 3 | 1 | Najpopularniejszy |
| 1215C | 14DI/10DO/2AI | 8 SM | 3 | 1 | 2 porty PROFINET |
| 1217C | 14DI/10DO/4AI | 8 SM | 3 | 1 | PTO4 (4 osie krokowe) |

**Typy modułów rozszerzeń:**
- **SM (Signal Module)** — z prawej: DI, DO, DI/DO, AI, AO — maksymalnie 8 sztuk.
- **CM (Comm Module)** — z lewej: RS232, RS485, PROFIBUS DP, AS-i, IO-Link master, GSM/GPRS.
- **SB (Signal Board)** — na froncie CPU: 2DI+2DO, AI, lub RS485 bez zajmowania slotu SM.

**Karta pamięci:** Micro SD pre-formatowana przez Siemens (nie zwykły consumer SD). Rola: backup programu, aktualizacja firmware, "Transfer Card" (wgranie programu na nowy CPU bez laptopa — wystarczy karta).

**Praktyczne limity:** Przy wielu modułach analogowych sumuj pobór prądu 5V z szyny wewnętrznej — max ~1A. Przekroczenie = moduły niestabilnie działają lub nie startują.

*Źródło: dane katalogowe Siemens S7-1200 System Manual*

### 1.12. Co to jest HMI i do czego służy w automatyce?

HMI (Human-Machine Interface) to panel operatorski umożliwiający wizualizację procesu, sterowanie, podgląd alarmów i trendów. Wyświetla: stany I/O, alarmy, trendy (wykresy wartości analogowych w czasie), tryby pracy maszyny, parametry produkcji.

**Typy panelów Siemens:**
- **Basic Panel (KTP400/700/900/1200 Basic)**: dotykowy lub klawiaturowy, WinCC Basic, od 4” do 12”. Brak trendów i receptur w wersji Basic. Dla prostych wizualizacji jednej maszyny.
- **Comfort Panel (TP700/900/1200/1500 Comfort)**: WinCC Advanced, pełne trendy, receptury, JavaScript, karty CF/SD. Standard dla maszyn produkcyjnych.
- **Mobile Panel (KTP700 Mobile)**: kabel lub WiFi. Homologowany dla stref Safety — posiada enabling device (przycisk potwierdzenia do trzymania przy wejściu do strefy niebezpiecznej).
- **PC-based / IPC (WinCC Unified)**: nowy standard Siemens, HTML5/SVG, OPC UA, skrypty TypeScript. Nie wymaga klasycznych wtyczek. Zastępuje WinCC RT Advanced w nowych instalacjach.

**Komunikacja:** HMI komunikuje się z PLC przez PROFINET (S7 protocol lub OPC UA) w TIA Portal — wspólna baza tagów synchronizowana automatycznie. Offline = HMI nie potrzebuje PLC do symulacji interfejsu (PLCSIM).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.13. Co to jest SCADA i czym różni się od HMI?

HMI: lokalne, przy maszynie, obsługuje jeden obiekt/maszynę, czas reakcji wymagany (operator).
SCADA (Supervisory Control and Data Acquisition): system nadrzędny, monitoruje i archiwizuje dane z wielu maszyn/stacji jednocześnie, na serwerze z komputerami PC. Nie steruje bezpośrednio w czasie rzeczywistym — nadzoruje, raportuje, alarmuje.

**Architektura Siemens WinCC:**
- **WinCC Basic / Advanced**: dla HMI panelów kompilowanych w TIA Portal — nie SCADA, obsługują do kilku sterowników.
- **WinCC V7.x (SCADA)**: osobne oprogramowanie, serwer OPC DA/UA, historian (archiwum trendów), redundantny serwer Hot Standby (przełączenie <1s), thin clients (Web Navigator przez przeglądarkę), receptury, raporty.
- **WinCC Unified**: nowy standard oparty na HTML5/SVG/OPC UA, web client bez wtyczek, skrypty TypeScript. Zastępuje WinCC V7 w nowych instalacjach.
- **WinCC Open Architecture (WinCC OA)**: dla najwyzszych wymagań (100k+ tagów, >100 klientów) — energetyka, infrastruktura.

**Pytanie kontrolne:** *Ile tagów obsługuje WinCC?* — WinCC V7 Comfort: 512 tagów; Professional: 512–unlimited (licencja). WinCC Unified: oparty na połączeniach OPC UA — brak jednej liczby. Nie podawaj liczby bez kontekstu wersji licencji.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.14. Co to jest PID i kiedy go używasz w PLC?

PID (Proportional-Integral-Derivative) to algorytm regulacji zamkniętej utrzymujący zadany setpoint: temperatura, ciśnienie, poziom, prędkość.
- P — reaguje proporcjonalnie do aktualnego błędu
- I — eliminuje uchyb ustalony (sumuje błąd w czasie)
- D — reaguje na szybkość zmiany błędu (tłumi oscylacje)
W TIA Portal: gotowy blok PID_Compact lub PID_3Step w OB35 (cykliczne przerwanie). W Safety PID nie jest stosowany — logika Safety jest binarna.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.15. Czym jest enkoder i jaka jest różnica między inkrementalnym a absolutnym?  🟡

**Enkoder** (przetwornik obrotowo-impulsowy) to czujnik zamieniający ruch mechaniczny (kąt/pozycję) na sygnał elektryczny odczytywany przez napęd lub PLC.

| Cecha | Inkrementalny | Absolutny |
|-------|---------------|-----------|
| **Sygnał wyjściowy** | Impulsy zliczane od punktu startowego | Unikalna wartość liczbowa = aktualna pozycja |
| **Po zaniku zasilania** | Traci pozycję — wymaga referencjonowania (homing) | Zachowuje pozycję *(absolutny)* |
| **Homing (referencja)** | Wymagany po każdym starcie | Nie wymagany *(single-turn)* lub nie wymagany *(multi-turn)* |
| **Interfejsy** | TTL (A/B/Z), HTL, sin/cos 1 Vpp | SSI, EnDat 2.1/2.2, HIPERFACE, HIPERFACE DSL |
| **Rozdzielczość** | 100 – 65 536 imp/obrót (PPR) | 12 – 25 bit/obrót |
| **Koszt** | Niższy | Wyższy |
| **Zastosowanie** | Przenośniki, wentylatory, proste osie | Roboty, osie pionowe, serwosystemy |

**Single-turn vs Multi-turn (absolutne):**
- **Single-turn:** unikalny kod dla 1 pełnego obrotu (0°–360°). Po przekręceniu o >1 obrót — traci pozycję absolutną.
- **Multi-turn:** dodatkowy mechanizm (getriebe optyczny lub zasilanie bateryjne) liczy pełne obroty. Np. 17 bit (131 072 poz/obrót) + 12 bit multi-turn (4096 obrotów) = ponad 536 mln unikalnych pozycji.

> ⚠️ **Osie pionowe i roboty:** zawsze absolutny enkoder multi-turn — po zaniku zasilania maszyna wie dokładnie gdzie jest ramię bez potrzeby homing. Inkrementalny = homing po każdym resecie = niebezpieczne przy obciążeniu.

> 💡 **Na rozmowie:** pytanie o enkodery często pojawia się razem z SLS/SDI — wspomnij że do tych funkcji Safety wymagane są enkodery certyfikowane (HIPERFACE Safety, EnDat Safety).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.16. Co to jest IO-Link i jakie korzyści daje względem klasycznych wejść analogowych PLC?  🟡

**IO-Link** (IEC 61131-9) to standardowy niskonapięciowy protokół komunikacji punkt-punkt między sterownikiem PLC (IO-Link Master) a inteligentnymi czujnikami/aktuatorami (IO-Link Device). Działa po standardowym 3-żyłowym kablu M12 — bez dodatkowego okablowania.

**Architektura:**
- **IO-Link Master** — moduł montowany w stacji ET200SP/ET200MP lub jako standalone (np. `6ES7148-6JA00-0AB0`). Jeden master obsługuje do 8 portów IO-Link.
- **IO-Link Device** — czujnik/zawór/kolumna świetlna z interfejsem IO-Link (producenci: Balluff, SICK, IFM, Turck, Pepperl+Fuchs).
- **IODD** *(IO Device Description)* — plik XML opisujący device, importowany do TIA Portal (analogia do GSDML dla PROFINET).

**Korzyści vs analogowe 4–20 mA / 0–10 V:**

| Cecha | Analogowe AI | IO-Link |
|-------|-------------|----------|
| Dane procesowe | 1 wartość (realna) | Wiele parametrów jednocześnie (pozycja, temp., błędy) |
| Konfiguracja czujnika | Fizycznie (trymer, DIP) | Zdalnie przez TIA Portal lub parametryzacja z DB |
| Diagnostyka | Brak | Pełna (kod błędu, temperatura, licznik cykli) |
| Okablowanie | 4 żyły + ekran | Standardowy kabel M12 3-żyłowy |
| Wymiana czujnika | Ręczna rekalibracja | Auto re-parametryzacja z DB (Data Storage mode) |
| Koszt na przekrój | Niższy | Wyższy dla mastera, niższy per czujnik |

**Tryб Data Storage (automatyczna reparametryzacja):**
Po wymianie uszkodzonego czujnika IO-Link Master automatycznie wgrywa zapisane parametry do nowego urządzenia — bez interwencji serwisanta. TIA Portal → właściwości portu IO-Link → `Data Storage: On`.

**Typowe zastosowania w automotive:**
- Czujniki pozycji z identyfikacją narzędzi (numer seryjny toolingu czytany z IO-Link)
- Kolumny świetlne z parametryzacją kolorów i wzorów przez PLC
- Zawory pneumatyczne z diagnostyką licznika zadziałań

> 💡 **IO-Link ≠ Safety** — standard IO-Link nie jest Safety-certified. Do zastosowań Safety wymagane są osobne kanały F-DI. IO-Link służy wyłącznie do danych procesowych i diagnostyki (standard world).

*Źródło: Siemens ET200SP IO-Link Master product documentation*

### 1.17. Co to jest przerzutnik SR i RS w TIA Portal i jaka jest różnica w priorytecie?  🟢

**Przerzutniki bistabilne SR i RS** to elementy PLC zapamiętujące stan (bit) po zaniku sygnału sterującego. Różnią się zachowaniem gdy **S i R są aktywne jednocześnie** — wtedy priorytet decyduje o stanie wyjścia.

**SR — priorytet Set (Set dominant):**
- Wyjście `Q` ustawia sygnał `S` (Set), kasuje sygnał `R1` (Reset)
- Gdy `S=1` i `R1=1` jednocześnie → `Q = 1` (Set wygrywa)
- Stosowany gdy **ważniejsze jest uruchomienie** niż zatrzymanie (np. zapłon palnika — jeśli coś każe zapalić, to zapala)

**RS — priorytet Reset (Reset dominant):**
- Wyjście `Q` ustawia sygnał `S1` (Set), kasuje sygnał `R` (Reset)
- Gdy `S1=1` i `R=1` jednocześnie → `Q = 0` (Reset wygrywa)
- Stosowany gdy **ważniejsze jest zatrzymanie** niż uruchomienie (np. blokada silnika przez warunek bezpieczeństwa — safety beat start)

**LAD w TIA Portal — wizualnie:**

![SR vs RS w TIA Portal LAD](images/safety/sr_rs_tia_portal.png)

**Równoważny kod SCL — implementacja ręczna:**

```scl
// SR — priorytet Set (kolejność: najpierw Reset, potem Set nadpisuje)
"MotorRunSR" := "MotorRunSR" OR "StartBtn";
IF "StopBtn" THEN "MotorRunSR" := FALSE; END_IF;
IF "StartBtn" THEN "MotorRunSR" := TRUE; END_IF;   // Set na końcu = priorytet

// RS — priorytet Reset (kolejność: najpierw Set, potem Reset nadpisuje)
"MotorRunRS" := "MotorRunRS" OR "StartBtn";
IF "StartBtn" THEN "MotorRunRS" := TRUE; END_IF;
IF "StopBtn" THEN "MotorRunRS" := FALSE; END_IF;    // Reset na końcu = priorytet
```

**Praktyczna zasada doboru:**

| Sytuacja | Wybór |
|----------|-------|
| Stop ma wyższy priorytet (99% maszyn przemysłowych) | **RS** |
| Start/Set ważniejszy (np. latch alarmu do potwierdzenia) | **SR** |
| Fizyczny E-Stop / Guard | Zawsze **RS** — Reset (bezpieczeństwo) dominuje |

> ⚠️ W TIA Portal LAD bloki SR/RS są dostępne w *Basic Instructions → Bistable operations*. Parametr `Q` to bit zapamiętany — musi być adres **Memory** (`M`) lub **DB bit**, nigdy wejście `I`.

*Źródło: TIA Portal Help — LAD Bistable Operations; IEC 61131-3 §3.2.3*


---

### 1.18. Czym różni się Dominacja SET od Dominacji RESET w układzie samopodtrzymania LAD?  🔴

**Dominacja** określa, który sygnał wygrywa gdy jednocześnie wciśniemy START i STOP. Jest to praktyczny odpowiednik priorytetu przerzutnika SR/RS, widoczny bezpośrednio w schemacie drabinkowym.

**Dominacja SET** (lewy obwód) — priorytet ma START:
- START steruje Lampką **bezpośrednio** (równolegle z samopodtrzymaniem przez Lampkę)
- STOP jest szeregowy z samopodtrzymaniem, ale gdy START=1 — omija STOP
- Gdy `START=1` i `STOP=1` jednocześnie → **Lampka = 1** (SET wygrywa)
- „START bezpośrednio steruje Lampką, dlatego STOP nie ma tutaj nic do gadania"

**Dominacja RESET** (prawy obwód) — priorytet ma STOP:
- START zasila Lampkę **przez** STOP (szeregowo w tej samej gałęzi)
- Gdy `START=1` i `STOP=1` jednocześnie → **Lampka = 0** (RESET wygrywa — STOP odcina zasilanie)
- „START zasila Lampkę poprzez STOP, dlatego przycisk wyłączenia jest ważniejszy"

![Dominacja SET vs RESET — porównanie obwodów LAD](images/safety/dominacja_set_reset_lad.png)

**Tabele prawdy — zachowanie Lampki:**

![Tabele prawdy Dominacja SET i RESET](images/safety/dominacja_set_reset_tabela.png)

| Stan | START | STOP | Lampka (Dominacja SET) | Lampka (Dominacja RESET) |
|------|-------|------|------------------------|--------------------------|
| Oba wciśnięte | 1 | 1 | **1** ← SET wygrywa | **0** ← RESET wygrywa |
| Tylko START | 1 | 0 | 1 | 1 |
| Tylko STOP | 0 | 1 | 0 | 0 |
| Żaden | 0 | 0 | * (stan poprzedni) | * (stan poprzedni) |

> Gwiazdka „*" oznacza stan zapamiętany — bez akcji na wejściach układ nie zmienia stanu (samopodtrzymanie działa).

**Związek z przerzutnikami bistabilnymi w TIA Portal:**

| Schemat LAD (ręczny) | Odpowiednik bloku TIA Portal |
|----------------------|------------------------------|
| Dominacja SET | Blok **SR** — Set-Dominant (S wygrywa) |
| Dominacja RESET | Blok **RS** — Reset-Dominant (R wygrywa) |

**Zasada projektowania bezpiecznych maszyn:** Zawsze stosuj **Dominację RESET** dla obwodów STOP i E-Stop. Operator musi mieć gwarancję, że wciśnięcie przycisku wyłączenia zatrzyma maszynę niezależnie od innych sygnałów (EN 60204-1 §9.2.2).

*Źródło: Kurs ControlByte — Układy samopodtrzymania, Dominacja SET/RESET; EN 60204-1 §9.2.2*


---

### 1.19. Jaką typową pułapkę w obwodzie samopodtrzymania LAD pokazuje zadanie „Znajdź różnice"?  🔴

**Pułapka samopodtrzymania** polega na błędnym umieszczeniu styku samopodtrzymania (Lampka) tak, że **omija on przycisk STOP** — wciśnięcie STOP nie wyłącza cewki, bo prąd płynie alternatywną ścieżką.

**Obwód LEWOSTRONNY — poprawny (Dominacja RESET):**
```
BARIERA_MAGISTRALI
+--[ START ]--+----[ /STOP ]----(  Lampka  )
              |
+--[ Lampka ]-+
```
- Styk `Lampka` (samopodtrzymanie) jest w gałęzi **równoległej do START** — przed STOP
- STOP jest **szeregowy z oboma ścieżkami** (START i samopodtrzymaniem)
- Wciśnięcie STOP → otwiera jedyną drogę do cewki → Lampka **gaśnie** ✅

**Obwód PRAWOSTRONNY — niepoprawny (STOP omijany):**
```
+--[ START ]--[ /STOP ]---(  Lampka  )
|                              |
+--------[ Lampka ]------------+
```
- Styk `Lampka` (samopodtrzymanie) jest w gałęzi **równoległej do całego szeregu START–STOP**
- Gdy Lampka=1 i operator wciśnie STOP: prąd nadal płynie dolną ścieżką przez `Lampka` → cewka **nadal zasilona** ❌
- STOP jest **bezużyteczny** gdy Lampka jest już włączona

**Tabela porównawcza:**

| Stan | STOP wciśnięty | Obwód LEWY (poprawny) | Obwód PRAWY (błędny) |
|------|----------------|----------------------|----------------------|
| Lampka=1 | TAK | Lampka → 0 ✅ | Lampka → **1** ❌ |
| Lampka=0 | TAK | Lampka → 0 ✅ | Lampka → 0 ✅ |
| START=1 | NIE | Lampka → 1 | Lampka → 1 |

> ⚠️ **Błąd projektowy klasy STOP-ignorowanego!** Prawy obwód sprawia wrażenie poprawnego podczas statycznej analizy schematu. Błąd ujawnia się dopiero w działaniu — gdy Lampka raz się załączy, przycisku STOP nie można jej wyłączyć. W systemach safety jest to krytyczny błąd bezpieczeństwa.

> 💡 **Reguła zapamiętywania:** Styk samopodtrzymania **zawsze przed STOP** (w gałęzi równoległej tylko do START). STOP musi być „po" całej logice podtrzymania, żeby faktycznie odcinał zasilanie cewki.

**Zastosowanie w praktyce:**
- Typowy obwód układu napędowego: `(START || KM_zal) AND STOP_NC → KM_cewka`
- W TIA Portal LAD: samopodtrzymanie = styk wyjściowego bitu Q równoległy do przycisku START, STOP zawsze w gałęzi głównej przed cewką
- Analogiczny błąd w SCL: `IF Start OR Q THEN Q := TRUE; IF Stop THEN Q := FALSE; END_IF;` — STOP nie zadziała jeśli `Start=TRUE` jednocześnie (priorytet SET)

*Źródło: Kurs ControlByte — Slajd 9/24 „Znajdź różnice", Układy samopodtrzymania; EN 60204-1 §9.2.2*


---

