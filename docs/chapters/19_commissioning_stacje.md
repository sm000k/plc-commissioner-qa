## 19. COMMISSIONING — DODAWANIE STACJI I URZĄDZEŃ DO PROJEKTU


### 19.1. Jak krok po kroku dodajesz nową wyspę sygnałową ET200SP Safety (F-peripheral) do istniejącego projektu?  🟡

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

> ⚠️ **F-Address = unikalny w całym F-CPU:** dwa moduły z tym samym F-Address → PROFIsafe nie wykryje który jest który → błąd komisjonowania Safety. Sprawdź `Safety addresses` w konfiguracji CPU.

> 💡 **EK (element kodujący):** F-Address zapisuje się w elektronicznym elemencie kodującym na szynie BaseUnit — nie w module! Wymiana modułu F (uszkodzony) nie wymaga ponownego przypisania adresu PROFIsafe.

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
4. Sprawdź ciśnienie zasilania wyspy (typowo 4–7 bar) — brak ciśnienia = zawory aktywne ale siłownik nie rusza.

**Typowe pułapki:**
- GSDML wersja niezgodna z hardware revision wyspy → błąd `Invalid device configuration`. Zawsze sprawdź hardware revision na tabliczce wyspy i pobierz odpowiedni GSDML.
- Liczba skonfigurowanych slotów w TIA Portal ≠ fizyczna liczba modułów na wyspie → CPU zgłasza błąd `Configuration mismatch`.
- Nazwa PROFINET przypisana ale wyspa nie komunikuje się → sprawdź wersję PROFINET (EX600 może wymagać PROFINET V2.3+) i czy nie ma duplikatu nazwy w sieci.

> ⚠️ **GSDML ≠ sprzęt:** plik GSDML musi odpowiadać **dokładnie** hardware revision urządzenia (tabliczka znamionowa). Instalacja złego GSDML daje błąd konfiguracji niewidoczny do czasu połączenia online.

> 💡 **Web server wyspy:** większość urządzeń PROFINET (SMC EX600, WAGO, Festo) ma wbudowany web server (IP → przeglądarka). Szybki dostęp do diagnozy, ustawienia IP, statusu zaworów — bez TIA Portal.

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
3. Po zakończeniu: `Speed controller optimization` → `Start` — silnik wykonuje serie ruchów testowych.
4. Sprawdź `r0047 = 0` po identyfikacji — brak błędów.

**Faza 5 — Download i weryfikacja:**
1. `Download to device → Hardware and software (only changes)`.
2. Przypisz PROFINET device name: `Accessible devices` → MAC napędu → przypisz nazwę.
3. Sprawdź komunikację: `Online → Drive → Diagnostics → Control/Status words` — word sterowania STW1 przychodzi z CPU, word statusu ZSW1 wraca do CPU.
4. Test uruchomienia: ustaw `STW1 bit 0 = 1` (ON), `bit 3 = 1` (Enable operation) + zadaj prędkość → napęd rusza.
5. Sprawdź `r0002 = 7` (Run), prąd `r0027`, prędkość rzeczywistą `r0021`.
6. Test STO: aktywuj STO → `r9722.0 = 1` (STO_Active) → napęd nie generuje momentu.

**Faza 6 — Safety komisjonowanie (obowiązkowe jeśli Safety):**
1. W Startdrive: `Safety Integrated → Safety commissioning → Start safety commissioning`.
2. Wykonaj test STO z podpisem: wpuść komendę STO, zmierz czas reakcji, zapisz wynik.
3. `Accept safety settings` → Startdrive generuje **Safety checksum (Safety ID)** — zanotuj lub drukuj raport.
4. Zmień hasło komisjonowania Safety po zakończeniu.

> ⚠️ **Telegram PROFIdrive p0922:** telegram musi być identyczny w napędzie i w DB PLC (`Drive_STW`/`Drive_ZSW`). Niezgodność = poprawna komunikacja PROFINET, ale bity sterowania/statusu na złych pozycjach → napęd nie rusza lub nie reaguje na komendy.

> ⚠️ **Safety komisjonowanie = wymagany test:** po każdej zmianie parametrów Safety (STO, SS1, SLS) obowiązuje **Safety Acceptance Test** z raportem i podpisem. Dotyczy każdego napędu z Safety Integrated.

> 💡 **`Take online device as preset`:** jeśli napęd był wcześniej skonfigurowany (legacy), użyj tej opcji — TIA Portal/Startdrive wczyta aktualną konfigurację z napędu jako punkt startowy, nie nadpisze parametrów.
---

