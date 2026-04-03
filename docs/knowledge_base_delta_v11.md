# DELTA KNOWLEDGE BASE — PATCH V11

## SEKCJA: 4. Struktury głosowania (1oo1 / 1oo2 / 2oo2 / 2oo3)

### Jak sterownik safety reaguje na błąd rozbieżności sygnału (Discrepancy Failure) w konfiguracji 1oo2?
Sterownik safety wykrywa błąd rozbieżności sygnału, gdy jeden z dwóch kanałów skonfigurowanych w ocenie 1oo2 straci ciągłość obwodu lub sygnały nie zadziałają równocześnie w określonym czasie. Jest to podstawowa funkcja diagnostyczna dla urządzeń elektromechanicznych i czujników z wyjściami tranzystorowymi.
- Błąd "Discrepancy failure" jest zgłaszany w buforze diagnostycznym PLC, wskazując kanał awarii.
- Po usunięciu przyczyny błędu (np. ponownym podłączeniu obwodu), diody modułu naprzemian migają na czerwono i zielono, sygnalizując możliwość resetu reintegracji.
- Czas rozbieżności (np. 50 ms) musi być precyzyjnie dobrany, aby uniknąć fałszywych błędów lub zbyt długiej zwłoki w wykryciu awarii.
*Źródło: transkrypcje ControlByte*

### Jakie są scenariusze awaryjne wykrywane przez moduł safety w układzie dwukanałowym 1oo2?
Moduł safety w układzie dwukanałowym 1oo2 jest w stanie wykryć różne scenariusze awaryjne, które mogą prowadzić do niebezpiecznych sytuacji, zapewniając wysoką diagnostykę.
- **Zwarcie do potencjału 0 V (zwarcie do masy):** Moduł zgłasza błąd "Overload or internal sensor supply short circuit to ground", pasywuje kanał i rozłącza styczniki.
- **Zwarcie międzykanałowe (do P):** Moduł zgłasza błąd "Internal sensor supply short circuit to P" lub "Short-circuit of two encoder supplies", cały moduł zapala się na czerwono.
- **Rozbieżność sygnału (Discrepancy failure):** Wykrywana, gdy jeden z kanałów straci ciągłość obwodu lub sygnały nie zadziałają równocześnie, co jest kluczowe dla urządzeń z mechanicznymi stykami (E-STOP, wyłączniki krańcowe) lub wyjściami tranzystorowymi.
*Źródło: transkrypcje ControlByte*

### Jak parametr "Reintegration after discrepancy error" wpływa na obsługę błędu rozbieżności sygnału?
Parametr "Reintegration after discrepancy error" w konfiguracji modułu safety określa, czy po wystąpieniu błędu rozbieżności sygnału wymagane jest doprowadzenie sygnału do stanu zerowego przed wykonaniem resetu.
- Jeśli wybrano opcję "Test zero signal necessary", operator musi wymusić stan zerowy na czujniku (np. wcisnąć i odciągnąć E-STOP) zanim możliwy będzie reset reintegracji.
- Ten parametr jest istotny dla sposobu obsługi stanowiska przez operatora, szczególnie w przypadku starszych urządzeń, które mogą generować sporadyczne błędy rozbieżności.
- Reset reintegracji kanałów safety w sterowniku PLC jest odrębny od resetu funkcji bezpieczeństwa, który wymaga innej logiki programowania.
*Źródło: transkrypcje ControlByte*

## SEKCJA: 8. Napędy Safety — SINAMICS z wbudowanym Safety

### Jakie funkcje bezpieczeństwa są wbudowane w serwowzmacniacz Sinamics V90 i jak należy je podłączyć?
Serwowzmacniacz Sinamics V90 jest wyposażony w funkcję bezpieczeństwa STO (Safe Torque Off), która zapewnia bezpieczne zdjęcie momentu obrotowego z napędu.
- Funkcja STO jest realizowana poprzez terminale STO+, STO1 i STO2.
- Domyślnie terminale te są zmostkowane, co oznacza, że funkcja STO jest nieaktywna w trybie bezpieczeństwa.
- W docelowej aplikacji sygnały STO należy podłączyć dwukanałowo do układu bezpieczeństwa, takiego jak przekaźnik bezpieczeństwa lub programowalny sterownik bezpieczeństwa (PLC Safety), aby zapewnić bezpieczne zatrzymanie napędu.
*Źródło: transkrypcje ControlByte*

## SEKCJA: 10. Robot ABB IRC5 — integracja z PLC

### Jakie protokoły komunikacyjne i format danych są wykorzystywane do integracji robota ABB IRC5 z PLC Siemens?
Integracja robota ABB z kontrolerem IRC5 ze sterownikiem PLC Siemens może być realizowana za pośrednictwem protokołu TCP lub UDP, z wykorzystaniem standardu XML do przesyłania danych.
- Komunikacja odbywa się z częstotliwością około 250 Hz (cykl co 4 ms) dzięki modułowi "Robot Reference Interface".
- **TCP (Transmission Control Protocol):** Wybierany, gdy kluczowe jest otrzymanie każdej ramki danych, nawet kosztem powtórnego wysyłania.
- **UDP (User Datagram Protocol):** Wybierany, gdy nie jest istotne otrzymanie każdej ramki (może zostać utracona), ale ważna jest aktualna wartość i ciągłość nadawania.
- Dane są przesyłane w formacie XML, który jest językiem znaczników umożliwiającym reprezentowanie informacji za pomocą struktury elementów i atrybutów.
*Źródło: transkrypcje ControlByte*

### Jakie są kluczowe elementy struktury telegramu XML wysyłanego z robota ABB IRC5 do PLC?
Telegram XML wysyłany z robota ABB IRC5 do PLC zawiera ustrukturyzowane dane dotyczące stanu i położenia robota, wykorzystując elementy i atrybuty.
- Głównymi częściami dokumentu XML są elementy, takie jak `RobData` (element nadrzędny/root), `RobMode`, `Ts_act`, `P_act`, `J_act`, `Ts_des`, `P_des`, `J_des`.
- Elementy mogą zawierać tekst (np. `RobMode` z wartością "Auto") lub atrybuty (np. `RobData` z atrybutami `Id` i `Ts` zawierającymi wartości w cudzysłowie).
- Możliwe jest zagnieżdżanie elementów, gdzie `RobData` zawiera inne elementy, które z kolei posiadają atrybuty informujące o aktualnym położeniu i orientacji robota.
- Telegram jest kodowany w standardzie UTF-8, który jest rozszerzonym kodowaniem obejmującym znaki ASCII.
*Źródło: transkrypcje ControlByte*

### Jak przebiega proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens?
Proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens obejmuje odbiór danych, konwersję znaków i ekstrakcję informacji z elementów i atrybutów XML.
- Sterownik PLC odbiera ramkę danych za pośrednictwem protokołu TCP.
- Odebrane bajty są dekodowane jako zmienne typu `character` (char), reprezentujące znaki w formacie ASCII/UTF-8.
- Następnie, z wykorzystaniem odpowiednich funkcji (np. z biblioteki LString), następuje dekodowanie poszczególnych pól dla elementów w znacznikach XML.
- Odczytywane są wartości atrybutów, które stanowią zmienne robota, takie jak położenie i orientacja.
- Do symulacji i testowania komunikacji można wykorzystać narzędzia takie jak PLCSIM Advanced i Node-RED, który generuje przykładowe telegramy XML.
*Źródło: transkrypcje ControlByte*

## SEKCJA: 16. Motion Control i SINAMICS — praktyka commissioning

### Jakie są podstawowe komponenty układu napędowego opartego o serwonapęd Sinamics V90 i sterownik Siemens?
Kompletny układ napędowy oparty o serwonapęd Sinamics V90 składa się z trzech głównych komponentów, które współpracują ze sobą w celu realizacji ruchu.
- **Sterownik PLC:** Mózg układu (np. Siemens S7-1200, S7-1500), odpowiedzialny za obliczenia dotyczące pozycjonowania osi oraz wydawanie komend ruchu.
- **Serwowzmacniacz (przekształtnik):** Odbiera telegramy wysyłane ze sterownika PLC poprzez sieć PROFINET i steruje serwosilnikiem. Seria V90 występuje w wersjach sterowanych sieciowo lub poprzez impulsy PTI (Pulse Train Input).
- **Serwosilnik:** Zainstalowany w układzie mechanicznym (np. napęd liniowy ze śrubą kulową), wykonuje ruch zgodnie z komendami ze wzmacniacza.
*Źródło: transkrypcje ControlByte*

### Jakie oprogramowanie jest wymagane do konfiguracji i programowania serwonapędu Sinamics V90?
Do konfiguracji i programowania serwonapędów Sinamics V90 niezbędne są dwa główne środowiska programistyczne i narzędzia.
- **Sinamics V-Assistant Commissioning tool:** Oprogramowanie służące do wstępnej konfiguracji serwowzmacniacza, testowania (np. tryb Jog), przywracania ustawień fabrycznych, wyboru serwomotoru, ustawiania trybu sterowania i przeprowadzania auto-tuningu.
- **TIA Portal (wersja 15.1 lub nowsza):** Środowisko do programowania sterownika PLC (np. S7-1200, S7-1500), konfiguracji sieci PROFINET (nadawanie adresu IP i nazwy PROFINETowej serwowzmacniaczowi) oraz pisania programu użytkownika do sterowania napędem.
*Źródło: transkrypcje ControlByte*

### Jakie są dostępne tryby sterowania dla serwowzmacniacza Sinamics V90 i jakie sterowniki PLC są z nimi kompatybilne?
Serwowzmacniacz Sinamics V90 oferuje dwa główne tryby sterowania, z których każdy ma określone wymagania dotyczące sterownika PLC.
- **Speed Control (Sterowanie prędkością):** W tym trybie serwowzmacniacz V90 współpracuje ze sterownikiem S7-1200. Wzmacniacz odpowiada za regulowanie prędkości do zadanej wartości, natomiast sterownik PLC wykonuje obliczenia związane z pozycjonowaniem.
- **Basic Positioner Control (Sterowanie pozycjonerem):** Ten tryb wymaga zastosowania sterownika S7-1500. W tym przypadku serwowzmacniacz samodzielnie realizuje funkcje pozycjonowania.
- Wybór odpowiedniego telegramu PROFINET jest kluczowy; sterownik S7-1200 współpracuje z telegramami 1, 2 lub 3, natomiast telegram 102 wymaga sterownika S7-1500.
*Źródło: transkrypcje ControlByte*

### Na czym polega procedura One Button Auto Tuning w Sinamics V-Assistant i jakie parametry są optymalizowane?
Procedura One Button Auto Tuning w oprogramowaniu Sinamics V-Assistant służy do automatycznej optymalizacji regulatorów serwonapędu Sinamics V90, dostosowując je do właściwości dynamicznych układu mechanicznego.
- Podczas auto-tuningu serwomechanizm wykonuje ruch w określonym zakresie (np. jeden obrót), analizując obciążenie i dynamikę układu.
- W wyniku tej procedury zmieniane są parametry regulatora prędkości, takie jak wzmocnienie (gain) i czas zdwojenia (integral time) dla części całkującej.
- Parametry regulatora pozycji pozostają bez zmian, ponieważ w trybie prędkościowym (Speed Control) nie są one wykorzystywane przez serwowzmacniacz.
- Zoptymalizowane wartości są zapisywane w pamięci nieulotnej ROM urządzenia.
*Źródło: transkrypcje ControlByte*

### Do czego służy blok funkcyjny MC_MoveJog w TIA Portal i jakie są jego podstawowe parametry wejściowe?
Blok funkcyjny MC_MoveJog w TIA Portal służy do sterowania osią z zadaną prędkością, najczęściej wykorzystywany jest do ruchu w trybie ręcznym (JOG), ale może być również używany w normalnym cyklu pracy maszyny.
- Jest to blok typu Enable, co oznacza, że działa tak długo, dopóki na jego wejściu `JogForward` lub `JogBackward` podany jest stan wysoki.
- **`Axis`:** Referencja do obiektu technologicznego (SpeedAxis, PositioningAxis, SynchronousAxis).
- **`JogForward` (BOOL):** Aktywuje ruch osi do przodu.
- **`JogBackward` (BOOL):** Aktywuje ruch osi do tyłu (jednoczesne aktywowanie obu powoduje błąd).
- **`Velocity` (Long Real):** Bezwzględna wartość prędkości, z jaką oś ma się poruszać (np. w mm/s); wartość ujemna jest traktowana jako bezwzględna, a kierunek nadaje `JogForward`/`JogBackward`.
- **`Acceleration`, `Deceleration`, `Jerk` (Long Real):** Parametry dynamiki ruchu; wartość -1 powoduje użycie parametrów skonfigurowanych w obiekcie technologicznym.
- **`PositionControl` (BOOL):** Aktywuje regulator pozycji (domyślnie True).
*Źródło: transkrypcje ControlByte*

### Jakie są kluczowe cechy i zachowania bloku MC_MoveJog podczas pracy?
Blok MC_MoveJog charakteryzuje się specyficznymi zachowaniami i wyjściami statusowymi, które informują o jego działaniu i umożliwiają dynamiczną kontrolę ruchu.
- Po aktywacji ruchu (np. `JogForward` = True), na wyjściu `Busy` pojawia się stan True, a po osiągnięciu zadanej prędkości, bit `InVelocity` również przyjmuje wartość True.
- W przypadku błędnej parametryzacji (np. nieodpowiednie przyspieszenie), na wyjściu `Error` pojawia się True, a `ErrorID` wskazuje kod błędu (np. 8004h dla "Illegal acceleration specification").
- Podczas trwania ruchu możliwe jest dynamiczne zmienianie parametrów `Velocity`, `Acceleration`, `Deceleration` i `Jerk` "w locie", co jest przydatne w aplikacjach wymagających adaptacji prędkości.
- Podanie wartości 0 dla `Velocity` podczas aktywnego bloku spowoduje zahamowanie osi i utrzymanie prędkości zerowej.
*Źródło: transkrypcje ControlByte*