## 7. PROFISAFE — KOMUNIKACJA SAFETY

### 7.1. Co to jest PROFIsafe i co zawiera jego pakiet?  🔴

<span style="color:#1a5276">**PROFIsafe**</span> to protokół Safety działający na **warstwie aplikacji** ponad standardowym PROFINET lub PROFIBUS — bez osobnego okablowania bezpieczeństwa.

**Dodatkowe dane w każdym pakiecie PROFIsafe** *(ponad normalne dane procesowe)*:

| Element | Rozmiar | Cel |
|---------|---------|-----|
| CRC (checksum) | 3 bajty | Wykrycie przekłamania danych |
| Licznik wiadomości | 1 bajt | Wykrycie utraty lub powtórzenia pakietu |
| F-Address | konfiguowalny | Wykrycie pakietu wysłanego do złego urządzenia |

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
