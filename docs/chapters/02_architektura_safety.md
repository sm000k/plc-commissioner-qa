## 2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED

### 2.1. Co to jest SIMATIC Safety Integrated i co oznacza 'wszystko w jednym sterowniku'?  🔴

<span style="color:#1a5276">**SIMATIC Safety Integrated**</span> to koncepcja Siemensa gdzie funkcje bezpieczeństwa (failsafe) i funkcje standardowe działają w **jednym fizycznym CPU** (F-CPU), jednym projekcie TIA Portal i przez jedną sieć PROFINET/PROFIsafe.

**Korzyści:**
- Jeden sterownik zamiast dwóch (standard + safety)
- Ten sam inżyniering w TIA Portal
- Ta sama diagnostyka, mniej okablowania, mniejsza szafa sterownicza

**SIMATIC Safety Integrated — jeden PLC, jeden inżyniering, jedna komunikacja:**
![SIMATIC Safety Integrated: TIA Portal, F-CPU, ET200 F-I/O, SINAMICS](images/safety/01b_simatic_safety_overview_p2.png)

### 2.2. Co to jest F-CPU i jak działa dual-channel processing?  🔴

**Dual-channel processing** to architektura, w której ten sam fragment kodu Safety jest wykonywany przez **dwa niezależne kanały obliczeniowe wewnątrz jednego CPU** (dwa osobne rdzenie lub dwa niezależne tory sprzętowe). Oba kanały przetwarzają identyczne dane wejściowe i produkują wyniki. Na końcu każdego cyklu Safety specjalny komparator porównuje wyniki obu kanałów:
- Wyniki zgodne → cykl OK, wyjścia Safety ustawiane normalnie.
- Wyniki różne (nawet 1 bit) → CPU wykrywa błąd wewnętrzny → **natychmiastowe przejście w bezpieczny stan** (pasywacja wyjść Safety, stop napędów).

**Co to oznacza w praktyce dla komisjonera/integratora:**
- Nie musisz pisać logiki redundantnej — piszesz jeden program Safety, hardware sam wykonuje go dwukrotnie i sprawdza.
- Błąd sprzetowy wewnątrz CPU (uszkodzony rejestr, przekłamanie RAM) jest wykrywalny — to jest właśnie cel tej architektury, nie programowej redundancji.
- Czas cyklu Safety (F_MAIN) jest dłuższy niż OB1, bo CPU wykonuje go dwa razy + porównanie. Typowo 2× czas cyklu standardowego.

**Ciągły self-test:** F-CPU w tle testuje pamięć RAM (CRC bloków), ALU, rejestry procesora. Program Safety działa w oddzielnym chronionym obszarze pamięci — standardowy program OB1 nie może go nadpisać ani odczytać bezpośrednio.

*Certyfikacja (informacyjnie):* F-CPU jest certyfikowany dla SIL 3 / PL e — ta informacja pochodzi z karty katalogowej napędu lub CPU; nie musisz jej znać na pamięć, ale warto wiedzieć że to TÜV zatwierdza architekturę, nie sam Siemens.

### 2.3. Jakie sterowniki Siemens obsługują funkcje Safety?

S7-1500F: CPU 1511F, 1513F, 1515F, 1516F, 1517F, 1518F — Advanced controllers z wbudowanym Safety.
S7-1200F: CPU 1212FC, 1214FC, 1215FC — Basic controllers z Safety, mniejsze aplikacje.
ET 200SP CPU F: CPU 1510SP F, 1512SP F — zdalny sterownik z Safety, montaż przy maszynie.
ET 200pro CPU F: CPU 1516pro F — IP67, bezpośrednio na maszynie.
Wszystkie programowane w TIA Portal z STEP 7 Safety Advanced lub Safety Basic.

### 2.4. Co to jest F-DB i dlaczego nie można go edytować ręcznie?

F-DB (Fail-safe Data Block) generowany jest automatycznie przez TIA Portal dla każdego bloku Safety. Zawiera: CRC (checksum logiki), F-signature (podpis programu Safety), parametry czasowe.
Ręczna edycja zniszczyłaby spójność podpisu → F-CPU odmówiłoby uruchomienia Safety. To celowe zabezpieczenie przed nieautoryzowaną modyfikacją.

### 2.5. Co to jest F-signature i collective signature?  🟡

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

### 2.8. Jakie są podstawowe komponenty i zasady programowania sterowników bezpieczeństwa Pilz PNOZmulti?

Pilz PNOZmulti to programowalny sterownik bezpieczeństwa, który umożliwia łatwe i intuicyjne tworzenie logiki bezpieczeństwa dla maszyn, wykorzystując dedykowane bloki funkcyjne i graficzne środowisko programowania.
- **Programowanie:**
  - Odbywa się za pomocą oprogramowania PNOZmulti Configurator.
  - Program jest podzielony na strony, co ułatwia organizację.
  - Wykorzystuje dedykowane bloki funkcyjne do obsługi elementów bezpieczeństwa (np. ML DH M gate, ML 2 D H M dla rygli, wejścia dwukanałowe).
  - Logika ryglowania i odryglowania jest zaimplementowana w specjalnych blokach.
- **Konfiguracja sprzętowa:**
  - W zakładce "Open Hardware Configuration" można zobaczyć jednostkę główną, dodatkowe moduły wejść/wyjść oraz urządzenia sieciowe (np. panel PMI, czytniki RFID podłączone przez switch).
  - Mapowanie zmiennych i wejść/wyjść odbywa się w zakładce "I O List".
- **Połączenie i diagnostyka:**
  - Połączenie ze sterownikiem odbywa się kablem Ethernet.
  - Adres IP i maska podsieci są dostępne w menu Ethernet -> info.
  - Opcja "Scan Network" pozwala wykryć sterownik w sieci.
  - W "Project Manager" należy wprowadzić Order number i Serial number sterownika, aby uzyskać dostęp.
  - Dostępne są trzy poziomy dostępu: pełna edycja, podgląd, zmiana parametrów.
  - Tryb "online Dynamic Program Display" podświetla aktywne sygnały na zielono, co ułatwia diagnostykę.
Praktyczne wskazówki:
- Programowanie PNOZmulti jest bardzo przyjazne użytkownikowi dzięki dedykowanym blokom.
- Diagnostyka w trybie online jest prosta, ponieważ aktywne sygnały są wizualnie wyróżnione.

**Kontekst na rozmowie:** PNOZmulti to *dedykowany sterownik bezpieczeństwa* (nie F-CPU) — często spotykany przy modernizacjach maszyn i w małych izolowanych aplikacjach Safety (prasy, ogrodzenia). Integracja z Siemens PLC: PNOZmulti jako IO-Device PROFINET (Safe PNOZmulti) lub przez wyjścia przekaźnikowe Safety do F-DI Siemens. Różnica od SIMATIC Safety: PNOZmulti jest tańszy i prostszy dla <20 sygnałów Safety, ale nie łączy logiki Safety z programem PLC w jednym środowisku jak TIA Portal.
*Źródło: transkrypcje ControlByte*

### 2.9. Co to jest S7-1500H (Hot Standby) i kiedy go stosujesz?  🟢

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

| Cecha | S7-1515F | S7-1516H | S7-1518HF |
|-------|----------|----------|-----------|
| Safety (F-CPU) | ✅ | ❌ | ✅ |
| Hot Standby | ❌ | ✅ | ✅ |
| Redundancja CPU | ❌ | ✅ | ✅ |

> ⚠️ **S7-1500H ≠ Safety redundancja** — Hot Standby gwarantuje dostępność (availability), nie poziom Safety (SIL). Do SIL wymagany F-CPU niezależnie od H.

> 💡 Programowanie w TIA Portal: H-system wygląda jak jeden CPU — piszesz kod jeden raz, TIA Portal automatycznie synchronizuje między Primary i Backup. Zmiana konfiguracji H wymaga krótkiego trybu serwisowego.

*Źródło: Siemens SIMATIC S7-1500H System Manual (6ES7518-4FX00-1AC2)*

---

