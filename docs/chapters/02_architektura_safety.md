## 2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED

### 2.1. Co to jest SIMATIC Safety Integrated i co oznacza 'wszystko w jednym sterowniku'?  🔴

<span style="color:#1a5276">**SIMATIC Safety Integrated**</span> to koncepcja Siemensa gdzie funkcje bezpieczeństwa (failsafe) i funkcje standardowe działają w **jednym fizycznym CPU** (F-CPU), jednym projekcie TIA Portal i przez jedną sieć PROFINET/PROFIsafe.

**Korzyści:**
- Jeden sterownik zamiast dwóch (standard + safety)
- Ten sam inżyniering w TIA Portal
- Ta sama diagnostyka, mniej okablowania, mniejsza szafa sterownicza

**SIMATIC Safety Integrated — jeden PLC, jeden inżyniering, jedna komunikacja:**
![SIMATIC Safety Integrated: TIA Portal, F-CPU, ET200 F-I/O, SINAMICS](images/safety/01b_simatic_safety_overview_p2.png)

*[ZWERYFIKOWANE] — [SIMATIC Safety Integrated — przegląd systemu](https://www.siemens.com/global/en/products/automation/systems/industrial/safety-integrated.html); [SIMATIC Safety — Konfiguracja i programowanie (A5E02714440-AK)](https://support.industry.siemens.com/cs/document/104547937/)*
### 2.2. Co to jest F-CPU i jak działa dual-channel processing?  🔴

**Dual-channel processing** to architektura, w której ten sam fragment kodu Safety jest wykonywany przez **dwa niezależne kanały obliczeniowe wewnątrz jednego CPU**. W S7-1500F realizowane programowo (diversified redundant processing w jednym fizycznym procesorze — ten sam program Safety wykonywany dwukrotnie z dywersyfikowanym przetwarzaniem, wyniki porównywane). W starszych generacjach (S7-300F/400F) — sprzętowo (dwa oddzielne procesory). Oba kanały przetwarzają identyczne dane wejściowe i produkują wyniki. Na końcu każdego cyklu Safety specjalny komparator porównuje wyniki obu kanałów:
- Wyniki zgodne → cykl OK, wyjścia Safety ustawiane normalnie.
- Wyniki różne (nawet 1 bit) → CPU wykrywa błąd wewnętrzny → **natychmiastowe przejście w bezpieczny stan** (pasywacja wyjść Safety, stop napędów).

**Co to oznacza w praktyce dla komisjonera/integratora:**
- Nie musisz pisać logiki redundantnej — piszesz jeden program Safety, hardware sam wykonuje go dwukrotnie i sprawdza.
- Błąd sprzętowy wewnątrz CPU (uszkodzony rejestr, przekłamanie RAM) jest wykrywalny — to jest właśnie cel tej architektury, nie programowej redundancji.
- Czas cyklu Safety (F_MAIN) jest dłuższy niż OB1, bo CPU wykonuje go dwa razy + porównanie. Typowo 2× czas cyklu standardowego.

**Ciągły self-test:** F-CPU w tle testuje pamięć RAM (CRC bloków), ALU, rejestry procesora. Program Safety działa w oddzielnym chronionym obszarze pamięci — standardowy program OB1 nie może go nadpisać ani odczytać bezpośrednio.

> ⚠️ **DO WERYFIKACJI:** Twierdzenie „F_MAIN wykonywany typowo 2× dłużej niż OB1" jest uproszczeniem. Rzeczywisty czas cyklu Safety zależy od rozmiaru programu F, konfiguracji sprzętu i komunikacji PROFIsafe — nie jest to prosta wielokrotność czasu OB1. Sprawdź w TIA Portal → CPU properties → Cycle time.

*Certyfikacja (informacyjnie):* F-CPU jest certyfikowany dla SIL 3 / PL e — ta informacja pochodzi z karty katalogowej napędu lub CPU; nie musisz jej znać na pamięć, ale warto wiedzieć że to TÜV zatwierdza architekturę, nie sam Siemens.

*[ZWERYFIKOWANE] — [SIMATIC Safety — Konfiguracja i programowanie (A5E02714440-AK)](https://support.industry.siemens.com/cs/document/104547937/), rozdział „Dual-channel processing / diversified redundant processing"; [SIMATIC Safety Getting Started (A5E02714463)](https://support.industry.siemens.com/cs/document/109751404/)*
### 2.3. Jakie sterowniki Siemens obsługują funkcje Safety?

S7-1500F: CPU 1511F, 1513F, 1515F, 1516F, 1517F, 1518F — Advanced controllers z wbudowanym Safety.
S7-1200F: CPU 1212FC, 1214FC, 1215FC — Basic controllers z Safety, mniejsze aplikacje.
ET 200SP CPU F: CPU 1510SP F, 1512SP F — zdalny sterownik z Safety, montaż przy maszynie.
ET 200pro CPU F: CPU 1516pro F — IP67, bezpośrednio na maszynie.
Wszystkie programowane w TIA Portal z STEP 7 Safety Advanced lub Safety Basic.

*[ZWERYFIKOWANE] — [SIMATIC S7-1500F — strona produktowa](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/s7-1500.html); [SIMATIC S7-1200F — strona produktowa](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/s7-1200.html)*
### 2.4. Co to jest F-DB i dlaczego nie można go edytować ręcznie?

F-DB (Fail-safe Data Block) generowany jest automatycznie przez TIA Portal dla każdego bloku Safety. Zawiera: CRC (checksum logiki), F-signature (podpis programu Safety), parametry czasowe.
Ręczna edycja zniszczyłaby spójność podpisu → F-CPU odmówiłoby uruchomienia Safety. To celowe zabezpieczenie przed nieautoryzowaną modyfikacją.

*[ZWERYFIKOWANE] — [SIMATIC Safety — Konfiguracja i programowanie (A5E02714440-AK)](https://support.industry.siemens.com/cs/document/104547937/), rozdział Safety Administration Editor*
### 2.5. Co to jest F-signature i collective signature?  🟡

F-signature to unikalny podpis (suma kontrolna CRC) jednego bloku Safety — zmienia się przy każdej modyfikacji kodu.
Collective signature (podpis zbiorczy) to podpis CAŁEGO programu Safety złożony ze wszystkich bloków. Widoczny na wyświetlaczu CPU lub w TIA Portal jako ciąg znaków (np. '5CBE6409').
Przy wgraniu CPU porównuje collective signature — niezgodność → Safety nie uruchamia się.

W TIA Portal w Safety Administration Editor widoczne są:
- **Zbiorczy podpis bezpieczeństwa** (collective F-signature) — zmienia się przy każdej zmianie danych projektu fail-safe
- **Podpis zbiorczy F-SW** — zmienia się przy zmianie programu Safety
- **Podpis zbiorczy F-HW** — zmienia się przy zmianie konfiguracji sprzętowej fail-safe

*[ZWERYFIKOWANE] — [SIMATIC Safety — Konfiguracja i programowanie (A5E02714440-AK)](https://support.industry.siemens.com/cs/document/104547937/), str. 83–84 „F-signatures"; [SIMATIC Safety Getting Started (A5E02714463)](https://support.industry.siemens.com/cs/document/109751404/), str. 32, 43*
### 2.6. Jakie są tryby pracy Safety CPU i jak się przełącza?

**Safety mode activated** — normalny tryb produktywny, program Safety działa, wyjścia sterowane przez logikę F.
**Safety mode deactivated** — tryb commissioning/testowy, wejścia/wyjścia F modułów mogą być nadpisywane ręcznie bez ochrony Safety (używany np. podczas uruchamiania do testów okablowania).
Przełączenie przez TIA Portal (Safety Administration Editor → „Disable safety mode") lub dedykowany sygnał w logice. Po przełączeniu wymagane potwierdzenie (hasło Safety). Zmiana trybu jest logowana z datą i użytkownikiem. Uwaga: dezaktywacja trybu Safety jest widoczna w diagnostyce i na wyświetlaczu CPU — nie można jej ukryć.

> ⚠️ **WARNING z dokumentacji Siemens:** „Deactivation of safety mode is intended for test purposes, commissioning, etc. Whenever safety mode is deactivated, the safety of the system must be ensured by other organizational measures, such as monitored operation, manual safety shutdown, and access restrictions to certain areas."

*[ZWERYFIKOWANE] — [SIMATIC Safety Getting Started (A5E02714463)](https://support.industry.siemens.com/cs/document/109751404/), str. 42–43; [SIMATIC Safety — Konfiguracja i programowanie (A5E02714440-AK)](https://support.industry.siemens.com/cs/document/104547937/), Safety Administration Editor*
### 2.7. Jakie są podstawowe komponenty i zasady programowania sterowników bezpieczeństwa Pilz PNOZmulti?

Pilz PNOZmulti to programowalny sterownik bezpieczeństwa, który umożliwia łatwe i intuicyjne tworzenie logiki bezpieczeństwa dla maszyn, wykorzystując dedykowane bloki funkcyjne i graficzne środowisko programowania.
- **Programowanie:**
  - Odbywa się za pomocą oprogramowania PNOZmulti Configurator.
  - Program jest podzielony na strony, co ułatwia organizację.
  - Wykorzystuje dedykowane bloki funkcyjne — nazwy kodują funkcję: **ML DH M gate** = Magnet Lock (elektrorygiel) + Door monitoring + Hazardous guard locking + Manual restart, dla bramy ochronnej; **ML 2 D H M** = to samo, ale **2-kanałowe** (redundancja czujników, wymagana dla PL d/e). Bloki bez „2" = jednokanałowe (PL c), z „2" = dwukanałowe (PL d–e). Litera **M** na końcu = operator musi fizycznie potwierdzić restart.
  - Logika ryglowania i odryglowania jest zaimplementowana w specjalnych blokach.
- **Konfiguracja sprzętowa:**
  - W zakładce "Open Hardware Configuration" można zobaczyć jednostkę główną, dodatkowe moduły wejść/wyjść oraz urządzenia sieciowe (np. panel PMI, czytniki RFID podłączone przez switch).
  - Mapowanie zmiennych i wejść/wyjść odbywa się w zakładce "I O List".
- **Połączenie i diagnostyka:**
  - Połączenie ze sterownikiem odbywa się kablem Ethernet.
  - Adres IP i maska podsieci są dostępne w menu Ethernet → info.
  - Opcja "Scan Network" pozwala wykryć sterownik w sieci.
  - W "Project Manager" należy wprowadzić Order number i Serial number sterownika, aby uzyskać dostęp.
  - Dostępne są trzy poziomy dostępu: pełna edycja, podgląd, zmiana parametrów.
  - Tryb "online Dynamic Program Display" podświetla aktywne sygnały na zielono, co ułatwia diagnostykę.

**Kontekst na rozmowie:** PNOZmulti to *dedykowany sterownik bezpieczeństwa* (nie F-CPU) — często spotykany przy modernizacjach maszyn i w małych izolowanych aplikacjach Safety (prasy, ogrodzenia). Integracja z Siemens PLC: PNOZmulti jako IO-Device PROFINET (Safe PNOZmulti) lub przez wyjścia przekaźnikowe Safety do F-DI Siemens. Różnica od SIMATIC Safety: PNOZmulti jest tańszy i prostszy dla <20 sygnałów Safety, ale nie łączy logiki Safety z programem PLC w jednym środowisku jak TIA Portal.

**Porównanie dedykowanych sterowników Safety — Pilz vs SICK vs Siemens F-CPU:**

| Cecha | Pilz PNOZmulti 2 | SICK Flexi Soft / FLX3-CPUC | Siemens F-CPU (S7-1500F) |
|-------|-------------------|------------------------------|--------------------------|
| Typ | Dedykowany Safety PLC | Dedykowany Safety PLC | Zintegrowany Safety w CPU standardowym |
| Programowanie | PNOZmulti Configurator (graficzne bloki) | SICK Safety Designer (FBD) | TIA Portal + STEP 7 Safety Advanced (LAD/FBD) |
| Max SIL / PL | SIL CL 3 / PL e | SIL CL 3 / PL e | SIL 3 / PL e |
| Skalowalność | Do ~20 F-I/O, rozszerzalny modułami | Do ~40 F-I/O, modułowe | Setki F-I/O przez ET200 + PROFIsafe |
| Koszt (orientacyjnie) | €800–1500 (jednostka + moduły) | €600–1200 (jednostka + moduły) | €3000–8000 (CPU F + licencja Safety) |
| Integracja z Siemens PLC | PROFINET IO-Device (opcja Safe) lub przekaźniki → F-DI | PROFINET IO-Device lub EtherNet/IP | Natywna — jeden projekt, jedna diagnostyka |
| Kiedy stosować | Mała maszyna standalone, modernizacja, <20 sygnałów Safety | Mała/średnia maszyna, ekosystem SICK (kurtyny, skanery) | Duża instalacja, wiele stref Safety, integracja z logiką standardową |

**Kluczowe różnice w praktyce:**
- **SICK jest tańszy** od Pilza przy porównywalnej funkcjonalności — Flexi Soft / FLX3 konkuruje ceną, szczególnie gdy w projekcie są już czujniki SICK (kurtyny deTec, skanery microScan — wtedy integracja „za darmo")
- **Pilz ma lepszą rozpoznawalność** w branży Safety — audytorzy i klienci „znają Pilz" jako synonim bezpieczeństwa maszyn, łatwiej przejść odbiór
- **Oba przegrywają z F-CPU** w dużych instalacjach — >30 sygnałów Safety lub komunikacja Safety-to-Safety między stacjami → dedykowany Safety PLC staje się ograniczeniem (osobne narzędzie, osobna diagnostyka, dodatkowy interfejs)
- **Modernizacja** — Pilz/SICK idealny gdy dorzucasz Safety do starej maszyny z S7-300 (bez F) — nie musisz wymieniać CPU, podłączasz standalone Safety controller obok

⚠️ **DO WERYFIKACJI** — ceny orientacyjne z 2024, mogą się różnić zależnie od konfiguracji i rabatów.
*Źródło: transkrypcje ControlByte + wiedza domenowa*

### 2.8. Co to jest S7-1500H (Hot Standby) i kiedy go stosujesz?  🟢

**S7-1500H** (Highly Available / Hot Standby) to konfiguracja redundantna dwóch identycznych CPU S7-1500 pracujących równolegle — jeden aktywny (Primary), drugi gotowy do natychmiastowego przejęcia sterowania (Backup).

**Zasada działania:**
- Oba CPU przetwarzają ten sam program synchronicznie w każdym cyklu
- Dane procesowe synchronizowane są przez dedykowaną sieć **Sync link** (Fiber lub Ethernet) — oddzielna od PROFINET
- Przy awarii Primary → Backup przejmuje sterowanie w czasie `< 1 cykl PLC` (bez STOP maszyny)
- **Bumpless switchover** — maszyna nie zauważa przełączenia

**Konfiguracja sprzętowa:**
- 2× CPU 1517H lub 1518HF (wersja z Safety)
- 2× IM 155-6 PN HF dla każdej stacji ET200SP (Shared-Device — oba CPU komunikują się z tą samą stacją)
- 2 fizyczne połączenia Sync link (redundancja linku synchronizacyjnego)

**Kiedy stosujesz S7-1500H:**
- Procesy ciągłe gdzie zatrzymanie CPU = duże straty (hutnictwo, chemia, petrochemia)
- Maszyny 24/7 gdzie planowanie okna serwisowego jest niemożliwe
- Wymagania SLA: `MTTR < 3s` (Mean Time To Recovery)

**Różnica H vs F (Safety):**

| Cecha | S7-1515F | S7-1517H | S7-1518HF |
|-------|----------|----------|-----------|
| Safety (F-CPU) | ✅ | ❌ | ✅ |
| Hot Standby | ❌ | ✅ | ✅ |
| Redundancja CPU | ❌ | ✅ | ✅ |

> ⚠️ **S7-1500H ≠ Safety redundancja** — Hot Standby gwarantuje dostępność (availability), nie poziom Safety (SIL). Do SIL wymagany F-CPU niezależnie od H.

> 💡 Programowanie w TIA Portal: H-system wygląda jak jeden CPU — piszesz kod jeden raz, TIA Portal automatycznie synchronizuje między Primary i Backup. Zmiana konfiguracji H wymaga krótkiego trybu serwisowego.

*Źródło: Siemens SIMATIC S7-1500H System Manual (6ES7518-4FX00-1AC2)*

### 2.9. Jak wygląda minimalna konfiguracja sprzętowa systemu S7-1500H?  🟢

**S7-1500H** (Hot Standby) to system z dwoma CPU pracującymi równolegle — Primary i Backup. Redundancja dotyczy **CPU** (wysoka dostępność), nie automatycznie sieci PROFINET. Minimalna konfiguracja wymaga 6 komponentów.

**Lista komponentów (minimum):**

| # | Komponent | Ilość | Rola |
|---|-----------|-------|------|
| 1 | CPU 1517H lub 1518H | 2 | Primary + Backup |
| 2 | PM 190W zasilacz | 2 | Osobne zasilanie per CPU (niezależność awaryjna) |
| 3 | Kabel Sync Link (X3↔X3, X4↔X4) | 2 | Synchronizacja danych — dedykowane, oddzielne od PROFINET |
| 4 | SCALANCE switch (np. XB208) lub bezpośrednie połączenie | 1+ | PROFINET — sieć I/O |
| 5 | ET200SP z IM 155-6 PN **HF** | 1 | Shared Device — 2 porty PN, widoczna przez oba CPU |
| 6 | Moduły I/O (DI/DQ/AI) | min. 1 | Wejścia/wyjścia procesowe |

**Kluczowe zasady:**
- **Sync Link = 2 fizyczne połączenia** (X3↔X3 i X4↔X4) — redundancja linku synchronizacji CPU. Fiber do dużych odległości, Ethernet do ~100 m
- **IM 155-6 PN HF** (nie zwykły IM!) — 2 porty PROFINET, komunikuje się z **oboma** CPU jednocześnie (System Redundancy R1). Przy switchover stacja nie traci połączenia
- **Czas switchover CPU** — typowo 0,5–1,5 s (zależy od rozmiaru programu i liczby IO-Devices). Aplikacja musi tolerować krótką przerwę sterowania
- **W TIA Portal** — konfigurujesz jeden H-CPU, TIA automatycznie generuje konfigurację Backup. Program piszesz raz

**Czego NIE potrzebujesz w minimalnej konfiguracji:**
- Redundancja PROFINET (ring MRP) — opcja, nie wymóg (patrz Q2.10)
- Moduły F (Safety) — H to dostępność, nie Safety
- Dodatkowa licencja — H-firmware jest w CPU 1517H/1518H

```
┌──────────────────┐         Sync Link ×2         ┌──────────────────┐
│   Szafa 1        │  X3 ════════════════════ X3   │   Szafa 2        │
│  ┌────────────┐  │  X4 ════════════════════ X4   │  ┌────────────┐  │
│  │ CPU 1517H  │  │                               │  │ CPU 1517H  │  │
│  │  PRIMARY   │  │                               │  │  BACKUP    │  │
│  └─────┬──────┘  │                               │  └─────┬──────┘  │
│    PM 190W       │                               │    PM 190W       │
└────────┼─────────┘                               └────────┼─────────┘
         │ PROFINET X1                                      │ PROFINET X1
         └──────────────┬───── SCALANCE XB208 ──────────────┘
                        │
                ┌───────┴───────┐
                │  ET200SP      │
                │  IM 155-6     │
                │  PN HF        │  ← 2 porty PN (Shared Device / R1)
                ├───────────────┤
                │ DI │ DQ │ AI  │
                └───────────────┘
```

*[ZWERYFIKOWANE] — [SIMATIC S7-1500H System Manual](https://support.industry.siemens.com/cs/document/109779336/); [S7-1500R/H strona produktowa](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/s7-1500/s7-1500r-h.html)*

---

### 2.10. Jakie topologie PROFINET można stosować dla redundancji sieci w systemie S7-1500H?  🟢

Redundancja CPU (H-system) nie oznacza automatycznie redundancji **sieci PROFINET**. Awaria kabla lub switcha może odciąć IO-Devices mimo działającego Backup CPU. Dobór topologii PROFINET decyduje o odporności sieci I/O na uszkodzenia fizyczne.

**Porównanie topologii:**

| Topologia | Redundancja kabla PN | Koszt sieci | Czas przełączenia (awaria kabla) | Uwagi |
|-----------|:-------------------:|:-----------:|:-----------------------------------:|-------|
| **Daisy chain** | ❌ | Brak | Utrata stacji za przerwą | Najprościej, bez switcha |
| **Gwiazda — niezarządzalny switch** (XB208) | ❌ | Niski | Utrata wszystkich stacji | Switch = SPOF |
| **Gwiazda — zarządzalny switch** (XC/XP) | ❌ | Średni | Utrata wszystkich stacji | Diagnostyka SNMP, ale wciąż SPOF |
| **Ring bez switcha** (porty CPU → devices → porty CPU) | ✅ | Brak | ≤ 200 ms (MRP) | Optymalne — redundancja bez kosztów |
| **Ring z zarządzalnym switchem** | ✅ | Wysoki | ≤ 200 ms / ≈ 0 ms (MRPD) | Wymagany dla IRT/S120 |
| **Dual-homed** (dwa niezależne trakty) | ✅ | Najwyższy | ≈ 0 ms | IM 155-6 **MF** HF (Multi-Fieldbus, nie zwykły PN HF!) |

> **Uwaga:** IM 155-6 **PN** HF (2 porty w jednym pierścieniu) vs IM 155-6 **MF** HF (2 niezależne interfejsy PROFINET → dual-homed na dwóch osobnych traktach). Dual-homed wymaga droższego MF HF.

---

**Schematy wszystkich topologii:**

> Sync Link (X3-X3, X4-X4) identyczny we wszystkich wariantach — pominięty na schematach.
> Legenda: `*` = port użyty, `o` = port wolny. Każde urządzenie pokazuje WSZYSTKIE porty.

---

**① Daisy chain** — najprostsza, bez redundancji kabla:
```
    +-------------------+
    | CPU PRIMARY       |
    +--------+----------+
        [P1] |
             | kabel 1
        [P1] |
    +--------+----------+
    | ET200SP_1         |
    | IM155-6 HF       |
    +--------+----------+
        [P2] |
             | kabel 2
        [P1] |
    +--------+----------+
    | ET200SP_2         |
    | IM155-6 HF       |
    +--------+----------+
        [P2] |
             | kabel 3
        [P1] |
    +--------+----------+
    | ET200SP_3         |
    | IM155-6 HF       |
    +--------+----------+
        [P2] |
             | kabel 4
        [P1] |
    +--------+----------+
    | CPU BACKUP        |
    +-------------------+
```
> ⚠️ Awaria kabla 2 → ET200SP_2, _3 i CPU BACKUP utracone. Kabel wchodzi do P1, wychodzi z P2. Oba CPU na koncach lancucha — brak redundancji kabla.

---

**② Gwiazda z niezarządzalnym switchem** (SCALANCE XB208):
```
    +-----------+                +-----------+
    | CPU PRI   |                | CPU BAK   |
    +-----+-----+                +-----+-----+
     [P1] |                       [P1] |
          | k1                         | k2
     [P1] |                       [P2] |
    +-----+----------------------------+-----+
    |            SCALANCE XB208              |
    |      (niezarzadzalny, 8 portow)        |
    |              oP6  oP7  oP8             |
    +-----+------------+------------+--------+
     [P3] |       [P4] |       [P5] |
          | k3         | k4         | k5
     [P1] |       [P1] |       [P1] |
    +-----+----+ +-----+----+ +----+-----+
    | ET200SP_1| | ET200SP_2| | ET200SP_3|
    | IM155 HF | | IM155 HF | | IM155 HF |
    | oP2      | | oP2      | | oP2      |
    +----------+ +----------+ +----------+
```
> ⚠️ Switch = SPOF. Kable z CPU wchodza do P1/P2 switcha, ze switcha P3-P5 do P1 stacji. P2 stacji wolne. Awaria XB208 = utrata CALEJ sieci I/O.

---

**③ Gwiazda z zarządzalnym switchem** (SCALANCE XC208):
```
    +-----------+                +-----------+
    | CPU PRI   |                | CPU BAK   |
    +-----+-----+                +-----+-----+
     [P1] |                       [P1] |
          | k1                         | k2
     [P1] |                       [P2] |
    +-----+----------------------------+-----+
    |            SCALANCE XC208              |
    |   (zarzadzalny, SNMP/LLDP, 8 portow)  |
    |              oP6  oP7  oP8             |
    +-----+------------+------------+--------+
     [P3] |       [P4] |       [P5] |
          | k3         | k4         | k5
     [P1] |       [P1] |       [P1] |
    +-----+----+ +-----+----+ +----+-----+
    | ET200SP_1| | ET200SP_2| | ET200SP_3|
    | IM155 HF | | IM155 HF | | IM155 HF |
    | oP2      | | oP2      | | oP2      |
    +----------+ +----------+ +----------+
```
> ⚠️ Wciąż SPOF jak ②, ale switch ma diagnostykę SNMP, LLDP, port mirroring. P2 stacji wolne.

---

**④ Ring bez switcha — porty CPU tworzą pierścień** (MRP, optymalne):
```
        +--------- k6 (zamyka pierscien) ---------+
        |                                         |
   [P2] |                                    [P2] |
    +---+-------------------+                     |
    | CPU PRIMARY (MRM)     |                     |
    +---+-------------------+                     |
   [P1] |                                         |
        | k1                                      |
   [P1] |                                         |
    +---+-------------------+                     |
    | ET200SP_1             |                     |
    | IM155-6 HF (MRC)    |                     |
    +---+-------------------+                     |
   [P2] |                                         |
        | k2                                      |
   [P1] |                                         |
    +---+-------------------+                     |
    | ET200SP_2             |                     |
    | IM155-6 HF (MRC)    |                     |
    +---+-------------------+                     |
   [P2] |                                         |
        | k3                                      |
   [P1] |                                         |
    +---+-------------------+                     |
    | ET200SP_3             |                     |
    | IM155-6 HF (MRC)    |                     |
    +---+-------------------+                     |
   [P2] |                                         |
        | k4                                      |
   [P1] |                                         |
    +---+-------------------+                     |
    | ET200SP_4             |                     |
    | IM155-6 HF (MRC)    |                     |
    +---+-------------------+                     |
   [P2] |                                         |
        | k5                                      |
   [P1] |                                    [P2] |
    +---+-------------------+-----------------+---+
    | CPU BACKUP (MRM standby)                    |
    +---------------------------------------------+

    Pierscien: PRI:P1 -> _1 -> _2 -> _3 -> _4 -> BAK:P1
    Zamkniecie: BAK:P2 -(k6)-> PRI:P2
    WSZYSTKIE porty uzyte na WSZYSTKICH urzadzeniach.
```
> ✅ **Optymalne.** CPU PRIMARY = MRM, CPU BACKUP = MRM standby. Oba CPU w pierścieniu — P1 i P2 użyte na każdym urządzeniu. Awaria kabla → MRP ≤ 200 ms. Zero switchy.

---

**⑤ Ring z zarządzalnymi switchami** (MRPD, dla IRT/S120):
```
    +-----------+                      +-----------+
    | CPU PRI   |                      | CPU BAK   |
    | oP2       |                      | oP2       |
    +-----+-----+                      +-----+-----+
     [P1] |                             [P1] |
          | k1                               | k2
     [P1] |                             [P1] |
    +-----+-----------+  kabel ring  +-------+---------+
    | SCALANCE        |              | SCALANCE        |
    | XC216-A         |              | XC216-B         |
    |  oP6..oP16      |              |  oP6..oP16      |
    +--+------+---+---+              +--+------+---+---+
  [P3] | [P4] |[P5]|              [P3] | [P4] |[P5]|
       |      |    |                    |      |    |
   k3  |  k4  | k5 |                k6  |  k7  | k8 |
       |      |    |                    |      |    |
  [P1] | [P1] |[P1]|              [P1] | [P1] |[P1]|
    +--+--+ +-+-+ +--+-+          +--+--+ +-+-+ +--+-+
    | _1  | | _2| | _3 |          | _4  | | _5| | _6 |
    | oP2 | |oP2| | oP2|          | oP2 | |oP2| | oP2|
    +-----+ +---+ +----+          +-----+ +---+ +----+
     ET200SP (IM155 HF)             ET200SP (IM155 HF)
```
> ✅ Switche w pierścieniu MRP/MRPD. MRPD = ≈ 0 ms. Kable ze switch P3-P5 do stacji P1. P2 na CPU i stacjach wolne — redundancję zapewnia ring switchów. Wymagane dla IRT/S120.

---

**⑥ Dual-homed — dwa niezależne trakty** (systemy krytyczne):
```
    TRAKT A                           TRAKT B

    +-----------+                     +-----------+
    | CPU PRI   |                     | CPU BAK   |
    | oP2       |                     | oP2       |
    +-----+-----+                     +-----+-----+
     [P1] |                            [P1] |
          | k1                              | k2
     [P1] |                            [P1] |
    +-----+-------+                   +-----+-------+
    | SCALANCE    |                   | SCALANCE    |
    | XC-A        |                   | XC-B        |
    | oP2 oP5-P16 |                   | oP2 oP5-P16 |
    +--+------+---+                   +--+------+---+
  [P3] |  [P4]|                     [P3] |  [P4]|
       |      |                          |      |
   k3  |  k5  |                      k4  |  k6  |
       |      |                          |      |
  [IF1]|  [IF1]|                    [IF2]|  [IF2]|
    +--+------+-------+           +--+------+-------+
    | ET200SP_1       |           | (te same stacje)|
    | IM 155-6 MF HF   |           |                 |
    +-----+-----------+           +-----------+-----+
    +--+------+-------+
    | ET200SP_2       |  k3: XC-A:P3 <-- IF1
    | IM 155-6 MF HF   |  k4: XC-B:P3 <-- IF2
    +-----------------+  k5: XC-A:P4 <-- IF1
                         k6: XC-B:P4 <-- IF2

    UWAGA: IM 155-6 MF HF =/= PN HF!
      MF HF: 2 NIEZALEZNE interfejsy (osobne MAC, osobne IP)
      PN HF: 2 porty, ale 1 interfejs (wewnetrzny switch)
```
> ✅ Kable z IF1 do Trakt A (XC-A), z IF2 do Trakt B (XC-B). Awaria traktu A → Trakt B przejmuje ~0 ms. Wymaga IM 155-6 **MF** HF (Multi-Fieldbus).

---

**Rekomendacja doboru topologii:**

| Zastosowanie | Topologia | Uzasadnienie |
|---|---|---|
| Budżet niski, mała linia | ① Daisy chain lub ② Gwiazda XB208 | Redundancja tylko CPU, nie sieci PN |
| Standard automotive / H-system | ④ Ring bez switcha (MRP) | Redundancja CPU + kabel PN, zero kosztów dodatkowych |
| Systemy krytyczne / napędy S120 | ⑤ Ring MRPD z SCALANCE XC/XP lub ⑥ Dual-homed | Minimalny przestój, IRT, pełna redundancja traktów |

**Kluczowe różnice między topologiami:**

| Cecha | ① Daisy | ②③ Gwiazda | ④ Ring MRP | ⑤ Ring MRPD | ⑥ Dual-homed |
|---|:---:|:---:|:---:|:---:|:---:|
| Redundancja kabla PN | NIE | NIE | TAK | TAK | TAK |
| Czas przełączenia | — | — | ≤ 200 ms | ≈ 0 ms | ≈ 0 ms |
| Dodatkowy sprzęt | brak | switch | brak | 2x switch | 2x switch + MF HF |
| SPOF (single point of failure) | kabel | switch | brak | brak | brak |
| Obsługa IRT (isochronous) | NIE | NIE | NIE | TAK | TAK |
| Porty CPU użyte | P1 | P1 | P1 + P2 | P1 | P1 |
| Moduł IM stacji | PN HF | PN HF | PN HF | PN HF | **MF HF** |
| Protokół redundancji | — | — | MRP | MRP/MRPD | System R1 |
| Koszt względny | najniższy | niski | niski | średni | wysoki |

**Najważniejsze zasady praktyczne:**
- **IM 155-6 PN HF** (2 porty, 1 interfejs) — dla topologii ①–⑤
- **IM 155-6 MF HF** (2 niezależne interfejsy, osobne MAC/IP) — wyłącznie dla ⑥ dual-homed
- W ringu MRP: CPU = **MRM** (Manager), stacje = **MRC** (Client)
- Sync Link (X3↔X3, X4↔X4) to **osobne połączenie peer-to-peer** między CPU — NIE jest częścią pierścienia PROFINET
- W topologii ④ ring zamyka się przez oba porty obu CPU — zero dodatkowego sprzętu

*[ZWERYFIKOWANE] — [SIMATIC S7-1500H System Manual](https://support.industry.siemens.com/cs/document/109779336/); [S7-1500R/H strona produktowa](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/s7-1500/s7-1500r-h.html); IEC 61158-6-10 (PROFINET MRP); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/)]*

---

