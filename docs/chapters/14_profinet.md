## 14. PROFINET — TOPOLOGIA, DIAGNOSTYKA I ZAAWANSOWANE FUNKCJE


### 14.1. Co to jest MRP (Media Redundancy Protocol) i kiedy go stosujesz?  🟢

<span style="color:#1a5276">**MRP**</span> (Media Redundancy Protocol) to protokół redundancji Ethernet w topologii **pierścieniowej** PROFINET.

| MRP wariant | Czas przełączenia | Limit urządzeń | Wymagania |
|-------------|------------------|----------------|-----------|
| **MRP** | ≤ 200 ms | max 50 | Standard switch z PROFINET |
| **MRPD** *(Planned Duplication)* | ≈ 0 ms | zależny od IRT | Tryb IRT, SCALANCE X lub CPU z IRT |

**Zasada działania:** w normalnej pracy pierścień działa jak linia — jeden port blokowany przez **MRM** (Media Redundancy Manager, zazwyczaj switch lub CPU). Przy zerwaniu kabla port otwiera się → ruch odbywa się w drugą stronę.

**Konfiguracja:** TIA Portal → Network view → właściwości switcha/CPU → PROFINET → `Media redundancy` → ustaw role MRM/MRC.

> ⚠️ Termin **„Fast-MRP"** nie jest oficjalnym pojęciem PROFINET — nie używaj go na rozmowie.

> 💡 Stosujesz gdy awaria pojedynczego kabla nie może zatrzymać produkcji.

*[ZWERYFIKOWANE - IEC 61158-6-10 (PROFINET MRP standard); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/); [SIMATIC NET PROFINET (Siemens)](https://www.siemens.com/global/en/products/automation/industrial-communication/profinet.html)]*
### 14.2. Co to jest IRT (Isochronous Real-Time) i kiedy jest wymagany?  🟢

<span style="color:#1a5276">**IRT**</span> (Isochronous Real-Time) to tryb PROFINET z deterministyczną synchronizacją cyklu do **250 µs** i jitterem **< 1 µs**, realizowaną sprzętowo (ASIC).

| Tryb | Cykl | Jitter | Realizacja | Zastosowanie |
|------|------|--------|------------|-------------|
| **RT** *(Real-Time, standard)* | ~1 ms | kilka–kilkanaście µs | Programowa | Standardowe I/O, roboty |
| **IRT** *(Isochronous Real-Time)* | do 250 µs | < 1 µs | Sprzętowa (ASIC) | S120 synchroniczny, systemy wieloosiowe |

**Wymagania IRT:**
- Zarządzane switche Siemens (np. SCALANCE X) lub topologia gwiazdki bez zewnętrznych switchów
- CPU obsługujące IRT (S7-1500 — większość modeli z interfejsem PN/DP, w tym standardowe, T-CPU i F-CPU)
- Telegram 105 (DSC) lub 111 dla SINAMICS S120

*[ZWERYFIKOWANE - IEC 61158-6-10 (PROFINET IRT specification); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/); [SINAMICS G120 Safety Function Manual (Entry ID: 109751595)](https://support.industry.siemens.com/cs/document/109751595/)]*
### 14.3. Jak diagnostykujesz sieć PROFINET w TIA Portal i PRONETA?  🟡

**Diagnostics w TIA Portal:**
1. Online → rozwiń `Devices & Networks` → prawym na urządzenie → `Diagnose`
2. Zakładka `Diagnostics` — stan komunikacji, aktywne alarmy, topology view (połączenia portów)
3. `Go Online` → mapa sieci ze statusami wszystkich urządzeń

**PRONETA** *(bezpłatne narzędzie Siemens)*:
- Standalone diagnostics PROFINET — niezależny od TIA Portal
- Skanuje sieć, pokazuje mapę urządzeń, nazwy PROFINET, IP, porty

> 💡 PRONETA jest szczególnie użyteczny gdy **nie masz projektu TIA** ani dostępu do sterownika — np. przy szybkiej diagnozie u klienta lub sprawdzeniu sieci nieznanego systemu.

*[ZWERYFIKOWANE - [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/) — rozdz. PRONETA, online diagnostics; [SIMATIC NET PRONETA tool (Siemens)](https://support.industry.siemens.com/cs/document/67460624/)]*
### 14.4. Co to jest Shared Device i kiedy go używasz?

**Shared Device** (PROFINET) to urządzenie I/O równocześnie zarządzane przez **dwa kontrolery** — każdy ma przypisany inny zakres modułów.

**Przykład:** ET200SP z 16 slotami:
- CPU A zarządza slotami 1–8 *(program standardowy)*
- CPU B zarządza slotami 9–16 *(program Safety)*

**Stosujesz gdy:**
- Integracja Safety z systemem standardowym obsługiwanym przez różnych dostawców PLC
- Aplikacja Safety i standardowa mają osobne sterowniki

**Konfiguracja:** TIA Portal → właściwości urządzenia → `Advanced Settings` → `Shared Device`

*[ZWERYFIKOWANE - [SIMATIC ET 200SP Shared Device (TIA Portal Help)](https://www.siemens.com/global/en/products/automation/systems/industrial/et-200sp.html); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/)]*
### 14.5. Jak działa Device replacement bez PG (automatic name assignment)?

CPU S7-1500 może automatycznie przypisać nazwę PROFINET nowemu modułowi bez laptopa z TIA Portal.

**Warunek:** TIA Portal → CPU Properties → `Support device replacement without exchangeable medium` *(domyślnie włączone w S7-1500)*

**Procedura:**
1. Wymień fizycznie urządzenie na **ten sam typ katalogowy**
2. Podłącz do sieci PROFINET
3. CPU widzi urządzenie bez nazwy → porównuje topologię (numery portów switch)
4. CPU przypisuje nazwę automatycznie

> ⚠️ **Nie działa** jeśli: nowe urządzenie ma inny typ katalogowy, lub topologia sieci jest niejednoznaczna (duplikaty portów).

*[ZWERYFIKOWANE - [TIA Portal Help: Device replacement without exchangeable medium](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [SIMATIC ET 200SP (Siemens)](https://www.siemens.com/global/en/products/automation/systems/industrial/et-200sp.html)]*
### 14.6. Jakie są rodzaje i funkcje przemysłowych switchy Ethernet w sieciach PROFINET?

Przemysłowe switche Ethernet zapewniają komunikację PROFINET w trudnych warunkach. Dzielą się na dwie kategorie:

**Niezarządzalne (Plug & Play):**
- Nie wymagają konfiguracji — podłącz i działa
- Fast Ethernet (10/100 Mb/s) lub Gigabit (10/100/1000 Mb/s), porty SFP (światłowód)
- Niektóre wspierają QoS (priorytet pakietów PROFINET) mimo braku konfiguracji
- Zastosowanie: proste segmenty sieci, rozgałęzienia I/O

**Zarządzalne:**
- Pełna kontrola: VLAN, QoS, RSTP/MRP (redundancja), SNMP, LACP (agregacja łączy), IGMP Snooping
- Diagnostyka: web interface, port monitoring, port mirroring
- Kontrola dostępu: 802.1X, Port Access Control, DHCP Snooping
- Wersje Gigabit z portami SFP, PoE+ (zasilanie kamer, czytników)
- **Wymagane** dla topologii pierścieniowych (MRP), IRT, sieci z diagnostyką

**Wspólne cechy przemysłowych switchy:**
- Metalowa obudowa IP30, montaż DIN, bezwentylatorowe (-40 do 75°C)
- Redundantne zasilanie DC + styk przekaźnikowy Fault
- Odporność EMC wg norm EN, architektura non-blocking

**Na co zwracać uwagę przy PROFINET:**
- QoS musi priorytetyzować ramki PROFINET (VLAN Priority 6/7)
- Zarządzalny switch = wymagany do MRP, IRT, TSN i diagnostyki PROFINET
- W Siemens: seria SCALANCE X (XB/XC/XP/XR) — zintegrowana z TIA Portal

*Źródło: transkrypcje ControlByte*

### 14.7. Co to jest S7 Communication (GET/PUT) i ISO on TCP — kiedy i jak je stosujesz?

S7 Communication to protokół komunikacji PLC–PLC i HMI–PLC firmy Siemens oparty na ISO on TCP (RFC 1006 — TCP/IP z warstwą ISO). Umożliwia bezpośredni dostęp do obszarów pamięci DB, M, I, Q zdalnego sterownika przez sieć PROFINET/Industrial Ethernet.

**Instrukcje GET/PUT:**
- `GET` — odczyt danych ze zdalnego PLC do lokalnego DB (dostępny w S7-1200/1500 z biblioteki Communication).
- `PUT` — zapis danych z lokalnego DB do zdalnego PLC.
- W S7-1200: bloki GET/PUT wbudowane. W S7-1500: dostępne przez Communication → S7 Communication.

**Zastosowania:**
- Komunikacja PLC–PLC między dwoma liniami bez SCADA (PLC A czyta statusy z PLC B).
- HMI firm trzecich (Weintek, Proface, IDEC) obsługujących S7 protocol — mapują bezpośrednio adresy DB, bez GSDML.
- Legacy integracja ze starszymi systemami SCADA (WinCC V6, InTouch) lub sterownikami S7-300/400.

**Kluczowe ograniczenie bezpieczeństwa — S7-1500:**
Domyślnie w S7-1500 dostęp PUT/GET z zewnętrznych urządzeń jest **zablokowany**. Aktywacja: TIA Portal → CPU Properties → Protection & Security → **Permit access with PUT/GET communication**.

> ⚠️ Włączenie PUT/GET obniża poziom bezpieczeństwa — każde urządzenie znające IP PLC może czytać/pisać pamięć bez uwierzytelniania. **Nigdy nie włączaj** w systemach podłączonych do sieci korporacyjnej bez firewalla.

> 💡 Dla nowych integracji z IT preferuj **OPC UA** (TLS 1.2 + certyfikaty). S7/ISO on TCP = szybkie (<1 ms), bez autentykacji. OPC UA = ~10 ms, z szyfrowaniem — wybór dla systemów IT/OT.

*[ZWERYFIKOWANE - [TIA Portal Help: S7 Communication GET/PUT](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [PROFINET diagnostics Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/); IEC 62541 (OPC UA standard)]*
### 14.8. Co to jest PROFINET TSN (Time Sensitive Networking) i czym różni się od IRT?  🟢

**PROFINET TSN** to następca IRT — stan standaryzacji IEEE 802.1 definiujący determinizm czasowy w standardowym Ethernet na poziomie sprzętowym, ale bez wymogu specjalistycznych ASIC-ów jak w IRT.

**Kluczowe cechy TSN:**

| Cecha | PROFINET IRT | PROFINET TSN |
|-------|-------------|-------------|
| Standard | Siemens-proprietary ASIC | IEEE 802.1AS/Qbv/Qbu (open standard) |
| Cykl | 250 µs | 31.25 µs – 1 ms (konfigurowalny) |
| Jitter | < 1 µs | < 1 µs |
| Switche | Tylko SCALANCE X (Siemens) | Dowolny switch TSN-compliant (multi-vendor) |
| Topologia | Gwiazdka lub linia (bez obcych switchów) | Elastyczna, mieszana |
| Telegram | 102, 105 (S120) | Te same (102, 105, 111) — zmiana na warstwie transportowej, nie aplikacji |

**Mechanizmy TSN (IEEE 802.1):**
- **802.1AS** — synchronizacja czasu gPTP *(generalized Precision Time Protocol)* z dokładnością < 1 µs
- **802.1Qbv** — Time-Aware Shaper: harmonogramowanie ramek Ethernet w oknach czasowych (time slots)
- **802.1Qbu** — Frame Preemption: przerywanie niskopriorytetowych ramek dla krytycznej transmisji

**Zastosowanie TSN:**
- Synchronizacja osi w systemach MRC (Motion Control Systems) z > 100 osi
- Koroboty (cobots) wymagające deterministycznej synchronizacji z PLC < 1 ms
- Fabryki przyszłości (Industry 4.0) — jeden segment Ethernet dla OT i IT jednocześnie

> ⚠️ **Stan w 2026:** PROFINET TSN jest zdefiniowany w PI (PROFIBUS & PROFINET International) specyfikacji V2.4. Sprzęt Siemens obsługujący pełne TSN: **SIMATIC S7-1500 V3.0+** oraz **SCALANCE XC/XP TSN**. Sprawdź aktualną wersję firmware przed projektem.

> 💡 **Na rozmowie:** pytanie o TSN pojawia się coraz częściej. Kluczowa odpowiedź: TSN = IRT-like deterministm ale na otwartym standardzie IEEE → nie wymaga jednorodnej infrastruktury Siemens.

*Źródło: PROFIBUS & PROFINET International (PI), PROFINET Specification V2.4*

---

