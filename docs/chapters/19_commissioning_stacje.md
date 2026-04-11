## 19. COMMISSIONING — DODAWANIE STACJI I URZĄDZEŃ DO PROJEKTU


### 19.1. Jak krok po kroku dodajesz nową wyspę sygnałową ET200SP Safety (F-peripheral) do istniejącego projektu?  🟡

Procedura commissioning nowej stacji ET200SP z modułami F-DI/F-DQ:

**Faza 1 — Projekt TIA Portal (offline):**
1. `Devices & Networks` → `Add new device` → `ET 200SP` → wskaż numer katalogowy IM (np. `6ES7155-6AU01-0BN0`)
2. Ustaw IP address i PROFINET device name (unikalne w sieci)
3. Dodaj moduły w slotach: BaseUnit + F-DI/F-DQ — kolejność slotów = kolejność fizyczna na szynie
4. Każdy moduł F: `Properties → Safety` → ustaw **F-Address** (unikalny w ramach F-CPU, zakres 1–65534)
5. Parametry F: discrepancy time (10–200ms), sensor supply, substitute value, F-monitoring time
6. `Compile → Hardware + Software (rebuild all)`

**Faza 2 — Przypisanie adresu PROFINET (online):**
1. `Go online` → `Assign PROFINET device name` → wyszukaj po MAC → przypisz nazwę

**Faza 3 — Przypisanie PROFIsafe address:**
1. Prawym na moduł F → `Assign PROFIsafe address` → diody LED migają → potwierdź
2. Adres zapisywany w elemencie kodującym (EK) na BaseUnit — nie przepada przy wymianie modułu

**Faza 4 — Download i weryfikacja:**
1. `Download to device → Hardware and software (only changes)`
2. Sprawdź Diagnostics buffer — brak nowych błędów, moduły online zielone
3. Monitoruj F-DB: `PASS_OUT = FALSE` = prawidłowa praca
4. Test Safety: zasymuluj zadziałanie czujnika → sprawdź passivation i reakcję logiki

**Typowe pułapki:**
- IP kolizja lub brak 24V BusAdapter → IM nie odpowiada na ping
- Czerwony LED F-DI → sprawdź okablowanie czujnika lub parametr Sensor supply
- Typ BaseUnit (P/A) musi pasować do modułu I/O

> ⚠️ **F-Address musi być unikalny w całym F-CPU** — duplikat = błąd PROFIsafe.

> 💡 **EK (element kodujący):** wymiana uszkodzonego modułu F nie wymaga ponownego przypisania F-Address.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 19.2. Jak dodajesz wyspę pneumatyczną SMC (seria EX600) do projektu TIA Portal przez PROFINET?

Wyspa zaworów pneumatycznych SMC EX600 komunikuje się przez PROFINET jako standardowe urządzenie I/O (nie Safety).

**Krok 1 — Instalacja GSDML:**
- Pobierz GSDML ze strony SMC (`smcworld.com` → Support) — wersja musi odpowiadać hardware revision z tabliczki
- TIA Portal → `Options → Manage GSD files → Install` → wskaż plik `.xml`

**Krok 2 — Konfiguracja w TIA Portal:**
1. Przeciągnij `EX600` z Hardware Catalog do Network view, połącz z CPU
2. Ustaw IP Address i PROFINET device name
3. Device view: skonfiguruj sloty modułów zaworów (1 bajt = 8 zaworów) — liczba = fizyczna konfiguracja
4. Opcjonalnie: moduł diagnostyczny i moduł wejść (DI) czujnikowych

**Krok 3 — Przypisanie nazwy PROFINET:**
1. `Assign PROFINET device name` → wyszukaj po MAC → przypisz
2. Alternatywnie: wbudowany web server wyspy (domyślne IP `192.168.0.1`)

**Krok 4 — Program i test:**
1. Adresy Q sterują elektrozaworami: `Q0.0 = TRUE` → zawór 1 otwarty
2. Test: `Force Values` w TIA Portal → sprawdź fizycznie czy zawór zadziałał
3. Sprawdź ciśnienie zasilania wyspy (4–7 bar) — brak ciśnienia = zawory aktywne ale siłownik stoi

**Typowe pułapki:**
- GSDML niezgodna z hardware revision → `Invalid device configuration`
- Liczba slotów w TIA ≠ fizyczna → `Configuration mismatch`
- Duplikat nazwy PROFINET w sieci → brak komunikacji

> ⚠️ **GSDML musi odpowiadać hardware revision** z tabliczki znamionowej urządzenia.

> 💡 Większość urządzeń PROFINET (SMC, WAGO, Festo) ma wbudowany web server — szybka diagnoza bez TIA Portal.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 19.3. Jak krok po kroku dodajesz napęd SINAMICS G120 przez PROFINET do projektu TIA Portal?

**Faza 1 — Przygotowanie sprzętowe:**
1. Sprawdź CU (musi obsługiwać PROFINET: CU240E-2 PN lub CU250S-2 PN) i Power Module (PM)
2. IP można przypisać przez TIA Portal (auto-assign), BOP2 (parametry PROFINET `p0918`–`p0924` ⚗️ DO WERYFIKACJI) lub Startdrive
3. Sprawdź firmware: `r0018` na BOP2 — zapisz wersję dla kompatybilności z TIA Portal

**Faza 2 — Konfiguracja w Startdrive (TIA Portal):**
1. `Add new device` → `SINAMICS G120` → wybierz CU i PM
2. Alternatywnie: `Accessible devices` → wykryj online → `Take online device as preset` (zachowa parametry)
3. Network view: połącz z PLC, ustaw IP i PROFINET device name
4. Telegram PROFIdrive `p0922`: 1 = standardowy, 20 = rozszerzony, 352 = Safety Integrated
5. Drive parameters: dane tabliczkowe silnika lub numer katalogowy

**Faza 3 — Safety (jeśli STO/SS1 przez PROFIsafe):**
1. Startdrive → Safety Integrated → Enable
2. Źródło komend: `Via PROFIsafe` / `Via terminals` / oba
3. Ustaw F-Address (identyczny w TIA Portal i napędzie)
4. Funkcje Safety: STO, SS1 (`p9560` = czas rampy), SLS (`p9531` = max prędkość)
5. Safety Commissioning password — ustaw własne w produkcji

**Faza 4 — Motor identification:**
1. Napęd w stanie Ready → Static identification (~30s, silnik stoi)
2. Opcjonalnie: Speed controller optimization (silnik się obraca — zabezpiecz strefę)
3. Sprawdź `r0047 = 0` po identyfikacji

**Faza 5 — Download i weryfikacja:**
1. `Download to device → Hardware and software`
2. Przypisz PROFINET device name: `Accessible devices` → MAC → assign
3. Online: Control/Status words → STW1 z CPU, ZSW1 z napędu
4. Test: STW1 bit 0+3 = ON + Enable, zadaj prędkość → sprawdź `r0002 = 7` (Run)
5. Test STO: aktywuj → `r9722.0 = 1` → napęd nie generuje momentu

**Faza 6 — Safety komisjonowanie (obowiązkowe):**
1. Startdrive → Safety commissioning → test STO z podpisem → Safety checksum (Safety ID)
2. Zmień hasło komisjonowania Safety po zakończeniu

> ⚠️ **Telegram `p0922`** musi być identyczny w napędzie i DB PLC — niezgodność = bity sterowania na złych pozycjach.

> ⚠️ Po **każdej** zmianie parametrów Safety wymagany Safety Acceptance Test z raportem.

> 💡 `Take online device as preset` — idealne gdy napęd był wcześniej skonfigurowany (legacy).
---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*

### 19.4. Jak dodajesz stację ET200MP z modułami Safety do istniejącej linii produkcyjnej z wieloma stacjami PROFINET?

**ET200MP** to wariant wysp I/O Siemens w formacie S7-300 (35mm) — stosowany gdy potrzebne są moduły o większej gęstości kanałów niż ET200SP.

**Krok 1 — Planowanie adresacji:**
- Sprawdź istniejącą tabelę adresów: wolny adres IP w podsieci, wolna nazwa PROFINET, wolne zakresy F-Address
- Zweryfikuj, czy F-Address nie kolidują z innymi stacjami F-I/O — duplikat = PROFIsafe error na OBU stacjach

**Krok 2 — Konfiguracja w TIA Portal:**
1. `Add new device` → `ET 200MP` → wybierz IM (np. IM155-5 PN) — numer katalogowy z tabliczki
2. Device view: wstaw moduły w slotach — kolejność musi odpowiadać fizycznej konfiguracji na szynie
3. Dla modułów F-DI/F-DQ: zakładka Safety → F-Address, discrepancy time, sensor evaluation, test pulse
4. Network view: połącz z F-CPU, sprawdź, że PROFINET subnet jest wspólna

**Krok 3 — Podłączenie fizyczne:**
- Kabel PROFINET RJ45 z istniejącego switcha/portu IM do nowej stacji
- Sprawdź topologię: ring (MRP) wymaga dwóch kabli, linia jeden kabel
- Zasilanie 24V DC: osobne zasilanie dla IM i osobne dla modułów I/O (rozdzielone w ET200MP)

**Krok 4 — Online: nazwy, adresy, download:**
1. `Assign PROFINET device name` po MAC
2. `Assign PROFIsafe address` dla każdego modułu F
3. Download → sprawdź Diagnostic Buffer → moduły zielone
4. Test Safety: wymuś sygnał na F-DI → sprawdź reakcję w F-programie

**Praktyka commissioning:** Na działającej linii — NIGDY nie rób „Download all" do F-CPU. Użyj „Download only changes" (delta download) — inaczej zatrzymasz Safety na całej linii i wymusisz pełny Safety Acceptance Test.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*

### 19.5. Co to jest „Assign PROFIsafe address" i dlaczego jest wymagane osobno od konfiguracji TIA Portal?

**PROFIsafe address (F-Address)** to unikalny identyfikator urządzenia Safety w sieci PROFIsafe. Musi być zapisany zarówno w projekcie TIA Portal (konfiguracja) jak i fizycznie w urządzeniu — i muszą się zgadzać.

- **Dlaczego osobno?** F-Address jest zapisywany w urządzeniu niezależnie od download projektu — jako zabezpieczenie przed przypadkową podmianą modułów. Gdyby F-Address był nadawany automatycznie przy download, wymiana modułu na identyczny w innym slocie mogłaby pozostać niezauważona → zagrożenie bezpieczeństwa
- **Mechanizm w ET200SP:** F-Address jest zapisywany w **elemencie kodującym (EK — Codierelement)** na BaseUnit, nie w samym module F-DI/F-DQ. Wymiana uszkodzonego modułu F nie wymaga ponownego „Assign PROFIsafe address" — adres pozostaje w EK
- **Mechanizm w ET200MP:** F-Address jest zapisywany w profilu modułu na szynie backplane
- **W napędach SINAMICS:** F-Address jest zapisywany w CU napędu (parametr wewnętrzny) — wymiana CU wymaga ponownego przypisania F-Address

**Procedura „Assign PROFIsafe address" w TIA Portal:**
1. Prawy klik na moduł F w network/device view → `Assign PROFIsafe address`
2. Diody LED na module migają (identyfikacja fizyczna — potwierdź, że to właściwy moduł)
3. Potwierdź → adres jest zapisywany w urządzeniu
4. Powtórz dla każdego modułu F w stacji

**Praktyka commissioning:** Przy rozbudowie istniejącej instalacji — spisz tabelę F-Address dla całej linii PRZED rozpoczęciem pracy. Kolizja F-Address jest trudna do zdiagnozowania i objawia się passivation na pozornie losowych modułach.

> Źródło: SIMATIC Safety - Konfiguracja i programowanie, rozdział „Zalecenia dotyczące przypisywania adresu PROFIsafe" [ZWERYFIKOWANE]

### 19.6. Jak dodajesz urządzenie firm trzecich (np. Festo, Beckhoff, WAGO) do projektu TIA Portal przez PROFINET?

**Urządzenia firm trzecich** komunikują się z PLC Siemens przez PROFINET jako standardowe I/O devices, ale wymagają instalacji pliku GSDML (GSD Markup Language) — odpowiednika sterownika urządzenia.

**Krok 1 — Pozyskanie GSDML:**
- Producent urządzenia udostępnia plik `.xml` (GSDML) na swojej stronie wsparcia technicznego
- **GSDML musi odpowiadać hardware revision** — numer rewizji jest na tabliczce znamionowej urządzenia. Niezgodna wersja → „Module does not match" lub brak urządzenia w katalogu

**Krok 2 — Instalacja w TIA Portal:**
1. `Options → Manage general station description files (GSD)` → `Install`
2. Wskaż folder z pobranym plikiem `.xml` → zainstaluj
3. Urządzenie pojawi się w Hardware Catalog w kategorii `Other field devices → PROFINET IO`

**Krok 3 — Konfiguracja:**
1. Przeciągnij urządzenie z katalogu do Network view → połącz z PLC
2. Ustaw IP address i PROFINET device name
3. Device view: skonfiguruj sloty/subsloty wg dokumentacji producenta (liczba i kolejność modułów musi odpowiadać fizycznej konfiguracji)
4. Jeśli urządzenie ma wbudowany web server (większość nowoczesnych urządzeń PROFINET) — wpisz IP w przeglądarkę dla szybkiej diagnostyki

**Krok 4 — Online:**
1. `Assign PROFINET device name` po MAC address
2. Download configuration do PLC
3. Sprawdź online status: zielone → komunikacja OK, czerwone → sprawdź GSDML version, IP, nazwę

**Typowe problemy:**
- Niekompatybilna wersja GSDML → „Station not configured" alarm w PLC
- Urządzenie nie odpowiada na `Assign device name` → sprawdź, czy firmware urządzenia obsługuje DCP (Discovery and Configuration Protocol)
- Duplikat nazwy PROFINET w sieci → jedno z urządzeń traci komunikację

**Praktyka commissioning:** Przed wyjazdem na obiekt — pobierz GSDML dla WSZYSTKICH urządzeń firm trzecich i zainstaluj w TIA Portal. Na obiekcie bez internetu nie pobierzesz brakującego pliku.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens i praktyki commissioning*

### 19.7. Jak wygląda procedura wymiany uszkodzonego modułu ET200SP na działającej linii (hot swap)?

**Wymiana modułu ET200SP** na działającej linii produkcyjnej to standardowa procedura serwisowa. ET200SP obsługuje wymianę modułów „na gorąco" (hot swapping) bez wyłączania całej stacji.

**Warunki hot swap:**
- Nowy moduł musi być identycznego typu (ten sam numer katalogowy) jak uszkodzony
- BaseUnit pozostaje na szynie — wymieniasz tylko moduł elektroniczny (electronic module)
- Element kodujący (EK) na BaseUnit zachowuje F-Address — nie trzeba ponownie przypisywać PROFIsafe address

**Procedura krok po kroku:**
1. **Identyfikacja uszkodzonego modułu** — w TIA Portal online: moduł z czerwonym statusem lub w Diagnostic Buffer. Fizycznie: czerwona/pomarańczowa dioda LED na module
2. **Odłóż moduł** — odblokuj zatrzask, wysuń moduł elektroniczny z BaseUnit. Stacja kontynuuje pracę — pozostałe moduły nie tracą komunikacji
3. **Włóż nowy moduł** — ten sam typ → moduł automatycznie przejmuje konfigurację. Diody przechodzą z pomarańczowej na zieloną w ciągu kilku sekund
4. **Weryfikacja** — TIA Portal online: moduł zielony, brak nowych wpisów diagnostycznych. Dla modułów F: sprawdź `PASS_OUT = FALSE` (brak passivation)
5. **Jeśli moduł F był w stanie passivation** — może wymagać reintegration (ACK z programu Safety lub przycisk Reset na HMI)

**Czego NIE wymaga wymiana identycznego modułu:**
- Nie trzeba download do PLC
- Nie trzeba ponownej konfiguracji w TIA Portal
- Nie trzeba Assign PROFIsafe address (dla ET200SP — adres w EK na BaseUnit)

**Praktyka commissioning:** Trzymaj zapas modułów na obiekcie — szczególnie F-DI i F-DO. Czas wymiany modułu ET200SP to dosłownie 30 sekund, ale czas oczekiwania na dostawę może być tygodniami. Zawsze zaznacz na schemacie elektrycznym który slot używa jakiego modułu.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens, procedura hot swap standardowa dla ET200SP*
