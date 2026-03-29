## 19. SŁOWNIK POJĘĆ — PLC / Safety / PROFINET / Napędy

Słownik zawiera **pełne definicje** (2–4 zdania) wszystkich kluczowych pojęć używanych w komisjonowaniu systemów Siemens. W odróżnieniu od ściągi — każde hasło wyjaśnia kontekst użycia i praktyczne znaczenie.

---

### Podstawy PLC

**Scan cycle** — jeden pełny cykl wykonania programu CPU: odczyt wejść → wykonanie programu → zapis wyjść → obsługa komunikacji. Czas cyklu wynosi typowo 1–20 ms; przy dużych projektach Safety może wzrosnąć do 50–100 ms. Zbyt długi scan cycle = opóźniona reakcja na sygnały bezpieczeństwa.

**OB (Organization Block)** — blok organizacyjny w TIA Portal definiujący punkt wywołania programu. OB1 = główny cykl, OB35 = przerwanie cykliczne (np. co 100 ms), OB100 = zimny start, F_MAIN = Safety OB.

**FB (Function Block)** — blok funkcjonalny z własną pamięcią instancji (IDB). Zachowuje stan między wywołaniami — używany dla silników, sekwencji, timerów. Każde wywołanie FB wymaga odrębnej instancji DB.

**FC (Function)** — blok bez pamięci własnej. Używany dla obliczeń jednorazowych, konwersji sygnałów, logiki bezstanowej. Tańszy pamięciowo niż FB.

**DB (Data Block)** — blok danych. Globalny DB: dostępny z całego programu. Instancja DB: dedykowana pamięć jednego FB, tworzona automatycznie przez TIA Portal.

**UDT (User Data Type)** — użytkowniczy typ złożony (np. `Motor_t` z polami Speed:REAL, Fault:BOOL). Wymusza spójną strukturę dla wielu identycznych urządzeń; jeden FB + UDT zastępuje N osobnych bloków.

**Tag (zmienna PLC)** — symboliczna nazwa adresu I/O, DB, merkera w tablicy tagów TIA Portal. Tagi globalne dostępne z całego projektu; lokalne — tylko w bloku.

**WatchDog timer** — wewnętrzny licznik CPU mierzący czas jednego cyklu; przy przekroczeniu limitu CPU przechodzi w STOP. Zabezpieczenie przed zawieszeniem się programu.

---

### Architektura Safety

**F-CPU (Fail-safe CPU)** — sterownik Siemens z certyfikowanym dual-channel processing. Oba kanały wykonują te same obliczenia równolegle; rozbieżność wyników → przejście w bezpieczny stan. Certyfikat TÜV: SIL 3 / PL e.

**F-signature** — kryptograficzny podpis jednego bloku Safety generowany przez TIA Portal podczas kompilacji. Zmienia się przy każdej modyfikacji kodu. Przechowywany w F-DB — nie można go edytować ręcznie.

**Collective signature (podpis zbiorczy)** — unikalny podpis całego programu Safety złożony ze wszystkich F-signatur. Widoczny na wyświetlaczu CPU. Niezgodność po wgraniu → Safety nie uruchamia się.

**F-DB (Fail-safe Data Block)** — blok danych generowany automatycznie przez TIA Portal dla każdego bloku Safety. Zawiera CRC, F-signature i parametry czasowe. Ręczna edycja zniszczyłaby spójność i uniemożliwiłaby uruchomienie Safety.

**Safety Integrated** — koncepcja Siemens: funkcje bezpieczeństwa (failsafe) i funkcje standardowe w jednym fizycznym CPU, jednym projekcie TIA Portal, przez jedną sieć PROFINET/PROFIsafe.

**LOCK / RUN (Safety CPU)** — tryby pracy Safety runtime. LOCK: program Safety zablokowany, wyjścia Safety → wartości zastępcze. RUN: Safety wykonuje się normalnie. Zmiana trybu wymaga hasła Safety i jest logowana.

**F-OB (Safety Main OB)** — blok organizacyjny Safety wywoływany osobnym cyklem F-CPU. Odpowiednik OB1 dla programu failsafe. W TIA Portal widoczny jako np. `Main_Safety_RTG1`.

---

### Moduły F-DI / F-DO

**Passivation** — stan błędu modułu F-I/O: wyjścia przyjmują substitute value (zwykle 0), wejścia raportowane są do F-CPU jako 0. Wyzwalana przez: urwanie kabla, discrepancy timeout, utratę PROFIsafe, błąd wewnętrzny modułu.

**Reintegration** — ręczne potwierdzenie (ACK) powrotu modułu do normalnej pracy po usunięciu błędu i passivation. Wymaga impulsu ACK_NEC — moduł nie wraca automatycznie (zasada „no silent recovery").

**ACK_REQ (Acknowledgement Required)** — wyjście bloku F ustawiane automatycznie gdy moduł wymaga potwierdzenia po błędzie (widoczne w Watch Table).

**ACK_NEC (Acknowledgement Necessary)** — wejście bloku F; wymaga impulsu zbocza narastającego. Stały sygnał TRUE nie potwierdzi reintegracji.

**ACK_GL** — blok z biblioteki Safety Advanced generujący zbiorczy impuls ACK do wszystkich F-I/O na raz — używany po awariach komunikacyjnych.

**VS* (Pulse testing / Sensor supply)** — impulsowe zasilanie wyjście modułu F-DI. Czujnik zasilany impulsami; ich powrót na wejście pozwala wykryć urwanie kabla (brak impulsów) i zwarcie do 24 V (ciągłe impulsy).

**Cross-circuit detection** — wykrywanie zwarć między kanałami F-DI realizowane przez VS* pulse testing. Zapewnia DC ≥ 99% bez dodatkowego okablowania — warunek konieczny dla Cat.4 / PL e.

**Discrepancy time** — maksymalny czas dopuszczalnej rozbieżności stanów dwóch kanałów czujnika 1oo2. Zbyt krótki → fałszywe błędy; zbyt długi → późne wykrycie uszkodzenia. Konfigurowany w parametrach F-DI w TIA Portal.

**Substitute value** — wartość przyjmowana przez wyjście F-DO podczas passivation (0 lub 1). Definiuje inżynier projektu na podstawie analizy ryzyka — nie Siemens.

**Value status** — bit jakości sygnału Safety w S7-1200/S7-1500. FALSE = sygnał zastępczy (passivation); TRUE = dane procesowe poprawne. Odwrotna logika niż klasyczny QBAD.

**pm switching** — tryb F-DO w którym przełączana jest linia P (plus, 24 V), masa wspólna. Prostsze okablowanie, niższy koszt.

**pp switching** — tryb F-DO w którym przełączane są obie linie P+, bez wspólnej masy. Wyższy poziom bezpieczeństwa — zwarcie jednej linii do masy nie powoduje przypadkowego zadziałania.

**F-PM-E (Fail-safe Power Module E)** — moduł Safety w ET 200SP/S odcinający zasilanie grupy standardowych modułów DO przez sygnał Safety. Tańsza alternatywa dla F-DQ przy spełnieniu wymagań SIL2/Cat.3/PLd.

---

### Struktury głosowania

**1oo1 (1 out of 1)** — jeden kanał; bez redundancji. Stosowany przy SIL1 lub gdy analiza ryzyka dopuszcza brak redundancji.

**1oo2 (1 out of 2)** — dwa czujniki; zatrzymanie gdy CHOĆBY JEDEN zgłosi problem. Wyższe bezpieczeństwo, ryzyko fałszywych alarmów. Obsługiwane sprzętowo przez moduł F-DI z discrepancy monitoring.

**2oo2 (2 out of 2)** — oba czujniki muszą zadziałać. Mniej fałszywych stopów, ale uszkodzenie „cichego" kanału może uniemożliwić reakcję w momencie zagrożenia.

**2oo3 (2 out of 3)** — trzy czujniki, decyzja większości (2 z 3). Balans bezpieczeństwa i dostępności; typowe w procesach ciągłych przemysłu chemicznego i naftowego.

---

### PROFIsafe i PROFINET

**PROFIsafe** — protokół Safety działający na warstwie aplikacji ponad PROFINET lub PROFIBUS. Każdy pakiet zawiera CRC, licznik wiadomości i F-Address. Wykrywa: utratę pakietu, powtórzenie, błędną sekwencję, przekłamanie danych, błędny adres docelowy.

**F-Address (F-Destination Address)** — unikalny adres Safety przypisany każdemu modułowi F w sieci. Musi być identyczny w TIA Portal i na fizycznym urządzeniu (DIP switch lub parametryzacja). Błędny F-Address → brak komunikacji Safety.

**F-monitoring time** — maksymalny czas oczekiwania F-CPU na kolejny pakiet PROFIsafe. Przekroczenie → passivation modułu. Za krótki → fałszywe alarmy; za długi → wolne wykrycie awarii sieci.

**F-peripheral** — zdalne urządzenie F-I/O podłączone do F-CPU przez PROFIsafe/PROFINET (np. ET200SP z modułami F-DI/F-DQ, ET200eco F). Awaria jednego peripherala passivuje tylko ten moduł, nie cały system.

**MRP (Media Redundancy Protocol)** — protokół redundancji dla topologii pierścieniowej PROFINET. Czas przełączenia < 200 ms (MRP) lub < 30 ms (Fast-MRP). MRM = Media Redundancy Manager zarządza pierścieniem.

**IRT (Isochronous Real-Time)** — tryb PROFINET z synchronizacją cyklu do 250 µs i jitterem < 1 µs, realizowaną sprzętowo na poziomie ASIC. Wymagany przy motion control z synchronizacją osi (SINAMICS S120, systemy wieloosiowe).

**GSDML** — plik XML opisujący urządzenie PROFINET (moduły I/O, parametry, obsługiwane adresy). Instalowany w TIA Portal: Options → Manage general station description files → Install.

**Shared Device** — urządzenie PROFINET zarządzane jednocześnie przez dwa kontrolery, każdy z przypisanym innym zakresem modułów. Stosowane przy integracji systemów Safety i standardowych obsługiwanych przez różnych dostawców.

**PRONETA** — bezpłatne narzędzie Siemens do standalone diagnostyki PROFINET, niezależne od TIA Portal. Skanuje sieć, pokazuje mapę urządzeń, IP, nazwy i porty — przydatne przy diagnozie bez dostępu do projektu.

---

### Napędy Safety — IEC 61800-5-2

**STO (Safe Torque Off)** — natychmiastowe odcięcie momentu przez zablokowanie impulsów PWM. Silnik wybiega swobodnie lub jest zatrzymywany hamulcem mechanicznym. Certyfikowany SIL3/PLe; realizowany sprzętowo w dwóch kanałach napędu. Odpowiada kategorii zatrzymania 0 (EN 60204-1).

**SS1 (Safe Stop 1)** — hamowanie wzdłuż zaprogramowanej rampy do zatrzymania, następnie aktywacja STO. Czas hamowania monitorowany — przekroczenie = natychmiastowe STO. Odpowiada kategorii zatrzymania 1 (EN 60204-1).

**SS2 (Safe Stop 2)** — hamowanie z rampą → SOS (napęd pozostaje zasilony i trzyma pozycję). Odpowiada kategorii zatrzymania 2 (EN 60204-1). Stosowane gdy po zatrzymaniu oś musi utrzymać pozycję.

**SOS (Safe Operating Stop)** — napęd zasilony, trzyma pozycję z monitoringiem odchylenia. Możliwe generowanie momentu gdy oś próbuje się ruszyć poza zdefiniowane okno pozycyjne.

**SLS (Safely Limited Speed)** — ograniczenie prędkości do bezpiecznego maksimum. Stosowane w trybie serwisowym gdy operator jest w strefie niebezpiecznej — maszyna nie musi być zatrzymana.

**SDI (Safe Direction)** — dopuszczony jest tylko jeden kierunek ruchu osi. Stosowane gdy przy otwartej osłonie oś może jechać wyłącznie od operatora.

**SBC (Safe Brake Control)** — certyfikowane, monitorowane sterowanie hamulcem mechanicznym. Monitoring prądu uzwojenia cewki hamulca; wykrywa uszkodzenie cewki lub zwarcie.

**STO_Active** — sygnał potwierdzający od napędu do F-CPU przez PROFIsafe, że STO jest aktywne i moment odcięty. Odróżnia STO od zwykłego wyłączenia programowego (które nie jest monitorowane).

---

### Obliczenia bezpieczeństwa

**SIL (Safety Integrity Level)** — poziom integralności bezpieczeństwa wg IEC 61508 / IEC 62061. SIL 1: PFH < 10⁻⁵; SIL 2: PFH < 10⁻⁶; SIL 3: PFH < 10⁻⁷ na godzinę.

**PL (Performance Level)** — poziom zapewnienia bezpieczeństwa wg EN ISO 13849-1. PL a (najniższy) → PL e (najwyższy). PL e odpowiada SIL 3.

**PFH (Probability of dangerous Failure per Hour)** — prawdopodobieństwo niebezpiecznej awarii niepostrzeżonej na godzinę pracy. Zsumowane dla wszystkich podsystemów łańcucha Safety (Detection + Evaluation + Reaction).

**DC (Diagnostic Coverage)** — pokrycie diagnostyczne: procent niebezpiecznych uszkodzeń wykrywanych przez diagnostykę wbudowaną. DC ≥ 99% wymagane dla Cat.4 / PL e.

**CCF (Common Cause Failure)** — awaria wspólnej przyczyny: jedna przyczyna (przepięcie, EMC, temperatura) niszczy oba kanały redundantnego systemu jednocześnie. ISO 13849-1 wymaga min. 65 punktów CCF dla Cat.3/Cat.4.

**B10** — liczba cykli po których 10% populacji danego urządzenia mechanicznego ulega awarii. Używany do obliczania MTTFd czujników i elementów wykonawczych.

**MTTFd (Mean Time to dangerous Failure)** — średni czas do niebezpiecznej awarii. Wyznaczany z B10 i częstotliwości użycia; wyższy MTTFd → lepszy PL.

**Proof test** — zaplanowany, periodyczny test ujawniający ukryte (niebezpieczne) usterki systemu Safety. Musi być dokumentowany; interwał wpływa na PFH systemu.

**Kategoria Cat.1–4** — architektura kanałów bezpieczeństwa wg EN ISO 13849-1. Cat.1: jeden kanał, wysoka jakość. Cat.2: jeden kanał + monitoring. Cat.3: dwa kanały, pojedyncza usterka nie powoduje utraty funkcji. Cat.4: jak Cat.3 + DC ≥ 99%, CCF ≥ 65 pkt.

---

### TIA Portal i commissioning

**FAT (Factory Acceptance Test)** — testy u dostawcy maszyny przed wysyłką. Każda funkcja Safety testowana, wyniki podpisywane przez dostawcę i klienta. Obowiązkowe dla maszyn SIL2/SIL3.

**SAT (Site Acceptance Test)** — testy u klienta po instalacji. Potwierdza działanie Safety w docelowym środowisku z okablowaniem terenowym i warunkami przemysłowymi.

**Know-How Protection** — hasłowe zablokowanie podglądu i edycji kodu bloku FB/FC/DB. Program nadal się uruchamia i podlega monitoringowi online, lecz kodu logiki nie można odczytać.

**Copy Protection** — kryptograficzne powiązanie bloku z numerem seryjnym (Serial Number) konkretnego CPU. Blok nie uruchomi się na innym urządzeniu — zabezpieczenie przed kopiowaniem instalacji.

**ProDiag** — narzędzie TIA Portal do inline diagnostyki maszyny: stany wejść I/O, warunki zablokowania startu, komentarze diagnostyczne widoczne bezpośrednio na HMI bez osobnych ekranów alarmowych.

**Technology Object (TO)** — obiekt osi w TIA Portal (S7-1500) enkapsulujący napęd + enkoder + parametry jako jeden obiekt. API: MC_Power, MC_Home, MC_MoveAbsolute, MC_Halt, MC_Stop.

**OPC UA** — otwarty protokół komunikacji PLC ↔ SCADA/MES/chmura. Szyfrowanie TLS 1.2, certyfikaty X.509. Aktywowany w właściwościach CPU w TIA Portal. Wyższe opóźnienie niż PROFINET — nie stosować do sterowania real-time.

**Partial download (Software only changes)** — wgranie wyłącznie zmienionych bloków; CPU pozostaje w RUN. Szybsze i bezpieczniejsze niż pełne wgranie (All). Wymaga projektu skompilowanego bez błędów.

---

### Robot ABB IRC5

**EIO.cfg** — plik konfiguracyjny sygnałów I/O robota ABB. Definiuje nazwy, typy i mapowanie sygnałów PROFINET (Group Input, Group Output, Digital I/O). Edytowany w RobotStudio lub ręcznie.

**Group Output (GO)** — sygnał PLC → robot: liczba (numer programu, offset pozycji) przesyłana jako INT przez bajt/bajty PROFINET. Odczytywana w RAPID przez funkcję `GOutput()`.

**Group Input (GI)** — sygnał robot → PLC: potwierdzenie, status, kod błędu robota. Używany np. do sygnalizacji `ProgramDone`, `RobotReady`, `ErrorCode`.

**RobotReady** — sygnał robota do PLC potwierdzający gotowość do przyjęcia komendy start. PLC sprawdza ten sygnał przed wysłaniem `goProcess`.

**ProgramDone** — sygnał robota do PLC po wykonaniu zadanego ruchu/programu. PLC może wówczas wysłać kolejną komendę lub zmienić numer programu.

---

### SICAR@GST

**SICAR (Siemens Automotive Reference)** — framework programistyczny Siemens dla branży automotive (fabryki robotyczne: Toyota, BMW, VW). Zawiera szablony TIA Portal, biblioteki Tec Units, wzorce alarmów i ProDiag. Skraca czas programowania przez drag-and-drop gotowych bloków.

**Tec Unit** — gotowy, parametryzowalny blok funkcjonalny SICAR dla urządzenia (silnik, zawór, napęd, robot) zawierający: FB PLC z logiką, ekrany HMI, definicje alarmów, obsługę trybów Auto/Manual/Local.

**Betriebsartenbereiche** — obszary trybów pracy (strefy ochronne) w SICAR; max 12 obszarów definiujących różne konfiguracje bezpieczeństwa i sekwencje dla każdego trybu produkcyjnego.

**OM1 / OM2 / OM3 (Operation Mode)** — tryby operacyjne sekwencji w SICAR. Każdy tryb ma własne sekwencje dla każdego urządzenia; bloki biblioteczne współdzielone między trybami.
