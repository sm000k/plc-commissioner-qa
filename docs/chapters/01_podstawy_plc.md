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
- OB100 — Startup OB, wykonywany raz po przejściu CPU z STOP→RUN. Inicjalizacja zmiennych, reset stanu maszyny, wyzerowanie wyjść. W TIA Portal S7-1200/1500: jedyny OB startu (nie ma OB101 Warm Restart / OB102 Cold Restart jak w S7-400).
- F_MAIN — Safety OB, oddzielny cykl dla programu failsafe, chroniony przez F-CPU.

**Diagnostyczne OB — ważne przy commissioning:**
- OB80 — cycle time exceeded (czas cyklu przekroczył watchdog). Sygnalizuje zbyt wolną logikę.
- OB82 — diagnostic error: moduł I/O zgłosił błąd diagnostyczny (np. zerwanie kabla, przegrzanie modułu F). W TIA Portal: blok RALRM lub ProDiag odbiera dane.
- OB86 — rack failure / PROFINET station failure. Wywołany gdy zdalna stacja (ET200SP, napęd) znika z sieci.
- OB121 — Programming Error: błędy programistyczne (dzielenie przez zero, błędna konwersja typów, przekroczenie zakresu tablicy).
- OB122 — I/O Access Error: błąd dostępu do modułu I/O (moduł nie istnieje, awaria komunikacji z modułem). Ważne rozróżnienie przy uruchamianiu nowego kodu.

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
- W Safety: program F_MAIN w starszych wersjach TIA Portal wymaga FBD lub LAD — SCL nie jest certyfikowany dla F-bloków Safety. SCL dla F-bloków Safety został wprowadzony w TIA Portal V19 (STEP 7 Safety V19). ⚗️ DO WERYFIKACJI: dokładna wersja i wymagany firmware F-CPU w Release Notes TIA Portal. Zawsze sprawdź dopuszczalne języki dla swojej wersji portalu przed użyciem SCL w logice Safety.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.7. Co to jest sygnał 4-20mA i dlaczego nie 0-20mA?

4-20mA to standardowy sygnał analogowy dla czujników przemysłowych (przetworniki ciśnienia, temperatury, przepływu). Zakres 4 mA (wartość minimalna procesu) do 20 mA (wartość maksymalna).

- **Dlaczego 4 a nie 0 mA:** Sygnał 0 mA jednoznacznie oznacza zerwanie kabla lub awarię zasilania czujnika — łatwa diagnostyka. Przy 0-20 mA nie da się odróżnić minimalnej wartości procesu od awarii.
- **Przewaga nad napięciowym (0-10V):** Sygnał prądowy nie spada na rezystancji kabla — można przesyłać na duże odległości (setki metrów) bez strat dokładności.
- **Zakres poniżej 4 mA (np. 3,6 mA) i powyżej 20 mA (np. 20,5 mA):** Oznacza sygnał poza zakresem — diagnostyka w PLC (wire break / overflow).
- **Skalowanie w TIA Portal:** Surowy sygnał z modułu AI: 0–27648 (integer) dla zakresu 4–20 mA. Blok `NORM_X` normalizuje do 0.0–1.0, a `SCALE_X` skaluje na zakres inżynierski (np. 0.0–100.0 bar). Alternatywnie: bezpośrednia przeliczenie REAL w SCL: `Ciśnienie := (REAL_AI - 4.0) / 16.0 * MaxRange;`
- **Podłączenie dwuprzewodowe (2-wire):** Zasilanie i sygnał na jednej parze kabli (czujnik = zmienna rezystancja). Oszczędność okablowania.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 1.8. Co to jest PROFINET i czym różni się od PROFIBUS?  🔴

PROFINET: Ethernet-based, 100Mbit/s (gigabit w nowych instalacjach), elastyczna topologia (gwiazdka, linia, pierścień), plug-and-play z GSDML, obsługuje PROFIsafe i IRT (250µs, jitter <1µs). Nowy standard dla wszystkich nowych projektów.
PROFIBUS: RS-485, max 12Mbit/s, liniowa topologia z terminatorami na obu końcach kabla, starszy standard. Nadal spotykany w modernizacjach i instalacjach sprzed 2010.

**Role urządzeń PROFINET — kluczowe na rozmowie:**
- **IO-Controller**: sterownik nadrzędny zarządzający cyklem wymiany danych — to jest CPU (np. S7-1500F). Maksymalna liczba IO-Devices zależy od modelu CPU (⚠️ DO WERYFIKACJI: np. S7-1518 — do 512, S7-1511 — mniej; sprawdź w danych katalogowych konkretnego CPU).
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
- **S7-300** *(wycofany z produkcji, nadal masowo zainstalowany)*: Modułowy sterownik na szynie S7-300.
  - **Zastosowanie:** Modernizacje, utrzymanie istniejących instalacji. Spotykany na starszych liniach produkcyjnych.
  - **Możliwości:** MPI/PROFIBUS, programowanie w STEP 7 Classic (Manager). Wersje F (315F-2, 317F-2) dla Safety. Zastąpiony przez S7-1500.
- **S7-400** *(wycofany, niszowe zastosowania)*: High-end, duże systemy procesowe.
  - **Zastosowanie:** Energetyka, chemia, rafinerie — tam gdzie wymagana redundancja H-CPU. Zastępowany przez S7-1500H.
  - **Możliwości:** Redundancja CPU (H-System), hot swap modułów, duża pamięć, PROFIBUS/PROFINET.
- **S7-1200**: Kompaktowe sterowniki ze zintegrowanymi wejściami i wyjściami.
  - **Zastosowanie:** Małe i średnie aplikacje, łączące dobrą wydajność z niską ceną.
  - **Możliwości:** Modułowa konstrukcja, port PROFINET, płytka sygnałowa, moduły rozszerzeń DI/DO/AI/AO, moduły technologiczne (np. wagowe), moduły komunikacyjne (RS232, RS485, PROFIBUS, AS-i, IO-Link, GSM), wbudowane szybkie wejścia/wyjścia (do enkoderów, silników krokowych/serwo), wersje failsafe (1214FC, 1215FC). Wbudowany serwer WWW.
- **S7-1500**: Dedykowane do najbardziej wymagających aplikacji.
  - **Zastosowanie:** Największa moc obliczeniowa, zaawansowane funkcje technologiczne i komunikacyjne.
  - **Możliwości:** Wbudowany OPC UA Server, Web Server, wyświetlacz diagnostyczny na froncie CPU, Motion Control (Technology Objects), wersje F (failsafe), T (motion), R (redundancja komunikacji), H (hot standby), HF (H+F). Do 512 IO-Devices PROFINET (zależnie od modelu CPU).
- **ET 200SP CPU** *(odmiany 1510SP, 1512SP, 1515SP)*: Kompaktowa alternatywa S7-1500 montowana bezpośrednio na szynie ET 200SP.
  - **Zastosowanie:** Zdalne szafy sterownicze, rozproszona automatyka (automotive, linie montażowe). Wersje F dostępne.
  - **Możliwości:** Identyczne programowanie jak S7-1500 w TIA Portal, mniejsza obudowa, moduły ET 200SP bezpośrednio na szynie.
Praktyczne wskazówki:
- Na rozmowie kwalifikacyjnej: S7-300/400 spotykasz przy modernizacjach — musisz znać STEP 7 Classic. Nowe projekty: S7-1200 lub S7-1500.
- Dla początkujących w programowaniu PLC, S7-1200 jest polecany ze względu na niższą cenę.
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
  - **Działanie:** Dane oznaczone jako retentywne są automatycznie zachowywane w pamięci nieulotnej (wbudowana Flash w S7-1200, SIMATIC Memory Card w S7-1500) i przywracane po ponownym uruchomieniu CPU. Pozwala na zachowanie wybranych danych (np. liczniki produkcji, aktualny stan maszyny, parametry receptur).
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
| 1217C | 14DI/10DO/2AI/2AO | 8 SM | 3 | 1 | PTO4 (4 osie krokowe), 2× PROFINET |

**Typy modułów rozszerzeń:**
- **SM (Signal Module)** — z prawej: DI, DO, DI/DO, AI, AO — maksymalnie 8 sztuk.
- **CM (Comm Module)** — z lewej: RS232, RS485, PROFIBUS DP, AS-i, IO-Link master, GSM/GPRS.
- **SB (Signal Board)** — na froncie CPU: 2DI+2DO, AI, lub RS485 bez zajmowania slotu SM.

**Karta pamięci:** Micro SD pre-formatowana przez Siemens (nie zwykły consumer SD). Rola: backup programu, aktualizacja firmware, "Transfer Card" (wgranie programu na nowy CPU bez laptopa — wystarczy karta).

**Praktyczne limity:** Przy wielu modułach analogowych sumuj pobór prądu 5V z szyny wewnętrznej — max ~1A. Przekroczenie = moduły niestabilnie działają lub nie startują.

*Źródło: dane katalogowe Siemens S7-1200 System Manual*

### 1.12. Czym jest enkoder i jaka jest różnica między inkrementalnym a absolutnym?  🟡

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
### 1.13. Co to jest IO-Link i jakie korzyści daje względem klasycznych wejść analogowych PLC?  🟡

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

**Co oznacza każda żyła w kablu M12:**

**Kabel 3-żyłowy (IO-Link / czujniki cyfrowe):**
- **Pin 1 (BN — brązowy):** L+ zasilanie (24 VDC)
- **Pin 3 (BU — niebieski):** M masa (0 V)
- **Pin 4 (BK — czarny):** C/Q — dane IO-Link (komunikacja) lub wyjście przełączające (SIO mode)

**Kabel 4-żyłowy (czujniki analogowe 4–20 mA / 0–10 V):**
- **Pin 1 (BN — brązowy):** L+ zasilanie (24 VDC)
- **Pin 2 (WH — biały):** Sygnał analogowy (wyjście czujnika → AI modułu)
- **Pin 3 (BU — niebieski):** M masa (0 V)
- **Pin 4 (BK — czarny):** Drugi kanał wyjścia lub ekran/rezerwa

> Złącze M12 to standard przemysłowy — kolory żył wg EN 60947-5-2. IO-Link celowo używa tego samego kabla co czujniki binarne (3-wire) — wymiana czujnika zwykłego na IO-Link nie wymaga przeokablowania.

**Tryb Data Storage (automatyczna reparametryzacja):**
Po wymianie uszkodzonego czujnika IO-Link Master automatycznie wgrywa zapisane parametry do nowego urządzenia — bez interwencji serwisanta. TIA Portal → właściwości portu IO-Link → `Data Storage: On`.

**Typowe zastosowania w automotive:**
- Czujniki pozycji z identyfikacją narzędzi (numer seryjny toolingu czytany z IO-Link)
- Kolumny świetlne z parametryzacją kolorów i wzorów przez PLC
- Zawory pneumatyczne z diagnostyką licznika zadziałań

> 💡 **IO-Link ≠ Safety** — standard IO-Link nie jest Safety-certified. Do zastosowań Safety wymagane są osobne kanały F-DI. IO-Link służy wyłącznie do danych procesowych i diagnostyki (standard world).

*Źródło: Siemens ET200SP IO-Link Master product documentation*

### 1.14. Co to jest przerzutnik SR i RS w TIA Portal i jaka jest różnica w priorytecie?  🟢

**Przerzutniki bistabilne SR i RS** to elementy PLC zapamiętujące stan (bit) po zaniku sygnału sterującego. Stosuje się je, bo operator wciska przycisk START na chwilę — a silnik musi pracować dalej (samopodtrzymanie). Różnią się zachowaniem gdy **S i R są aktywne jednocześnie** — wtedy priorytet decyduje o stanie wyjścia.

**SR — priorytet Set (Set dominant):**
- Wyjście `Q` ustawia sygnał `S` (Set), kasuje sygnał `R1` (Reset)
- Gdy `S=1` i `R1=1` jednocześnie → `Q = 1` (Set wygrywa)
- Stosowany gdy **ważniejsze jest uruchomienie** niż zatrzymanie (np. latch alarmu — alarm musi trzymać do ręcznego potwierdzenia)

**RS — priorytet Reset (Reset dominant):**
- Wyjście `Q` ustawia sygnał `S1` (Set), kasuje sygnał `R` (Reset)
- Gdy `S1=1` i `R=1` jednocześnie → `Q = 0` (Reset wygrywa)
- Stosowany gdy **ważniejsze jest zatrzymanie** niż uruchomienie (99% maszyn — STOP/E-Stop musi wygrać ze STARTem)

**Tabela prawdy — SR (Set-dominant):**

| S | R1 | Q (wyjście) |
|:-:|:--:|:-----------:|
| 0 | 0  | Q_prev (stan zapamiętany) |
| 1 | 0  | **1** (Set) |
| 0 | 1  | **0** (Reset) |
| 1 | 1  | **1** ← Set wygrywa |

**Tabela prawdy — RS (Reset-dominant):**

| S1 | R | Q (wyjście) |
|:--:|:-:|:-----------:|
| 0  | 0 | Q_prev (stan zapamiętany) |
| 1  | 0 | **1** (Set) |
| 0  | 1 | **0** (Reset) |
| 1  | 1 | **0** ← Reset wygrywa |

> Jedyna różnica → wiersz ostatni (oba aktywne). Reszta identyczna.

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

### 1.15. Jak zbudować układ samopodtrzymania w LAD i czym różni się Dominacja SET od Dominacji RESET?  🔴

**Samopodtrzymanie** (seal-in) to obwód LAD, w którym cewka wyjściowa podtrzymuje się sama — styk NO tego samego bitu jest podłączony **równolegle do START**. Dzięki temu operator wciska START na chwilę, a cewka pracuje dalej. **Dominacja** określa, który sygnał wygrywa gdy START i STOP są aktywne jednocześnie — zależy od **struktury obwodu**, czyli gdzie w drabince siedzi styk STOP.

**Dominacja RESET — STOP wygrywa (bezpieczna):**

```
  |                                              |
  |    START         STOP(NC)     ( Lampka )     |
  +----] [-----+-----]/[---------(        )----- +
  |            |                                  |
  |   Lampka   |                                  |
  +----] [-----+                                  |
  |                                              |
```
- Górna gałąź: `START` → do węzła `+`
- Dolna gałąź: `Lampka` (samopodtrzymanie) → do tego samego węzła `+`
- Za węzłem: `STOP(NC)` **szeregowo** → cewka `( Lampka )`
- STOP odcina **jedyną drogę** do cewki — blokuje i START, i podtrzymanie
- `START=1, STOP=1` → **Lampka = 0** (RESET wygrywa)
- 💡 „Obie ścieżki prowadzą przez STOP — przycisk wyłączenia jest ważniejszy"

**Dominacja SET — START wygrywa (niebezpieczna):**

```
  |                                              |
  |    START                      ( Lampka )     |
  +----] [-------------------+---(        )----- +
  |                          |                    |
  |   Lampka    STOP(NC)     |                    |
  +----] [------]/[----------+                    |
  |                                              |
```
- Górna gałąź: `START` → **bezpośrednio** do cewki (omija STOP!)
- Dolna gałąź: `Lampka` (samopodtrzymanie) → `STOP(NC)` → do cewki
- STOP odcina **tylko podtrzymanie** — START dalej zasila cewkę górą
- `START=1, STOP=1` → **Lampka = 1** (SET wygrywa)
- 💡 „START omija STOP górną gałęzią — przycisk wyłączenia nie działa gdy START wciśnięty"

**Kluczowa różnica — pozycja STOP w obwodzie:**

| Cecha | Dominacja RESET | Dominacja SET |
|-------|:-:|:-:|
| STOP odcina | **obie** ścieżki (START + seal-in) | **tylko** seal-in |
| START=1, STOP=1 | **Lampka = 0** | **Lampka = 1** |
| Bezpieczeństwo | ✅ bezpieczna | ⚠️ niebezpieczna |

**Dlaczego układ trzyma stan gdy START=0, STOP=0?**
STOP jest stykiem NC `]/[` — gdy nikt go nie wciska (`STOP=0`), styk NC jest **zamknięty** (przepuszcza). Prąd płynie przez seal-in `Lampka` → przez zamknięty STOP(NC) → do cewki. Układ **trzyma stan poprzedni** — identycznie jak SR/RS z S=0, R=0.

**Tabela prawdy:**

| Stan | START | STOP | Dom. RESET | Dom. SET |
|:-----|:-----:|:----:|:----------:|:--------:|
| Oba wciśnięte | **1** | **1** | **0 ← STOP** | **1 ← START** |
| Tylko START | 1 | 0 | 1 | 1 |
| Tylko STOP | 0 | 1 | 0 | 0 |
| Żaden | 0 | 0 | * (trzyma) | * (trzyma) |

> `*` = stan podtrzymany przez seal-in (styk NC STOP jest zamknięty → cewka trzyma). Jedyna różnica → wiersz `START=1, STOP=1`.

**Powiązanie z blokami SR/RS i cewkami (S)/(R):**

Układ seal-in z normalną cewką `( )`, bloki SR/RS i cewki `(S)`/`(R)` to **ta sama logika bistabilna** — trzy różne notacje, identyczna tabela prawdy.

| Implementacja | Podtrzymanie | Dominację decyduje |
|---|---|---|
| Seal-in + cewka `( )` | Styk NO wyjścia równolegle do START (budujesz sam) | **Pozycja STOP** w obwodzie |
| Cewki `(S)` / `(R)` | Wbudowane w cewkę (nie trzeba styku) | **Kolejność skanowania** (ostatni network wygrywa) |
| Blok SR / RS | Wbudowane w blok | **Typ bloku** (SR → S wygrywa, RS → R wygrywa) |

| Obwód seal-in | Cewki LAD | Blok TIA Portal |
|---|---|---|
| Dominacja RESET | `(S)` → potem `(R)` (R ostatni) | **RS** — Reset-Dominant |
| Dominacja SET | `(R)` → potem `(S)` (S ostatni) | **SR** — Set-Dominant |

**Zasada bezpieczeństwa:** Zawsze stosuj **Dominację RESET** dla obwodów STOP i E-Stop. Operator musi mieć gwarancję, że STOP zatrzyma maszynę niezależnie od innych sygnałów (EN 60204-1 §9.2.2).

*Źródło: Kurs ControlByte — Układy samopodtrzymania, Dominacja SET/RESET; EN 60204-1 §9.2.2*

