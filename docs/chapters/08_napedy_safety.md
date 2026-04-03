## 8. NAPĘDY SAFETY — SINAMICS Z WBUDOWANYM SAFETY

### 8.1. Co to jest STO (Safe Torque Off) i jak działa?  🔴

<span style="color:#c0392b">**STO**</span> natychmiastowo odcina moment obrotowy — falownik blokuje impulsy PWM do silnika. Silnik wybiega swobodnie (lub hamuje hamulec mechaniczny).

**Kluczowe cechy:**
- Brak rampy hamowania — natychmiastowe odcięcie
- Certyfikowany wg <span style="color:#1a5276">**IEC 61800-5-2**</span> — realizowany sprzętowo (dwa kanały w napędzie)
- Napęd potwierdza brak momentu do F-CPU przez PROFIsafe: sygnał `STO_Active`

> ⚠️ **Różnica od wyłączenia programowego:** komenda `OFF` przez PLC — niecertyfikowana, niemonitorowana, napęd może technicznie nadal generować moment.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.2. Jaka jest różnica między STO a zwykłym wyłączeniem napędu przez PLC?

| Cecha | STO | Wyłączenie programowe |
|-------|-----|----------------------|
| Certyfikacja | <span style="color:#1a5276">**SIL3/PLe**</span> | Brak |
| Realizacja | Sprzętowa (2 kanały w napędzie) | Programowa |
| Potwierdzenie braku momentu | `STO_Active` → F-CPU | Brak |
| Monitoring | TAK (PROFIsafe lub zaciski) | NIE |
| Restart po odwołaniu | Wymaga potwierdzenia Safety | Natychmiastowy |

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.3. Co to jest SS1 i kiedy go używasz zamiast STO?  🔴

<span style="color:#c0392b">**SS1**</span> (Safe Stop 1): napęd hamuje wzdłuż zaprogramowanej rampy do zerowej prędkości, następnie aktywuje STO.

**Kiedy SS1 zamiast STO:**
- Natychmiastowe odcięcie momentu (STO) jest **niebezpieczne** — duże masy inercyjne
- Obrabiarka z ciężkim stołem — ryzyko zderzenia narzędzia przy wybiegu
- Winda, dźwig — wybieg = niekontrolowany ruch z ładunkiem

> ⚠️ Czas hamowania SS1 jest **monitorowany** — jeśli napęd nie zatrzyma się w zadanym czasie → natychmiastowe STO jako zabezpieczenie.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.4. Co to są SS2, SOS, SLS, SDI, SBC?  🟢

| Funkcja Safety | Pełna nazwa | Działanie | Kiedy stosujesz |
|----------------|-------------|-----------|-----------------|
| **SS2** | Safe Stop 2 | Hamowanie z rampą → SOS (napęd zasilony, trzyma pozycję) | Wstrzymanie z zachowaniem pozycji (ramiona robotów, pionowe osie) |
| **SOS** | Safe Operating Stop | Napęd zasilony, monitoruje pozycję, może wytworzyć moment przy ruchu | Po SS2 lub gdy oś ma trzymać pozycję podczas inspekcji |
| **SLS** | Safely Limited Speed | Ograniczenie prędkości do bezpiecznego max | Tryb serwisowy — operator wchodzi do strefy, oś może się wolno ruszać |
| **SDI** | Safe Direction | Tylko jeden kierunek ruchu dozwolony | Osłona otwarta — oś może jechać tylko od operatora |
| **SBC** | Safe Brake Control | Certyfikowane sterowanie hamulcem — monitoring prądu uzwojenia | Osie pionowe z hamulcem mechanicznym Safety |

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.5. Jak STO jest realizowane sprzętowo — zaciski vs PROFIsafe?

Zaciski hardwarowe (STO1/STO2): bezpośrednie odcięcie sygnałów PWM przez zewnętrzny sygnał 24V z modułu Safety. Szybsze (bez opóźnienia sieci), prostsze, niezależne od komunikacji.
PROFIsafe: komenda STO przesyłana przez PROFINET. Umożliwia zaawansowane funkcje (SS1, SLS, SDI, diagnostyka przez sieć). Wymaga sprawnego połączenia sieciowego.
W praktyce: przy G120/S120 można łączyć oba sposoby — PROFIsafe dla zaawansowanych funkcji + zaciski STO jako backup.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.6. Co sprawdzasz przy commissioning napędu z STO?

Procedura:
- Podaję sygnał STO (przez zaciski lub PROFIsafe) — weryfikuję że napęd zatrzymał się i nie ma momentu
- Sprawdzam potwierdzenie STO_Active w statusie napędu (w TIA Portal lub Startdrive)
- Weryfikuję że nie można uruchomić napędu gdy STO aktywne
- Zdejmuję STO — sprawdzam poprawny restart
- Testuję czas reakcji
- Sprawdzam poprawność adresu PROFIsafe jeśli używany
- Dokumentuję wyniki z podpisem

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.7. Czym różnią się telegramy PROFIdrive 1, 20, 102, 352 i jak dobirasz telegram dla napędu SINAMICS?

Telegram PROFIdrive określa format wymiany danych między CPU a napędem przez PROFINET. Numer musi być zgodny w napędzie (`p0922`) i w konfiguracji Startdrive/TIA Portal.

| Telegram | Dane procesowe | Typowe zastosowanie |
|----------|---------------|---------------------|
| **1** | STW1/ZSW1 (16b) + NSET/NIST (16b) | Standardowy napęd, proste zadawanie prędkości V/f lub wektorowe bez enkodera |
| **20** | STW1/ZSW1 + NSET + prąd/moment + alarmy | Rozszerzony monitoring — Startdrive, diagnostyka prądu |
| **102** | STW + NSET + enkoder (pozycja + prędkość) | S7-1500 Motion Control (TO_SpeedAxis / TO_PositioningAxis) z enkoderem |
| **105** | Telegram DSC (Dynamic Servo Control) + enkoder | S7-1500 TO_SynchronousAxis — wymagany IRT i Startdrive |
| **352** | STW1/ZSW1 + PROFIsafe Safety | SINAMICS G120/S120 z Safety Integrated (STO/SS1/SLS przez PROFIsafe) |

**Jak dobrać telegram:**
- Tylko prędkość, bez enkodera, bez Safety → Telegram 1
- Motion Control S7-1500 z enkoderem → Telegram 102
- Synchronizacja osi, IRT → Telegram 105
- Safety (STO/SS1/SLS przez PROFIsafe) → Telegram 352

**Uwaga praktyczna:** Niezgodność telegramu między `p0922` a konfiguracją TIA Portal → napęd nie komunikuje się lub dane są przesunięte — błędne sterowanie bez alarmu. Zawsze weryfikuj `p0922` online po podłączeniu nowego napędu.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 8.8. Jakie funkcje bezpieczeństwa są wbudowane w serwowzmacniacz Sinamics V90 i jak należy je podłączyć?
Serwowzmacniacz Sinamics V90 jest wyposażony w funkcję bezpieczeństwa STO (Safe Torque Off), która zapewnia bezpieczne zdjęcie momentu obrotowego z napędu.
- Funkcja STO jest realizowana poprzez terminale STO+, STO1 i STO2.
- Domyślnie terminale te są zmostkowane, co oznacza, że funkcja STO jest nieaktywna w trybie bezpieczeństwa.
- W docelowej aplikacji sygnały STO należy podłączyć dwukanałowo do układu bezpieczeństwa, takiego jak przekaźnik bezpieczeństwa lub F-CPU (np. S7-1500F), aby zapewnić funkcję STO (Safe Torque Off) napędu.
*Źródło: transkrypcje ControlByte*

---

