<!-- Źródło: knowledge_base_controlbyte.md -->

## 16. Motion Control i SINAMICS — praktyka commissioning

### Czym jest Motion Control i jakie silniki są w nim wykorzystywane?
Odpowiedź — Motion Control to dziedzina automatyki zajmująca się precyzyjnym sterowaniem ruchem części mechanicznych maszyn, wymagająca wysokiej dokładności pozycjonowania i często dużej dynamiki.
- **Definicja:** Precyzyjne sterowanie ruchem.
- **Silniki wykorzystywane w Motion Control [Motor Control]:**
    - **Silniki DC szczotkowe:** Używane w przeszłości w układach serwo ze względu na prosty układ sterowania. Obecnie rzadko, głównie w pozycjonerach o małej liczbie cykli, w trybie pracy dorywczej.
    - **Silniki asynchroniczne klatkowe z enkoderem:** Stosowane w aplikacjach o małej dynamice. Charakteryzują się słabą dynamiką ze względu na duży moment bezwładności wirnika.
    - **Silniki asynchroniczne przystosowane do pracy serwo:** Ulepszona wersja silników asynchronicznych, ze zmniejszoną wagą i momentem bezwładności wirnika, co poprawia dynamikę. Posiadają zabudowany enkoder.
    - **Silniki synchroniczne z magnesami trwałymi (Servo Motors):** Najlepsze parametry dynamiczne, najczęściej wykorzystywane w aplikacjach precyzyjnego sterowania ruchem.
    - **Silniki liniowe:** Odmiana silnika synchronicznego z magnesami trwałymi, gdzie wirnik jest rozwinięty do postaci listwy, a stojan ma formę sztaby mocowanej do wózka.
    - **Silniki krokowe:** Tanie w produkcji

<!-- Źródło: knowledge_base_delta_v11.md -->

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