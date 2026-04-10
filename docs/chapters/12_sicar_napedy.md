## 12. NAPĘDY SINAMICS

### 12.1. Co to jest SINAMICS Startdrive w TIA Portal?

**SINAMICS Startdrive** to wtyczka do TIA Portal do parametryzacji, uruchamiania i diagnostyki napędów SINAMICS (G120, S120, V90) bezpośrednio z TIA Portal — bez osobnego oprogramowania STARTER.

**Możliwości:**
- Konfiguracja napędu i autotuning
- Monitoring parametrów online
- Diagnostyka błędów (fault codes)
- Konfiguracja Safety Integrated (STO, SS1, SLS przez PROFIsafe)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 12.2. Jak konfigurujesz SINAMICS G120 z Safety przez PROFIsafe?  🟡

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
