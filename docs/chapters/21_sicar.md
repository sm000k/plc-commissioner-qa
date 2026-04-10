## 21. SICAR@TIA — STANDARD AUTOMATYKI AUTOMOTIVE

### 21.1. Co to jest SICAR@TIA i do czego służy?  🟢

**SICAR@TIA** (Siemens Automation Platform for CAR Plants) to gotowa platforma automatyki Siemensa przeznaczona do **sterowania sekwencyjnego** w fabrykach automotive (linie spawalnicze, montażowe, klejenie, studwelding). Składa się ze skoordynowanego oprogramowania PLC (S7-1500/1500F) i HMI (WinCC Advanced).

**Dwa pakiety oprogramowania:**
- **SICAR@TIA** — bazowy pakiet: tryby pracy (operation modes), interfejs HMI, dane produkcyjne, Tec Units, diagnostyka fieldbusowa, PLC Webserver z topologią sieci
- **DiagAddOn** — rozszerzenie: sterowanie sekwencyjne (255 sekwencji × 228 kroków), diagnostyka online kroków w LAD/STL na HMI, ekrany ruchów ręcznych, synchronizacja, historia komunikatów, RSS-Feed

**Główna korzyść:** ujednolicona filozofia obsługi i diagnostyki na wszystkich liniach — maintenance z różnych fabryk i dostawców szybko lokalizuje błędy, bo interfejs i struktura programu są wszędzie takie same.

**Wymagane licencje:** TIA Step7 Professional + WinCC Advanced + opcjonalnie TIA Safety Advanced. DiagAddOn nie wymaga osobnej licencji.

> 💡 Na rozmowie podkreśl: SICAR to nie biblioteka bloków — to **cały framework** z ustalonym standardem folderów, nazewnictwa, trybów pracy i diagnostyki. Programista nie buduje struktury od zera, tylko programuje sekwencje w gotowym szkielecie.

*[ZWERYFIKOWANE] — źródło: 10_Introduction SICAR@TIA DiagAddOn, Edition 2022-04*

### 21.2. Jak wygląda struktura programu PLC w SICAR?  🟡

Program PLC w SICAR ma **ściśle zdefiniowaną strukturę folderów** — każdy projekt wygląda tak samo, co ułatwia orientację na nowej linii:

**Foldery bazowe (00–07)** — wspólne dla wszystkich projektów:
- **00_Organization blocks** — OB1 (Main), OB cykliczne
- **01_Initialization** — FC1981 (CallInit) z blokiem GlobalInfo_FB — tu ustawiasz liczbę HMI i OPModes
- **02_HMI_OperationModes** — FC1983 (bazowy) i FC983 (DiagAddOn) — wywołania paneli i trybów pracy
- **04_User** — folder na bloki użytkownika (kopie z 08_Zz jeśli trzeba zmodyfikować)
- **07_Diagnosis** — diagnostyka PROFINET, alarmy systemowe

**Folder 08_ZzComponents** — gotowe komponenty (napędy, roboty):
- Prefix „Zz" = bloki **których NIE WOLNO modyfikować**
- Jeśli musisz zmienić blok → kopiujesz go do **04_User** z własnym wersjonowaniem

**Folder 10_Sequence & Messageblocks** — tu programujesz sekwencje linii:
- Podział na OPMode areas: `++0` (globalne komunikaty), `++1` (area 1), `++2`…`++8`
- Nazewnictwo stacji: `++1.010 FX1` = OPMode area 1, stacja 10, Fixture 1; `++1.020 IR1` = area 1, stacja 20, Robot 1

**Zasoby systemowe (nie wolno zmieniać):**
- FB/FC/DB 900–1299, UDT 900–999 — zarezerwowane dla DiagAddOn
- MB1 = clock memory byte, MB2 = system memory byte — obowiązkowe w konfiguracji PLC

> 💡 Na rozmowie: „Kiedy dostaję nowy projekt SICAR, zaczynam od 10_Sequence — tam jest logika linii. Foldery 00–07 to szkielet, 08_Zz to gotowe komponenty — tych nie ruszam."

*[ZWERYFIKOWANE] — źródło: 10_Introduction sekcja 6 Structure PLC-program, 40_User_Guideline sekcja 1.1*

### 21.3. Jakie tryby pracy (Operation Modes) obsługuje SICAR i jak je uruchamiasz?  🟡

SICAR zarządza do **8 niezależnych obszarów trybów pracy** (OPMode areas) na jednym PLC. Każdy area może działać w innym trybie jednocześnie (np. area 1 w Auto, area 3 w Manual).

**Trzy tryby pracy:**
- **Automatic** — sekwencje wykonują się automatycznie; spełnienie warunku `transAuto = 1` → przejście do następnego kroku
- **Inching (krokowy)** — jak Auto, ale krok po kroku z potwierdzeniem; można krokować jedną sekwencję lub wszystkie w area
- **Manual** — ruchy ręczne przez ekrany ruchów (movement screens) na HMI; przycisk ruchu → interlock + limit sprawdzane dla danego kroku

**Warunki uruchomienia trybu (memory word MW10–MW24 per area):**
- `M x.0` = E-Stop aktywny (wymagany dla WSZYSTKICH trybów)
- `M x.1` = drzwi Safety zamknięte (wymagany dla Auto i Inching)
- `M x.2` = warunki bazowe Manual OK
- `M x.4` = warunki bazowe ogólne OK

**Procedura przełączenia (np. Manual → Auto):**
1. Naciśnij przycisk „AUTO" w nagłówku WinCC
2. Potwierdź zmianę (popup lub bez — zależy od stałej `WITH_POPUP`)
3. Przycisk „AUTO" miga → naciśnij „START" (lub klucz zewnętrzny)
4. Trzymaj „START" aż przycisk przestanie migać → tryb aktywny

**Funkcje specjalne (dostępne w Auto):**
- **Stop** — zatrzymanie sekwencji natychmiast (`DBB24=0`) lub po bieżącym kroku (`DBB24=255`)
- **Initial Position** — żądanie pozycji wyjściowej przed startem
- **Stop End of Cycle** — zatrzymanie po zakończeniu cyklu
- **Empty Line** / **Ghost Run** — praca bez detali / symulacja

> 💡 Na commissioning: zawsze zaczynaj od Manual → sprawdź każdy ruch osobno → przełącz na Inching → dopiero potem Auto.

*[ZWERYFIKOWANE] — źródło: 31_Initialization and Operation modes, Edition 2022-07*

### 21.4. Jak działa sterowanie sekwencyjne (Sequence Control) w SICAR?  🔴

Sterowanie sekwencyjne to serce SICAR — blok **FB1000** zarządza do 255 sekwencji równolegle, każda do 228 kroków. Struktura jest liniowa (z możliwością rozgałęzień).

**Numeracja bloków — prosta reguła (numer sekwencji + 1000):**
- Sekwencja 4 → FC1004 (wywołanie + wyjścia), FB1004 (logika kroków), DB1004 (dane sekwencji)

**Budowa bloku sekwencji (FB100x):**
- **Network 1: Branch distributor** — skok do aktywnego kroku (programowany w STL: `JU PERM`, `JU S001`, `JU S002`…)
- **Permanent step (PERM)** — warunki obowiązujące dla WSZYSTKICH kroków (np. crash interlocks wspólne dla całej sekwencji)
- **Selective steps (S001, S002…)** — warunki konkretnego kroku, wykonywany jest tylko aktywny krok

**Każdy krok (selective step) ma dwie części:**
1. **Interlock (ILOCK)** — warunki bezpieczeństwa / crash interlocks (czy ruch jest bezpieczny?)
2. **Transition / Limit** — w Auto: `transAuto` = warunek przejścia do następnego kroku; w Manual: `limitManual` = feedback że ruch się zakończył

**Kluczowe zmienne w #sequence:**
- `ilockManual` / `ilockAuto` — interlocki per tryb
- `transAuto` — warunek przejścia (Auto)
- `limitManual` — feedback ruchu (Manual)
- `twdSetpoint` — czas watchdog (monitoring)
- `setError` — natychmiastowy błąd
- `motionButton` — przycisk ruchu z ekranu HMI (Manual)

**Wyjścia (akcje)** programujesz w **FC100x** — po wywołaniu FC998 używasz flag kroków z DB do sterowania Tec Units i napędami.

**Reguła diagnostyki:** w blokach sekwencji (FB/FC 1001–1255) wolno używać **tylko** wejść/wyjść, merkerów i bitów z **nieoptymalizowanych** DB — inaczej DiagAddOn nie pokaże diagnostyki na HMI.

> 💡 Na rozmowie: „W SICAR nie piszę sterownika od zera — programuję warunki interlocków i tranzycji per krok. FB1000 sam zarządza przełączaniem kroków, synchronizacją i diagnostyką."

*[ZWERYFIKOWANE] — źródło: 34_1 Sequence- and messageblocks, Edition 2022-06*

### 21.5. Co to są Tec Units w SICAR i jak ich używasz?  🟢

**Tec Units** to gotowe, parametryzowalne bloki funkcjonalne w folderze **08_ZzComponents** dla typowych urządzeń na linii: silnik, zawór, napęd SINAMICS, robot (ABB IRC5, KUKA KRC4, FANUC R-30iB, Yaskawa YRC1000).

**Każdy Tec Unit zawiera:**
- FB z logiką sterowania (tryby Auto/Manual/Local)
- Ekrany HMI
- Definicje alarmów
- Interfejs do sekwencji (wywoływany z FC100x po flagach kroków)

**Zasada „Zz":** bloki w folderach z prefixem „Zz" **nie wolno modyfikować**. Jeśli musisz zmienić Tec Unit → kopiujesz do **04_User** i kontynuujesz jako blok użytkownika z własnym wersjonowaniem w bibliotece.

**Typowe wywołanie w programie:**
1. W sekwencji FC1004, po wyjściu kroku (step flag z DB1004), wywołujesz Tec Unit napędu lub zaworu
2. Tec Unit sam obsługuje logikę ruchu, feedback, alarmy i ekran HMI

> 💡 Na linii spawalniczej typowe Tec Units: interfejs robota (goProcess/goAck), napęd podnośnika/przenośnika, zawory pneumatyczne gripperów, czujniki RFID do identyfikacji karoserii.

*[ZWERYFIKOWANE] — źródło: 10_Introduction sekcja 6.1.3, 40_User_Guideline sekcja Configuration of movements*

### 21.6. Jak działa synchronizacja i diagnostyka w SICAR DiagAddOn?  🟡

**Synchronizacja** rozwiązuje kluczowy problem: po ręcznych ruchach (Manual) lub awarii — jak wrócić do produkcji automatycznej bez resetowania całej linii?

**Mechanizm:**
1. Po wybraniu trybu OFF, naciśnij „Synchronize" (dla jednej sekwencji lub wszystkich)
2. DiagAddOn analizuje KAŻDY krok sekwencji sprawdzając: `ilockAuto = 1` AND `transAuto = 0`
3. Jeśli dokładnie **jeden krok** spełnia ten warunek → sekwencja jest zsynchronizowana do tego kroku
4. Przełączasz na Auto → produkcja kontynuuje natychmiast od zsynchronizowanego kroku

**Diagnostyka na HMI (DiagAddOn):**
- Ekran diagnostyczny pokazuje **online** stan każdego bloku sekwencji: aktywny krok, warunki interlocków i tranzycji w formie LAD/STL
- **Watchdog time** (`twdSetpoint`) — monitoring czasu kroku; po przekroczeniu → diagnostyka automatycznie pokazuje, który warunek (interlock/transition) nie jest spełniony
- **Automatyczny pomiar watchdog** — przy pierwszym przebiegu Auto system sam mierzy i zapisuje czasy kroków
- **Message blocks** — komunikaty alarmowe z kategoryzacją i historią, wyświetlane na dedykowanym ekranie HMI
- **Cross reference** — z ekranu diagnostycznego możesz przejść bezpośrednio do szczegółów blokującego warunku

**Narzędzie DiagGen:**
- Generator danych diagnostycznych uruchamiany na PG/PC
- Wykorzystuje TIA Openness do przygotowania danych dla ekranów DiagAddOn na HMI
- Uruchamiasz po zmianach w blokach sekwencji → regeneruje powiązania krok↔HMI

> 💡 Na rozmowie: „Największa wartość DiagAddOn to diagnostyka — maintenance widzi online na HMI, który dokładnie warunek w którym kroku blokuje sekwencję. Nie muszą otwierać TIA Portal."

*[ZWERYFIKOWANE] — źródło: 10_Introduction sekcja 1.2.2 DiagAddOn for PLC, 34_1 Sequence- and messageblocks sekcja Watchdog/Synchronization*
