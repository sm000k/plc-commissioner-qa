## 7. PROFISAFE — KOMUNIKACJA SAFETY

### 7.1. Co to jest PROFIsafe i co zawiera jego pakiet?  🔴

<span style="color:#1a5276">**PROFIsafe**</span> to protokół Safety działający na **warstwie aplikacji** ponad standardowym PROFINET lub PROFIBUS — bez osobnego okablowania bezpieczeństwa.

**Struktura ramki PROFIsafe** *(dodatkowe dane ponad normalne dane procesowe)*:

| Element | Rozmiar | Cel |
|---------|---------|-----|
| F-Data (dane procesowe Safety) | zmienny | Bezpieczne dane wejść/wyjść |
| Status/Control byte | 1 bajt | Toggle bit, potwierdzenia, sterowanie komunikacją |
| CRC | 3 bajty (CRC1) lub 4 bajty (CRC2) | Integralność — obliczany z uwzględnieniem Virtual Consecutive Number (VCN) i F-Address |

Ochrona przed utratą/powtórzeniem pakietów (VCN) i błędnym adresowaniem (F-Address) jest realizowana **wewnątrz obliczenia CRC** — nie są to osobne pola w ramce.

**Błędy wykrywane przez PROFIsafe**, których zwykły PROFINET nie wykrywa:
- Utrata pakietu
- Powtórzenie pakietu (replay)
- Błędna sekwencja
- Przekłamanie danych (bit flip)
- Błędny adres odbiorcy

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 7.2. Co to jest F-Address i jak go konfigurujesz?  🔴

`F-Address` (F-Destination Address) to unikalny F-address przypisany do każdego modułu F w sieci. **Musi być identyczny** w konfiguracji TIA Portal i na fizycznym urządzeniu (DIP switch lub parametryzacja).

**Konfiguracja:**
- TIA Portal → właściwości modułu F → zakładka `Safety` → pole `Safety address`
- Na urządzeniu: DIP switch lub przez TIA Portal `Assign PROFIsafe address` (online)

> ⚠️ **Przy wymianie modułu:** nowy moduł musi dostać **ten sam F-Address** co stary — inaczej nie uruchomisz systemu Safety.
> Błędny F-Address → moduł nie komunikuje się z F-CPU i pozostaje spassivowany.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 7.3. Co to jest F-monitoring time i co się dzieje po jego przekroczeniu?

`F-monitoring time` to maksymalny czas oczekiwania F-CPU na kolejny pakiet PROFIsafe od modułu. Po przekroczeniu (np. przerwa w sieci, przeciążony switch) → moduł zostaje <span style="color:#c0392b">**spassivowany**</span>.

| Nastawienie | Skutek |
|-------------|--------|
| Za krótki | Fałszywe alarmy przy chwilowym obciążeniu sieci |
| Za długi | Wolne wykrywanie prawdziwej awarii komunikacji |

> 💡 Ustawiasz w parametrach modułu Safety. Wartość dobierasz do topologii sieciowej i obciążenia switcha — dla przeciążonych sieci zwiększ, dla wymagań szybkiego wykrycia awarii zmniejsz.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 7.4. Jak Safety działa przez ET200 (zdalne I/O) i czym jest F-peripheral?

**F-peripheral** (fail-safe peripheral) to zdalne urządzenie I/O Safety podłączone do F-CPU przez PROFIsafe/PROFINET.

| F-peripheral | Stopień ochrony | Montaż |
|-------------|----------------|--------|
| ET200SP + moduły F-DI/F-DQ | IP20 | Szafa sterownicza, szyna DIN |
| ET200eco F | IP67 | Przy maszynie, bez szafy |
| ET200pro F | IP67 | Modułowe, trudne warunki |

**Zasada działania:**
- F-CPU wysyła i odbiera pakiety PROFIsafe do każdego F-peripherala **niezależnie**
- Każdy ma własny `F-Address` i `F-monitoring time`
- Awaria jednego peripherala <span style="color:#c0392b">**passivuje tylko ten moduł**</span>, nie cały system Safety

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*

### 7.5. Jakie telegramy PROFIsafe są stosowane w napędach SINAMICS i co zawierają?

**Telegramy PROFIsafe w napędach** to dodatkowe submoduły komunikacyjne konfigurowane w TIA Portal obok standardowych telegramów PROFIdrive. Przesyłają komendy Safety (STO, SS1, SLS…) i status Safety napędu przez tę samą sieć PROFINET.

- **Telegram PROFIsafe 30** — podstawowy telegram Safety dla napędów SINAMICS. Zawiera:
  - Dane sterujące (F-CPU → napęd): komendy aktywacji/deaktywacji funkcji Safety (STO, SS1, SLS, SDI itp.)
  - Dane statusowe (napęd → F-CPU): potwierdzenie aktywnych funkcji Safety, status błędów Safety
  - Stosowany w SINAMICS G120 (CU250S-2) i S120 dla prostych konfiguracji Safety
- **Telegram PROFIsafe 54** — rozszerzony telegram Safety z dodatkowymi danymi diagnostycznymi, używany w zaawansowanych konfiguracjach S120
- **Telegram PROFIsafe 900/902** — telegramy Safety dla SINAMICS S120, stosowane w trybie izochronicznym (IRT). Telegram 902 jest konfigurowany np. na CU310-2 PN V5.1 dla synchronizacji Safety z cyklem PROFINET
- **Konfiguracja w TIA Portal:** Device view napędu → zakładka „Submodules" → dodaj submoduł PROFIsafe (np. „PROFIsafe Telegram 30") → ustaw F-Address, F-monitoring time

**Relacja telegram PROFIdrive + PROFIsafe:**
Napęd może mieć jednocześnie telegram PROFIdrive (np. telegram 20 — sterowanie prędkością) i telegram PROFIsafe (np. telegram 30 — komendy Safety). Oba działają równolegle na tym samym połączeniu PROFINET.

**Praktyka commissioning:** Po dodaniu telegramu PROFIsafe do napędu → F-Address musi być identyczny w TIA Portal i w napędzie. Po każdej zmianie parametrów Safety wymagany jest Safety Acceptance Test z podpisem. W S120 z trybem izochronicznym (telegram 902) należy skonfigurować także partition image process (PIP) dedykowane tylko dla F-I/O.

> Źródło: SIMATIC Safety - Konfiguracja i programowanie (2), s.62 — konfiguracja submodułu „Profisafe Telgr 902" sterownika SINAMICS S120 CU310-2 PN V5.1 [ZWERYFIKOWANE]

### 7.6. Jak oblicza się i dobiera F-monitoring time dla modułów PROFIsafe?

**F-monitoring time (czas monitorowania PROFIsafe, TPSTO)** to parametr określający maksymalny dozwolony czas między kolejnymi poprawnymi ramkami PROFIsafe. Po jego przekroczeniu moduł F przechodzi do stanu bezpiecznego (passivation).

- **Konfiguracja:**
  - Centralnie: we właściwościach F-CPU → „Default F-monitoring time for F-I/O of this interface" — domyślna wartość dla wszystkich modułów F na danym interfejsie
  - Indywidualnie: we właściwościach każdego F-I/O → „F-monitoring time" — nadpisuje wartość domyślną
- **Zasada doboru:**
  - **Za krótki** → fałszywe passivation przy chwilowym obciążeniu sieci (np. duży ruch PROFINET, wiele stacji)
  - **Za długi** → wolna reakcja na rzeczywistą awarię komunikacji — wydłuża czas odpowiedzi Safety
- **Narzędzie do obliczeń:** Siemens udostępnia arkusz kalkulacyjny Excel do obliczenia minimalnego F-monitoring time na podstawie: czasu cyklu PROFINET, liczby F-I/O, czasu cyklu grupy F-runtime, topologii sieci. Dostępny na support.automation.siemens.com (Entry ID: 49368678)
- **Czynniki wpływające:** czas cyklu PROFINET (Send Clock), liczba urządzeń na interfejsie, update time F-I/O, czas cyklu F-runtime group

**Procedura weryfikacji na obiekcie (z dokumentacji Siemens):**
1. Dodaj tymczasowy F-I/O do sieci
2. Ustaw na nim krótszy F-monitoring time niż na produkcyjnych F-I/O
3. Jeśli tymczasowy F-I/O generuje „Monitoring time for safety message frame exceeded" → wartość jest poniżej minimum
4. Zwiększaj F-monitoring time aż przestanie generować błędy — to przybliżone minimum dla sieci

**Praktyka commissioning:** Na nowych instalacjach zacznij od wartości domyślnej F-CPU. Jeśli pojawiają się sporadyczne passivation bez widocznej przyczyny sieciowej → zwiększ F-monitoring time o 50%. Zawsze dokumentuj wartości w tabeli komisjonowania.

> Źródło: SIMATIC Safety - Konfiguracja i programowanie (2), s.654-655 — procedura kontroli czasu monitorowania PROFIsafe [ZWERYFIKOWANE]

### 7.7. Jak PROFIsafe chroni przed przekłamaniem danych i jakie mechanizmy bezpieczeństwa stosuje ramka PROFIsafe?

**PROFIsafe** implementuje warstwę bezpieczeństwa na standardowym PROFINET/PROFIBUS, stosując mechanizm „black channel" — traktuje sieć jako kanał niebezpieczny i zabezpiecza się przed wszystkimi typami błędów transmisji.

**Mechanizmy ochronne w ramce PROFIsafe:**

- **CRC (Cyclic Redundancy Check)** — obliczany na podstawie danych Safety, F-Address i Virtual Consecutive Number (VCN). Wykrywa przekłamanie danych (bit flip) i błędne zaadresowanie (moduł dostaje dane innego modułu)
  - CRC1 (3 bajty) — dla krótszych telegramów
  - CRC2 (4 bajty) — dla dłuższych telegramów, wyższe pokrycie błędów
- **Virtual Consecutive Number (VCN)** — wirtualny numer sekwencyjny wbudowany w obliczenie CRC (nie jest osobnym polem w ramce). Chroni przed: utratą pakietu, powtórzeniem pakietu (replay), błędną sekwencją
- **Toggle bit** — w status/control byte ramki PROFIsafe. Zmienia się przy każdej nowej ramce — pozwala odbiorcy wykryć, czy otrzymał nową ramkę czy powtórzenie
- **F-Address w CRC** — adres nadawcy/odbiorcy jest wbudowany w obliczenie CRC. Jeśli ramka dotrze do niewłaściwego urządzenia, CRC się nie zgadza → passivation
- **Watchdog (F-monitoring time)** — jeśli prawidłowa ramka nie dotrze w określonym czasie → passivation

**Porównanie z „gołym" PROFINET:**
| Zagrożenie | PROFINET | PROFIsafe |
|-----------|----------|-----------|
| Bit flip | Ethernet CRC (L2) — nie fail-safe | CRC1/CRC2 z F-Address — fail-safe |
| Utrata pakietu | Brak wykrycia | VCN + watchdog |
| Powtórzenie/replay | Brak wykrycia | VCN + toggle bit |
| Błędny adres | Routing do IP — nie fail-safe | F-Address w CRC |

**Praktyka commissioning:** PROFIsafe nie wymaga specjalnego okablowania ani dedykowanych switchy — działa na standardowej infrastrukturze PROFINET. Ale jakość sieci wpływa na ilość retransmisji i ryzyko passivation. Na obciążonych sieciach → monitoruj wskaźnik retransmisji PROFIsafe w diagnostyce TIA Portal.

*[ZWERYFIKOWANE] — na podstawie SIMATIC Safety Integrated broszura (PROFINET i PROFIsafe, „black channel", s.7) + SIMATIC Safety - Konfiguracja i programowanie*

### 7.8. Jak działa komunikacja Safety między dwoma F-CPU (Safety-to-Safety communication) przez PROFIsafe?

**Komunikacja Safety-to-Safety (F-CPU ↔ F-CPU)** pozwala na wymianę danych bezpieczeństwa między dwoma sterownikami Safety bez pośrednictwa standardowego kodu — np. przekazanie stanu E-Stop z jednej linii do drugiej.

- **Realizacja:** Przez instrukcje `SENDDP/RCVDP` (S7-300F/400F) lub przez **Safety Data Exchange (S7-1500F)** — wymiana danych Safety przez PROFINET IO między dwoma F-CPU
- **Mechanizm:**
  - Jeden F-CPU jest IO-Controller, drugi jest IO-Device (lub oba mają funkcję Shared Device / I-Device)
  - Dane Safety przesyłane są przez PROFIsafe z pełnym CRC, VCN i F-monitoring time — identycznie jak dla F-I/O
  - Każde połączenie Safety-to-Safety wymaga osobnego F-Address i F-monitoring time
- **Zastosowanie:**
  - Linia produkcyjna z wieloma stacjami, każda ma własny F-CPU — E-Stop na jednej stacji musi zatrzymać napędy na sąsiednich
  - Robot ABB z dedykowanym PLC Safety — wymiana danych Safety z nadrzędnym F-CPU linii
  - Automotive: SICAR — każda cela robotyczna ma własny F-CPU, sygnały Safety (bramki, E-Stop, kurtyny) muszą być dzielone między celami

**Konfiguracja w TIA Portal:**
1. F-CPU „nadawca" konfiguruje transfer area w Safety Administration → definiuje jakie dane wysyła
2. F-CPU „odbiorca" konfiguruje odbieranie z podaniem F-Address nadawcy
3. Oba F-CPU muszą mieć identyczne collective signature Safety po konfiguracji

**Praktyka commissioning:** Przy Safety-to-Safety upewnij się, że F-monitoring time jest dostatecznie długi — komunikacja przechodzi przez PROFINET między CPU, co dodaje opóźnienie. Na dużych instalacjach z wieloma hopami sieciowymi zwiększ F-monitoring time o współczynnik 2-3x względem lokalnych F-I/O.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens, szczegóły konfiguracji Safety-to-Safety mogą się różnić między S7-300F/400F a S7-1500F*
