## 11. COMMISSIONING I DIAGNOSTYKA

### 11.1. Co sprawdzasz przed pierwszym RUN Safety?  🔴

**Checklista przed pierwszym uruchomieniem Safety:**

- [ ] Poprawność okablowania modułów F (`VS*`, `NC`, konfiguracja dwukanałowa)
- [ ] `F-Address` zgodny w TIA Portal i na modułach fizycznych (DIP switch lub elektroniczny)
- [ ] <span style="color:#c0392b">**Collective signature**</span> skompilowana i wgrana kompletnie do F-CPU
- [ ] Substitute values ustawione zgodnie z projektem Safety
- [ ] `Discrepancy time` dopasowany do czujników — nie za krótki!
- [ ] `ACK_NEC` podpięte do przycisku Reset (jako impuls, nie poziom stały)
- [ ] `F-monitoring time` skonfigurowany dla topologii sieci
- [ ] Safety CPU w trybie **RUN Safety** (nie LOCK, nie STOP)
- [ ] Dokumentacja Safety dostępna (Safety plan, listy testów, F-signature baseline)

**Przypisanie adresów PROFIsafe (procedura online):**
1. TIA Portal → `Devices & Networks` → prawym na moduł → `Assign PROFIsafe address`
2. Kliknij `Identification` → diody LED modułu **migają zielono jednocześnie**
3. Zaznacz `Confirm` → `Assign`

> 💡 Adres PROFIsafe zapisywany jest w **elektronicznym elemencie kodującym** modułu — przy wymianie modułu nowy moduł dziedziczy stary `F-Address` automatycznie, jeśli element kodujący pozostaje.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.2. Jak testujesz e-stop podczas commissioning?  🟡

**Procedura testu e-stop — wykonaj dla każdego e-stopu osobno:**

1. Uruchom maszynę w trybie wolnym/testowym przy bezpiecznej prędkości
2. Wciśnij e-stop — weryfikuj natychmiastowe zatrzymanie **WSZYSTKICH** osi/napędów
3. Sprawdź że nie można uruchomić maszyny z wciśniętym grzybkiem
4. Odblokuj e-stop (przekręć) i wykonaj ACK — sprawdź poprawny powrót do RUN
5. Zmierz i zapisz **czas reakcji** (od wciśnięcia do zatrzymania) — porównaj z wartością z oceny ryzyka
6. **Dokumentuj wynik z datą i podpisem** — wymagane do FAT/SAT

> ⚠️ Powtórz dla **KAŻDEGO** e-stopu w każdej lokalizacji na maszynie. Jeden nieprzetestowany e-stop = maszyna nie może być odebrana!

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.3. Co to jest FAT i SAT w kontekście Safety?  🟢

| Test | Gdzie | Cel |
|------|-------|-----|
| **FAT** *(Factory Acceptance Test)* | Zakład dostawcy maszyny | Testy przed wysyłką — każda funkcja Safety, wyniki podpisane przez dostawcę i klienta |
| **SAT** *(Site Acceptance Test)* | U klienta po instalacji | Potwierdzenie że Safety działa w docelowym środowisku (okablowanie terenowe, warunki przemysłowe) |

Dla Safety: oba zawierają **obowiązkowe testy każdego e-stopu, kurtyny i krańcówek** — wyniki dokumentowane i podpisywane.

> 💡 Safety Report z TIA Portal (Collective Signature) jest częścią dokumentacji FAT — potwierdza że program Safety nie był modyfikowany po certyfikacji.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.4. Jak postępujesz gdy odkryjesz błąd w logice Safety po FAT?

> ⚠️ **Nie modyfikujesz samodzielnie bez formalnej zgody** — każda zmiana programu Safety wymaga ścieżki Change Request i ponownej akceptacji (nowa `F-signature`).

**Procedura zmiany Safety po FAT:**

1. Zgłaszam do Safety Engineer / project managera — formalny `Change Request`
2. Zmiana zaakceptowana → dokonuję modyfikacji w TIA Portal
3. Kompiluję → nowa `F-signature` → wgranie do CPU
4. Przeprowadzam **testy regresji** (retesty dotkniętych funkcji Safety)
5. Generuję nowy Safety Report z nową <span style="color:#c0392b">**Collective Signature**</span>
6. Dokumentuję: co zmieniono, kiedy, kto zatwierdził, wyniki testów po zmianie

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.5. Jakie są najczęstsze przyczyny passivation F-DI w praktyce?  🟡

Najczęstsze przyczyny <span style="color:#c0392b">**passivation**</span> modułu F-DI wg doświadczenia commissionerów:

| Przyczyna | Jak zdiagnozować |
|-----------|----------------|
| Zerwany kabel czujnika *(najczęściej)* | Multimetr na zaciskach modułu |
| Czujnik NC „przyklejony" — uszkodzony mechanicznie | Ręczna aktywacja, sprawdź otwieranie NC |
| Źle przyłączony `VS*` — brak zasilania impulsowego | Sprawdź LED `VS*` modułu lub oscyloskop |
| `Discrepancy time` za krótki dla danego czujnika/prędkości | Zwiększ `discrepancy time` w parametrach modułu |
| Utrata komunikacji PROFIsafe — przeciążony switch | Sprawdź obciążenie switcha i `F-monitoring time` |
| Złe ustawienie `F-monitoring time` | Zweryfikuj topologię sieci, dostosuj wartość |
| Zwarcie do 24V na wejściu (np. łączenie kabli w trasie kablowej) | Pomiar izolacji kabla |

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.6. Jak reagować gdy moduł F świeci błędem którego nie możesz skasować?

**Systematyczna checklista debugowania:**

- [ ] Odczytaj **dokładny kod błędu** z diagnostyki TIA Portal — nie tylko status LED
- [ ] Sprawdź czy błąd fizyczny faktycznie usunięty (kabel, czujnik multimetrem)
- [ ] `ACK_NEC` podany jako **impuls** (zbocze narastające), NIE stały poziom HIGH?
- [ ] F-CPU w trybie **RUN Safety** — nie LOCK?
- [ ] Przy błędzie wewnętrznym modułu: wymień moduł — **zachowaj ten sam `F-Address`**
- [ ] Przy błędzie `F-signature`: pełna rekompilacja + pełne wgranie (`Download → All`)
- [ ] Jeśli nic nie pomaga: backup projektu → pełen restart CPU (`MRES`)

> ⚠️ Po wymianie modułu `F-Address` musi być **identyczny** ze starym — bez tego moduł pozostanie <span style="color:#c0392b">**spassivowany**</span> nawet przy sprawnym sprzęcie.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.7. Jak wygląda typowy workflow pierwszego commissioning z TIA Portal — od projektu do działającej maszyny?

Sekwencja kroków w praktyce commissioning z TIA Portal:

**1. Weryfikacja projektu (offline):**
- Sprawdź wersję TIA Portal w projekcie vs zainstalowana na laptopie — niezgodność = nie otworzysz projektu.
- Sprawdź wersję firmware CPU w projekcie vs fizyczny sterownik — TIA Portal ostrzega, ale może odmówić Download.
- Przejrzyj `Devices & Networks` — czy IP adresy nie kolidują, czy wszystkie moduły są skonfigurowane.

**2. Go Online — pierwsze połączenie:**
- Podłącz laptop przez PROFINET lub USB PG. TIA Portal → `Online → Go online`.
- Jeśli CPU i projekt niezsynchronizowane: `Compare offline/online` → sprawdź różnice.
- Pierwsze wgranie: `Download to device → Hardware and software → All`.

**3. Diagnoza startu:**
- `Diagnostics buffer` (Online → PLC → Diagnostics) — ostatni wpis = ostatnie zdarzenie (STOP, błąd, start). Pierwsze miejsce diagnostyki.
- Moduły I/O: wszystkie zielone = OK. Pomarańczowe/czerwone = błąd konfiguracji lub awaria sprzętu.
- Safety: sprawdź tryb Safety RUN, collective signature zatwierdzona, F-Address przypisany.

**4. Monitoring I/O:**
- Watch Table: dodaj kluczowe zmienne (czujniki, wyjścia, timery) → monitoruj wartości na żywo.
- Force Values: wymuś wartości I/O do testów okablowania — tylko przy wyłączonej maszynie.

**5. Typowe pułapki pierwszego uruchomienia:**

> ⚠️ **CPU w STOP po Download** → sprawdź `Diagnostics buffer` — prawdopodobnie błąd adresowania lub konfiguracji.

> ⚠️ **Moduł pokazuje błąd ale kabel OK** → sprawdź numer katalogowy w TIA Portal = fizyczny moduł (inna rewizja hardware ≠ ten sam katalog).

> ⚠️ **HMI nie łączy się z PLC** → sprawdź IP w tej samej podsieci i czy firewall laptopa nie blokuje portu `102` (S7 protocol).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 11.8. Jakie są etapy uruchomienia napędu SINAMICS G120 — od sprzętu do pierwszego ruchu?

SINAMICS G120 to przemiennik częstotliwości zbudowany z wymiennych komponentów: **CU (Control Unit)** + **PM (Power Module)**. Uruchomienie odbywa się przez **Startdrive** (wtyczka TIA Portal) lub standalone **STARTER**.

**Budowa — dobór komponentów:**
- CU: np. CU240E-2 DP (PROFIBUS), CU240E-2 PN (PROFINET), CU250S-2 (z enkoderem)
- PM: PM230 (bez hamowania), PM240-2 (z chopperem hamującym), PM250 (regeneratywny)
- Moc PM musi pasować do silnika — dobór wg karty katalogowej

**Etapy uruchomienia w Startdrive (TIA Portal):**

**1. Dodanie napędu do projektu:**
- `Devices & Networks` → `Add new device` → SINAMICS G120 → wybierz wersję CU
- Ustaw adres PROFINET (nazwa urządzenia + IP) — synchronizacja z fizycznym napędem przez `Assign device name`

**2. Quick Commissioning (p0010 = 1):**
- `p0100` — normy silnika: 0 = IEC (50 Hz, kW), 1 = NEMA (60 Hz, hp)
- `p0300` — typ silnika: 1 = silnik asynchroniczny (IM), 2 = PMSM (synchroniczny)
- Dane z tabliczki znamionowej silnika: `p0304` (napięcie), `p0305` (prąd znamionowy), `p0307` (moc), `p0308` (cos φ), `p0309` (sprawność), `p0310` (częstotliwość), `p0311` (prędkość)
- `p1080` / `p1082` — prędkość minimalna / maksymalna [rpm]
- `p1120` / `p1121` — czas rampy przyspieszania / hamowania [s]
- Zakończenie Quick Commissioning: `p3900 = 1` → napęd przelicza parametry i wraca do `p0010 = 0`

**3. Identyfikacja silnika (Motor Data Identification):**
- `p1910 = 1` → napęd wykonuje pomiar rezystancji uzwojeń przy zatrzymanym silniku
- `p1910 = 3` → identyfikacja silnika przy obracającym się wale (Rotating Motor Identification)
- `p1960 = 1` → optymalizacja regulatora prędkości (Speed Controller Optimization) — odrębny proces od identyfikacji silnika
- Wyniki zapisywane automatycznie do parametrów regulatora

**4. Telegram PROFINET i PZD:**
- `p0922` — wybór telegramu: 1 = standard (STW1/ZSW1 + Setpoint/Actual speed), 20 = rozszerzony, 352 = Safety
- W TIA Portal: w konfiguracji sprzętowej przypisz telegram G120 do DB komunikacyjnego; użyj FB `SINA_SPEED` (startdrive library)

**5. Fabryczny reset (gdy napęd był już używany):**
- `p0010 = 30`, następnie `p0970 = 1` → pełny reset do ustawień fabrycznych

**6. Weryfikacja i diagnostyka:**
- `r0002` — aktualny stan napędu (gotowy / run / fault)
- `r0945` — kod ostatniego błędu (Fault code) — niezbędny przy diagnostyce
- `r0947` — kod ostatniego alarmu (Alarm code)
- `r0949` — wartość powiązana z błędem (dodatkowa informacja diagnostyczna)
- Panel BOP-2 lub IOP na froncie CU — podgląd parametrów i stanów bez laptopa

**Praktyczne wskazówki:**

> 💡 Zawsze sprawdź zgodność napięcia zasilania PM z siecią zakładową (400 V / 480 V).

> 💡 Po `p3900 = 1` napęd generuje automatycznie parametry regulatora prędkości — nie nadpisuj ręcznie bez potrzeby.

> ⚠️ **PROFINET:** nazwa urządzenia w napędzie musi być **identyczna** jak w konfiguracji TIA Portal — **wielkość liter ma znaczenie**.

> ⚠️ **Fault `F07801`** (przetężenie) przy starcie → silnik za mały do PM lub zbyt krótki czas rampy (`p1120`).

*Źródło: Siemens SINAMICS G120 Getting Started / Startdrive commissioning guide*

### 11.10. Co to jest ProDiag i jak go używasz do diagnostyki maszyny?  🟢

ProDiag (Process Diagnostics) to mechanizm wbudowany w TIA Portal dla S7-1500 i ET200SP CPU. Pozwala definiować komunikaty diagnostyczne bezpośrednio w kodzie PLC i automatycznie wyświetlać je na HMI jako alarmy z opisem warunku.

**Jak działa:**
- W TIA Portal kliknij prawym na styk/cewkę w LAD/FBD → `Add supervision` → podaj tekst komunikatu (np. *„Motor M1 — brak potwierdzenia startu po 5s”*).
- TIA Portal wstawia blok ProDiag do kodu i rejestruje warunek.
- Na HMI (WinCC Unified lub Comfort): dodajesz widget `Diagnostic View` → automatycznie wyświetla aktywne komunikaty ProDiag z nazwą warunku i kontekstem.
- Dostępny online w TIA Portal bez HMI: Online → CPU → Diagnostics → Process diagnostics.

**Korzyści vs. klasyczne alarmy HMI:**
- Klasyczne alarmy WinCC: każdy alarm musisz ręcznie zdefiniować, zmapować bit, napisać tekst — czasochłonne dla 500+ alarmów.
- ProDiag: definicja w kodzie PLC → TIA Portal synchronizuje teksty do HMI automatycznie. Zmiana logiki = alarm aktualizuje się razem z kodem.

**Ograniczenia:**
- Dostępne tylko dla S7-1500 i ET200SP CPU — nie S7-1200.
- Wymaga WinCC Unified lub WinCC Comfort V15+ dla wyświetlania na HMI.
- Nie zastępuje Safety Alarms — Safety ma osobny mechanizm diagnostyki.

> 💡 **Na rozmowie:** Jeśli pytają o „jak robisz diagnostykę maszyny” — wymień ProDiag obok Watch Table i Diagnostics Buffer. Pokazuje to znajomość narzędzi nowszych wersji TIA Portal (V16+).

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
