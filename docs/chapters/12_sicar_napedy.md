## 12. SICAR I NAPĘDY SINAMICS

### 12.1. Co to jest SICAR i gdzie jest używany?  🟢

SICAR (Siemens Automation Platform for CAR Plants) to gotowy framework programistyczny Siemensa dla branży **automotive** (fabryki: Toyota, Tesla, BMW, VW). Oparty na TIA Portal.

**Zawartość SICAR:**
- Szablony PLC i HMI
- Biblioteki **Tec Units** — gotowe bloki dla silników, zaworów, napędów, robotów
- Wzorce alarmów i **ProDiag** dla diagnostyki

> 💡 Cel: skrócenie czasu programowania przez drag-and-drop gotowych bloków zamiast pisania logiki od zera.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 12.2. Co to są Tec Units i jak z nich korzystasz?  🟢

**Tec Units** to gotowe, parametryzowalne bloki funkcjonalne w SICAR dla typowych urządzeń: silnik, zawór, przenośnik taśmowy, napęd, robot. Każdy zawiera:
- FB PLC z logiką
- Ekrany HMI
- Definicje alarmów
- Obsługę trybów (Auto / Manual / Local)

> 💡 Używasz przez drag-and-drop Tec Unit na projekt, ustawiasz parametry (adres I/O, limity, czasy) — gotowe, bez pisania logiki od podstaw.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 12.3. Co to jest SINAMICS Startdrive w TIA Portal?

**SINAMICS Startdrive** to wtyczka do TIA Portal do parametryzacji, uruchamiania i diagnostyki napędów SINAMICS (G120, S120, V90) bezpośrednio z TIA Portal — bez osobnego oprogramowania STARTER.

**Możliwości:**
- Konfiguracja napędu i autotuning
- Monitoring parametrów online
- Diagnostyka błędów (fault codes)
- Konfiguracja Safety Integrated (STO, SS1, SLS przez PROFIsafe)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 12.4. Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?  🟡

**Konfiguracja SINAMICS G120 z Safety (w SINAMICS Startdrive):**

1. Dodaj napęd G120 do projektu (`CU240E-2 PN` lub `CU250S-2 PN`) — ustaw adres PROFINET i telegram (`p0922`)
2. Zakładka `Safety Integrated` → włącz PROFIsafe, ustaw `F-Address`
3. Wybierz funkcje Safety: `STO`, `SS1` (`p9560` = ramp time ⚠️ DO WERYFIKACJI w SINAMICS G120 Safety Function Manual), `SLS` (`p9531` = max prędkość ⚠️ DO WERYFIKACJI)
4. Autotuning: Static motor identification → Speed controller optimization
5. Weryfikacja Safety: test STO → accept safety settings → Safety checksum/Safety ID

Po stronie F-CPU: blok Safety dla napędu (F-FB dla G120 z biblioteki) odbiera/wysyła telegram PROFIsafe.

> ⚠️ `F-Address` musi być **identyczny** w TIA Portal i na fizycznym napędzie — inaczej Safety nie uruchomi się.

> 💡 Pełna procedura krok po kroku: → Sekcja 19 *(Commissioning — Dodawanie napędu G120)*.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
