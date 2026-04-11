## 17. REALNE SCENARIUSZE COMMISSIONING


### 17.1. Maszyna startuje sama po ACK bez przycisku Start — co sprawdzasz?

**Systematyczna checklista:**

- [ ] **Logika inicjalizacji OB100:** czy po resecie CPU warunek Start jest `TRUE` bez oczekiwania na zbocze?
- [ ] **HMI — typ eventu przycisku Start:** `Press` (zbocze) czy `State` (poziom)? Poziom = `TRUE` przez cały czas trzymania → program widzi ciągły sygnał start
- [ ] **Logika startowa:** czy warunek to zbocze narastające (`R_TRIG`) czy poziom `BOOL`? Maszyny **wymagają zbocza** — jednorazowy impuls
- [ ] **Fizyczny przycisk:** czy styk NO nie jest przyklejony lub przewód zwarty?
- [ ] **Safety ACK + start w logice:** jeśli ACK kasuje blokadę i jednocześnie zmienna startowa jest aktywna (nie skasowana po awaryjnym zatrzymaniu) — maszyna ruszy

> ⚠️ **Pułapka Safety + Start:** logika musi wymagać nowego impulsu Start **po** ACK. ACK samo w sobie nie powinno uruchamiać napędów.

*[ZWERYFIKOWANE - [TIA Portal Help: Safety program, ACK logic](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); EN 60204-1 §10.7 (start/restart requirements after safety stop); [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/)]*
### 17.2. HMI pokazuje alarm którego nie ma w projekcie TIA Portal — skąd pochodzi?

**Możliwe źródła „obcych" alarmów:**

| Źródło | Opis | Gdzie szukać |
|--------|------|-------------|
| **System alarm** *(auto)* | Generowany przez TIA Portal dla zdarzeń sprzętowych (moduł offline, błąd Safety, utrata komunikacji) | HMI → `System alarms` → `Diagnostic alarms` |
| **Stary projekt HMI** | Alarm do tagu który już nie istnieje — „stale" wpisy w alarm buffer | TIA Portal → HMI Alarms → Discrete Alarms → szukaj po numerze |
| **Alarm z urządzenia** | Napęd/robot wysyła alarm diagnostyczny przez PROFINET alarm mechanism | WinCC → `Diagnostic alarms` lub alarm z adresem sprzętowym |

> 💡 **Procedura:** TIA Portal → HMI Alarms → Discrete Alarms / Analog Alarms — filtruj po numerze alarmu. Jeśli brak → sprawdź `System alarms → Diagnostic alarms`.

*[ZWERYFIKOWANE - [TIA Portal Help: HMI Alarms, System alarms, Diagnostic alarms](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/)]*
### 17.3. Moduł ET200SP nie pojawia się w sieci po podłączeniu — lista kroków diagnostycznych.

- [ ] **Kabel fizyczny:** czy dioda LINK/ACT na porcie modułu lub switcha miga? Zamień kabel.
- [ ] **Zasilanie BusAdapter:** ET200SP wymaga zasilania `BA 2×RJ45` lub `BA SCRJ` — czy `L+` i `M` podłączone?
- [ ] **Nazwa PROFINET:** brak nazwy → moduł nowy/po resecie → TIA Portal → Online → `Accessible devices` → przypisz nazwę
- [ ] **Duplikat nazwy PROFINET:** dwa moduły o tej samej nazwie → konflikt — sprawdź całą sieć przez PRONETA
- [ ] **Switch / VLAN:** czy moduł w tej samej VLAN co CPU? *(SCALANCE CLI lub Web GUI → port status)*
- [ ] **Mapa topologii:** Online → `Devices & Networks` → Topology view → czy moduł widoczny?
- [ ] **GSDML / firmware:** stary hardware z nowym projektem może wymagać aktualizacji firmware modułu

> 💡 PRONETA → skan sieci → sprawdź czy moduł odpowiada na ARP — szybki sposób bez TIA Portal.

*[ZWERYFIKOWANE - [SIMATIC ET 200SP (Siemens)](https://www.siemens.com/global/en/products/automation/systems/industrial/et-200sp.html); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/) — rozdz. PRONETA, network scan, device name assignment]*
### 17.4. Napęd SINAMICS G120 świeci ciągłym czerwonym LED i nie kasuje się — co robisz?  🟢

Ciągły czerwony RDY LED = aktywny <span style="color:#c0392b">**fault**</span> (F-alarm), nie alarm (A-alarm, który jest żółty).

**Procedura diagnostyki:**
1. Odczytaj kod: `r0945[0]` w Startdrive (online) lub na panelu BOP-2 → zapisz `r0945[0..7]`
2. Sprawdź w Parameter Manual: każdy `Fxxxxx` ma opis przyczyny i działania korygującego
3. Najczęstsze: `F30001` (przetężenie wyjścia / overcurrent), `F07800-F07802` (temperatura silnika), `F30002` (przepięcie / nadnapięcie DC-bus — overvoltage), `F30004` (przegrzanie radiatora — overtemperature heatsink)

> ⚠️ Jeśli fault **kasuje się ale wraca natychmiast**: przyczyna fizyczna wciąż aktywna — nie idź dalej bez usunięcia przyczyny.

> ⚠️ Fault nie daje się skasować → sprawdź czy **STO nie jest aktywne** (`r9772` = STO status) — napęd nie ruszy ani się nie skasuje przy aktywnym STO.

> 💡 Jeśli kasowanie przez sieć nie działa: hardware reset — chwilowe odcięcie zasilania 24V Control Unit *(zachowaj 400V Power Module)*.

*[ZWERYFIKOWANE - [SINAMICS G120 (Siemens)](https://www.siemens.com/global/en/products/drives/sinamics/low-voltage-inverters/sinamics-g120.html); kody faultów F30001/F07800-F07802 ⚠️ DO WERYFIKACJI w SINAMICS G120 Parameter Manual (Fault and Alarm List); STO status r9772 ⚠️ DO WERYFIKACJI w SINAMICS G120 Safety Function Manual (Entry ID: 109751595)]*
### 17.5. CPU przeszło w STOP podczas produkcji — pierwsze 3 kroki.  🟢

CPU w STOP = zatrzymanie wszystkich wyjść. Prawidłowa kolejność: odczyt → diagnoza → przyczyna → **dopiero wtedy** akcja.

**Kroki:**
1. **Odczytaj informację ze sprzętu:** wyświetlacz S7-1500 pokazuje skrócony opis przyczyny STOP. Dioda RUN/STOP: ciągłe żółte = STOP. Zanotuj wszystko zanim podłączysz się do sieci.
2. **Diagnostics buffer w TIA Portal:** Online → CPU → `Diagnostics → Diagnostic buffer`. Ostatni wpis = przyczyna zatrzymania.

| Typowa przyczyna STOP | Co oznacza |
|----------------------|------------|
| `Time error OB cyclic` | Scan time przekroczony — za dużo kodu lub zablokowane wywołanie FB |
| `STOP requested by program` | Instrukcja `STP` w kodzie — szukaj w bloku aktywnym w chwili STOP |
| `Hardware failure` | Moduł I/O wypadł z konfiguracji lub zwarcie |
| `Safety STOP` | F-CPU wykryło błąd Safety — sprawdź F-Runtime group |

3. **Nie uruchamiaj niczego** zanim nie znasz przyczyny.

> ⚠️ **Zakaz Download przed diagnozą:** Download kasuje Diagnostics buffer na CPU — tracisz ślad przyczyny. Zawsze odczytaj Diagnostic buffer PRZED downloadem.

> 💡 **Warm restart a STOP:** `Warm restart` (Run) bez zrozumienia przyczyny = maszyna może natychmiast znów wejść w STOP. Jeśli przyczyną jest zwarcie I/O, warm restart tylko powtórzy błąd.

*[ZWERYFIKOWANE - [TIA Portal Help: CPU Diagnostic buffer, STOP modes](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [SIMATIC S7-1500 (Siemens)](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/simatic-s7-1500.html)]*
### 17.6. Po czym poznajesz, że projekt w TIA Portal jest skalowalny?  🟡

Skalowalny projekt TIA Portal to taki, który można rozszerzać (nowe urządzenia, sekcje, osie) bez przepisywania istniejącego kodu — tylko przez parametryzację lub powielanie gotowych wzorców.

**Cechy skalowalnego projektu:**
- **Global Library / Project Library (PLCtype):** każda nowa instancja = przeciągnięcie z biblioteki. Zmiana w typie → aktualizacja wszystkich instancji jednym kliknięciem.
- **UDT jako interfejs danych:** struktury UDT dla każdego urządzenia (np. `typeValve`: cmd, status, alarm, mode) — dodanie nowego zaworu = 1 zmienna UDT.
- **Tablice + pętle FOR:** zamiast 20 identycznych sieci LAD — jeden FB parametryzowany indeksem. Dodajesz urządzenie 21 przez zwiększenie `MAX_DEVICES`.
- **Symbolic addressing only:** zmiana konfiguracji sprzętowej (nowa karta IO, zmiana slotu) nie łamie programu.
- **Rezerwa slotów i adresów PROFINET:** nowe moduły dodajesz bez przesypywania konfiguracji.
- **Modularny kod Safety:** każda strefa jako osobny F-FB z własnym `ACK` i `PASS_OUT`.
- **Spójna konwencja nazw:** np. `++STATION_Drive01` — autogeneracja dokumentacji i wyszukiwanie po wzorcu.

> ⚠️ **Red flags braku skalowalności:** copy-paste FC z ręczną edycją numerów, absolutne adresy `I0.0`/`Q0.0`, brak bibliotek, każdy napęd w osobnym OB.

> 💡 **Na rozmowie:** skalowalność = biblioteki + UDT + tablice. Pokaż przykład: "Mamy 12 zaworów w tablicy, dodanie 13. to zmiana jednej stałej `MAX_VALVES`."

*[ZWERYFIKOWANE - [TIA Portal Help: Global Library, Project Library, UDT](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); IEC 61131-3 §6.4 (structured programming, data types, arrays)]*
### 17.7. Co sprawdzasz na FAT (Factory Acceptance Test) dla instalacji z Safety? 🟡
FAT (Factory Acceptance Test) to weryfikacja systemu u producenta maszyny przed wysyłką do klienta. Dla Safety obejmuje funkcjonalne testy każdej funkcji bezpieczeństwa zgodnie z wymaganiami normy EN ISO 13849-1 i dokumentacją techniczną.
- Weryfikacja F-Signatures (F-DB i F-CPU): sprawdź match między TIA Portal a CPU → F-Program → Signature Comparison
- Test każdego E-Stop fizycznie: wciśnij → CPU pasywuje → wyjścia = substitute values → zwolnij → ACK → restart
- Test discrepancy: symuluj opóźnienie jednego kanału 1oo2 > discrepancy time → passivation
- Test muting: aktywuj oba czujniki muting w oknie czasowym → kurtyna działa → odblokowanie
- Test napędów Safety: sprawdź STO, SS1, SLS każdej osi — porównaj z Safety Matrix
- Documented: każdy test zapisany w protokole FAT z datą, podpisem, numerem PO
- Checklista: F-Version, F-Address, F-Monitoring Time, passivation time, substitute values

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/) — rozdz. FAT checklist, F-Signature; EN ISO 13849-1 §10 (validation — dokumentacja, testy funkcjonalne)]*
### 17.8. Jak realizujesz SAT (Site Acceptance Test) po dostarczeniu maszyny do klienta? 🟡
SAT (Site Acceptance Test) to weryfikacja systemu na miejscu klienta po instalacji. Różni się od FAT tym, że uwzględnia rzeczywiste środowisko: okablowanie obiektowe, medium procesowe, warunki bezpieczeństwa operacyjnego.
- Krok 1: Upload projektu z CPU i porównaj z referencją z FAT (Project → Compare)
- Krok 2: Sprawdź F-Signature CPU vs wartość zapisana w FAT-protokole — muszą być identyczne
- Krok 3: Fizyczny test E-Stop i kurtyn w normalnych warunkach pracy maszyny
- Krok 4: Próba produkcyjna z rzeczywistym materiałem (opcjonalnie)
- Krok 5: Przeszkolenie operatorów i techników serwisu
- Dokumentacja: protokół SAT + podpis inżyniera Safety i przedstawiciela klienta
- Jeśli F-Signature różni się od FAT → STOP — ktoś zmienił program po FAT, eskalacja

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/) — rozdz. SAT, F-Signature verification; IEC 62061 §8.4 (validation and verification procedures)]*
### 17.9. Jak podejść do diagnostyki nieznanego lub legacy projektu TIA Portal, który przejmujesz po raz pierwszy? 🟡

**Scenariusz:** dostajesz maszynę z projektem TIA Portal od innego integratora lub starszą wersję — musisz zrozumieć co robi i ewentualnie poprawić usterki.

**Krok po kroku — archeologia projektu:**
1. **Wersja TIA Portal:** sprawdź `~AL\project.hmi` lub po prostu próbuj otworzyć — TIA informuje o wersji źródłowej; pobierz właściwą wersję (nie uaktualniaj bez decyzji)
2. **Firmware CPU:** Online → Device → Properties → porównaj z wymaganiami projektu; `r0018` = firmware napędu
3. **Upload z CPU:** Online → Upload Device as New Station — zawsze upload najpierw zanim cokolwiek zmienisz; masz wtedy rzeczywisty state PLC
4. **Compare Online/Offline:** Online → Compare → rozwiń różnice; każda różnica = ktoś zmieniał na żywym obiekcie bez zapisu projektu
5. **Diagnostics Buffer:** Online → Diagnostics → Diagnostics buffer — historia alarmów sprzętowych CPU; szukaj wzorców czasowych
6. **Cross-References:** w TIA Portal: Extras → Cross-references → szukaj gdzie i jak używana jest zmienna alarmowa
7. **F-Signature:** jeśli Safety — odczytaj F-Signature i porównaj z dokumentacją SAT; brak dokumentacji = czerwona flaga
8. **Komentarze w kodzie:** często brakuje — szukaj w historii edycji (`git blame` o ile projekt jest w SVN/GIT) lub wypytaj poprzedniego komisjonera
9. **HMI Cross-reference:** czy zmienne HMI odpowiadają zmiennym PLC (tag table); rozbieżności = źródło problemów

**Zasady bezpieczeństwa:**
- Nie zmieniaj nic bez zrozumienia konsekwencji
- Rób kopię zapasową przed każdą modyfikacją (Project → Save As)
- Dokumentuj każdą zmianę nawet jeśli projekt nie miał żadnej dokumentacji
- Jeśli Safety — każda zmiana wymaga nowego SAV/F-Signature i akceptacji klienta

> ⚠️ **Pułapka:** Upload z CPU nie zawsze daje pełny projekt — symbolicznie nazwane zmienne mogą być zastąpione adresami absolutnymi; komentarze i UDT mogą być stracone.

> 💡 **Na rozmowie:** pokaż, że znasz procedurę upload + compare + diagnostics buffer — to klasyczny scenariusz serwisowy. Wspomnij o F-Signature dla projektów Safety.

*Źródło: praktyka commissioning, transkrypcja ControlByte*

---

