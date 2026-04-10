## 15. KURTYNY BEZPIECZEŃSTWA I MUTING


### 15.1. Czym różni się kurtyna bezpieczeństwa Type 2 od Type 4 (IEC 61496)?

| Cecha | <span style="color:#1a5276">**Type 2**</span> | <span style="color:#1a5276">**Type 4**</span> |
|-------|-------|-------|
| Diagnostyka | Zewnętrzny moduł testujący (External Test Device) | Wewnętrzna, w każdym cyklu (self-testing) |
| DC | 60–99% | ≥ 99% |
| Max poziom Safety | do <span style="color:#1a5276">**PL d / SIL 2**</span> *(przy architekturze 1oo2)* | do <span style="color:#1a5276">**PL e / SIL 3**</span> |
| Kategoria | Cat.2 lub Cat.3 | Cat.4 |
| Zastosowanie | Lekkie maszyny, dostępy serwisowe | Robotyzowane linie automotive, prasy |

> ⚠️ Type 2 **NIE** jest ograniczona do PL c / SIL 1 — z architekturą 1oo2 osiąga PL d / SIL 2. Częste nieporozumienie na rozmowach!

**W TIA Portal:** podłączasz jako F-DI z `1oo2 evaluation` lub OSSD bezpośrednio na wejście Safety.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 15.2. Jak działa muting i czym różni się od override?

| Cecha | **Muting** | **Override** |
|-------|-----------|-------------|
| Inicjacja | Automatyczna przez program Safety | Ręczna przez operatora (klucz/przycisk) |
| Powtarzalność | Wielokrotna, automatyczna | Jednorazowe, z licznikiem i logowaniem |
| Warunki | Fizyczne (czujniki mutingowe, okno czasowe) | Brak — tylko dostęp serwisowy |
| Cel | Normalny przepływ materiału | Usuwanie awarii, serwis |
| Status prawny | Element projektu Safety (uwzględniony w ocenie ryzyka) | Środek awaryjny z ograniczonym dostępem |

**Przykład muting:** paleta wjeżdża na taśmę — czujniki mutingowe po obu stronach muszą oba zadziałać w czasie `< 4s`, tylko wtedy kurtyna jest zawieszona na czas przejazdu.

**W TIA Portal:** certyfikowany blok `MUTING_FKT` (z biblioteki LSafe) obsługuje schematy 4-czujnikowe (cross i parallel). Wymaga 2 par czujników i okna czasowego sekwencji.

> ⚠️ Override jest środkiem **wyłącznie awaryjnym** — musi być rejestrowany (kto, kiedy, ile razy). Nie stosuj jako alternatywy dla prawidłowo działającego muting.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 15.3. Jak podłączasz OSSD (Output Signal Switching Device) kurtyny do modułu F-DI?

**OSSD** to para wyjść kurtyny (OSSD1, OSSD2) — dwa kanały sygnałów bezpieczeństwa z wbudowanym testowaniem impulsowym.

**Podłączenie:**
- `OSSD1` → kanał A modułu F-DI
- `OSSD2` → kanał B modułu F-DI *(para 1oo2)*

> ⚠️ **NIE podłączaj** zasilania `VS*` (pulse test) modułu F-DI do OSSD — kurtyna sama generuje własne impulsy testowe. W TIA Portal ustaw parametr `Sensor supply` tego kanału na `None` / `Disabled` — inaczej impulsy F-DI **zablokują sygnał** z kurtyny.

`Discrepancy time`: dopasuj do specyfikacji kurtyny (zazwyczaj 10–30 ms ⚠️ DO WERYFIKACJI — sprawdź w karcie katalogowej konkretnej kurtyny).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 15.4. Jakie jest zastosowanie wyjść tranzystorowych z czujników bezpieczeństwa w systemach PLC Safety?

Wyjścia tranzystorowe z czujników bezpieczeństwa, takich jak kurtyny bezpieczeństwa czy skanery, są kluczowe dla systemów PLC Safety, ponieważ umożliwiają dwukanałowe monitorowanie i szybkie wykrywanie awarii.
- **Podłączenie:** Wyjścia tranzystorowe z czujników bezpieczeństwa podłącza się do wejść bezpieczeństwa sterownika PLC.
- **Wykrywanie awarii:**
  - Jeśli jedno z wyjść tranzystorowych ulegnie uszkodzeniu (np. spali się lub będzie miało zwarcie), system Safety natychmiast wykryje sytuację awaryjną.
  - Jest to analogiczne do wykrywania rozbieżności sygnału ("discrepancy error") w przypadku styków mechanicznych.
Praktyczne wskazówki:
- W przypadku uszkodzenia jednego z wyjść tranzystorowych kurtyny bezpieczeństwa, F-CPU natychmiast zgłosi błąd, co zapobiega dalszej pracy maszyny w niebezpiecznym stanie.
*Źródło: transkrypcje ControlByte*

### 15.5. Jakie typy elektrygli bezpieczeństwa (door interlocks) istnieją i jak dobirasz odpowiedni Performance Level?  🟡

**Elektrorygiel bezpieczeństwa** *(door interlock / guard locking)* to urządzenie mechaniczno-elektryczne które:
1. Monitoruje stan osłony (otwarta/zamknięta) — sygnał Safety do F-DI
2. Rygluje osłonę mechanicznie — uniemożliwia otwarcie strefy niebezpiecznej gdy maszyna działa

**Typy elektrygli (na przykładzie Pilz PSENm):**

| Model | Zasada | Max PL | Cechy charakterystyczne |
|-------|--------|--------|-------------------------|
| **PSENmlock mini** | Elektromechaniczny | PL d / Cat.3 | Kompaktowy, proste aplikacje, dedykowany aktuator |
| **PSENmlock** | Elektromechaniczny z klamką | PL e / Cat.4 | Klamka awaryjna (escape release) — operator może wyjść od środka; siła trzymania 7500 N; ryglowanie i odryglowanie impulsowe (bez stałego zasilania cewki); IP67; montaż na profilach 40 mm |
| **PSENslock 2** | Elektromagnetyczny (brak mechaniki) | PL e / Cat.4 | Wbudowany w osłonę, brak ruchomego aktuatora → eliminuje zużycie mechaniczne; trzymanie siłą elektromagnesu |

**Kryteria doboru:**
- **PL d wystarczy?** → PSENmlock mini (tańszy, prostszy montaż)
- **Wymagany PL e?** → PSENmlock lub PSENslock 2
- **Operator może zostać zatrzaśnięty w strefie** → PSENmlock z klamką *(wymóg EN ISO 13849-1)*
- **Aplikacja bez klamki wymaganej, chcesz uniknąć konserwacji mechanicznej** → PSENslock 2

**Podłączenie do PLC Safety:**
- Elektrorygiel ma wyjścia cyfrowe (sygnały Safety) — podłącz do F-DI Siemens z ewaluacją 1oo2
- Cewka ryglowania: steruj przez F-DO lub standardowe DQ + F-PM-E (jeśli SIL 2 wystarczy)
- Sygnały z PNOZmulti: elektrorygiel podłącz do dedykowanego bloku `ML 2 D H M` w konfiguratorze PNOZmulti

**Funkcja Key in Pocket (RFID):**
- Kaseta Pilz PIT z czytnikiem RFID + elektrorygiel = operator musi `zalogować się tagiem RFID` aby wejść do strefy
- PLC monitoruje `czy operator z tagiem JEST w środku` (Key in Pocket) — ryglowanie możliwe tylko gdy wszystkie tagi są na zewnątrz
- Zapobiega przypadkowemu zamknięciu i zaryglowaniu strefy z operatorem wewnątrz

> ⚠️ **Siła trzymania a PL:** sama siła mechaniczna ryglowania nie decyduje o PL — decyduje architektura sygnałów Safety (1oo2, DC, CCF). Elektrorygiel z katalogową wartością PL e osiąga ten poziom tylko przy prawidłowym okablowaniu i konfiguracji systemu Safety.

*Źródło: transkrypcje ControlByte — Pilz PSENmlock, dokumentacja Pilz*

### 15.6. Czym jest czujnik radarowy bezpieczeństwa (np. Pilz PSEN RD 1.2) i kiedy go stosujesz zamiast skanera laserowego?  🟢

**Czujnik radarowy Safety** to urządzenie bezpieczeństwa oparte na emisji fal elektromagnetycznych (radar) do wykrywania obecności osób w strefie niebezpiecznej — zamiast wiązki laserowej.

**Architektura systemu Pilz PSEN RD 1.2:**
- **Czujniki radarowe** — do 5 m zasięgu, kąt ±50° od osi — komunikacja przez magistralę CAN (daisy chain)
- **Analizator** — przetwarza sygnały z czujników, konfiguracja przez Ethernet; wyjścia cyfrowe Safety lub PROFIsafe/Safety over EtherCAT
- 1 analizator obsługuje kilka czujników łącznie

**4 strefy wykrywania na jeden czujnik:**
- Strefa 1 (dalsza, np. 1 m) → spowolnienie robota do prędkości bezpiecznej (tryb SLS)
- Strefa 2 (bliższa, np. 0.4 m) → pełne zatrzymanie (STO/SS1)
- Konfiguracja stref przez oprogramowanie `PSEN RD1 Configurator` (GUI, Ethernet)

**Porównanie radar vs skaner laserowy:**

| Cecha | Skaner laserowy (SICK, PILZ) | Radar PSEN RD 1.2 |
|-------|------------------------------|-------------------|
| Zasada | Wiązka laserowa (optoelektronika) | Fale elektromagnetyczne |
| Wrażliwość na pył/mgłę/dym | Wysoka (błędne detekcje lub zaniki) | Bardzo niska (radar przebija pył) |
| Warunki środowiskowe | Czyste / kontrolowane | Trudne: odlewnie, spawalnie, pilarnie |
| Zasięg | do 5,5 m (safe area scanner) | do 5 m / do 9 m (wersje) |
| Konfiguracja stref | Oprogramowanie + teach-in | `PSEN RD1 Configurator`, 4 strefy/czujnik |
| Koszt systemu | Wyższy per czujnik | Niższy przy dużym obszarze |

**Kiedy stosujesz radar:**
- Spawalnie (iskry, dym), odlewnie (pył metalowy), pilarnie (trociny)
- Strefy z dużym zabrudzeniem gdzie skaner laserowy generuje fałszywe alarmy
- Monitorowanie robotów mobilnych AGV/AMR w trudnym środowisku

> ⚠️ **Integracja z Siemens Safety:** analizator PSEN RD 1.2 obsługuje PROFIsafe → możesz go podłączyć bezpośrednio do F-CPU Siemens przez PROFINET. Alternatywnie: wyjścia cyfrowe Safety (OSSD) → F-DI.

*Źródło: transkrypcja ControlByte — Poradnik Safety Czujnik radarowy Pilz PSEN RD 1.2*

---

