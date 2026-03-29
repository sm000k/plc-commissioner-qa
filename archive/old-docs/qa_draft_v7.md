# KOMPENDIUM Q&A
### PLC Programmer / Commissioner / Automatyk
### Siemens TIA Portal · Safety PLC · ET200 · Napedy SINAMICS · Robot ABB · SICAR
### Pytania + odpowiedzi zweryfikowane pod katem rozmow kwalifikacyjnych.
### Zrodla: Siemens Application Example 21064024 (E-Stop SIL3 V7.0.1), Wiring Examples 39198632, SIMATIC Safety Integrated dokumentacja.
---
KOMPENDIUM Q&A
PLC Programmer / Commissioner / Automatyk
Siemens TIA Portal · Safety PLC · ET200 · Napędy SINAMICS · Robot ABB · SICAR
Pytania + odpowiedzi zweryfikowane pod kątem rozmów. Źródła: Siemens SIMATIC Safety Integrated, Wiring Examples 39198632, wiedza praktyczna, Siemens Application Example 21064024 (E-Stop SIL3 V7.0.1 02/2023).
  1. PODSTAWY PLC I AUTOMATYKI  
### 1.1. Co to jest PLC i czym różni się od zwykłego komputera?
PLC (Programmable Logic Controller) to przemysłowy komputer czasu rzeczywistego do sterowania maszynami. Kluczowe różnice:
• Deterministyczny scan cycle — program wykonywany cyklicznie z przewidywalnym czasem (ms)
• Odporność na EMI, drgania, temperatury, wilgoć przemysłową
• Dedykowane moduły I/O (DI, DO, AI, AO) bezpośrednio do czujników i aktuatorów
• Watchdog timer — CPU restartuje się przy zawieszeniu zamiast „wisieć"
• Brak systemu plików jak Windows — działa natychmiast po włączeniu zasilania
### 1.2. Co to jest scan cycle i ile trwa?
Scan cycle to jeden pełny cykl pracy CPU: odczyt wejść → wykonanie programu → zapis wyjść → komunikacja.
Typowy czas: 1–20ms dla prostych programów. Przy dużych projektach lub Safety może wzrosnąć do 50–100ms.
W S7-1500 monitorujesz czas cyklu online (Cycle time w diagnostyce CPU). Zbyt długi scan = wolna reakcja na sygnały.
### 1.3. Co to jest OB1, OB35, OB100 — kiedy każdego używasz?
Bloki organizacyjne (OB) to punkt wejścia do programu wywoływany przez system operacyjny CPU w ściśle określonych warunkach.

**Podstawowe OB:**
• OB1 — główny cykl programu, wykonywany ciągle. Tutaj trafia główna logika maszyny. Przerwany przez OB o wyższym priorytecie.
• OB35 — przerwanie cykliczne (np. co 100ms). Używasz dla PID, komunikacji z napędami, obliczeń niezależnych od obciążenia OB1. Wyższy priorytet niż OB1.
• OB100 — zimny start (Startup OB), wykonywany raz po przejściu CPU z STOP→RUN. Inicjalizacja zmiennych, reset stanu maszyny, wyzerowanie wyjść. W TIA Portal S7-1200/1500: jedyny OB startu (nie ma OB101/OB102 jak w starym S7-300).
• F_MAIN — Safety OB, oddzielny cykl dla programu failsafe, chroniony przez F-CPU.

**Diagnostyczne OB — ważne przy commissioning:**
• OB80 — cycle time exceeded (czas cyklu przekroczył watchdog). Sygnalizuje zbyt wolną logikę.
• OB82 — diagnostic error: moduł I/O zgłosił błąd diagnostyczny (np. zerwanie kabla, przegrzanie modułu F). W TIA Portal: blok RALRM lub ProDiag odbiera dane.
• OB86 — rack failure / PROFINET station failure. Wywołany gdy zdalna stacja (ET200SP, napęd) znika z sieci.
• OB121 / OB122 — błędy programistyczne (np. dostęp do nieistniejącej zmiennej) — ważne przy uruchamianiu nowego kodu.
### 1.4. Co to jest FB, FC, DB — kiedy używasz każdego?
• FC (Function) — blok bez pamięci własnej (brak sekcji VAR_STAT). Używasz dla prostych obliczeń, konwersji sygnałów, logiki bez stanu. Może zwracać wartość (Return Value). Ma tylko VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT i VAR_TEMP.
• FB (Function Block) — ma instancję DB z pamięcią stanu między wywołaniami (sekcja VAR_STAT). Używasz dla sterowania silnikiem, sekwencji, timerów — wszędzie gdzie blok musi "pamiętać". Multi-instance: jeden FB może zawierać instancje innych FB bez osobnych DB.
• DB (Data Block) — blok danych. Globalny DB: dostęp z całego programu. Instancja DB: dedykowana pamięć jednego FB.

**Typy zmiennych w blokach (ważne rozróżnienie):**
• `VAR_TEMP` — tymczasowe, przechowywane na stosie CPU. Tracą wartość po zakończeniu wywołania. Dostępne we wszystkich blokach (FB, FC, OB).
• `VAR_STAT` — statyczne, zachowują wartość między wywołaniami. Tylko w FB, przechowywane w instancji DB.
• `VAR_INPUT` / `VAR_OUTPUT` / `VAR_IN_OUT` — parametry interfejsu bloku.

W TIA Portal: bloki z włączonym *Optimized Block Access* używają wyłącznie nazw symbolicznych — brak adresowania absolutnego (%.0, %DB1.DBX0.0). Standardowe ustawienie dla nowych projektów.
### 1.5. Co to jest UDT i po co go używasz?
UDT (User Data Type) to własny złożony typ danych, np. typ 'Motor_t' z polami Speed:REAL, Current:REAL, Fault:BOOL, Running:BOOL.
Używasz gdy: masz wiele identycznych urządzeń (np. 20 silników — jeden FB + UDT zamiast 20 osobnych bloków), chcesz wymusić spójną strukturę danych, lub przekazujesz zestaw danych jako jeden parametr.
### 1.6. Co to są języki programowania PLC — LAD, FBD, SCL, GRAPH?
• LAD (Ladder) — graficzny, podobny do schematów przekaźnikowych. Dobry dla logiki binarnej, łatwy dla elektryków. Najczęściej używany.
• FBD (Function Block Diagram) — bloki połączone liniami. Dobry dla logiki kombinacyjnej i programów Safety w TIA Portal.
• SCL (Structured Control Language) — tekstowy, składnia podobna do Pascala (wysokopoziomowy). Używasz dla algorytmów, pętli, obliczeń matematycznych, obsługi tablic, przetwarzania STRING.
• GRAPH (SFC) — sekwencyjny, kroki i przejścia. Idealny dla sekwencji technologicznych (napełnianie, obróbka, mycie). Certyfikowany wg IEC 61131-3.
• STL (Statement List) — niskopoziomowy, lista instrukcji podobna do asemblera. Dostępny w TIA Portal ale uznawany za przestarzały — nie stosuj w nowych projektach.

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
- W Safety: program F_MAIN zawsze w FBD lub LAD (SCL nie jest certyfikowany dla F-bloków Safety w STEP 7 Safety Advanced do V18).
### 1.7. Co to jest sygnał 4-20mA i dlaczego nie 0-20mA?
4-20mA to standardowy sygnał analogowy dla czujników przemysłowych. Zakres 4mA (min) do 20mA (max).
Dlaczego 4 a nie 0: sygnał 0mA jednoznacznie oznacza zerwanie kabla lub awarię zasilania czujnika — łatwa diagnostyka. Przy 0-20mA nie da się odróżnić minimalnej wartości od awarii.
Sygnał prądowy ma też przewagę nad napięciowym (0-10V): nie spada na rezystancji kabla — można przesyłać na duże odległości bez strat.
### 1.8. Co to jest PROFINET i czym różni się od PROFIBUS?
PROFINET: Ethernet-based, 100Mbit, elastyczna topologia (gwiazdka, linia, pierścień), plug-and-play z GSDML, obsługuje PROFIsafe i IRT (izochroniczny). Nowy standard dla nowych projektów.
PROFIBUS: RS-485, max 12Mbit, liniowa topologia z terminatorami, starszy standard. Nadal spotykany w modernizacjach i starszych instalacjach.
W nowych projektach Siemens standardowo używa PROFINET.
### 1.9. Co to jest HMI i do czego służy w automatyce?
HMI (Human-Machine Interface) to panel operatorski umożliwiający operatorowi wizualizację i sterowanie procesem. Wyświetla: stany wejść/wyjść, alarmy, trendy wartości analogowych, tryby pracy maszyny.
W Siemensie: Simatic HMI (KTP, TP, MP serii) programowane w WinCC w TIA Portal — ta sama baza danych tagów co program PLC.
### 1.10. Co to jest SCADA i czym różni się od HMI?
HMI: lokalne, przy maszynie, obsługuje jeden obiekt/maszynę.
SCADA (Supervisory Control and Data Acquisition): system nadrzędny, monitoruje i archiwizuje dane z wielu maszyn/stacji jednocześnie, zazwyczaj na serwerze z komputerami PC. Siemens WinCC (pełna wersja SCADA) vs WinCC Basic/Advanced (HMI). SCADA zazwyczaj nie steruje bezpośrednio — nadzoruje.
### 1.11. Co to jest PID i kiedy go używasz w PLC?
PID (Proportional-Integral-Derivative) to algorytm regulacji zamkniętej utrzymujący zadany setpoint: temperatura, ciśnienie, poziom, prędkość.
• P — reaguje proporcjonalnie do aktualnego błędu
• I — eliminuje uchyb ustalony (sumuje błąd w czasie)
• D — reaguje na szybkość zmiany błędu (tłumi oscylacje)
W TIA Portal: gotowy blok PID_Compact lub PID_3Step w OB35 (cykliczne przerwanie). W Safety PID nie jest stosowany — logika Safety jest binarna.
  2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED  
### 2.1. Co to jest SIMATIC Safety Integrated i co oznacza 'wszystko w jednym sterowniku'?
SIMATIC Safety Integrated to koncepcja Siemensa gdzie funkcje bezpieczeństwa (failsafe) i funkcje standardowe działają w jednym fizycznym CPU (F-CPU), jednym projekcie TIA Portal i przez jedną sieć PROFINET/PROFIsafe.
Korzyści: jeden sterownik zamiast dwóch (standard + safety), ten sam inżyniering w TIA Portal, ta sama diagnostyka, mniej okablowania, mniejsza szafa sterownicza.
### 2.2. Co to jest F-CPU i jak działa dual-channel processing?
F-CPU (Fail-safe CPU) posiada dwa redundantne kanały obliczeniowe wykonujące te same obliczenia równolegle i porównujące wyniki. Jeśli wyniki się różnią → system przechodzi w bezpieczny stan. F-CPU jest certyfikowany przez TÜV dla SIL 3 (IEC 61508) / PL e (ISO 13849-1). Każdy F-CPU posiada SIL CL (Safety Integrity Level Claim Limit) podany w karcie katalogowej — wartość ta nie może być wyższa niż SIL wynikający z analizy ryzyka.
Dodatkowo F-CPU wykonuje ciągły self-test: pamięci RAM, ALU, rejestrów. Program Safety działa w oddzielnym chronionym obszarze pamięci — standardowy program nie może go nadpisać.
### 2.3. Jakie sterowniki Siemens obsługują funkcje Safety?
S7-1500F: CPU 1511F, 1513F, 1515F, 1516F, 1517F, 1518F — Advanced controllers z wbudowanym Safety.
S7-1200F: CPU 1212FC, 1214FC, 1215FC — Basic controllers z Safety, mniejsze aplikacje.
ET 200SP CPU F: CPU 1510SP F, 1512SP F — zdalny sterownik z Safety, montaż przy maszynie.
ET 200pro CPU F: CPU 1516pro F — IP67, bezpośrednio na maszynie.
Wszystkie programowane w TIA Portal z STEP 7 Safety Advanced lub Safety Basic.
### 2.4. Co to jest F-DB i dlaczego nie można go edytować ręcznie?
F-DB (Fail-safe Data Block) generowany jest automatycznie przez TIA Portal dla każdego bloku Safety. Zawiera: CRC (checksum logiki), F-signature (podpis programu Safety), parametry czasowe.
Ręczna edycja zniszczyłaby spójność podpisu → F-CPU odmówiłby uruchomienia Safety. To celowe zabezpieczenie przed nieautoryzowaną modyfikacją.
### 2.5. Co to jest F-signature i collective signature?
F-signature to unikalny podpis kryptograficzny jednego bloku Safety — zmienia się przy każdej modyfikacji kodu.
Collective signature (podpis zbiorczy) to podpis CAŁEGO programu Safety złożony ze wszystkich bloków. Widoczny na wyświetlaczu CPU lub w TIA Portal jako ciąg znaków (np. '5CBE6409').
Przy wgraniu CPU porównuje collective signature — niezgodność → Safety nie uruchamia się.
### 2.6. Jakie są tryby pracy Safety CPU i jak się przełącza?
LOCK — Safety program zablokowany, nie wykonuje się. Wyjścia Safety → wartości zastępcze.
RUN — Safety program działa normalnie.
Przełączenie przez TIA Portal (Safety Administration) lub dedykowany sygnał w logice. Po przełączeniu wymagane potwierdzenie (hasło Safety lub ACK). Zmiana trybu jest logowana z datą i użytkownikiem.
### 2.7. Co to jest STEP 7 Safety Advanced vs Safety Basic?
Safety Basic: licencja dla prostszych aplikacji, S7-1200F i ET 200SP F. Ograniczone funkcje, niższy koszt.
Safety Advanced: pełna licencja dla S7-1500F, wszystkie funkcje Safety, certyfikowane biblioteki funkcji (muting, two-hand, ESTOP), możliwość symulacji w PLCSIM.
Obydwie są wtyczką do TIA Portal — nie są osobnym oprogramowaniem.
  3. MODUŁY F-DI / F-DO — OKABLOWANIE I PARAMETRY  
### 3.1. Co to jest F-DI i jak różni się od standardowego DI?
F-DI (Fail-safe Digital Input) to moduł wejść bezpieczeństwa. Różnice od standardowego:
• VS* (pulse testing) — impulsowe zasilanie do diagnostyki okablowania
• Obsługa dwukanałowych czujników Safety (1oo2) z discrepancy time
• Cross-circuit detection — wykrywanie zwarć między kanałami
• Komunikacja przez PROFIsafe z CRC do F-CPU
• Self-test kanałów w tle
Moduły ET200SP F-DI, ET200MP F-DI, ET200eco F-DI, S7-1200 SM 1226 F-DI.
### 3.2. Co to jest VS* (pulse testing) i jak wykrywa usterki?
VS* to wyjście zasilające na module F-DI które wysyła krótkie impulsy testowe zamiast stałego napięcia. Czujnik zasilany jest tymi impulsami, a sygnał wraca na wejście razem z impulsami.
Moduł analizuje czy impulsy wróciły:
• Brak impulsów → zerwanie przewodu lub zwarcie do masy
• Impulsy cały czas bez przerwy → zwarcie do 24V
To mechanizm cross-circuit detection zapewniający Diagnostics Coverage (DC) bez dodatkowego okablowania. VS* z cross-circuit detection zapewnia DC ≥ 99% (Diagnostic Coverage) — warunek konieczny do osiągnięcia kategorii Cat.4 i Performance Level e (PL e) wymaganego przez SIL 3 per ISO 13849-1.
### 3.3. Dlaczego czujniki Safety podłącza się jako NC (normalnie zamknięty)?
Zasada bezpieczna (fail-safe): zerwanie kabla, przepalenie bezpiecznika, uszkodzenie czujnika → obwód otwarty → sygnał 0 → system Safety traktuje to jako zadziałanie i zatrzymuje maszynę.
Przy NO (normalnie otwartym): zerwanie kabla = brak sygnału = maszyna nie wie o zagrożeniu → niebezpieczeństwo.
NC to zasada 'fail-safe by design' wymagana przez normy bezpieczeństwa.
### 3.4. Co to jest discrepancy time i jak go konfigurujesz?
Discrepancy time to maksymalny czas w którym dwa kanały czujnika 1oo2 mogą pokazywać różne wartości bez generowania błędu. Przykład: przy otwieraniu osłony mechanicznej jeden styk reaguje 15ms wcześniej niż drugi — to normalne i fizyczne.
Konfigurujesz w TIA Portal: właściwości modułu F-DI → parametry kanału → Discrepancy time (typowo 10–200ms w zależności od czujnika).
Zbyt krótki → fałszywe błędy. Zbyt długi → późne wykrycie uszkodzenia.
### 3.5. Co to jest substitute value na F-DO i kto decyduje o jego wartości?
Substitute value to wartość którą przyjmuje wyjście F-DO po przejściu modułu w passivation (stan błędu). Konfigurujesz w TIA Portal we właściwościach kanału F-DO: wartość 0 lub 1.
Decyduje inżynier projektu na podstawie analizy bezpieczeństwa — nie Siemens. Przykłady: napęd → 0 (stop), zawór bezpieczeństwa → może być 1 (pozostaje otwarty), pompa chłodząca → może być 1 (chłodzi nadal).
### 3.6. Co to jest pm switching i pp switching — różnica?
pm switching (plus-minus): F-DO przełącza linię P (plus, 24V) do aktuatora. Masa (M) jest wspólna. Prostsze okablowanie, niższy koszt.
pp switching (plus-plus): F-DO przełącza obie linie P+ do aktuatora, bez wspólnej masy. Wyższy poziom bezpieczeństwa — zwarcie jednej linii do masy nie powoduje przypadkowego zadziałania. Używane przy wyższych wymaganiach SIL/PL.
F-PM-E (Power Module) w ET 200SP/S może realizować oba tryby.
### 3.7. Co to jest F-PM-E i do czego służy?
F-PM-E (Fail-safe Power Module E) to moduł zasilający Safety w systemie ET 200SP/S. Umożliwia bezpieczne odcięcie zasilania grupy standardowych modułów DO przez sygnał Safety — bez ich fizycznej wymiany na moduły F.
Działanie: F-CPU nakazuje F-PM-E odciąć 24V dla grupy standardowych DQ → wszystkie wyjścia grupy idą na 0 (PM switching do SIL2/Cat.3/PLd).
Tańsze rozwiązanie niż wymiana wszystkich DQ na F-DQ.
### 3.8. Jak bezpiecznie wyłączyć standardowe moduły wyjść przez Safety?
Trzy główne metody (wg dokumentu Siemens 39198632):
• Safety Relay (np. 3SK1) — zewnętrzny przekaźnik bezpieczeństwa odcina zasilanie grupy DQ. Niezależne od PLC.
• F-PM-E (pm lub pp switching) — moduł Safety w tej samej stacji ET200 odcina zasilanie grupy standardowych DQ (SIL2/Cat.3/PLd).
• F-DO + zewnętrzny przekaźnik — F-DO steruje cewką przekaźnika który odcina zasilanie modułów standardowych. Feedback z przekaźnika do DI.
Ważne: standardowe moduły DI nie mogą być używane do odczytu sygnałów Safety — wymagane F-DI.
  4. STRUKTURY GŁOSOWANIA — 1oo1/1oo2/2oo2/2oo3  
### 4.1. Wyjaśnij notację XooY i podaj przykład każdej architektury.
XooY = X z Y: ile (X) z dostępnych (Y) kanałów musi zadziałać aby system zareagował.
• 1oo1: 1 czujnik, 1 kanał. Bez redundancji — podstawa. Stosowane przy SIL1 lub gdzie analiza ryzyka dopuszcza.
• 1oo2: 2 czujniki, wystarczy że JEDEN zgłosi problem → zatrzymanie. Bezpieczniejsze, więcej fałszywych alarmów. Moduł F-DI weryfikuje discrepancy.
• 2oo2: 2 czujniki, OBA muszą zgłosić problem. Mniej fałszywych alarmów, ale jeden uszkodzony czujnik 'cichy' może przegazować zagrożenie.
• 2oo3: 3 czujniki, 2 z 3 muszą zadziałać. Balans bezpieczeństwa i dostępności — typowe w procesach ciągłych.
### 4.2. Kiedy wybierasz 1oo2 a kiedy 2oo2?
1oo2 gdy priorytet to bezpieczeństwo (zatrzymanie przy pierwszym sygnale) — np. osłony maszyn, e-stopy przy prasach. Wyższy SIL, akceptowalne fałszywe zatrzymania.
2oo2 gdy priorytet to dostępność (unikanie fałszywych stopów) — np. procesy chemiczne gdzie zatrzymanie jest bardzo kosztowne, ale jedno 'głuche' zadziałanie nie jest katastrofą.
Uwaga: przy 2oo2 uszkodzenie jednego kanału (zepsuty ale nie zgłaszający błędu) może spowodować że system nie zadziała gdy będzie potrzeba.
### 4.3. Jak 1oo2 jest realizowane w module F-DI Siemens?
Dwa sygnały z dwóch czujników podłączone na dwa kanały tego samego modułu F-DI (lub dwóch osobnych modułów). Moduł F-DI porównuje oba sygnały:
• Oba zgodne → OK
• Różnica przekracza discrepancy time → błąd → passivation lub alarm
Ewaluację 1oo2 wykonuje sam moduł F-DI sprzętowo — odciążając F-CPU. Wynik trafia do programu Safety jako jeden bezpieczny sygnał.
  5. PASSIVATION, REINTEGRATION, ACK  
### 5.1. Co to jest passivation i co się dzieje z wyjściami/wejściami?
Passivation to stan błędu modułu F: wszystkie wyjścia modułu przyjmują substitute value (zwykle 0), a wejścia raportowane są do F-CPU jako wartość bezpieczna (0).
Przyczyny passivation:
• Urwanie kabla lub zwarcie (wykryte przez pulse testing)
• Przekroczenie discrepancy time (1oo2)
• Utrata komunikacji PROFIsafe (przekroczenie F-monitoring time)
• Błąd wewnętrzny modułu
• Błąd spójności danych Safety
### 5.2. Dlaczego moduł nie wraca automatycznie po usunięciu błędu?
Celowo — żeby operator/technik wiedział że coś się stało i potwierdził że błąd faktycznie usunął. To zasada 'no silent recovery' w systemach Safety.
Mechanizm: po usunięciu błędu moduł czeka na reintegration. W bloku F w TIA Portal pojawia się ACK_REQ=TRUE. Operator musi podać impuls na ACK_NEC (np. przycisk 'Reset Safety' na HMI lub kasecie) → moduł wraca do normalnej pracy.
### 5.3. Moduł nie wychodzi z passivation — co sprawdzasz?
Krok po kroku:
• Czy błąd fizyczny faktycznie usunięty? (sprawdź kabel, czujnik multimetrem)
• Czy w diagnostyce TIA Portal brak aktywnych błędów modułu?
• Czy sygnał ACK_NEC podany jako impuls (zbocze), nie poziom stały?
• Czy F-CPU jest w trybie RUN Safety (nie LOCK)?
• Czy F-monitoring time nie jest przekroczony przez przeciążoną sieć?
• Czy nie ma drugiego ukrytego błędu na innym kanale tego modułu? Uwaga diagnostyczna: w S7-1200/S7-1500 tradycyjny bit QBAD zastąpiony jest przez value status (odwrotna logika: value status FALSE = wartości zastępcze, TRUE = prawidłowe dane procesowe) — sprawdź właściwą zmienną w Watch Table.
### 5.4. Co to jest ACK_REQ i ACK_NEC w praktyce?
ACK_REQ (Acknowledgement Required) — zmienna wyjściowa bloku F ustawiana automatycznie gdy moduł wymaga potwierdzenia po błędzie. Widzisz ją w Watch Table.
ACK_NEC (Acknowledgement Necessary) — zmienna wejściowa bloku F. Podajesz impuls (zbocze narastające) gdy chcesz potwierdzić błąd.
W praktyce: przycisk 'Reset' na HMI generuje jednorazowy impuls → ACK_NEC=TRUE na 1 cykl → moduł reintegruje się. Nie może być stałe TRUE — tylko impuls. Dla jednoczesnej reintegracji WSZYSTKICH modułów F w grupie runtime użyj bloku ACK_GL (z STEP 7 Safety Advanced) — generuje on zbiorczy impuls ACK do wszystkich F-I/O na raz po awarii komunikacyjnej lub błędzie kanałowym.
  6. SAFE STATE — BEZPIECZNY STAN  
### 6.1. Co to jest Safe State i kto go definiuje?
Safe State to stan systemu po wykryciu zagrożenia lub błędu Safety. Definiuje go inżynier projektu na podstawie analizy ryzyka maszyny — Siemens dostarcza tylko narzędzia.
Przykłady: prasa → stop silnika, pompa chemiczna → może pozostać WŁĄCZONA (stop = wyciek = gorsze), zawór odcinający → zależy od procesu (normalnie otwarty lub zamknięty).
### 6.2. Dlaczego Safe State to nie zawsze wyłączenie?
Bo wyłączenie może być BARDZIEJ niebezpieczne niż działanie. Przykłady:
• Pompa cyrkulacyjna reaktora — stop = przegrzanie = niekontrolowana reakcja
• Wentylator chłodzący transformator — stop = pożar
• Podajnik na linii produkcyjnej — nagły stop = zablokowanie i awaria mechaniczna
Dlatego substitute value F-DO może być 1 (wyjście aktywne przy passivation) — to decyzja inżyniera, nie Siemensa.
### 6.3. Jak F-DO substitute value wpływa na Safe State?
Parametr substitute value w TIA Portal (właściwości kanału F-DO) określa co wyjście robi przy passivation:
• substitute value = 0: wyjście wyłączone (napęd stop, zawór zamknięty)
• substitute value = 1: wyjście aktywne (pompa nadal działa, zawór otwarty)
To jest implementacja Safe State na poziomie sprzętowym — zadziała nawet przy awarii sieci komunikacyjnej.
  7. PROFISAFE — KOMUNIKACJA SAFETY  
### 7.1. Co to jest PROFIsafe i co zawiera jego pakiet?
PROFIsafe to protokół Safety działający na warstwie aplikacji ponad PROFINET lub PROFIBUS. Każdy pakiet PROFIsafe zawiera oprócz danych użytkownika:
• CRC (checksum) — wykrywa przekłamanie danych
• Licznik wiadomości — wykrywa utratę lub powtórzenie pakietu
• F-Address — wykrywa wysłanie pakietu do złego urządzenia
Dzięki temu wykrywa: utratę, powtórzenie, błędną sekwencję, przekłamanie, błędny adres — czego zwykły PROFINET nie robi.
### 7.2. Co to jest F-Address i jak go konfigurujesz?
F-Address (F-Destination Address) to unikalny adres Safety przypisany do każdego modułu F w sieci. Musi być identyczny w konfiguracji TIA Portal i na fizycznym urządzeniu (DIP switch, parametryzacja).
Konfigurujesz: właściwości modułu F w TIA Portal → Safety address. Błędny F-Address → moduł nie komunikuje się z F-CPU.
Przy wymianie modułu: nowy moduł musi dostać ten sam F-Address co stary — inaczej nie uruchomisz systemu.
### 7.3. Co to jest F-monitoring time i co się dzieje po jego przekroczeniu?
F-monitoring time to maksymalny czas oczekiwania F-CPU na kolejny pakiet PROFIsafe od modułu. Przy jego przekroczeniu (np. przerwa w sieci, przeciążenie switcha) → moduł zostaje spassivowany.
Ustawiasz w parametrach modułu Safety. Za krótki → fałszywe alarmy przy obciążeniu sieci. Za długi → wolne wykrywanie prawdziwej awarii komunikacji.
### 7.4. Jak Safety działa przez ET200 (zdalne I/O) i czym jest F-peripheral?
F-peripheral (fail-safe peripheral) to zdalne urządzenie I/O Safety podłączone do F-CPU przez PROFIsafe/PROFINET.
Przykłady: ET200SP z modułami F-DI/F-DQ, ET200eco F, ET200pro F — montowane przy maszynie (IP67).
F-CPU wysyła i odbiera pakiety PROFIsafe do każdego F-peripherala niezależnie. Każdy ma własny F-Address i F-monitoring time. Awaria jednego peripherala passivuje tylko ten moduł, nie cały system.
  8. NAPĘDY SAFETY — SINAMICS Z WBUDOWANYM SAFETY  
### 8.1. Co to jest STO (Safe Torque Off) i jak działa?
STO natychmiastowo odcina moment obrotowy — falownik blokuje impulsy PWM do silnika. Silnik wybiega (lub hamuje hamulec mechaniczny). Brak rampy hamowania.
Certyfikowany wg IEC 61800-5-2. Realizowany sprzętowo w dwóch kanałach wewnątrz napędu.
Różnica od wyłączenia programowego: STO jest monitorowane i potwierdzane przez napęd do F-CPU (sygnał STO_Active). Zwykłe wyłączenie — nie.
### 8.2. Jaka jest różnica między STO a zwykłym wyłączeniem napędu przez PLC?
Zwykłe wyłączenie: komenda programowa, nie monitorowana, nie certyfikowana Safety, nie spełnia wymogów SIL/PL. Napęd może technicznie nadal generować moment.
STO: certyfikowany SIL3/PLe, realizowany sprzętowo, napęd potwierdza brak momentu do F-CPU przez PROFIsafe. Napęd wymaga STO potwierdzenia zanim można wznowić pracę.
### 8.3. Co to jest SS1 i kiedy go używasz zamiast STO?
SS1 (Safe Stop 1): napęd hamuje wzdłuż zaprogramowanej rampy do zerowej prędkości, następnie aktywuje STO.
Używasz gdy natychmiastowe odcięcie momentu (STO) jest niebezpieczne — np. obrabiarka z dużymi masami inercyjnymi (ryzyko zderzenia narzędzia), winda, dźwig. Czas hamowania jest monitorowany — jeśli napęd nie zatrzyma się w czasie → natychmiastowe STO.
### 8.4. Co to jest SS2, SOS, SLS, SDI, SBC?
SS2 (Safe Stop 2): hamowanie z rampą → SOS (napęd nadal zasilony, trzyma pozycję). Używane gdy potrzeba szybkiego wstrzymania z zachowaniem pozycji.
SOS (Safe Operating Stop): napęd zasilony, trzyma pozycję z monitoringiem. Silnik nadal może wytworzyć moment jeśli oś się ruszy.
SLS (Safely Limited Speed): ograniczenie prędkości do bezpiecznego max — np. tryb serwisowy, operator w strefie.
SDI (Safe Direction): tylko jeden kierunek ruchu dozwolony — np. osłona otwarta, oś może jechać tylko od operatora.
SBC (Safe Brake Control): certyfikowane sterowanie hamulcem mechanicznym — monitoring prądu uzwojenia.
### 8.5. Jak STO jest realizowane sprzętowo — zaciski vs PROFIsafe?
Zaciski hardwarowe (STO1/STO2): bezpośrednie odcięcie sygnałów PWM przez zewnętrzny sygnał 24V z modułu Safety. Szybsze (bez opóźnienia sieci), prostsze, niezależne od komunikacji.
PROFIsafe: komenda STO przesyłana przez PROFINET. Umożliwia zaawansowane funkcje (SS1, SLS, SDI, diagnostyka przez sieć). Wymaga sprawnego połączenia sieciowego.
W praktyce: przy G120/S120 można łączyć oba sposoby — PROFIsafe dla zaawansowanych funkcji + zaciski STO jako backup.
### 8.6. Co sprawdzasz przy commissioning napędu z STO?
Procedura:
• Podaję sygnał STO (przez zaciski lub PROFIsafe) — weryfikuję że napęd zatrzymał się i nie ma momentu
• Sprawdzam potwierdzenie STO_Active w statusie napędu (w TIA Portal lub Startdrive)
• Weryfikuję że nie można uruchomić napędu gdy STO aktywne
• Zdejmuję STO — sprawdzam poprawny restart
• Testuję czas reakcji
• Sprawdzam poprawność adresu PROFIsafe jeśli używany
• Dokumentuję wyniki z podpisem
  9. TIA PORTAL — SAFETY PRAKTYKA  
### 9.1. Jak wygląda struktura programu Safety w TIA Portal?
Program Safety w TIA Portal składa się z:
• F-OB (Safety Main OB, np. Main_Safety_RTG1) — główny cykl Safety, odpowiednik OB1 dla Safety
• F-FB / F-FC — bloki logiki Safety programowane w F-LAD lub F-FBD
• F-DB — instancje bloków, generowane automatycznie przez TIA Portal
Kompilacja Safety generuje CRC dla każdego bloku i collective signature dla całości. Program Safety jest logicznie oddzielony od standardowego OB1.
### 9.2. Jak przekazujesz sygnał z obszaru F do standardowego OB?
Z F do standard: poprzez F-DB — zmienne wynikowe Safety są dostępne do odczytu ze standardowego programu. Przykład: F-DB.SafetyOK (BOOL) możesz odczytać w OB1 do wyświetlenia na HMI lub logowania.
Ze standard do F: przez dedykowane zmienne 'safe interlock' — standardowy program może pisać do specjalnych zmiennych które F-CPU traktuje jako niezaufane (nie używa do decyzji Safety).
Bezpośredni zapis ze standardowego do F-DB — zablokowany. Zalecany wzorzec Siemens (wg doc. 21064024): dwa globalne DB — DataFromSafety (zapisuje F-program, czyta standard) i DataToSafety (zapisuje standard, czyta F-program). Synchronizacja przez konsekwentne używanie tych DB eliminuje ryzyko niezamierzonego wpływu programu standardowego na logikę Safety.
### 9.3. Jak wgrywasz zmianę w programie Safety?
Modyfikujesz logikę F → kompilacja → TIA Portal ostrzega o zmianie F-signature → wymagane potwierdzenie zmiany (kliknięcie Accept lub hasło Safety) → wgranie do CPU (Download) → CPU weryfikuje collective signature → Safety RUN.
Każda zmiana jest logowana z datą i użytkownikiem w projekcie TIA Portal.
### 9.4. Co się dzieje gdy F-signature nie zgadza się po wgraniu?
F-CPU nie uruchamia programu Safety i zgłasza błąd 'F-signature mismatch'. Przyczyny: niekompletne wgranie, wgranie programu z innego projektu, ingerencja w F-DB.
Rozwiązanie: skompiluj projekt ponownie (Compile → Software) i wykonaj pełne wgranie (Download to device → All). Nie próbuj edytować F-DB ręcznie.
### 9.5. Jak czytasz diagnostykę F-modułu online w TIA Portal?
Online → w drzewie projektu rozwiń moduł F → Device diagnostics → zakładka Diagnostics.
Widzisz: status passivation (TAK/NIE), aktywne błędy kanałów (urwanie, zwarcie, discrepancy), status komunikacji PROFIsafe, liczniki błędów.
Alternatywnie: Watch Table z zmiennymi F-DB modułu (DIAG, PASS_OUT, ACK_REQ, QBAD).
### 9.6. Co to jest PLCSIM i jak pomaga w Safety?
PLCSIM to symulator TIA Portal umożliwiający testowanie programu PLC bez fizycznego sprzętu. Obsługuje również programy Safety — możesz symulować działanie F-CPU, testować logikę Safety, weryfikować ACK, passivation, reintegration.
Oszczędza czas commissioning bo błędy logiczne wyłapujesz przed wyjazdem do klienta. Nie zastępuje testów na prawdziwym sprzęcie dla certyfikacji — ale znacznie skraca czas FAT.
  10. ROBOT ABB IRC5 — INTEGRACJA Z PLC  
### 10.1. Jak przebiega komunikacja Siemens PLC z robotem ABB IRC5?
Przez PROFINET: Siemens PLC = master (controller), robot ABB IRC5 = slave (device).
Konfiguracja: 1) W RobotStudio konfigurujesz PROFINET slave i sygnały I/O w pliku EIO.cfg. 2) Eksportujesz GSDML z IRC5. 3) W TIA Portal importujesz GSDML — robot widoczny jak każde urządzenie PROFINET. 4) Mapujesz adresy wejść/wyjść. 5) Ustawiasz IP robota i nazwę PROFINET zgodną z RobotStudio.
### 10.2. Co to jest GSDML i jak go instalujesz w TIA Portal?
GSDML (General Station Description Markup Language) to plik XML opisujący urządzenie PROFINET — jego moduły I/O, parametry, obsługiwane adresy.
Instalacja: TIA Portal → Options → Manage general station description files → Install → wskazujesz plik GSDML.
Plik GSDML dla ABB IRC5 znajdziesz w folderze instalacji RobotStudio lub w IRC5 controller disk.
### 10.3. Jak PLC wysyła numer programu do robota i jak robot go odczytuje?
Po stronie robota (EIO.cfg): definiujesz Group Input (GI) — np. GI_ProgramNumber, 8 bitów, zmapowany na bajt z PROFIsafe/PROFINET.
Po stronie PLC (TIA Portal): piszesz wartość INT (np. 5) do obszaru wyjść PROFINET przypisanego do robota.
Po stronie RAPID (kod robota): nrProgram := GInput(GI_ProgramNumber); a następnie SELECT nrProgram → IF 1 → MoveL pos1 → IF 2 → MoveL pos2 itd.
### 10.4. Jak działa przesyłanie offsetu pozycji z PLC do RAPID?
PLC wysyła wartość offsetu (np. X, Y w mm×10 jako INT, żeby uniknąć przecinka) przez Group Input PROFINET.
W RAPID: offsetX := GInput(GI_OffsetX) / 10.0;
Dodajesz do pozycji bazowej: targetPos := Offs(basePos, offsetX, offsetY, 0);
MoveL targetPos, v100, fine, tool1;
Metoda stosowana przy systemach wizyjnych i zmiennych pozycjach detali.
### 10.5. Jak debugujesz brak komunikacji PROFINET między PLC a robotem?
Kolejność sprawdzania:
• Czy robot ma poprawne IP i nazwę PROFINET (zgodne z TIA Portal)?
• Ping z PLC do IP robota — czy odpowiada?
• W TIA Portal diagnostyka PROFINET — czy urządzenie widoczne w sieci?
• W RobotStudio — czy interfejs PROFINET aktywny, czy sygnały skonfigurowane?
• Czy GSDML wersja pasuje do wersji RobotWare (starsze RW → starszy GSDML)?
• Czy nie ma duplikatu nazwy PROFINET w sieci?
  11. COMMISSIONING I DIAGNOSTYKA  
### 11.1. Co sprawdzasz przed pierwszym RUN Safety?
Checklistа przed pierwszym uruchomieniem:
• Poprawność okablowania modułów F (VS*, NC, dwukanałowe)
• F-Address zgodny w TIA Portal i na modułach fizycznych
• Collective signature skompilowana i wgrana kompletnie
• Substitute values ustawione zgodnie z projektem Safety
• Discrepancy time dopasowany do czujników
• ACK_NEC podpięte do przycisku Reset
• F-monitoring time skonfigurowany dla sieci Przypisanie adresów PROFIsafe: w TIA Portal → Devices & Networks → PPP zrób "Assign PROFIsafe address" → wskaż moduł → kliknij Identification → gdy diody LED modułu migają zielono jednocześnie → zaznacz Confirm → Assign. Adres zapisywany jest w elektronicznym elemencie kodującym modułu — przy wymianie modułu new module inherit old F-Address automatycznie jeśli element kodujący pozostaje.
• Safety CPU w trybie RUN
• Dokumentacja Safety dostępna (Safety plan, listy testów)
### 11.2. Jak testujesz e-stop podczas commissioning?
Procedura:
• Uruchom maszynę w trybie wolnym/testowym przy bezpiecznej prędkości
• Wciśnij e-stop — weryfikuj natychmiastowe zatrzymanie WSZYSTKICH osi/napędów
• Sprawdź że nie można uruchomić maszyny z wciśniętym grzybkiem
• Odblokuj e-stop (przekręć) i wykonaj ACK — sprawdź poprawny powrót do RUN
• Powtórz dla KAŻDEGO e-stopu w każdej lokalizacji na maszynie
• Zmierz i zapisz czas reakcji (od wciśnięcia do zatrzymania)
• Dokumentuj wynik z datą i podpisem
### 11.3. Co to jest FAT i SAT w kontekście Safety?
FAT (Factory Acceptance Test) — testy w zakładzie dostawcy maszyny przed wysyłką. Lista testów każdej funkcji Safety, podpisywana przez dostawcę i klienta.
SAT (Site Acceptance Test) — testy u klienta po instalacji. Potwierdza że Safety działa poprawnie w docelowym środowisku (okablowanie terenowe, warunki przemysłowe).
Dla Safety: oba zawierają obowiązkowe testy każdego e-stopu, kurtyny, krańcówek — wyniki dokumentowane i podpisywane.
### 11.4. Jak postępujesz gdy odkryjesz błąd w logice Safety po FAT?
Nie modyfikujesz samodzielnie bez formalnej zgody — Safety wymaga ścieżki Change Request.
Zgłaszam do Safety Engineer / project managera. Zmiana → nowa F-signature → wymaga ponownej akceptacji. Dokonuję modyfikacji, kompiluję, wgrywam. Przeprowadzam testy regresji (retesty dotkniętych funkcji). Dokumentuję: co zmieniono, kiedy, kto zatwierdził, wyniki testów po zmianie.
### 11.5. Jakie są najczęstsze przyczyny passivation F-DI w praktyce?
Z doświadczenia commissionerów:
• Zerwany kabel czujnika (najczęściej)
• Czujnik NC 'przyklejony' w pozycji otwartej — uszkodzony mechanicznie
• Źle przyłączony VS* (brak zasilania impulsowego)
• Discrepancy time za krótki dla danego czujnika/prędkości
• Utrata komunikacji PROFIsafe przez przeciążony switch sieciowy
• Złe ustawienie F-monitoring time
• Zwarcie do 24V na wejściu (np. łączenie kabli w trasie kablowej)
### 11.6. Jak reagować gdy moduł F świeci błędem którego nie możesz skasować?
Systematycznie:
• Odczytaj dokładny kod błędu z diagnostyki TIA Portal (nie tylko status LED)
• Sprawdź czy błąd fizyczny usunięty (kabel, czujnik)
• Sprawdź czy ACK_NEC podany jako impuls (nie stały poziom)
• Czy F-CPU jest w trybie RUN Safety?
• Przy błędzie wewnętrznym modułu: wymień moduł, zachowaj ten sam F-Address
• Przy błędzie F-signature: pełna rekompilacja + pełne wgranie
• Jeśli nic nie pomaga: backup projektu + CPU restart
  12. SICAR I NAPĘDY SINAMICS  
### 12.1. Co to jest SICAR i gdzie jest używany?
SICAR (Siemens Automation Platform for CAR Plants) to gotowy framework programistyczny Siemensa dla branży automotive (fabryki: Toyota, Tesla, BMW, VW). Oparty na TIA Portal.
Zawiera: szablony PLC i HMI, biblioteki Tec Units (gotowe bloki dla silników, zaworów, napędów, robotów), wzorce alarmów, ProDiag dla diagnostyki. Cel: skrócenie czasu programowania przez drag-and-drop gotowych bloków zamiast pisania od zera.
### 12.2. Co to są Tec Units i jak z nich korzystasz?
Tec Units to gotowe, parametryzowalne bloki funkcjonalne w SICAR dla typowych urządzeń: silnik, zawór, przenośnik taśmowy, napęd, robot. Każdy zawiera: FB PLC z logiką, ekrany HMI, definicje alarmów, obsługę trybów (Auto/Manual/Local).
Używasz przez drag-and-drop Tec Unit na projekt, ustawiasz parametry (adres I/O, limity, czasy), gotowe. Nie piszesz logiki od podstaw.
### 12.3. Co to jest SINAMICS Startdrive w TIA Portal?
SINAMICS Startdrive to wtyczka do TIA Portal do parametryzacji, uruchamiania i diagnostyki napędów SINAMICS (G120, S120, V90) bezpośrednio z TIA Portal — bez osobnego oprogramowania Starter.
Umożliwia: konfigurację napędu, autotuning, monitoring parametrów online, diagnostykę błędów, konfigurację Safety (STO, SS1, SLS przez PROFIsafe).
### 12.4. Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?
W SINAMICS Startdrive (TIA Portal):
• Dodajesz napęd G120 do projektu (CU240E-2 PN lub CU250S-2 PN), konfigurujesz PROFINET i telegram (`p0922`)
• W zakładce Safety Integrated: włączasz PROFIsafe, ustawiasz F-Address (musi być identyczny w TIA Portal i napędzie)
• Wybierasz funkcje Safety: STO, SS1 (`p9560` = ramp time), SLS (`p9531` = max prędkość)
• Autotuning: Static motor identification → Speed controller optimization (p.szczeg. → Sekcja 19)
• Weryfikacja Safety: test STO, accept safety settings → Safety checksum/Safety ID
Po stronie F-CPU: blok Safety dla napędu (F-FB dla G120 z biblioteki) odbiera/wysyła telegram PROFIsafe.
Pełna procedura krok po kroku: → Sekcja 19 (Commissioning — Dodawanie napędu G120).
  13. E-STOP — NORMY, IMPLEMENTACJA I OBLICZENIA BEZPIECZEŃSTWA  

### 13.1. Jakie są kategorie zatrzymania wg EN 60204-1 i jak wpływają na wybór STO vs SS1?
Kategoria 0 (Stop niekontrolowany): natychmiastowe odcięcie zasilania napędów — odpowiada STO (Safe Torque Off). Oś wybiega swobodnie lub hamowana hamulcem mechanicznym. Stosuj gdy wybieg jest akceptowalny i bezpieczny.
Kategoria 1 (Stop kontrolowany): napęd hamuje wzdłuż rampy do zatrzymania, następnie odcięcie zasilania — odpowiada SS1 (Safe Stop 1). Stosuj gdy inercja maszyny (prasy, obrabiarki, dźwigi) wyklucza bezpieczny wybieg.
Kategoria 2 (Stop kontrolowany z zachowanym zasilaniem): hamowanie z rampą, napęd pozostaje zasilony i monitoruje pozycję — odpowiada SS2 → SOS. Stosuj gdy po zatrzymaniu oś musi trzymać pozycję (ramiona robotów, pionowe slide).
Uwaga normatywna: EN 60204-1 wymaga, by e-stop realizował kategorię 0 lub 1 (nie 2) chyba że analiza ryzyka uzasadnia inaczej.
### 13.2. Co to jest LSafe_EStop i gdzie go znajdziesz w TIA Portal?
LSafe_EStop to certyfikowany przez TÜV blok funkcjonalny z biblioteki LSafe (STEP 7 Safety Advanced). Realizuje kompletną logikę e-stopu: odcięcie wyjścia aktuatora, blokadę restartu, sekwencję ACK i monitorowanie styczników.
Wejścia kluczowe: eStop (BOOL, NC — FALSE = e-stop wciśnięty), start/stop, acknowledge (impuls), feedback1/feedback2 (zwrotne styczniki), feedbackTime (max czas reakcji stycznika), actuatorVS (value status F-DO).
Wyjścia: actuator (BOOL — steruje F-DO → styczniki), acknowledgeRequestedEStop (TRUE = wymagane ACK), eStopReleased (TRUE = e-stop odblokowany), fault (błąd logiki lub stycznika).
Lokalizacja w TIA Portal: Safety Advanced → Libraries → LSafe → LSafe_EStop. Blok musi być wywołany z Safety OB (F_MAIN lub Safety Main OB).
Ważne: oba kanały e-stopu (2xNC) podłączone do jednego pary kanałów F-DI z ewaluacją 1oo2 — sam moduł F-DI dostarcza już jeden przetworzony sygnał BOOL do bloku (kanały nie są widoczne osobno w programie).
### 13.3. Co to jest feedback circuit (obwód sprzężenia zwrotnego styczników) i dlaczego jest wymagany dla SIL 3 / PL e?
Feedback circuit to monitorowanie stanu styków pomocniczych (NC, pozytywnie sterowanych) styczników wykonawczych podłączone z powrotem na wejście DI lub F-DI.
Cel: wykrywanie zgrzania (welding) lub zacięcia styku stycznika. Zgrzany styk = kontakt NC pozostaje otwarty mimo odcięcia cewki → feedback = niezgodność → maszyna nie może wystartować.
Dla Cat.4 / PL e / SIL 3 wymagana jest REDUNDANCJA ścieżki wyłączania (2 styczniki szeregowo lub równolegle) PLUS monitoring feedback obydwu — bez tego system nie spełnia DC ≥ 99% w podsystemie Reaction.
Parametr feedbackTime w LSafe_EStop definiuje max czas w którym stycznik musi się przełączyć po komendzie (typowo 100–300ms). Przekroczenie → fault na bloku.
Połaczenie styczników: pozytywne otwarcie (EN 60947-5-1) — jeśli cewka odcięta, styk NC jest MECHANICZNIE zmuszony do otwarcia nawet przy zgrzaniu. Wymagane przez normy w obwodach Safety.
### 13.4. Co to są CCF (Common Cause Failure) i jakie środki są wymagane dla Cat.4?
CCF (Common Cause Failure / Usterka wspólnej przyczyny) to scenariusz gdzie JEDNA przyczyna (np. przepięcie, temperatura, EMC, błąd montaży) uszkadza oba kanały redundantnego systemu jednocześnie — co pozbawia system odporności na błędy.
ISO 13849-1 Tablica F.1 wymaga minimum 65 punktów CCF dla architektury Cat.3 i Cat.4. Punkty przyznawane za środki jak: separacja/oddzielenie tras kablowych kanałów (+15), różne technologie czujników (+20), ochrona EMC (+25), warunki środowiskowe (+10) itd.
W praktyce: prowadź kable kanału 1 i 2 w osobnych trasach, stosuj różnych producentów czujników (diverse redundancy), zachowuj separację przestrzenną.
Siemens F-DI realizuje diagnostykę cross-circuit (zwarcie między kanałami) i pulse-testing — ale CCF środki leżą po stronie projektu i montażu, nie CPU.
### 13.5. Jak wygląda łańcuch Safety dla e-stopu: Detection → Evaluation → Reaction i co liczy się do PFH?
Zgodnie z ISO 13849-1 (i weryfikacją w TIA Selection Tool) cały łańcuch bezpieczeństwa dzielony jest na podsystemy:
Detection (Detekcja): przycisk e-stop (2×NC, Cat.4). Parametry: B10=100,000 ops, udNiebezpieczny=20%, T1=175,200h, CCF≥65, DC≥99% (cross-comparison F-DI). Wynik przykładowy: PFHD = 9.06×10⁻¹⁰ → PL e.
Evaluation (Ewaluacja): F-CPU + F-DI + F-DQ komunikujące przez PROFIsafe. Dane z karty katalogowej Siemens: CPU 1516F PFHD = 2.0×10⁻⁹, F-DI = 1.0×10⁻⁹, F-DQ = 2.0×10⁻⁹. Suma = 5.0×10⁻⁹ → PL e.
Reaction (Reakcja): styczniki (2 szeregowo, Cat.4). Parametry: B10=1,000,000 ops, udNiebezpieczny=73%, T1=175,000h, CCF≥65, DC≥99% (feedback monitoring). Wynik: PFHD = 1.45×10⁻⁹ → PL e.
Łącznie: PFHD_total = 9.06×10⁻¹⁰ + 5.0×10⁻⁹ + 1.45×10⁻⁹ ≈ 7.35×10⁻⁹ → PL e (granica SIL 3: PFHD < 10⁻⁷).
Narzędzie: Siemens TIA Selection Tool (wbudowane w TIA Portal lub online) automatyzuje obliczenia — wymagaj od klienta wymagań PL/SIL przed doborem sprzętu.
### 13.6. Czy można łączyć przyciski e-stop szeregowo do jednego wejścia F-DI?
Tak, ale z ograniczeniami. EN ISO 13850 i IEC 62061 dopuszczają szeregowe połączenie e-stopów TYLKO jeśli można wykluczyć jednoczesne naciśnięcie dwóch e-stopów ORAZ jednoczesne wystąpienie awarii i naciśnięcia.
Problem: przy szeregowym połączeniu nie wiadomo KTÓRY e-stop zadziałał → brak diagnostyki granularnej. Siemens zaleca oddzielne kanały F-DI per e-stop dla szybszej lokalizacji usterek i lepszej diagnostyki ProDiag/HMI.
Praktyczny kompromis Siemens (wg doc. 21064024): każdy e-stop na osobnej parze kanałów F-DI z 1oo2 evaluation → każdy e-stop widoczny osobno w diagnostyce TIA Portal i na HMI.
Jeśli szeregowo: każde zadziałanie to osobna "supplementary safety function" — analiza ryzyka musi obejmować wszystkie e-stopy indywidualnie.
  14. PROFINET — TOPOLOGIA, DIAGNOSTYKA I ZAAWANSOWANE FUNKCJE  

### 14.1. Co to jest MRP (Media Redundancy Protocol) i kiedy go stosujesz?
MRP to protokół redundancji Ethernet w topologii pierścieniowej PROFINET. W konfiguracji normalnej pierścień działa jak linia — jeden port jest zablokowany przez MRM (Media Redundancy Manager, zazwyczaj switch lub CPU). Przy zerwaniu przewodu zablokowany port otwiera się i ruch odbywa się w drugą stronę — czas przełączenia ≤ 200ms (MRP, max 50 urządzeń) lub ≈ 0ms (MRPD — Media Redundancy with Planned Duplication, wymaga trybu IRT). Uwaga: termin 'Fast-MRP' nie jest oficjalnym pojęciem PROFINET — nie używaj go na rozmowie. Stosujesz gdy linia produkcyjna wymaga wysokiej dostępności sieci i awaria pojedynczego kabla nie może zatrzymać produkcji. Konfiguracja: TIA Portal → Network view → właściwości switcha/CPU → PROFINET → Media redundancy → ustaw role MRM/MRC.
### 14.2. Co to jest IRT (Isochronous Real-Time) i kiedy jest wymagany?
IRT (Isochronous Real-Time) to tryb PROFINET z deterministyczną synchronizacją cyklu do 250µs i jitterem < 1µs, realizowaną sprzętowo na poziomie ASIC. Wymagany przy aplikacjach motion control z omotion synchronization (SINAMICS S120 w trybie synchronicznym, systemy wieloosiowe). Różnica od RT (Real-Time, standard): RT działa programowo, cykl ~1ms, jitter kilka–kilkanaście µs — wystarczający dla standardowych I/O i robotów. IRT wymaga zarządzanych switchów Siemens (np. SCALANCE X) lub topologii gwiazdki z CPU obsługującym IRT.
### 14.3. Jak diagnostykujesz sieć PROFINET w TIA Portal i PRONETA?
W TIA Portal: Online → rozwiń Devices & Networks → kliknij prawym na urządzenie → Diagnose → zakładka Diagnostics. Widać: stan komunikacji, aktywne alarmy, topology view (połączenia portów). Pomocne: "Go online" → mapa sieci ze statusami. PRONETA (bezpłatne narzędzie Siemens): standalone diagnostics PROFINET, skanuje sieć niezależnie od TIA Portal, pokazuje mapę urządzeń, nazwy, IP, porty. Użyteczne gdy nie masz projektu TIA ani dostępu do sterownika — np. przy szybkiej diagnozie u klienta.
### 14.4. Co to jest Shared Device i kiedy go używasz?
Shared Device (PROFINET) to urządzenie I/O które jest jednocześnie w dwóch projektach / sterowanych przez dwa kontrolery, przy czym każdy kontroler ma przypisany inny zakres modułów. Przykład: stacja ET200SP z 16 slotami — CPU A zarządza slotami 1–8, CPU B slotami 9–16. Stosowane przy integracji systemów Safety z systemem standardowym obsługiwanym przez różnych dostawców PLC, lub gdy aplikacja Safety i standardowa mają osobne sterowniki. Konfiguracja: TIA Portal → właściwości urządzenia → Advanced Settings → Shared Device.
### 14.5. Jak działa Device replacement bez PG (automatic name assignment)?
Przy wymianie urządzenia PROFINET bez laptopa z TIA Portal CPU może automatycznie przypisać nazwę PROFINET nowemu modułowi na podstawie swojej konfiguracji. Warunek: w TIA Portal włączone "Support device replacement without exchangeable medium" (domyślnie włączone w S7-1500). Procedura: wymień fizycznie urządzenie (ten sam typ) → po podłączeniu do sieci CPU widzi urządzenie bez nazwy → CPU porównuje topologię (numery portów switch) → przypisuje nazwę automatycznie. Nie działa jeśli nowe urządzenie ma inny typ lub gdy topologia jest niejednoznaczna.
  15. KURTYNY BEZPIECZEŃSTWA I MUTING  

### 15.1. Czym różni się kurtyna bezpieczeństwa Type 2 od Type 4 (IEC 61496)?
Type 2: wymaga weryfikacji poprawności działania przez zewnętrzny moduł testujący (External Test Device), DC typowo 60–99%. Przy poprawnej architekturze 2-kanałowej (1oo2) może osiągnąć do PL d / SIL 2 — NIE jest ograniczona do PL c / SIL 1. Przykłady: kurtyny z zewnętrznym monitoringiem OSSD. Type 4: najwyższy poziom, DC ≥ 99%, kategoria Cat.4, pełna wewnętrzna diagnostyka (self-testing) w każdym cyklu bez zewnętrznego modułu, dopuszczony do PL e / SIL 3. Pojedyncza usterka nie prowadzi do utraty funkcji Safety. W robotyzowanych liniach automotive (prasy, roboty) wymagana jest kurtyna Type 4. W TIA Portal podłączasz ją jako F-DI z 1oo2 evaluation lub OSSD (Output Signal Switching Device) bezpośrednio na wejście Safety.
### 15.2. Jak działa muting i czym różni się od override?
Muting to tymczasowe, automatyczne zawieszenie funkcji kurtyny bezpieczeństwa przez program Safety (bez ingerencji operatora) gdy spełnione są określone warunki fizyczne. Przykład: paleta wjeżdża na taśmo na linię — czujniki mutingowe po obu stronach muszą oba zadziałać w czasie < 4s, tylko wtedy kurtyna jest zawieszona na czas przejazdu palety. Muting jest powtarzalny i automatyczny.
• Override: ręczne (operator), jednorazowe, wymaga klucza lub przycisku z podtrzymaniem, z licznikiem i logowaniem. Stosowany tylko serwisowo — np. usuwanie zakleszczonego materiału.
• Kluczowa różnica prawna: muting to element projektu Safety (uwzględniony w ocenie ryzyka), override to środek awaryjny z ograniczonym dostępem.
• W TIA Portal: certyfikowany blok MUTING_FKT (z biblioteki LSafe) obsługuje schematy 4-czujnikowe (cross i parallel). Wymaga 2 par czujników i okna czasowego sekwencji.
### 15.3. Jak podłączasz OSSD (Output Signal Switching Device) kurtyny do modułu F-DI?
OSSD to para wyjść kurtyny (OSSD1, OSSD2) — dwa kanały sygnałów bezpieczeństwa z wbudowanym testowaniem impulsowym. Podłączasz OSSD1 → kanał A modułu F-DI, OSSD2 → kanał B, jako parę 1oo2. Ważne: NIE podłączaj zasilania VS* (pulse test) modułu F-DI do OSSD — kurtyna sama generuje własne impulsy testowe. W TIA Portal ustaw parametr "Sensor supply" tego kanału na "None" lub "Disabled" — inaczej impulsy F-DI zablokują sygnał z kurtyny. Discrepancy time: dopasuj do specyfikacji kurtyny (zazwyczaj 10–30ms).
  16. MOTION CONTROL I SINAMICS — PRAKTYKA COMMISSIONING  

### 16.1. Co to jest Technology Object (TO) w TIA Portal i jak go używasz?
Technology Object to abstrakcja osi w TIA Portal dla motion control (dostępna w S7-1500, ET200SP CPU). TO enkapsuluje napęd + enkoder + parametry osi jako jeden obiekt z gotowym API w SCL: MC_Power, MC_Home, MC_MoveAbsolute, MC_MoveVelocity, MC_Halt, MC_Stop. Typy TO: TO_SpeedAxis (tylko prędkość), TO_PositioningAxis (pozycjonowanie absolutne/względne), TO_SynchronousAxis (synchronizacja do osi master), TO_ExternalEncoder. Konfiguracja: TIA Portal → Add new object → Technology object → wybierz typ → przypisz napęd (SINAMICS przez telegram PROFIdrive 105/111). Sterowanie z programu: wywołujesz bloki MC_ jak każde FB z instancją DB.
### 16.2. Jak robisz autotuning napędu G120/V90 w Startdrive?
Startdrive (wtyczka TIA Portal): Online → wybierz napęd → Commissioning → Motor identification. Procedura:
• Motor identification (statyczna, silnik stoi): Startdrive → Drive → Commissioning → Motor identification → Static → Start. Trwa ~30s, napęd mierzy rezystancję i induktancję uzwojeń. Wymagane uziemienie silnika, napęd w stanie Ready.
• Speed controller optimization (dynamiczna, silnik się obraca): Motor identification → Speed controller optimization → Start. Silnik wykonuje sekwencję ruchów testowych — odblokuj strefę bezpieczeństwa. Wyznacza Kp (wzmocnienie) i Ti (czas całkowania) regulatora prędkości.
• Po autotuningu: sprawdź r0047 (status identyfikacji) = 0 brak błędu. Parametry zapisane automatycznie w napędzie.
• Jeśli napęd mechatronicznie połączony z ciężką maszyną: uruchom identyfikację na biegu jałowym lub przy odłączonej mechanice, a potem ręcznie dostraj Kp.
### 16.3. Jakie są najważniejsze parametry SINAMICS G120 które musisz znać?
Podstawowe parametry diagnostyczne i konfiguracyjne:
• p0840 — ON/OFF1 (komenda rozruchu z PLC lub przez terminal). Źródło sygnału start.
• p1120 — czas rozruchu rampy (ramp-up time) w sekundach od 0 do max prędkości.
• p1121 — czas hamowania rampy (ramp-down time).
• r0002 — status napędu (bitmapa: gotowy, praca, błąd, alarm).
• r0945[0..7] — kody błędów (fault codes). Tu szukasz przyczyny F-alarmu.
• r2110 — numer aktualnego alarmu (warning, nie zatrzymuje).
• p0922 — telegram PROFIdrive (selekcja telegramu komunikacyjnego: 1=standard, 20=rozszerzony, 352/900=Safety PROFIsafe). Musi zgadzać się z konfiguracją w TIA Portal/Startdrive. Błędny telegram = brak komunikacji lub brak danych Safety.
• p9501/p9601 — Safety parameters (STO enable, SS1 ramp time). Tylko gdy Safety włączone.
### 16.4. Jak interpretujesz i kasujesz fault F30001 i F07801 w SINAMICS?
F30001 (Power unit: Ground fault — błąd doziemny wyjścia): wykrycie upływu prądu na uziemienie lub spięcie na wyjściu Power Module do silnika. Przyczyny: uszkodzona izolacja kabla silnikowego, zwarcie w uzwojeniu, kabel silnikowy zbyt długi bez filtra sinusoidalnego. Sprawdź: odłącz kabel silnika od napędu i mierz rezystancję izolacji (megaomomierz 500V DC) między żyłami a PE — powinna być >10MΩ. Uwaga: w starszych wersjach firmware G120 F30001 może oznaczać różne usterki Power Unit — zawsze weryfikuj w dokumentacji Parameter Manual dla konkretnej wersji firmware (r0018 = wersja firmware napędu).
• F07801 (Motor overtemperature — motor model): model termiczny wewnątrz napędu obliczył przegrzanie silnika (na podstawie prądu i parametrów silnika). Przyczyny: za duże obciążenie, za mały silnik, filtr chłodzenia zapchany, za długie rozruchy. Sprawdź: czy klasa termiczna silnika (p0335=klasa izolacji) jest poprawna, czy wentylacja silnika działa.
• Kasowanie faultów: r0945 pokazuje historię. Kasowanie programowo: p2103=1 (ACK faults) lub przez bit w telegram PROFIdrive (bit 7 słowa sterowania STW1). Na panelu BOP: długie wciśnięcie przycisku ESC/OK.
  17. REALNE SCENARIUSZE COMMISSIONING  

### 17.1. Maszyna startuje sama po ACK bez przycisku Start — co sprawdzasz?
Systematyczna lista kroków:
• Sprawdź logikę inicjalizacji: OB100 może resetować warunek startu — czy po resecie CPU warunek start jest TRUE bez oczekiwania na zbocze?
• Sprawdź HMI: czy przycisk Start na HMI ma event "Press" (zbocze) czy "State" (poziom)? Poziom = TRUE przez cały czas trzymania → program widzi ciągły sygnał start.
• Sprawdź zmienną startową w logice: czy warunek to zbocze narastające (R_TRIG) czy poziom BOOL? Maszyny wymagają zbocza — jednorazowy impuls.
• Sprawdź fizyczny przycisk: czy styk NO nie jest przyklejony lub zwarty przewód.
• Sprawdź Safety ACK: jeśli ACK kasuje blokadę i jednocześnie start jest aktywny w logice (np. zmienna startowa nie skasowana po zatrzymaniu awaryjnym) — maszyna ruszy. Logika powinna wymagać nowego impulsu Start AFTER ACK.
### 17.2. HMI pokazuje alarm którego nie ma w projekcie TIA Portal — skąd pochodzi?
Możliwe źródła "obcych" alarmów:
• Alarm diagnostyczny Siemens (System alarm): generowany automatycznie przez TIA Portal dla zdarzeń sprzętowych (moduł offline, błąd Safety, utrata komunikacji). Nie definiujesz ich — pojawiają się automatycznie jeśli HMI ma skonfigurowane "System alarms / Diagnostic alarms".
• Alarm z poprzedniej wersji projektu: HMI ma stary obraz z alarmami do tagów które już nie istnieją — mamy "stale" wpisy w alarm buffer.
• Alarm z urządzenia (napęd, robot): urządzenia PROFINET mogą wysyłać alarmy diagnostyczne przez PROFINET alarm mechanism → TIA Portal automatycznie tworzy odpowiadające alarmy w WinCC jeśli skonfigurowano.
• Sprawdź: w TIA Portal → HMI Alarms → Discrete Alarms / Analog Alarms — filtruj po numerze alarmu. Jeśli brak → sprawdź System alarms → Diagnostic alarms.
### 17.3. Moduł ET200SP nie pojawia się w sieci po podłączeniu — lista kroków diagnostycznych.
• Sprawdź fizycznie: czy dioda LINK/ACT na porcie modułu lub switcha miga → czy kabel Ethernet jest sprawny. Zamień kabel.
• Sprawdź zasilanie BusAdapter: moduł ET200SP wymaga zasilania BusAdapter (BA 2×RJ45 lub BA SCRJ) — czy L+ i M podłączone?
• Sprawdź IP i nazwę PROFINET w TIA Portal vs. na module: brak nazwy → moduł nowy/po resecie → TIA Portal → Online → Accessible devices → przypisz nazwę.
• Sprawdź czy nie ma duplikatu nazwy PROFINET w sieci (dwa moduły ta sama nazwa → konflikt).
• Sprawdź SCALANCE/switch: czy moduł jest w tej samej VLAN co CPU, czy port switcha zezwala na protokół PROFINET. Na SCALANCE: CLI lub Web GUI → port status.
• W TIA Portal: Online → Devices & Networks → mapa topologii → czy moduł widoczny? Jeśli nie → PRONETA → skan sieci → sprawdź czy moduł odpowiada na ARP.
• Sprawdź wersję GSDML / firmware: stary hardware z nowym projektem może wymagać aktualizacji firmware.
### 17.4. Napęd SINAMICS G120 świeci ciągłym czerwonym LED i nie kasuje się — co robisz?
Ciągły czerwony RDY LED = aktywny fault (F-alarm), nie alarm (A-alarm, który jest żółty). Procedura:
• Odczytaj kod: r0945[0] w Startdrive (online) lub na panelu BOP-2 (przełącz na r0945). Zapisz wszystkie r0945[0..7].
• Sprawdź w dokumentacji SINAMICS Parameter Manual lub Error List: każdy Fxxxxx ma opis przyczyny i działania korygującego. Najczęstsze: F30001 (doziemienie wyjścia), F07800-F07802 (temperatura silnika), F30002 (przetężenie DC-bus), F30004 (przekroczenie prędkości).
• Jeśli fault kasuje się ale wraca natychmiast: przyczyna fizyczna wciąż aktywna — nie idź dalej bez usunięcia przyczyny.
• Fault nie daje się skasować (kasowanie nie skutkuje): sprawdź czy STO nie jest aktywne (napęd nie ruszy z aktywnym STO) — sprawdź p9772/r9772 (STO status).
• Jeśli kasowanie przez sieć nie działa: spróbuj hardware reset (przycisk RESET na module lub chwilowe odcięcie zasilania 24V przy zachowanym 400V — deenergizuj Power Module, nie Control Unit).
### 17.5. CPU przeszło w STOP podczas produkcji — pierwsze 3 kroki.
• Nie ruszaj nic — zanim zaczniesz diagnostykę: odczytaj ze STOP LED + wyświetlacza CPU (S7-1500) kod błędu lub opis. Na wyświetlaczu pojawia się skrócony opis przyczyny STOP.
• W TIA Portal: Online → PLC → Diagnostics buffer (Diagnostikpuffer). Ostatni wpis w buforze = przyczyna zatrzymania. Typowe: "Time error OB cyclic" (za długi scan), "STOP requested by program" (STP instrukcja w kodzie), "Hardware failure" (moduł I/O wypadł).
• Nie rób Download ani "warm restart" zanim nie rozumiesz przyczyny — możesz nadpisać ważne dane diagnostyczne lub powtórzyć awarię.
  18. TIA PORTAL — ZAAWANSOWANE FUNKCJE  

### 18.1. Jak działa Know-How Protection i czym różni się od Copy Protection?
Know-How Protection (ochrona wiedzy): hasłem blokujesz podgląd i edycję kodu bloku FB/FC/DB. Możesz uruchomić, monitorować online (Watch Table), ale nie możesz otworzyć logiki. Stosowane przez integratorów do ochrony własności intelektualnej. Ustawiasz: kliknij prawym na blok → Protection → Know-how protection → ustaw hasło.
• Copy Protection (ochrona kopiowania): wiąże blok kryptograficznie z konkretnym CPU (serial number) lub kartą pamięci. Blok uruchamia się TYLKO na tym urządzeniu. Zapobiega kopiowaniu know-how na inne instalacje bez zgody autora.
• Oba mechanizmy można łączyć. Uwaga: jeśli stracisz hasło Know-How Protection — nie odzyskasz kodu. Siemens nie ma backdoora.
### 18.2. Co to są Project Libraries vs Global Libraries i kiedy używasz każdej?
Project Library: biblioteka wewnątrz projektu TIA Portal. Przechowuje wersjonowane bloki, typy PLC (PLCtype), ekrany HMI, UDT do ponownego użycia w ramach jednego projektu. Każda zmiana w bibliotece → aktualizacja wszystkich instancji. Idealna dla standardowych rozmów jednego zakładu/línii.
• Global Library: biblioteka zewnętrzna (.al17 plik) niezależna od projektu. Możesz ją otwierać w dowolnym projekcie TIA Portal i wstawiać jej elementy. Stosuj dla firmowych standardów używanych w wielu projektach dla wielu klientów — np. SICAR Tec Units, certyfikowane bloki Safety, własne wzorce.
• Workflow: rozwijaj w Global Library → insertuj do Project Library → deploy do projektu. Wersjonowanie w Global Library umożliwia zarządzanie zmianami we wszystkich projektach naraz.
### 18.3. Jak robisz partial download żeby nie resetować całego CPU?
TIA Portal rozróżnia typy downloadów:
• "Download to device → Software (only changes)": pobiera wyłącznie zmienione bloki — CPU pozostaje w RUN, zmiana aplikowana online. Bezpieczne dla drobnych poprawek kodu.
• "Download to device → Hardware and Software (only changes)": gdy zmieniłeś konfigurację sprzętu (nowy moduł IO, zmiana IP). CPU może przejść chwilowo przez STOP.
• "Download to device → All": pełne wgranie — CPU zawsze do STOP i z powrotem. Unikaj na produkcji.
• Warunek partial download: projekt musi być skompilowany bez błędów. Zmiany w Safety zawsze wymagają akceptacji F-signature — CPU zatrzymuje Safety runtime na moment (Safety LOCK → RUN), ale standard może działać.
• Praktyczna wskazówka: przed downloadem online sprawdź "Compare offline/online" — TIA Portal pokaże diff co realnie się zmieni.
### 18.4. Do czego służy OPC UA w TIA Portal i jak go aktywujesz?
OPC UA (Open Platform Communications Unified Architecture) to otwarte, bezpieczne (szyfrowanie + certyfikaty) API do integracji PLC z systemami SCADA, MES, ERP, chmurą i systemami IT (Python, C#, Java). Zalety nad S5/S7 Protocol lub Modbus: standaryzacja, bezpieczeństwo (TLS 1.2), model danych (nodes, methods, events), nie jest zależny od Siemens.
• Aktywacja: TIA Portal → CPU properties → OPC UA → Server → Enable OPC UA server → ustaw port (4840 domyślny), certyfikat, listę dostępnych węzłów (selected DB lub automatycznie wszystkie tagów).
• Klient: SIMATIC WinCC Advanced/Unified, Node-RED, Python opcua library, Kepware, Ignition. W praktyce commissioning: OPC UA server na PLC + Node-RED do szybkiego prototypowania dashboardów lub wysyłania danych do chmury.
• Ograniczenia: OPC UA ma wyższe opóźnienie niż PROFINET (~10ms vs <1ms) — nie stosuj do sterowania real-time, tylko do monitoringu i konfiguracji.

---

  19. COMMISSIONING — DODAWANIE STACJI I URZĄDZEŃ DO PROJEKTU  

### 19.1. Jak krok po kroku dodajesz nową wyspę sygnałową ET200SP Safety (F-peripheral) do istniejącego projektu?

Procedura commissioning nowej stacji ET200SP z modułami F-DI/F-DQ:

**Faza 1 — Projekt TIA Portal (offline):**
1. `Devices & Networks` → `Add new device` → wybierz `ET 200SP` → wskaż konkretny numer katalogowy modułu interfejsowego (IM) np. `6ES7155-6AU01-0BN0` (IM155-6 PN HF). Jeśli nie znasz numeru: `Not specified` → po wykryciu online TIA Portal zaproponuje podmianę.
2. Skonfiguruj **IP address** i **PROFINET device name** — muszą być unikalne w sieci.
3. Dodaj moduły w slotach: przeciągnij z hardware catalog → BaseUnit (BU20-P16+A10+2B) + moduły F-DI i F-DQ. Kolejność slotów MUSI odpowiadać fizycznej kolejności montażu na szynie.
4. Dla każdego modułu F: zakładka `Properties → Safety` → ustaw **F-Address** (PROFIsafe Address) — każda wartość unikalna w ramach F-CPU, zakres typowo 1–65534.
5. Skonfiguruj parametry F:
   - F-DI: `Discrepancy time` (10–200ms), `Sensor supply` (VS*/external)
   - F-DQ: `Substitute value` (0 lub 1 per kanał), `F-monitoring time`
6. Podłącz moduły do programu Safety: zmienne F-DI i F-DQ pojawiają się automatycznie w obszarze danych Safety po kompilacji.
7. `Compile → Hardware (rebuild all)` → `Compile → Software (rebuild all)`.

**Faza 2 — Przypisanie adresu PROFINET (online, przez sieć):**
1. Podłącz się do CPU: `Go online`.
2. `Online & diagnostics` → `Functions → Assign PROFINET device name` → wyszukaj nowe urządzenie po adresie MAC → wpisz nazwę zgodną z projektem → `Assign name`.
3. Alternatywnie przez `Accessible devices`: TIA Portal wykryje urządzenia bez nazwy i pozwoli przypisać.

**Faza 3 — Przypisanie PROFIsafe address na modułach F:**
1. `Devices & Networks` → prawym na moduł F → `Assign PROFIsafe address`.
2. Diody LED modułu F migają → potwierdź w TIA Portal → `Assign`. Adres zapisywany w elektronicznym elemencie kodującym (EK) modułu — nie przepada przy wymianie CPU.
3. Po przypisaniu wszystkich F-Address: czerwone LED modułów F powinny zgasnąć.

**Faza 4 — Download i weryfikacja:**
1. `Download to device → Hardware and software (only changes)` → CPU przejdzie przez krótki STOP.
2. Po uruchomieniu: sprawdź `Diagnostics buffer` — brak nowych błędów.
3. Sprawdź online pasek stanu modułów: wszystkie zielone = OK. Pomarańczowy/czerwony = błąd (kliknij → Device diagnostics).
4. Monitoruj F-DB modułu: zmienna `PASS_OUT = FALSE` oznacza brak passivation = prawidłowa praca.
5. Test funkcji Safety: zasymuluj zadziałanie czujnika NC → sprawdź czy F-DI passivuje się i czy logika Safety reaguje.

**Typowe pułapki:**
- Moduł IM nie reaguje na ping → sprawdź IP kolizję (dwa urządzenia ten sam adres), brak zasilania 24V BusAdapter, zerwany kabel.
- Czerwony LED F-DI po przypisaniu F-Address → sprawdź okablowanie czujnika lub parametr Sensor supply (brak zasilania VS*).
- Compilation error po dodaniu modułu → sprawdź czy typ BaseUnit (P/A-type) pasuje do modułu I/O.

---

### 19.2. Jak dodajesz wyspę pneumatyczną SMC (seria EX600) do projektu TIA Portal przez PROFINET?

Wyspa zawór pneumatycznych SMC EX600 komunikuje się przez PROFINET jako standardowe urządzenie I/O (nie Safety).

**Krok 1 — Instalacja GSDML:**
- Pobierz GSDML dla SMC EX600 ze strony SMC (`smcworld.com` → Support → GSDML) lub z płyty CD dołączonej do urządzenia.
- TIA Portal → `Options → Manage general station description files (GSD) → Install` → wskaż plik `.xml` (GSDML).
- Po instalacji w Hardware Catalog pojawia się node: `Other field devices → Drives → SMC → EX600`.

**Krok 2 — Konfiguracja w TIA Portal:**
1. Przeciągnij `EX600-GEN1` (lub właściwy wariant) z Hardware Catalog do `Network view`.
2. Połącz z interfejsem PROFINET CPU (linia ethernet).
3. Ustaw IP Address i PROFINET device name (musi zgadzać się z fizycznym urządzeniem).
4. W `Device view` wyspy: skonfiguruj sloty modułów wyjść zaworów (`SY Output Module` 1×, 2× lub 4×) — liczba i typ musi odpowiadać fizycznej konfiguracji wyspy. Każdy moduł wyjść to 1 bajt (8 zaworów) lub 2 bajty (16 zaworów).
5. Skonfiguruj moduł diagnostyczny (jeśli obecny): zwraca status zaworów, ciśnienie, błędy.
6. Skonfiguruj moduł wejść (DI) jeśli wyspa ma też wejścia czujnikowe.
7. Zapisz adresy wejść/wyjść (I-Addresses, Q-Addresses) widoczne w konfiguracji slotów.

**Krok 3 — Przypisanie nazwy PROFINET na fizycznym urządzeniu:**
1. `Accessible devices` lub `Assign PROFINET device name` → wyszukaj MAC wyspy SMC.
2. Przypisz nazwę zgodną z projektem → `Assign`.
- Alternatywnie: na fizycznym urządzeniu EX600 można ustawić IP przez rotary switch lub wbudowany web server (domyślne IP: `192.168.0.1`, login: `admin/admin`).

**Krok 4 — Program i testowanie:**
1. W programie PLC adresy Q (wyjścia) bezpośrednio sterują elektrozaworami:
   - `Q0.0 = TRUE` → zawór 1 otwarty (lub przełączony w zależności od typu zaworu 5/2 lub 3/2).
2. Diagnoza online: moduł diagnostyczny wyspy wysyła status do PLC → sprawdź bit błędu w danych wejściowych.
3. Test: wymuś `Q0.0 = TRUE` przez TIA Portal `Force Values` → sprawdź fizycznie czy zawór zadziałał i czy siłownik się przesunął.
4. Sprawdź ciśnienie zasilania wyspy (typowo 4–7 bar) — brak ciśnienia = zawory aktivne ale siłownik nie rusza.

**Typowe pułapki:**
- GSDML wersja niezgodna z hardware revision wyspy → błąd `Invalid device configuration`. Zawsze sprawdź hardware revision na tabliczce wyspy i pobierz odpowiedni GSDML.
- Liczba skonfigurowanych slotów w TIA Portal ≠ fizyczna liczba modułów na wyspie → CPU zgłasza błąd `Configuration mismatch`.
- Nazwa PROFINET przypisana ale wyspa nie komunikuje się → sprawdź wersję PROFINET (EX600 może wymagać PROFINET V2.3+) i czy nie ma duplikatu nazwy w sieci.

---

### 19.3. Jak krok po kroku dodajesz napęd SINAMICS G120 przez PROFINET do projektu TIA Portal?

**Faza 1 — Sprzętowe przygotowanie napędu:**
1. Sprawdź kartę sterowniczą (CU) i Power Module (PM) — upewnij się że CU obsługuje PROFINET (CU240E-2 PN lub CU250S-2 PN).
2. Ustaw adres IP napędu — jeśli BOP2 zainstalowany: `MENU → Parameters → p0016` (PROFINET mode) = 1. IP można przypisać przez TIA Portal (auto-assign) lub ręcznie przez BOP2 (`p61001` = IP adres, `p61000` = tryb assigning).
3. Firmware napędu: sprawdź `r0018` na BOP2 — zapisz wersję. Przy starszym firmware może być konieczna aktualizacja dla pełnej kompatybilności z TIA Portal V17+.

**Faza 2 — Konfiguracja w TIA Portal (Startdrive):**
1. `Devices & Networks` → `Add new device` → `Drives → SINAMICS → G120 → CU240E-2 PN` (wybierz właściwy wariant).
   - Alternatywnie: bezpośrednio w `Accessible devices` → wykryj napęd online → `Take online device as preset` → TIA Portal automatycznie pobierze konfigurację z napędu.
2. Połącz ikoną PROFINET z CPU w `Network view`.
3. Ustaw IP Address i PROFINET device name — identyczne z tym co jest lub zostanie przypisane na fizycznym napędzie.
4. `Device view` napędu → zakładka `Drive parameters` (Startdrive):
   - `p0922` → wybierz telegram PROFIdrive: `1` = standardowy, `20` = rozszerzony (prędkość + prąd), `352` = Safety Integrated + prędkość. Musi pasować do mapowania DB w programie PLC.
   - Skonfiguruj `Drive unit` → `Motor data`: numer katalogowy silnika lub ręcznie moc/napięcie/prąd/prędkość (z tabliczki silnika).

**Faza 3 — Konfiguracja Safety (jeśli STO/SS1 przez PROFIsafe):**
1. W Startdrive → zakładka `Safety Integrated` → `Enable Safety Integrated`.
2. Wybierz źródło komend Safety: `Via PROFIsafe` lub `Via terminals` (zaciski STO1/STO2) lub oba.
3. Ustaw `F-Address` (PROFIsafe Address) — musi być identyczny w TIA Portal i zostanie zapisany do napędu.
4. Wybierz funkcje Safety: STO, SS1 (ustaw `p9560` = czas rampy SS1 w ms), SLS (ustaw `p9531` = max prędkość SLS).
5. Po zakończeniu konfiguracji Safety: Startdrive wymaga **Safety Commissioning password** (domyślnie bez hasła, ustaw własne w produkcji).

**Faza 4 — Motor identification (autotuning):**
1. Online → napęd musi być w stanie `Ready` (RDY LED zielony migający).
2. `Commissioning → Motor identification → Static identification` → `Start`.
   - Napęd wykonuje pomiary rezystancji i induktancji (~30s) przy stojącym silniku.
   - **Strefa musi być bezpieczna** — napęd aplikuje napięcie do silnika.
3. Po zakończeniu: `Speed controller optimization` → `Start` — silnik wykonuje serie ruchów testowych. Odblokuj strefę bezpieczeństwa lub ustaw niską prędkość SLS.
4. Sprawdź `r0047 = 0` po identyfikacji — brak błędów.

**Faza 5 — Download i weryfikacja:**
1. `Download to device → Hardware and software (only changes)`.
2. Przypisz PROFINET device name: `Accessible devices` → MAC napędu → przypisz nazwę.
3. Sprawdź komunikację: `Online → Drive → Diagnostics → Control/Status words` — word sterowania STW1 przychodzi z CPU, word statusu ZSW1 wraca do CPU.
4. Test uruchomienia:
   - Ustaw `STW1 bit 0 = 1` (ON) → napęd powinien przejść do `Ready to switch on`.
   - Ustaw `STW1 bit 1 = 0 → 1` (OFF2 enable) i `bit 2 = 0 → 1` (OFF3 enable) → `Ready`.
   - Ustaw `STW1 bit 3 = 1` (Enable operation) + zadaj prędkość → napęd rusza.
   - Sprawdź `r0002 = 7` (Run), prąd `r0027`, prędkość rzeczywistą `r0021`.
5. Test STO: aktywuj STO (przez zaciski lub PROFIsafe) → `r9722.0 = 1` (STO_Active) → napęd nie generuje momentu → zdejmij STO → napęd wraca do Ready.

**Faza 6 — Safety komisjonowanie (obowiązkowe jeśli Safety):**
1. W Startdrive: `Safety Integrated → Safety commissioning → Start safety commissioning`.
2. Wykonaj test STO z podpisem: wpuść komendę STO, zmierz czas reakcji, zapisz wynik.
3. `Accept safety settings` → Startdrive generuje **Safety checksum (Safety ID)** — zanotuj lub drukuj raport.
4. Zmień hasło komisjonowania Safety po zakończeniu.

**Typowe pułapki:**
- Napęd nie pojawia się w sieci: sprawdź `r61000` (PROFINET diagnostic) — wartość 0 = brak połączenia z CPU; sprawdź kabel, IP, czy CPU w RUN.
- F30001 (Ground fault) po pierwszym uruchomieniu: sprawdź izolację kabla silnikowego (megaomomierz), długość kabla (>30m bez filtra sinusoidalnego = ryzyko pojemnościowych prądów upływu).
- Błąd Safety commissioning `F01653` (Safety parameters not accepted): wykonaj `p9700 = 1` (Safety factory reset) → re-konfiguruj Safety.
- Telegram mismatch: typ telegramu w TIA Portal (`p0922`) musi być identyczny z typem telegramu w DB komunikacyjnym programu PLC.

---

## 20. SŁOWNIK POJĘĆ — PLC / Safety / PROFINET / Napędy

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

**MRP (Media Redundancy Protocol)** — protokół redundancji dla topologii pierścieniowej PROFINET. Czas przełączenia ≤ 200 ms (standardowe MRP, max 50 urządzeń). MRPD (Media Redundancy with Planned Duplication) osiąga ≈ 0 ms przełączenia, wymaga trybu IRT. MRM = Media Redundancy Manager zarządza pierścieniem.

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

**SIL (Safety Integrity Level)** — poziom integralności bezpieczeństwa wg IEC 61508 / IEC 62061. Zakresy PFHD: SIL 1: 10⁻⁶ ≤ PFHD < 10⁻⁵; SIL 2: 10⁻⁷ ≤ PFHD < 10⁻⁶; SIL 3: 10⁻⁸ ≤ PFHD < 10⁻⁷ na godzinę. Jeśli PFHD < 10⁻⁸ — wymagania SIL 3 są przekroczone (brak SIL 4 w normie IEC 61508).

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

**SICAR (Siemens Automation Platform for CAR Plants)** — framework programistyczny Siemens dla branży automotive (fabryki robotyczne: Toyota, BMW, VW). Zawiera szablony TIA Portal, biblioteki Tec Units, wzorce alarmów i ProDiag. Skraca czas programowania przez drag-and-drop gotowych bloków.

**Tec Unit** — gotowy, parametryzowalny blok funkcjonalny SICAR dla urządzenia (silnik, zawór, napęd, robot) zawierający: FB PLC z logiką, ekrany HMI, definicje alarmów, obsługę trybów Auto/Manual/Local.

**Betriebsartenbereiche** — obszary trybów pracy (strefy ochronne) w SICAR; max 12 obszarów definiujących różne konfiguracje bezpieczeństwa i sekwencje dla każdego trybu produkcyjnego.

**OM1 / OM2 / OM3 (Operation Mode)** — tryby operacyjne sekwencji w SICAR. Każdy tryb ma własne sekwencje dla każdego urządzenia; bloki biblioteczne współdzielone między trybami.

---

### Commissioning — dodawanie urządzeń

**IM (Interface Module)** — moduł interfejsowy w stacji ET200SP/MP odpowiedzialny za komunikację PROFINET. Przykład: IM155-6 PN HF (ET200SP). Każda stacja ma dokładnie jeden IM; moduły I/O montowane w slotach obok.

**BusAdapter (BA)** — plastikowy adapter w ET200SP określający typ złącza PROFINET (2×RJ45, SC, M12). Montowany na IM155. Wymaga oddzielnego zasilania 24V (styki 1-L+ i 1-M).

**Electronic coding element (EK / BusAdapter coding)** — elektroniczny element kodujący w ET200SP przechowujący konfigurację modułu (F-Address, parametry Safety). Przy wymianie uszkodzonego modułu: przesuń EK ze starego do nowego modułu → nowy moduł automatycznie dziedziczy wszystkie ustawienia bez dostępu do TIA Portal.

**BOP-2 (Basic Operator Panel 2)** — panel operatorski SINAMICS G120 do lokalnej parametryzacji i diagnostyki napędu. Wyświetla parametry (`r0948` = czas faultów, `r0945` = kody błędów) oraz umożliwia ręczne kasowanie faultów i nieograniczoną parametryzację bez laptopa.

**Motor identification / Autotuning** — procedura SINAMICS Startdrive, w której napęd automatycznie mierzy parametry elektryczne silnika (rezystancja, induktancja) i wyznacza optymalne nastawy regulatora prędkości. Konieczna przy każdej nowej kombinacji napęd–silnik.

**p9700 (Safety factory reset)** — parametr SINAMICS G120/S120 do usunięcia wszystkich ustawień Safety i powrotu do domyślnych. Wymagane `p9700 = 1` + potwierdzenie hasłem Safety. Używasz gdy Safety commissioning jest nieodwracalnie zablokowane lub przy ponownym komisjonowaniu po wymianie CU.

**STW1 / ZSW1 (Steuerwort / Zustandswort)** — słowo sterowania (PLC → napęd) i słowo statusu (napęd → PLC) w telegramie PROFIdrive. STW1 bit 0 = ON/OFF1, bit 3 = Enable operation, bit 7 = Fault ACK. ZSW1 bit 0 = Ready to switch on, bit 2 = Operation enabled, bit 3 = Fault active.

**EX600 (SMC)** — seria jednostek sterujących wysp zaworów pneumatycznych SMC z komunikacją PROFINET. Konfiguracja przez GSDML, standardowe I/O — nie Safety. Wbudowany web server do konfiguracji IP i diagnostyki.

**GSDML (dla urządzeń nie-Siemens)** — plik XML dostarczany przez producenta urządzenia PROFINET (np. SMC, Festo, Balluff). Instalowany w TIA Portal przez `Options → Manage GSD files`. Opisuje moduły I/O, parametry i obsługiwane telegramy urządzenia.

