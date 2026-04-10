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
