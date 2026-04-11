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

### 21.7. Czym różni się ilockExtSync od ilockExtInt i jak działa synchronizacja zewnętrzna między sekwencjami?  🔴

W SICAR każdy krok sekwencji oprócz `ilockAuto` dysponuje dwoma dodatkowymi warunkami: **ilockExtSync** i **ilockExtInt** — oba zatrzymują watchdog gdy = 0, ale różnią się udziałem w synchronizacji.

**ilockExtSync — zewnętrzny warunek synchronizacji:**
- **Uczestniczy w synchronizacji** (Participation in synchronization = Yes) — to kluczowa różnica
- Służy do synchronizacji **między sekwencjami** (np. robot czeka na fixture, fixture czeka na robota)
- Gdy `ilockExtSync = 0` → watchdog jest zatrzymany (nie generuje alarmu)
- Preset = 1 (jeśli nieprogramowany → nie blokuje)
- Programujesz sygnały z **innych sekwencji** — typowo wyniki FC975/FC976

**ilockExtInt — zewnętrzny warunek procesu:**
- **NIE uczestniczy w synchronizacji** (Participation in synchronization = No)
- Służy do warunków **procesowych zewnętrznych** (pozycje narzędzi, sygnały z urządzeń peryferyjnych)
- Również zatrzymuje watchdog gdy = 0
- Sygnały powinny być programowane w innym module z własną diagnostyką

**Bloki pomocnicze do synchronizacji:**
- **FC975 (SeqCheckStep_FC)** — sprawdza czy podany krok jest aktywny (Auto/Inching) lub zsynchronizowany (tryb Off, dokładnie jeden krok zsynchronizowany) → zwraca `extSync`
- **FC976 (CheckIlock_FC)** — sprawdza czy `ilockAuto` kroku PERM **i** `ilockAuto` wybranego kroku selektywnego oba = 1 → zwraca `extSync`
- Oba bloki **muszą być wywołane PO FC998** w sekwencji

**Typowy scenariusz na linii spawalniczej:**
1. Sekwencja robota (FB1020) w kroku S005 czeka na fixture
2. W sekwencji fixture (FB1004) wywołujesz FC975 z parametrem „step = 8" → sprawdza czy krok 8 fixture jest aktywny
3. Wynik `extSync` podajesz do `ilockExtSync` w kroku S005 robota
4. Robot rusza dopiero gdy fixture jest w pozycji (krok 8 aktywny)

> 💡 Na rozmowie: „extSync używam do koordynacji robot-fixture — robot nie ruszy dopóki fixture nie potwierdzi pozycji. extInt używam do sygnałów procesowych jak czujniki narzędzi."

*[ZWERYFIKOWANE] — źródło: 34_1 Sequence- and messageblocks, Edition 2022-06, sekcje 2.3.9–2.3.10, strony 15–18*

### 21.8. Jak działają rozgałęzienia (branching) i funkcja Stop/Hold w sekwencjach SICAR?  🔴

**Branching — #sequence.stepNplus1:**
Pozwala na **warunkowe rozgałęzienie** sekwencji liniowej — zamiast przejścia do kolejnego kroku, FB1000 przeskakuje do wskazanego numeru kroku.

**Mechanizm:**
1. W aktualnym kroku sprawdzasz warunek (np. typ karoserii)
2. Jeśli warunek spełniony → ładujesz numer docelowego kroku do `#sequence.stepNplus1`
3. Przy następnym `transAuto = 1` → FB1000 przechodzi do kroku z `stepNplus1` zamiast do kolejnego liniowo
4. Wartość `stepNplus1` jest ładowana **niezależnie** od stanu `transAuto` — ważne, by sprawdzać warunek rozgałęzienia **tylko gdy transAuto jest spełniony**

**Przykład (STL):**
```
S002:
  AN  #sequence.transAuto     // sprawdź tylko gdy trans spełniony
  JC  E006
  AN  M 600.2                 // warunek: typ karoserii
  JC  E006
  L   5                       // skok do kroku 5
  T   #sequence.stepNplus1
E006: BEU
```
Jeśli `M600.2 = 1` → następny krok = 5 (pomija 3 i 4). Jeśli `M600.2 = 0` → normalnie krok 3.

**Stop/Hold — #sequence.stopInStepN:**
Kontroluje zachowanie sekwencji po naciśnięciu przycisku „Stop" na HMI w trybie Auto.

**Wartości programowalne:**
- `255` (domyślna) — bieżący krok zostaje dokończony, potem sekwencja przechodzi do trybu Off
- `0` — **natychmiastowe zatrzymanie** sekwencji (przerwanie kroku)
- `1–228` — sekwencja kontynuuje do podanego kroku, dopiero tam się zatrzymuje

**Sygnały statusu w I-DB sekwencji:**
- `#sequence.OM_SB_Hold_request` — Stop (Hold) został aktywowany
- `#sequence.OM_SB_Hold_Pos_reached` — pozycja Stop (Hold) została osiągnięta

**holdPosExternReached:**
- Dodatkowy sygnał potwierdzenia — jeśli `holdPosExternReached = 0`, aktywny krok zostanie dokończony **niezależnie** od `stopInStepN = 0` czy `twdRun = 0`
- Preset = 1 (jeśli nieprogramowany → nie wpływa na zachowanie)

**Wartość domyślną** `stopInStepN` (255) można zmienić globalnie w FC980, Network 3, parametr `Hold_Init_Value`.

> 💡 Na commissioning: „Dla robotów programuję stopInStepN = 255 (dokończ ruch), dla prostych siłowników zostawiam 0 (zatrzymaj natychmiast). Na linii z wieloma stacjami — programuję warunkowe stopInStepN per krok, żeby robot dojechał do bezpiecznej pozycji."

*[ZWERYFIKOWANE] — źródło: 34_1 Sequence- and messageblocks, Edition 2022-06, sekcje 2.3.11–2.3.12, strony 30–33*

### 21.9. Co to jest DB1000 (UiDiagAddOn_DB) i jak wykorzystujesz go w programowaniu?  🔴

**DB1000 (UiDiagAddOn_DB)** to centralny blok danych stanowiący **interfejs między oprogramowaniem użytkownika a oprogramowaniem DiagAddOn**. Wszystkie informacje potrzebne do sterowania z poziomu kodu użytkownika są dostępne w DB1000.

**Struktura DB1000 — główne sekcje:**

**1. OM_Seq[1..255] — status per sekwencja (1 bajt na sekwencję):**
- `.0` = Automatic (sekwencja w trybie Auto)
- `.1` = Inching (tryb krokowy)
- `.2` = Manual (tryb ręczny)
- `.3` = Inching_Step_plus1 / Hold in Step 1
- `.4` = Start (sekwencja wystartowana)
- `.5` = Acknowledge (restart watchdog)
- `.6` = Clock (sygnał zegarowy)
- `.7` = Synchronize (sekwencja zsynchronizowana)

**2. Common — sygnały ogólne:**
- Informacja czy istnieje aktywny komunikat błędu lub błąd sekwencji
- Typowe zastosowanie: sterowanie lampą błędu na kolumnie sygnalizacyjnej

**3. OPMode[1..8] — status per obszar trybów pracy:**
- Informacje o aktywnym trybie, warunkach startowych, alarmach per area
- Przykład: sterowanie syreną przy aktywacji Auto w danym area

**4. Lock Movements — blokada ekranów ruchów:**
- `Panel[x].movButtonActive` — na HMI x naciśnięto przycisk ruchu
- `Panel[x].activeMovScreen` — który ekran ruchów jest otwarty (1–64)
- `Panel[x].lockMovScreens` — zablokuj WSZYSTKIE ekrany ruchów na HMI x
- `Panel[x].OPMode[y].lockMovements` — zablokuj ruchy w danym OPMode area na HMI x

**5. Reset — przycisk resetowania per HMI:**
- Od wersji V14.4.0 dostępny przycisk „Reset" w nagłówku DiagAddOn
- Sygnał per HMI + sygnał zbiorczy wszystkich aktywnych HMI
- Przypisanie w FC1983

**Typowe zastosowania programistyczne:**
- Wymuszenie trybu Auto dla wybranej sekwencji niezależnie od OPMode area → nadpisz bity `OM_Seq[x]` w DB1000 **przed** wywołaniem FC998
- Sterowanie lampami/syrenami na podstawie stanu trybów z `OPMode[x]`
- Blokada ruchów przy pracy wielopanelowej (use case: ruch na HMI1 → blokada HMI2)
- Nawigacja między ekranami WinCC a DiagAddOn przez FC978 (Screenselect)

> 💡 Na rozmowie: „DB1000 to mój główny punkt dostępu do stanu linii — stamtąd odczytuję tryby sekwencji, steruje blokadami ruchów między panelami i nadpisuję tryby dla sekwencji systemowych jak RFID."

*[ZWERYFIKOWANE] — źródło: 40_User_Guideline SICAR@TIA DiagAddOn, Edition 2022-04, sekcja 4 User interface*

### 21.10. Jak działają ekrany ruchów (Movement Screens) i blokada ruchów (Lock Movements) w SICAR?  🟡

**Movement Screens** to ekrany HMI w DiagAddOn umożliwiające **ręczne sterowanie ruchami** maszyny w trybie Manual. Każda sekwencja/krok może mieć przypisany ruch na dedykowanym ekranie. System obsługuje do **64 ekranów ruchów** per HMI.

**Parametryzacja ekranu ruchu (w narzędziu DiagGen):**
- **Tekst ruchu** (movement text) — najważniejszy parametr; usunięcie tekstu kasuje cały wiersz ruchu
- **Aktywna indykacja** — operand sygnalizujący wykonywanie ruchu (np. wyjście zaworu)
- **Indykacja pozycji granicznej** — do 8 operandów feedback (np. czujniki krańcowe)
- **Kaskada i krok** — powiązanie z `#sequence.motionButton` (ruch aktywuje konkretny krok sekwencji)
- **Wartość pozycji** — parametryzacja DB i DBD dla wyświetlania pozycji (format: `DBx.DBDy`)
- Jeśli nie podano operandów indykacji → system generuje je automatycznie z `limitManual` i `ilockManual`

**motionButton — klucz ruchu:**
- Zmienna `#sequence.motionButton` = 1 gdy operator naciśnie przycisk ruchu na ekranie HMI
- Ustawiana **osobno per sekwencję** — ruch na jednym ekranie nie wpływa na inne sekwencje
- **Zawsze programowana jako pierwszy warunek** w `ilockManual`: `A #sequence.motionButton`
- Przejście z Manual do Auto możliwe natychmiast przez synchronizację (bez resetowania)

**Lock Movements — blokada przy wielu panelach HMI:**
Gdy na linii pracuje kilka paneli HMI jednocześnie, **ruch na jednym panelu musi blokować pozostałe** — to wymóg bezpieczeństwa.

**Sygnały w DB1000 per HMI (Panel[x]):**
- `movButtonActive` — czy przycisk ruchu jest naciśnięty na dowolnym ekranie HMI x
- `activeMovScreen` — numer otwartego ekranu ruchów (1–64)
- `lockMovScreens` — zablokuj WSZYSTKIE ekrany ruchów na HMI x
- `OPMode[y].lockMovements` — zablokuj ruchy tylko w wybranym OPMode area na HMI x

**Typowe use case'y blokady:**
1. **Wzajemna blokada paneli** — ruch na HMI1 → `lockMovScreens` na HMI2 (i odwrotnie)
2. **Blokada wybranych ekranów** — zablokuj ekrany 2+3 na HMI2 jeśli są otwarte na HMI2
3. **Blokada per OPMode area** — HMI2 może sterować tylko area 2, area 1 zablokowany (linia z HMI1=area 1+2, HMI2=area 2)
4. **Nawigacja z WinCC** — FC978 (Screenselect DiagAddOn) pozwala przejść z dowolnego ekranu WinCC bezpośrednio do konkretnego ekranu ruchu w DiagAddOn

> 💡 Na commissioning: „Przy uruchamianiu linii z dwoma panelami — najpierw konfiguruję Lock Movements w DB1000, żeby operatorzy na dwóch HMI nie mogli jednocześnie ruszać tym samym urządzeniem. To kwestia bezpieczeństwa."

*[ZWERYFIKOWANE] — źródło: 40_User_Guideline SICAR@TIA DiagAddOn, Edition 2022-04, sekcje 2.2.1 Configuration of movements, 4.4 Lock Movements, 5 External Screen select*
