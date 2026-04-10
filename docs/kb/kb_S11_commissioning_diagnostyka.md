<!-- Źródło: knowledge_base_controlbyte.md -->

## 11. Commissioning i diagnostyka

### Jakie są kluczowe aspekty uruchomienia i diagnostyki sterownika PLC oraz systemu HMI w TIA Portal?
Odpowiedź — Uruchomienie i diagnostyka w TIA Portal obejmuje konfigurację sprzętu, wgranie programu, symulację oraz monitorowanie zmiennych i błędów, zarówno w sterowniku, jak i na panelu HMI.
- **Instalacja i pierwszy projekt [TIA Portal]:**
    - Pobranie TIA Portal V15.1 TRIAL (21 dni pełnej wersji) oraz STEP 7 PLCSIM.
    - Włączenie Framework 3.5 w Windows 10.
    - Utworzenie projektu, dodanie sterownika (np. S7-1200 1211C Firmware 4.2) i panelu HMI (np. KTP400 Firmware 15.0.0).
    - Włączenie opcji "Support simulation during block compilation" dla sterownika.
    - Wgranie programu do symulatora PLC (PLCSIM Advanced).
    - Uruchomienie symulatora panelu HMI.
- **Diagnostyka sterownika PLC [TIA Portal]:**
    - **Bufor diagnostyczny:** Wyświetla błędy (np. "Overload or internal sensor supply short circuit to ground" dla zwarcia do 0V, "Discrepancy failure" dla rozbieżności sygnału).
    - **Watch Table:** Umożliwia monitorowanie wartości zmiennych w czasie rzeczywistym, w różnych formatach (np. Hex, Char).
    - **Online view:** Podświetla aktywne sygnały na zielono w programie (np. w PNOZmulti Configurator).
    - **Web Server:** Wbudowany w S7-1200, pozwala na diagnostykę i wyświetlanie własnych stron WWW.
- **Diagnostyka panelu HMI [HMI]:**
    - **System Screens:** Dostęp do ekranów systemowych, takich jak diagnostyka systemu PLC, informacje projektowe, zarządzanie użytkownikami, informacje systemowe, konfiguracja panelu HMI.
    - **Alarms:** Wyświetlanie alarmów (np. w formie okien pop-up lub na dedykowanych ekranach).
    - **Diagnostic buffer:** Komunikaty od sterownika PLC (np. przejścia trybów pracy, błędy).
    - **Trends:** Wykresy generowane na bieżąco, z możliwością poruszania się, zatrzymywania i wznawiania.
*Praktyk: [Podczas uruchomień często zostaje się samemu z problemem, który trzeba szybko rozwiązać, co jest końcowym sprawdzianem umiejętności automatyka. Etykiety przewodów i urządzeń na schematach elektrycznych są bardzo pomocne w diagnozowaniu systemu.] [TIA Portal] [HMI] [PLC]*

### Jakie są etapy uruchomienia i konfiguracji serwonapędu SINAMICS V90 za pomocą oprogramowania V-Assistant?
Odpowiedź — Uruchomienie serwonapędu SINAMICS V90 wymaga użycia dedykowanego oprogramowania V-Assistant do konfiguracji parametrów napędu oraz TIA Portal do programowania sterownika PLC.
- **Wymagane oprogramowanie [Sinamics] [TIA Portal]:**
    - Sinamics V-Assistant Commissioning tool.
    - TIA Portal V15.1 lub nowsza.
- **Połączenie z V-Assistant [Sinamics]:**
    - Możliwe przez interfejs USB lub sieciowy (Ethernet).
    - Po odnalezieniu serwowzmacniacza w sieci, wybiera się "Device Commissioning".
- **Przywracanie ustawień fabrycznych [Sinamics]:**
    - W V-Assistant: Tools -> Factory Default -> Yes. Napęd resetuje wszystkie ustawienia.
- **Konfiguracja podstawowa [Sinamics]:**
    - **Select Drive:** Wybór serwomotoru (domyślny lub inny z listy, np. z hamulcem/bez).
    - **Control Mode:** Wybór trybu sterowania.
        - "Speed Control" dla S7-1200 (serwowzmacniacz reguluje prędkość, PLC wykonuje obliczenia pozycjonowania).
        - "Basic Positioner Control" dla S7-1500.
    - **Jog:** Testowanie ruchu napędu w trybie ręcznym.
        - Ustawienie prędkości (np. 500 obrotów/min).
        - Sprawdzenie, czy servo działa, co potwierdza prawidłowe okablowanie.
    - **Set PROFINET:** Wybór telegramu komunikacyjnego (np. telegram nr 3 dla S7-1200; telegram nr 102 dla S7-1500).
    - **Konfiguracja sieciowa:** Adres IP i nazwa PROFINETowa nadawane z TIA Portal.
    - **Set Limits:** Ustawienie limitów momentu obrotowego (np. 300% momentu znamionowego) i prędkości.
    - **Digital Input Output:** Konfiguracja wejść/wyjść cyfrowych (np. ograniczenie momentu, zakresu prędkości, Emergency Stop, gotowość napędu, błąd).
- **Optymalizacja napędu (Tuning) [Sinamics]:**
    - **Optimize Drive:** Zakładka do testowania interfejsu, wejść/wyjść cyfrowych.
    - **One Button Auto Tuning:** Automatyczna procedura tuningu regulatorów.
        - Wprowadzenie zakresu ruchu (np. jeden obrót).
        - Servo porusza się, sprawdzając właściwości dynamiczne układu mechanicznego i dostosowując regulator.
    - **Optimize Drive Tuning Parameters:** Wyświetla zmienione parametry regulatora prędkości (wzmocnienie, czas zdwojenia) po autotuningu. Regulator pozycji pozostaje bez zmian w trybie prędkościowym.
- **Zapis parametrów [Sinamics]:**
    - Akceptacja wartości i zapis w pamięci nieulotnej ROM.
*Praktyk: [Fakt, że servo działa w trybie Jog, świadczy o prawidłowym podłączeniu okablowania i sprawności układu. Servo może być przeciążone nawet trzykrotnie w krótkim okresie, ale nie należy nadużywać tej funkcjonalności.] [Sinamics]*

### Jakie są możliwości diagnostyki i testowania programów PLC za pomocą języka Python i protokołu OPC UA?
Odpowiedź — Język Python, w połączeniu z protokołem OPC UA, umożliwia automatyzację testów oprogramowania PLC, co jest szczególnie przydatne w przypadku złożonych projektów, gdzie testy manualne są czasochłonne i podatne na błędy.
- **Zastosowanie Pythona w automatyce przemysłowej [Python]:**
    - Automatyzacja powtarzalnych zadań na poziomie GUI w środowiskach PLC (np. Codesys).
    - Komunikacja w protokołach przemysłowych (Modbus, OPC UA).
    - Programowanie Raspberry Pi.
    - Testowanie oprogramowania PLC (np. biblioteka Pytest).
    - Przetwarzanie danych z obiektu (SCADA, systemy chmurowe), generowanie raportów (CSV, wykresy).
    - Tworzenie aplikacji desktopowych/webowych dla automatyki (Django, Flask).
- **Testy automatyczne z Pythonem [Python]:**
    - **Cel:** Zautomatyzowanie testów bloków funkcyjnych PLC.
    - **Zalety:** Powtarzalność, dokładność, oszczędność czasu i zasobów (automatyków).
    - **Komunikacja:** Protokół OPC UA. Sterownik PLC działa jako serwer, skrypt Python jako klient.
    - **Wymagane biblioteki Python:**
        - `opcua`: Do komunikacji z serwerem OPC UA.
        - `pytest`: Do automatyzacji testów.
        - `pytest-html`: Do generowania raportów HTML.
        - `time`: Do generowania opóźnień w skrypcie.
    - **Struktura testu:**
        - Plik `opc.py`: Funkcje do łączenia/rozłączania z serwerem OPC UA.
        - Plik `tags.py`: Definicja zmiennych PLC (np. start, stop, emergency, czujnik, x_sygnalizacja), które będą wymieniane przez OPC UA.
        - Plik `test_unit.py`: Zawiera funkcje testowe (np. `test_start_button`, `test_stop_button`, `test_emergency_stop`).
        - **`assert`:** Słowo kluczowe do sprawdzania poprawności wyników testów.
    - **Przebieg testu:**
        1. Inicjalizacja (połączenie z serwerem OPC UA, reset tagów).
        2. Symulacja działania wejść (np. ustawienie `start` na `True`, odczekanie).
        3. Sprawdzenie stanu wyjść (np. czy `x_sygnalizacja` zmieniła się z `False` na `True`).
        4. Reset tagów po każdym teście.
    - **Generowanie raportu:** Komenda `pytest --html=report.html` tworzy plik HTML z wynikami testów.
*Praktyk: [Można testować oprogramowanie PLC na wirtualnym sterowniku (SoftPLC) uruchomionym na komputerze PC, bez potrzeby posiadania fizycznego sprzętu. W przypadku błędu w programie PLC, testy automatyczne szybko go wykrywają, co jest informacją dla programisty o konieczności naprawy.] [Python] [TIA Portal] [Codesys]*

