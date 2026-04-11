# KOMPENDIUM Q&A — v12.5

### PLC Programmer / Commissioner / Automatyk

### Siemens TIA Portal · Safety PLC · ET200 · Napędy SINAMICS · Robot ABB · SICAR

### Wersja: v12.5 | Data: 2026-04-11 16:01 | Pytania: 177

### Pytania + odpowiedzi zweryfikowane pod kątem rozmów kwalifikacyjnych.

### Źródła: Siemens App. Example 21064024 (E-Stop SIL3 V7.0.1), Wiring Examples 39198632, SIMATIC Safety Integrated, ControlByte Transkrypcje.

### Wersja: v12.5 | Data: 2026-04-11 15:39 | Pytania: 177

---

## SPIS TREŚCI

### Sekcje
- [1. PODSTAWY PLC I AUTOMATYKI](#1-podstawy-plc-i-automatyki)
- [2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED](#2-architektura-simatic-safety-integrated)
- [3. MODUŁY F-DI / F-DO — OKABLOWANIE I PARAMETRY](#3-moduły-f-di--f-do--okablowanie-i-parametry)
- [4. STRUKTURY GŁOSOWANIA — 1oo1/1oo2/2oo2/2oo3](#4-struktury-głosowania--1oo11oo22oo22oo3)
- [5. PASSIVATION, REINTEGRATION, ACK](#5-passivation-reintegration-ack)
- [6. SAFE STATE — BEZPIECZNY STAN](#6-safe-state--bezpieczny-stan)
- [7. PROFISAFE — KOMUNIKACJA SAFETY](#7-profisafe--komunikacja-safety)
- [8. NAPĘDY SAFETY — SINAMICS Z WBUDOWANYM SAFETY](#8-napędy-safety--sinamics-z-wbudowanym-safety)
- [9. TIA PORTAL — SAFETY PRAKTYKA](#9-tia-portal--safety-praktyka)
- [10. ROBOT ABB IRC5 — INTEGRACJA Z PLC](#10-robot-abb-irc5--integracja-z-plc)
- [11. COMMISSIONING I DIAGNOSTYKA](#11-commissioning-i-diagnostyka)
- [12. NAPĘDY SINAMICS](#12-napędy-sinamics)
- [13. E-STOP — NORMY, IMPLEMENTACJA I OBLICZENIA BEZPIECZEŃSTWA](#13-e-stop--normy-implementacja-i-obliczenia-bezpieczeństwa)
- [14. PROFINET — TOPOLOGIA, DIAGNOSTYKA I ZAAWANSOWANE FUNKCJE](#14-profinet--topologia-diagnostyka-i-zaawansowane-funkcje)
- [15. KURTYNY BEZPIECZEŃSTWA I MUTING](#15-kurtyny-bezpieczeństwa-i-muting)
- [16. MOTION CONTROL I SINAMICS — PRAKTYKA COMMISSIONING](#16-motion-control-i-sinamics--praktyka-commissioning)
- [17. REALNE SCENARIUSZE COMMISSIONING](#17-realne-scenariusze-commissioning)
- [18. TIA PORTAL — ZAAWANSOWANE FUNKCJE](#18-tia-portal--zaawansowane-funkcje)
- [19. COMMISSIONING — DODAWANIE STACJI I URZĄDZEŃ DO PROJEKTU](#19-commissioning--dodawanie-stacji-i-urządzeń-do-projektu)
- [20. SCHEMATY ELEKTRYCZNE — CZYTANIE, ANALIZA I PRAKTYKA COMMISSIONING](#20-schematy-elektryczne--czytanie-analiza-i-praktyka-commissioning)
- [21. SICAR@TIA — STANDARD AUTOMATYKI AUTOMOTIVE](#21-sicartia--standard-automatyki-automotive)

### Pytania

**1. PODSTAWY PLC I AUTOMATYKI**
- [1.1. Co to jest PLC i czym różni się od zwykłego komputera?](#11-co-to-jest-plc-i-czym-różni-się-od-zwykłego-komputera--)
- [1.2. Co to jest scan cycle i ile trwa?](#12-co-to-jest-scan-cycle-i-ile-trwa--)
- [1.3. Co to jest OB1, OB35, OB100 — kiedy każdego używasz?](#13-co-to-jest-ob1-ob35-ob100--kiedy-każdego-używasz)
- [1.4. Co to jest FB, FC, DB — kiedy używasz każdego?](#14-co-to-jest-fb-fc-db--kiedy-używasz-każdego--)
- [1.5. Co to jest UDT i po co go używasz?](#15-co-to-jest-udt-i-po-co-go-używasz)
- [1.6. Co to są języki programowania PLC — LAD, FBD, SCL, GRAPH?](#16-co-to-są-języki-programowania-plc--lad-fbd-scl-graph)
- [1.7. Co to jest sygnał 4-20mA i dlaczego nie 0-20mA?](#17-co-to-jest-sygnał-4-20ma-i-dlaczego-nie-0-20ma)
- [1.8. Co to jest PROFINET i czym różni się od PROFIBUS?](#18-co-to-jest-profinet-i-czym-różni-się-od-profibus--)
- [1.9. Jakie są główne rodziny sterowników PLC Siemens i do jakich zastosowań są dedykowane?](#19-jakie-są-główne-rodziny-sterowników-plc-siemens-i-do-jakich-zastosowań-są-dedykowane)
- [1.10. Jakie są kluczowe aspekty pamięci sterownika PLC Siemens S7-1200/1500?](#110-jakie-są-kluczowe-aspekty-pamięci-sterownika-plc-siemens-s7-12001500)
- [1.11. Jakie są warianty CPU S7-1200 i jakie mają możliwości rozbudowy?](#111-jakie-są-warianty-cpu-s7-1200-i-jakie-mają-możliwości-rozbudowy)
- [1.12. Czym jest enkoder i jaka jest różnica między inkrementalnym a absolutnym?](#112-czym-jest-enkoder-i-jaka-jest-różnica-między-inkrementalnym-a-absolutnym--)
- [1.13. Co to jest IO-Link i jakie korzyści daje względem klasycznych wejść analogowych PLC?](#113-co-to-jest-io-link-i-jakie-korzyści-daje-względem-klasycznych-wejść-analogowych-plc--)
- [1.14. Co to jest przerzutnik SR i RS w TIA Portal i jaka jest różnica w priorytecie?](#114-co-to-jest-przerzutnik-sr-i-rs-w-tia-portal-i-jaka-jest-różnica-w-priorytecie--)
- [1.15. Jak zbudować układ samopodtrzymania w LAD i czym różni się Dominacja SET od Dominacji RESET?](#115-jak-zbudować-układ-samopodtrzymania-w-lad-i-czym-różni-się-dominacja-set-od-dominacji-reset--)

**2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED**
- [2.1. Co to jest SIMATIC Safety Integrated i co oznacza 'wszystko w jednym sterowniku'?](#21-co-to-jest-simatic-safety-integrated-i-co-oznacza-wszystko-w-jednym-sterowniku--)
- [2.2. Co to jest F-CPU i jak działa dual-channel processing?](#22-co-to-jest-f-cpu-i-jak-działa-dual-channel-processing--)
- [2.3. Jakie sterowniki Siemens obsługują funkcje Safety?](#23-jakie-sterowniki-siemens-obsługują-funkcje-safety)
- [2.4. Co to jest F-DB i dlaczego nie można go edytować ręcznie?](#24-co-to-jest-f-db-i-dlaczego-nie-można-go-edytować-ręcznie)
- [2.5. Co to jest F-signature i collective signature?](#25-co-to-jest-f-signature-i-collective-signature--)
- [2.6. Jakie są tryby pracy Safety CPU i jak się przełącza?](#26-jakie-są-tryby-pracy-safety-cpu-i-jak-się-przełącza)
- [2.7. Jakie są podstawowe komponenty i zasady programowania sterowników bezpieczeństwa Pilz PNOZmulti?](#27-jakie-są-podstawowe-komponenty-i-zasady-programowania-sterowników-bezpieczeństwa-pilz-pnozmulti)
- [2.8. Co to jest S7-1500H (Hot Standby) i kiedy go stosujesz?](#28-co-to-jest-s7-1500h-hot-standby-i-kiedy-go-stosujesz--)
- [2.9. Jak wygląda minimalna konfiguracja sprzętowa sieci S7-1500H?](#29-jak-wygląda-minimalna-konfiguracja-sprzętowa-sieci-s7-1500h--)

**3. MODUŁY F-DI / F-DO — OKABLOWANIE I PARAMETRY**
- [3.1. Co to jest F-DI i jak różni się od standardowego DI?](#31-co-to-jest-f-di-i-jak-różni-się-od-standardowego-di--)
- [3.2. Co to jest VS* (pulse testing) i jak wykrywa usterki?](#32-co-to-jest-vs-pulse-testing-i-jak-wykrywa-usterki--)
- [3.3. Dlaczego czujniki Safety podłącza się jako NC (normalnie zamknięty)?](#33-dlaczego-czujniki-safety-podłącza-się-jako-nc-normalnie-zamknięty--)
- [3.4. Co to jest discrepancy time i jak go konfigurujesz?](#34-co-to-jest-discrepancy-time-i-jak-go-konfigurujesz--)
- [3.5. Co to jest substitute value na F-DO i kto decyduje o jego wartości?](#35-co-to-jest-substitute-value-na-f-do-i-kto-decyduje-o-jego-wartości)
- [3.6. Co to jest pm switching i pp switching — różnica?](#36-co-to-jest-pm-switching-i-pp-switching--różnica--)
- [3.7. Co to jest F-PM-E i do czego służy?](#37-co-to-jest-f-pm-e-i-do-czego-służy)
- [3.8. Jak bezpiecznie wyłączyć standardowe moduły wyjść przez Safety?](#38-jak-bezpiecznie-wyłączyć-standardowe-moduły-wyjść-przez-safety)
- [3.9. Jak F-CPU reaguje na typowe awarie wejść dwukanałowych (1oo2)?](#39-jak-f-cpu-reaguje-na-typowe-awarie-wejść-dwukanałowych-1oo2)
- [3.10. Jakie parametry są kluczowe przy konfiguracji wejść dwukanałowych w sterowniku bezpieczeństwa?](#310-jakie-parametry-są-kluczowe-przy-konfiguracji-wejść-dwukanałowych-w-sterowniku-bezpieczeństwa)

**4. STRUKTURY GŁOSOWANIA — 1oo1/1oo2/2oo2/2oo3**
- [4.1. Wyjaśnij notację XooY i podaj przykład każdej architektury.](#41-wyjaśnij-notację-xooy-i-podaj-przykład-każdej-architektury--)
- [4.2. Kiedy wybierasz 1oo2 a kiedy 2oo2?](#42-kiedy-wybierasz-1oo2-a-kiedy-2oo2--)
- [4.3. Jak 1oo2 jest realizowane w module F-DI Siemens?](#43-jak-1oo2-jest-realizowane-w-module-f-di-siemens)
- [4.4. Jak F-CPU reaguje na błąd rozbieżności sygnału (Discrepancy Failure) w konfiguracji 1oo2?](#44-jak-f-cpu-reaguje-na-błąd-rozbieżności-sygnału-discrepancy-failure-w-konfiguracji-1oo2)
- [4.5. Jakie są scenariusze awaryjne wykrywane przez moduł F-DI w układzie dwukanałowym 1oo2?](#45-jakie-są-scenariusze-awaryjne-wykrywane-przez-moduł-f-di-w-układzie-dwukanałowym-1oo2)
- [4.6. Jak parametr "Reintegration after discrepancy error" wpływa na obsługę błędu rozbieżności sygnału?](#46-jak-parametr-reintegration-after-discrepancy-error-wpływa-na-obsługę-błędu-rozbieżności-sygnału)
- [4.7. Co to jest discrepancy time (czas rozbieżności) w F-DI 1oo2 i co się dzieje gdy zostanie przekroczony?](#47-co-to-jest-discrepancy-time-czas-rozbieżności-w-f-di-1oo2-i-co-się-dzieje-gdy-zostanie-przekroczony-)
- [4.8. Jak moduł F-DI ET200SP wykrywa zwarcie między kanałami (cross-circuit detection) w obwodzie 1oo2?](#48-jak-moduł-f-di-et200sp-wykrywa-zwarcie-między-kanałami-cross-circuit-detection-w-obwodzie-1oo2-)

**5. PASSIVATION, REINTEGRATION, ACK**
- [5.1. Co to jest passivation i co się dzieje z wyjściami/wejściami?](#51-co-to-jest-passivation-i-co-się-dzieje-z-wyjściamiwejściami--)
- [5.2. Dlaczego moduł nie wraca automatycznie po usunięciu błędu?](#52-dlaczego-moduł-nie-wraca-automatycznie-po-usunięciu-błędu)
- [5.3. Moduł nie wychodzi z passivation — co sprawdzasz?](#53-moduł-nie-wychodzi-z-passivation--co-sprawdzasz)
- [5.4. Co to jest ACK_REQ, ACK_NEC i ACK_REI w praktyce?](#54-co-to-jest-ack_req-ack_nec-i-ack_rei-w-praktyce--)

**6. SAFE STATE — BEZPIECZNY STAN**
- [6.1. Co to jest Safe State i kto go definiuje?](#61-co-to-jest-safe-state-i-kto-go-definiuje)
- [6.2. Dlaczego Safe State to nie zawsze wyłączenie?](#62-dlaczego-safe-state-to-nie-zawsze-wyłączenie)
- [6.3. Jak F-DO substitute value wpływa na Safe State?](#63-jak-f-do-substitute-value-wpływa-na-safe-state)
- [6.4. Czym różni się STO jako Safe State napędu SINAMICS od zatrzymania programowego (OFF1/OFF2)?](#64-czym-różni-się-sto-jako-safe-state-napędu-sinamics-od-zatrzymania-programowego-off1off2-)
- [6.5. Jak konfigurujesz substitute values dla F-DO i jaką wartość wybrać dla zaworu, siłownika i napędu?](#65-jak-konfigurujesz-substitute-values-dla-f-do-i-jaką-wartość-wybrać-dla-zaworu-siłownika-i-napędu-)

**7. PROFISAFE — KOMUNIKACJA SAFETY**
- [7.1. Co to jest PROFIsafe i co zawiera jego pakiet?](#71-co-to-jest-profisafe-i-co-zawiera-jego-pakiet--)
- [7.2. Co to jest F-Address i jak go konfigurujesz?](#72-co-to-jest-f-address-i-jak-go-konfigurujesz--)
- [7.3. Co to jest F-monitoring time i co się dzieje po jego przekroczeniu?](#73-co-to-jest-f-monitoring-time-i-co-się-dzieje-po-jego-przekroczeniu)
- [7.4. Jak Safety działa przez ET200 (zdalne I/O) i czym jest F-peripheral?](#74-jak-safety-działa-przez-et200-zdalne-io-i-czym-jest-f-peripheral)
- [7.5. Jakie telegramy PROFIsafe są stosowane w napędach SINAMICS i co zawierają?](#75-jakie-telegramy-profisafe-są-stosowane-w-napędach-sinamics-i-co-zawierają)
- [7.6. Jak oblicza się i dobiera F-monitoring time dla modułów PROFIsafe?](#76-jak-oblicza-się-i-dobiera-f-monitoring-time-dla-modułów-profisafe)
- [7.7. Jak PROFIsafe chroni przed przekłamaniem danych i jakie mechanizmy bezpieczeństwa stosuje ramka PROFIsafe?](#77-jak-profisafe-chroni-przed-przekłamaniem-danych-i-jakie-mechanizmy-bezpieczeństwa-stosuje-ramka-profisafe)
- [7.8. Jak działa komunikacja Safety między dwoma F-CPU (Safety-to-Safety communication) przez PROFIsafe?](#78-jak-działa-komunikacja-safety-między-dwoma-f-cpu-safety-to-safety-communication-przez-profisafe)

**8. NAPĘDY SAFETY — SINAMICS Z WBUDOWANYM SAFETY**
- [8.1. Co to jest STO (Safe Torque Off) i jak działa?](#81-co-to-jest-sto-safe-torque-off-i-jak-działa--)
- [8.2. Jaka jest różnica między STO a zwykłym wyłączeniem napędu przez PLC?](#82-jaka-jest-różnica-między-sto-a-zwykłym-wyłączeniem-napędu-przez-plc)
- [8.3. Co to jest SS1 i kiedy go używasz zamiast STO?](#83-co-to-jest-ss1-i-kiedy-go-używasz-zamiast-sto--)
- [8.4. Co to są SS2, SOS, SLS, SDI, SBC?](#84-co-to-są-ss2-sos-sls-sdi-sbc--)
- [8.5. Jak STO jest realizowane sprzętowo — zaciski vs PROFIsafe?](#85-jak-sto-jest-realizowane-sprzętowo--zaciski-vs-profisafe)
- [8.6. Co sprawdzasz przy commissioning napędu z STO?](#86-co-sprawdzasz-przy-commissioning-napędu-z-sto)
- [8.7. Czym różnią się telegramy PROFIdrive 1, 20, 102, 352 i jak dobirasz telegram dla napędu SINAMICS?](#87-czym-różnią-się-telegramy-profidrive-1-20-102-352-i-jak-dobirasz-telegram-dla-napędu-sinamics)
- [8.8. Jakie funkcje bezpieczeństwa są wbudowane w serwowzmacniacz Sinamics V90 i jak należy je podłączyć?](#88-jakie-funkcje-bezpieczeństwa-są-wbudowane-w-serwowzmacniacz-sinamics-v90-i-jak-należy-je-podłączyć)

**9. TIA PORTAL — SAFETY PRAKTYKA**
- [9.1. Jak wygląda struktura programu Safety w TIA Portal?](#91-jak-wygląda-struktura-programu-safety-w-tia-portal)
- [9.2. Jak przekazujesz sygnał z obszaru F do standardowego OB?](#92-jak-przekazujesz-sygnał-z-obszaru-f-do-standardowego-ob)
- [9.3. Jak wgrywasz zmianę w programie Safety?](#93-jak-wgrywasz-zmianę-w-programie-safety--)
- [9.4. Co się dzieje gdy F-signature nie zgadza się po wgraniu?](#94-co-się-dzieje-gdy-f-signature-nie-zgadza-się-po-wgraniu)
- [9.5. Jak czytasz diagnostykę F-modułu online w TIA Portal?](#95-jak-czytasz-diagnostykę-f-modułu-online-w-tia-portal--)
- [9.6. Co to jest PLCSIM i jak pomaga w Safety?](#96-co-to-jest-plcsim-i-jak-pomaga-w-safety)
- [9.7. Co to jest Safety Matrix w TIA Portal i jak z niej korzystasz?](#97-co-to-jest-safety-matrix-w-tia-portal-i-jak-z-niej-korzystasz--)
- [9.8. Jak generujesz Safety Report / certyfikat Safety w TIA Portal i co zawiera?](#98-jak-generujesz-safety-report--certyfikat-safety-w-tia-portal-i-co-zawiera--)

**10. ROBOT ABB IRC5 — INTEGRACJA Z PLC**
- [10.1. Jak przebiega komunikacja Siemens PLC z robotem ABB IRC5?](#101-jak-przebiega-komunikacja-siemens-plc-z-robotem-abb-irc5--)
- [10.2. Co to jest GSDML i jak go instalujesz w TIA Portal?](#102-co-to-jest-gsdml-i-jak-go-instalujesz-w-tia-portal)
- [10.3. Jak PLC wysyła numer programu do robota i jak robot go odczytuje?](#103-jak-plc-wysyła-numer-programu-do-robota-i-jak-robot-go-odczytuje)
- [10.4. Jak działa przesyłanie offsetu pozycji z PLC do RAPID?](#104-jak-działa-przesyłanie-offsetu-pozycji-z-plc-do-rapid)
- [10.5. Jak debugujesz brak komunikacji PROFINET między PLC a robotem?](#105-jak-debugujesz-brak-komunikacji-profinet-między-plc-a-robotem)
- [10.6. Jakie protokoły komunikacyjne i format danych są wykorzystywane do integracji robota ABB IRC5 z PLC Siemens?](#106-jakie-protokoły-komunikacyjne-i-format-danych-są-wykorzystywane-do-integracji-robota-abb-irc5-z-plc-siemens)
- [10.7. Jakie są kluczowe elementy struktury telegramu XML wysyłanego z robota ABB IRC5 do PLC?](#107-jakie-są-kluczowe-elementy-struktury-telegramu-xml-wysyłanego-z-robota-abb-irc5-do-plc)
- [10.8. Jak przebiega proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens?](#108-jak-przebiega-proces-dekodowania-telegramu-xml-z-robota-abb-w-sterowniku-plc-siemens)

**11. COMMISSIONING I DIAGNOSTYKA**
- [11.1. Co sprawdzasz przed pierwszym RUN Safety?](#111-co-sprawdzasz-przed-pierwszym-run-safety--)
- [11.2. Jak testujesz e-stop podczas commissioning?](#112-jak-testujesz-e-stop-podczas-commissioning--)
- [11.3. Co to jest FAT i SAT w kontekście Safety?](#113-co-to-jest-fat-i-sat-w-kontekście-safety--)
- [11.4. Jak postępujesz gdy odkryjesz błąd w logice Safety po FAT?](#114-jak-postępujesz-gdy-odkryjesz-błąd-w-logice-safety-po-fat)
- [11.5. Jakie są najczęstsze przyczyny passivation F-DI w praktyce?](#115-jakie-są-najczęstsze-przyczyny-passivation-f-di-w-praktyce--)
- [11.6. Jak reagować gdy moduł F świeci błędem którego nie możesz skasować?](#116-jak-reagować-gdy-moduł-f-świeci-błędem-którego-nie-możesz-skasować)
- [11.7. Jak wygląda typowy workflow pierwszego commissioning z TIA Portal — od projektu do działającej maszyny?](#117-jak-wygląda-typowy-workflow-pierwszego-commissioning-z-tia-portal--od-projektu-do-działającej-maszyny)
- [11.8. Jakie są etapy uruchomienia napędu SINAMICS G120 — od sprzętu do pierwszego ruchu?](#118-jakie-są-etapy-uruchomienia-napędu-sinamics-g120--od-sprzętu-do-pierwszego-ruchu)
- [11.9. Co to jest commissioning i jak przeprowadzić pełne uruchomienie instalacji — od fazy offline do RUN z Safety i Safety Matrix?](#119-co-to-jest-commissioning-i-jak-przeprowadzić-pełne-uruchomienie-instalacji--od-fazy-offline-do-run-z-safety-i-safety-matrix--)
- [11.10. Co to jest ProDiag i jak go używasz do diagnostyki maszyny?](#1110-co-to-jest-prodiag-i-jak-go-używasz-do-diagnostyki-maszyny--)

**12. NAPĘDY SINAMICS**
- [12.1. Co to jest SINAMICS Startdrive w TIA Portal?](#121-co-to-jest-sinamics-startdrive-w-tia-portal)
- [12.2. Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?](#122-jak-konfigurujesz-sinamics-g120-z-safety-przez-profisafe--)
- [12.3. Z jakich komponentów składa się napęd SINAMICS G120 i jaką rolę pełni każdy z nich?](#123-z-jakich-komponentów-składa-się-napęd-sinamics-g120-i-jaką-rolę-pełni-każdy-z-nich)
- [12.4. Czym są telegramy PROFIdrive i jakie telegramy stosuje się w SINAMICS G120?](#124-czym-są-telegramy-profidrive-i-jakie-telegramy-stosuje-się-w-sinamics-g120)
- [12.5. Jak wygląda procedura pierwszego uruchomienia (commissioning) SINAMICS G120 przez Startdrive?](#125-jak-wygląda-procedura-pierwszego-uruchomienia-commissioning-sinamics-g120-przez-startdrive)
- [12.6. Czym różnią się napędy SINAMICS G120, S120 i V90 i kiedy stosuje się każdy z nich?](#126-czym-różnią-się-napędy-sinamics-g120-s120-i-v90-i-kiedy-stosuje-się-każdy-z-nich)
- [12.7. Jak wygląda diagnostyka napędu SINAMICS G120 — fault codes, ostrzeżenia i kasowanie błędów?](#127-jak-wygląda-diagnostyka-napędu-sinamics-g120--fault-codes-ostrzeżenia-i-kasowanie-błędów)
- [12.8. Czym jest sterowanie wektorowe (Vector Control) vs skalarne (V/f) w SINAMICS G120 i kiedy stosujesz każdy tryb?](#128-czym-jest-sterowanie-wektorowe-vector-control-vs-skalarne-vf-w-sinamics-g120-i-kiedy-stosujesz-każdy-tryb)
- [12.9. Czym różni się architektura SINAMICS S120 od G120 i jak wygląda jej konfiguracja w TIA Portal?](#129-czym-różni-się-architektura-sinamics-s120-od-g120-i-jak-wygląda-jej-konfiguracja-w-tia-portal)
- [12.10. Jak wyglądają typowe scenariusze wymiany napędu SINAMICS G120 na obiekcie (service/replacement)?](#1210-jak-wyglądają-typowe-scenariusze-wymiany-napędu-sinamics-g120-na-obiekcie-servicereplacement)

**13. E-STOP — NORMY, IMPLEMENTACJA I OBLICZENIA BEZPIECZEŃSTWA**
- [13.1. Jakie są kategorie zatrzymania wg EN 60204-1 i jak wpływają na wybór STO vs SS1?](#131-jakie-są-kategorie-zatrzymania-wg-en-60204-1-i-jak-wpływają-na-wybór-sto-vs-ss1--)
- [13.2. Co to jest LSafe_EStop i gdzie go znajdziesz w TIA Portal?](#132-co-to-jest-lsafe_estop-i-gdzie-go-znajdziesz-w-tia-portal--)
- [13.3. Co to jest feedback circuit (obwód sprzężenia zwrotnego styczników) i dlaczego jest wymagany dla SIL 3 / PL e?](#133-co-to-jest-feedback-circuit-obwód-sprzężenia-zwrotnego-styczników-i-dlaczego-jest-wymagany-dla-sil-3--pl-e--)
- [13.4. Co to są CCF (Common Cause Failure) i jakie środki są wymagane dla Cat.4?](#134-co-to-są-ccf-common-cause-failure-i-jakie-środki-są-wymagane-dla-cat4--)
- [13.5. Czy można łączyć przyciski e-stop szeregowo do jednego wejścia F-DI?](#135-czy-można-łączyć-przyciski-e-stop-szeregowo-do-jednego-wejścia-f-di)
- [13.6. Jak wygląda obliczenie PFHD (Probability of Dangerous Failure per Hour) dla funkcji Safety E-Stop z F-CPU S7-1500F?](#136-jak-wygląda-obliczenie-pfhd-probability-of-dangerous-failure-per-hour-dla-funkcji-safety-e-stop-z-f-cpu-s7-1500f)
- [13.7. Co to jest DC (Diagnostic Coverage) i jak jest osiągane w poszczególnych podsystemach E-Stop?](#137-co-to-jest-dc-diagnostic-coverage-i-jak-jest-osiągane-w-poszczególnych-podsystemach-e-stop)
- [13.8. Jak wygląda obliczenie czasów odpowiedzi (response time) w funkcji Safety E-Stop i co na nie wpływa?](#138-jak-wygląda-obliczenie-czasów-odpowiedzi-response-time-w-funkcji-safety-e-stop-i-co-na-nie-wpływa)

**14. PROFINET — TOPOLOGIA, DIAGNOSTYKA I ZAAWANSOWANE FUNKCJE**
- [14.1. Co to jest MRP (Media Redundancy Protocol) i kiedy go stosujesz?](#141-co-to-jest-mrp-media-redundancy-protocol-i-kiedy-go-stosujesz--)
- [14.2. Co to jest IRT (Isochronous Real-Time) i kiedy jest wymagany?](#142-co-to-jest-irt-isochronous-real-time-i-kiedy-jest-wymagany--)
- [14.3. Jak diagnostykujesz sieć PROFINET w TIA Portal i PRONETA?](#143-jak-diagnostykujesz-sieć-profinet-w-tia-portal-i-proneta--)
- [14.4. Co to jest Shared Device i kiedy go używasz?](#144-co-to-jest-shared-device-i-kiedy-go-używasz)
- [14.5. Jak działa Device replacement bez PG (automatic name assignment)?](#145-jak-działa-device-replacement-bez-pg-automatic-name-assignment)
- [14.6. Jakie są rodzaje i funkcje przemysłowych switchy Ethernet w sieciach PROFINET?](#146-jakie-są-rodzaje-i-funkcje-przemysłowych-switchy-ethernet-w-sieciach-profinet)
- [14.7. Co to jest S7 Communication (GET/PUT) i ISO on TCP — kiedy i jak je stosujesz?](#147-co-to-jest-s7-communication-getput-i-iso-on-tcp--kiedy-i-jak-je-stosujesz)
- [14.8. Co to jest PROFINET TSN (Time Sensitive Networking) i czym różni się od IRT?](#148-co-to-jest-profinet-tsn-time-sensitive-networking-i-czym-różni-się-od-irt--)

**15. KURTYNY BEZPIECZEŃSTWA I MUTING**
- [15.1. Czym różni się kurtyna bezpieczeństwa Type 2 od Type 4 (IEC 61496)?](#151-czym-różni-się-kurtyna-bezpieczeństwa-type-2-od-type-4-iec-61496)
- [15.2. Jak działa muting i czym różni się od override?](#152-jak-działa-muting-i-czym-różni-się-od-override)
- [15.3. Jak podłączasz OSSD (Output Signal Switching Device) kurtyny do modułu F-DI?](#153-jak-podłączasz-ossd-output-signal-switching-device-kurtyny-do-modułu-f-di)
- [15.4. Jakie jest zastosowanie wyjść tranzystorowych z czujników bezpieczeństwa w systemach PLC Safety?](#154-jakie-jest-zastosowanie-wyjść-tranzystorowych-z-czujników-bezpieczeństwa-w-systemach-plc-safety)
- [15.5. Jakie typy elektrygli bezpieczeństwa (door interlocks) istnieją i jak dobirasz odpowiedni Performance Level?](#155-jakie-typy-elektrygli-bezpieczeństwa-door-interlocks-istnieją-i-jak-dobirasz-odpowiedni-performance-level--)
- [15.6. Czym jest czujnik radarowy bezpieczeństwa (np. Pilz PSEN RD 1.2) i kiedy go stosujesz zamiast skanera laserowego?](#156-czym-jest-czujnik-radarowy-bezpieczeństwa-np-pilz-psen-rd-12-i-kiedy-go-stosujesz-zamiast-skanera-laserowego--)

**16. MOTION CONTROL I SINAMICS — PRAKTYKA COMMISSIONING**
- [16.1. Co to jest Technology Object (TO) w TIA Portal i jak go używasz?](#161-co-to-jest-technology-object-to-w-tia-portal-i-jak-go-używasz)
- [16.2. Jak robisz autotuning napędu G120/V90 w Startdrive?](#162-jak-robisz-autotuning-napędu-g120v90-w-startdrive)
- [16.3. Jakie są najważniejsze parametry SINAMICS G120 które musisz znać?](#163-jakie-są-najważniejsze-parametry-sinamics-g120-które-musisz-znać)
- [16.4. Jak interpretujesz i kasujesz fault F30001 i F07801 w SINAMICS?](#164-jak-interpretujesz-i-kasujesz-fault-f30001-i-f07801-w-sinamics)
- [16.5. Czym jest SINAMICS G120 i do jakich silników oraz aplikacji jest przeznaczony?](#165-czym-jest-sinamics-g120-i-do-jakich-silników-oraz-aplikacji-jest-przeznaczony-)
- [16.6. Jakie są podstawowe komponenty układu napędowego z SINAMICS G120 i sterownikiem Siemens?](#166-jakie-są-podstawowe-komponenty-układu-napędowego-z-sinamics-g120-i-sterownikiem-siemens-)
- [16.7. Jakie oprogramowanie służy do konfiguracji i uruchomienia SINAMICS G120?](#167-jakie-oprogramowanie-służy-do-konfiguracji-i-uruchomienia-sinamics-g120-)
- [16.8. Jakie tryby sterowania oferuje SINAMICS G120 i czym się różnią?](#168-jakie-tryby-sterowania-oferuje-sinamics-g120-i-czym-się-różnią-)
- [16.9. Jak przebiega procedura identyfikacji silnika (Motor ID) w SINAMICS G120 i dlaczego jest niezbędna?](#169-jak-przebiega-procedura-identyfikacji-silnika-motor-id-w-sinamics-g120-i-dlaczego-jest-niezbędna-)
- [16.10. Jak wygląda pełna procedura commissioning SINAMICS G120 z TIA Portal krok po kroku?](#1610-jak-wygląda-pełna-procedura-commissioning-sinamics-g120-z-tia-portal-krok-po-kroku-)
- [16.11. Do czego służy blok funkcyjny MC_MoveJog w TIA Portal i jakie są jego podstawowe parametry wejściowe?](#1611-do-czego-służy-blok-funkcyjny-mc_movejog-w-tia-portal-i-jakie-są-jego-podstawowe-parametry-wejściowe)
- [16.12. Jakie są kluczowe cechy i zachowania bloku MC_MoveJog podczas pracy?](#1612-jakie-są-kluczowe-cechy-i-zachowania-bloku-mc_movejog-podczas-pracy)
- [16.13. Jakie są parametry enkoderów inkrementalnych i absolutnych — rozdzielczość, co mogą i czego nie mogą?](#1613-jakie-są-parametry-enkoderów-inkrementalnych-i-absolutnych--rozdzielczość-co-mogą-i-czego-nie-mogą--)
- [16.14. Jakie są interfejsy enkoderów i jak konfigurujesz enkoder w SINAMICS i TIA Portal?](#1614-jakie-są-interfejsy-enkoderów-i-jak-konfigurujesz-enkoder-w-sinamics-i-tia-portal--)
- [16.15. Czym są silniki IE5 (IPM / synchroniczne z magnesami trwałymi) i dlaczego zastępują klasyczne silniki indukcyjne w nowych projektach?](#1615-czym-są-silniki-ie5-ipm--synchroniczne-z-magnesami-trwałymi-i-dlaczego-zastępują-klasyczne-silniki-indukcyjne-w-nowych-projektach--)

**17. REALNE SCENARIUSZE COMMISSIONING**
- [17.1. Maszyna startuje sama po ACK bez przycisku Start — co sprawdzasz?](#171-maszyna-startuje-sama-po-ack-bez-przycisku-start--co-sprawdzasz)
- [17.2. HMI pokazuje alarm którego nie ma w projekcie TIA Portal — skąd pochodzi?](#172-hmi-pokazuje-alarm-którego-nie-ma-w-projekcie-tia-portal--skąd-pochodzi)
- [17.3. Moduł ET200SP nie pojawia się w sieci po podłączeniu — lista kroków diagnostycznych.](#173-moduł-et200sp-nie-pojawia-się-w-sieci-po-podłączeniu--lista-kroków-diagnostycznych)
- [17.4. Napęd SINAMICS G120 świeci ciągłym czerwonym LED i nie kasuje się — co robisz?](#174-napęd-sinamics-g120-świeci-ciągłym-czerwonym-led-i-nie-kasuje-się--co-robisz--)
- [17.5. CPU przeszło w STOP podczas produkcji — pierwsze 3 kroki.](#175-cpu-przeszło-w-stop-podczas-produkcji--pierwsze-3-kroki--)
- [17.6. Po czym poznajesz, że projekt w TIA Portal jest skalowalny?](#176-po-czym-poznajesz-że-projekt-w-tia-portal-jest-skalowalny--)
- [17.7. Co sprawdzasz na FAT (Factory Acceptance Test) dla instalacji z Safety?](#177-co-sprawdzasz-na-fat-factory-acceptance-test-dla-instalacji-z-safety-)
- [17.8. Jak realizujesz SAT (Site Acceptance Test) po dostarczeniu maszyny do klienta?](#178-jak-realizujesz-sat-site-acceptance-test-po-dostarczeniu-maszyny-do-klienta-)
- [17.9. Jak podejść do diagnostyki nieznanego lub legacy projektu TIA Portal, który przejmujesz po raz pierwszy?](#179-jak-podejść-do-diagnostyki-nieznanego-lub-legacy-projektu-tia-portal-który-przejmujesz-po-raz-pierwszy-)

**18. TIA PORTAL — ZAAWANSOWANE FUNKCJE**
- [18.1. Co to są Project Libraries vs Global Libraries i kiedy używasz każdej?](#181-co-to-są-project-libraries-vs-global-libraries-i-kiedy-używasz-każdej)
- [18.2. Jak robisz partial download żeby nie resetować całego CPU?](#182-jak-robisz-partial-download-żeby-nie-resetować-całego-cpu)
- [18.3. Do czego służy OPC UA w TIA Portal i jak go aktywujesz?](#183-do-czego-służy-opc-ua-w-tia-portal-i-jak-go-aktywujesz)
- [18.4. Czym jest SIMATIC ProDiag i jak konfigurujesz pierwsze monitory diagnostyczne?](#184-czym-jest-simatic-prodiag-i-jak-konfigurujesz-pierwsze-monitory-diagnostyczne-)

**19. COMMISSIONING — DODAWANIE STACJI I URZĄDZEŃ DO PROJEKTU**
- [19.1. Jak krok po kroku dodajesz nową wyspę sygnałową ET200SP Safety (F-peripheral) do istniejącego projektu?](#191-jak-krok-po-kroku-dodajesz-nową-wyspę-sygnałową-et200sp-safety-f-peripheral-do-istniejącego-projektu--)
- [19.2. Jak dodajesz wyspę pneumatyczną SMC (seria EX600) do projektu TIA Portal przez PROFINET?](#192-jak-dodajesz-wyspę-pneumatyczną-smc-seria-ex600-do-projektu-tia-portal-przez-profinet)
- [19.3. Jak krok po kroku dodajesz napęd SINAMICS G120 przez PROFINET do projektu TIA Portal?](#193-jak-krok-po-kroku-dodajesz-napęd-sinamics-g120-przez-profinet-do-projektu-tia-portal)
- [19.4. Jak dodajesz stację ET200MP z modułami Safety do istniejącej linii produkcyjnej z wieloma stacjami PROFINET?](#194-jak-dodajesz-stację-et200mp-z-modułami-safety-do-istniejącej-linii-produkcyjnej-z-wieloma-stacjami-profinet)
- [19.5. Co to jest „Assign PROFIsafe address" i dlaczego jest wymagane osobno od konfiguracji TIA Portal?](#195-co-to-jest-assign-profisafe-address-i-dlaczego-jest-wymagane-osobno-od-konfiguracji-tia-portal)
- [19.6. Jak dodajesz urządzenie firm trzecich (np. Festo, Beckhoff, WAGO) do projektu TIA Portal przez PROFINET?](#196-jak-dodajesz-urządzenie-firm-trzecich-np-festo-beckhoff-wago-do-projektu-tia-portal-przez-profinet)
- [19.7. Jak wygląda procedura wymiany uszkodzonego modułu ET200SP na działającej linii (hot swap)?](#197-jak-wygląda-procedura-wymiany-uszkodzonego-modułu-et200sp-na-działającej-linii-hot-swap)

**20. SCHEMATY ELEKTRYCZNE — CZYTANIE, ANALIZA I PRAKTYKA COMMISSIONING**
- [20.1. Co to jest schemat elektryczny i jakie rodzaje schematów spotykasz na obiekcie?](#201-co-to-jest-schemat-elektryczny-i-jakie-rodzaje-schematów-spotykasz-na-obiekcie)
- [20.2. Jak czytasz schemat rozruchu gwiazda-trójkąt (Y/Δ) i jakie elementy musisz na nim zidentyfikować?](#202-jak-czytasz-schemat-rozruchu-gwiazda-trójkąt-yδ-i-jakie-elementy-musisz-na-nim-zidentyfikować)
- [20.3. Jak czytasz schemat rewersji silnika (zmiana kierunku obrotów) i co MUSISZ sprawdzić?](#203-jak-czytasz-schemat-rewersji-silnika-zmiana-kierunku-obrotów-i-co-musisz-sprawdzić)
- [20.4. Co to jest układ samopodtrzymania na schemacie i jak go rozpoznajesz?](#204-co-to-jest-układ-samopodtrzymania-na-schemacie-i-jak-go-rozpoznajesz)
- [20.5. Jak czytasz schemat Dahlandera (silnik dwubiegowy) i czym różni się od Y/Δ na schemacie?](#205-jak-czytasz-schemat-dahlandera-silnik-dwubiegowy-i-czym-różni-się-od-yδ-na-schemacie)
- [20.6. Jak wygląda na schemacie blokada elektryczna i mechaniczna między stycznikami i po co ją sprawdzasz?](#206-jak-wygląda-na-schemacie-blokada-elektryczna-i-mechaniczna-między-stycznikami-i-po-co-ją-sprawdzasz)
- [20.7. Jak na schemacie rozpoznajesz obwód bezpieczeństwa (Safety) i czym różni się od standardowego obwodu sterowania?](#207-jak-na-schemacie-rozpoznajesz-obwód-bezpieczeństwa-safety-i-czym-różni-się-od-standardowego-obwodu-sterowania)

**21. SICAR@TIA — STANDARD AUTOMATYKI AUTOMOTIVE**
- [21.1. Co to jest SICAR@TIA i do czego służy?](#211-co-to-jest-sicartia-i-do-czego-służy--)
- [21.2. Jak wygląda struktura programu PLC w SICAR?](#212-jak-wygląda-struktura-programu-plc-w-sicar--)
- [21.3. Jakie tryby pracy (Operation Modes) obsługuje SICAR i jak je uruchamiasz?](#213-jakie-tryby-pracy-operation-modes-obsługuje-sicar-i-jak-je-uruchamiasz--)
- [21.4. Jak działa sterowanie sekwencyjne (Sequence Control) w SICAR?](#214-jak-działa-sterowanie-sekwencyjne-sequence-control-w-sicar--)
- [21.5. Co to są Tec Units w SICAR i jak ich używasz?](#215-co-to-są-tec-units-w-sicar-i-jak-ich-używasz--)
- [21.6. Jak działa synchronizacja i diagnostyka w SICAR DiagAddOn?](#216-jak-działa-synchronizacja-i-diagnostyka-w-sicar-diagaddon--)
- [21.7. Czym różni się ilockExtSync od ilockExtInt i jak działa synchronizacja zewnętrzna między sekwencjami?](#217-czym-różni-się-ilockextsync-od-ilockextint-i-jak-działa-synchronizacja-zewnętrzna-między-sekwencjami--)
- [21.8. Jak działają rozgałęzienia (branching) i funkcja Stop/Hold w sekwencjach SICAR?](#218-jak-działają-rozgałęzienia-branching-i-funkcja-stophold-w-sekwencjach-sicar--)
- [21.9. Co to jest DB1000 (UiDiagAddOn_DB) i jak wykorzystujesz go w programowaniu?](#219-co-to-jest-db1000-uidiagaddon_db-i-jak-wykorzystujesz-go-w-programowaniu--)
- [21.10. Jak działają ekrany ruchów (Movement Screens) i blokada ruchów (Lock Movements) w SICAR?](#2110-jak-działają-ekrany-ruchów-movement-screens-i-blokada-ruchów-lock-movements-w-sicar--)

---

## PLAN NAUKI — JAK UŻYWAĆ TEGO DOKUMENTU

> **177 pytań / 21 sekcji.**


---

### TECHNIKA SZYBKIEJ NAUKI (Feynman Loop)

1. **Przeczytaj pytanie** — zakryj odpowiedź
2. **Powiedz własnym słowami** (głośno lub pisząc)
3. **Odkryj odpowiedź** — sprawdź co przegapiłeś
4. **Zapamiętaj 1–2 kluczowe słowa** z odpowiedzi (np. *"passivation = substitute value"*)

Dziennie: **5–8 pytań z Fazy 1 lub 2** zamiast czytania całego dokumentu.

---

