## 6. SAFE STATE — BEZPIECZNY STAN

### 6.1. Co to jest Safe State i kto go definiuje?

<span style="color:#c0392b">**Safe State**</span> to stan systemu po wykryciu zagrożenia lub błędu Safety. Definiuje go **inżynier projektu** na podstawie analizy ryzyka maszyny — Siemens dostarcza tylko narzędzia.

| Urządzenie | Safe State | Uzasadnienie |
|-----------|-----------|-------------|
| Prasa | Stop silnika | Brak ruchu = bezpieczny |
| Pompa cyrkulacyjna reaktora | Pozostaje **WŁĄCZONA** | Stop = przegrzanie = niekontrolowana reakcja |
| Wentylator chłodzący | Pozostaje **WŁĄCZONY** | Stop = pożar urządzenia |
| Zawór odcinający | NO lub NC — zależy od procesu | Analiza ryzyka musi to określić jednoznacznie |

> ⚠️ **Safe State definiuje inżynier, nie Siemens.** Siemens mówi: *"narzędzia są tu — użyj ich zgodnie z analizą ryzyka"*.

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/); EN ISO 12100 §5.5 (definiowanie bezpiecznego stanu — obowiązek integratora)]*
### 6.2. Dlaczego Safe State to nie zawsze wyłączenie?

Bo wyłączenie może być **bardziej niebezpieczne** niż kontynuacja działania:
- Pompa cyrkulacyjna reaktora — stop = przegrzanie = niekontrolowana reakcja chemiczna
- Wentylator chłodzący transformator — stop = pożar
- Podajnik na linii produkcyjnej — nagły stop = zablokowanie i awaria mechaniczna

> ⚠️ **`substitute value` F-DO może być `1`** (wyjście aktywne przy passivation) — to decyzja inżyniera, nie ustawienie domyślne Siemensa.

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. substitute value F-DO](https://support.industry.siemens.com/cs/document/109751404/)]*
### 6.3. Jak F-DO substitute value wpływa na Safe State?

Parametr `substitute value` w TIA Portal (właściwości kanału F-DO) określa co wyjście robi przy passivation:

| `substitute value` | Zachowanie wyjścia | Kiedy używasz |
|-------------------|--------------------|---------------|
| `0` *(domyślne)* | Wyjście wyłączone | Napęd stop, zawór zamknięty — brak ruchu = bezpieczny |
| `1` | Wyjście aktywne | Pompa nadal działa, zawór otwarty — stop = większe ryzyko |

> 💡 To jest implementacja Safe State na **poziomie sprzętowym** — zadziała nawet przy awarii sieci komunikacyjnej, bez udziału logiki CPU.

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. F-DO substitute value configuration](https://support.industry.siemens.com/cs/document/109751404/)]*
### 6.4. Czym różni się STO jako Safe State napędu SINAMICS od zatrzymania programowego (OFF1/OFF2)? 🔴

W napędach SINAMICS istnieją **dwie kategorie** zatrzymań — i trzeba je wyraźnie oddzielić, bo mieszanie ich prowadzi do błędów w projekcie Safety.

---

#### A) Zatrzymania PROGRAMOWE (sterowane przez PLC — bez certyfikacji Safety)

Komendy OFF1/OFF2/OFF3 to standardowe zatrzymania napędu, wysyłane przez program PLC lub panel operatorski. **Nie są funkcjami Safety** — nie mają monitoringu, certyfikacji ani sprzętowego zabezpieczenia.

| Komenda | Kat. zatrzymania (EN 60204-1) | Co robi | Restart |
|---------|:-----------------------------:|---------|---------|
| **OFF1** | 1 | Hamowanie po rampie deceleracji → po zatrzymaniu odcięcie impulsów | Komenda ON — bez potwierdzenia |
| **OFF2** | 0 | Natychmiastowe odcięcie impulsów — wolny wybieg silnika | Komenda ON — bez potwierdzenia |
| **OFF3** | 1 (rampa awaryjna) | Szybka rampa hamowania → po zatrzymaniu odcięcie impulsów | Komenda ON — bez potwierdzenia |

> ⚠️ OFF2 wygląda jak STO (też odcina impulsy), ale **nie jest funkcją Safety** — jest sterowana programowo, bez monitoringu i bez redundancji sprzętowej.

---

#### B) Funkcje SAFETY (certyfikowane wg IEC 61800-5-2 — SIL3/PLe)

Funkcje Safety są realizowane **sprzętowo** w napędzie (dwa niezależne kanały) i monitorowane przez PROFIsafe lub dedykowane zaciski. Nawet błąd oprogramowania nie może ich obejść.

| Funkcja | Kat. zatrzymania | Co robi | Restart |
|---------|:----------------:|---------|---------|
| **STO** (Safe Torque Off) | 0 | Sprzętowe zablokowanie impulsów PWM → brak momentu → wolny wybieg | Wymaga ACK Safety |
| **SS1** (Safe Stop 1) | 1 | Hamowanie po rampie → po zatrzymaniu aktywacja STO | Wymaga ACK Safety |
| **SS2** (Safe Stop 2) | 2 | Hamowanie po rampie → po zatrzymaniu SOS (Safe Operating Stop — napęd zasilony, trzyma pozycję) | Wymaga ACK Safety |
| **SBC** (Safe Brake Control) | — | Certyfikowane załączenie hamulca mechanicznego (monitoring prądu cewki) | Wymaga ACK Safety |

---

#### Podsumowanie: STO vs OFF — kluczowe różnice

| Cecha | **STO** (Safety) | **OFF1/OFF2/OFF3** (programowe) |
|-------|:----------------:|:-------------------------------:|
| Certyfikacja | SIL3 / PLe | ❌ Brak |
| Realizacja | Sprzętowa — 2 kanały | Programowa |
| Monitoring | PROFIsafe / zaciski HW | Brak |
| Gwarancja braku momentu | ✅ TAK | ❌ NIE |
| Ponowne uruchomienie | ACK Safety | Komenda ON |

---

#### Jak Safe State łączy się z F-DO

Passivation modułu F-DO (substitute value = 0) → wyjście `STO_enable` = 0 → napęd aktywuje **STO**. To jest implementacja Safe State na poziomie obwodu Safety — działa nawet przy awarii komunikacji.

#### Osie pionowe — kiedy STO nie wystarczy

Na osi pionowej (robot, podnośnik, winda) **STO = niebezpieczne**, bo wolny wybieg oznacza niekontrolowany spadek ładunku. Rozwiązania:
- **SS1** (Safe Stop 1) — kontrolowane hamowanie po rampie → STO dopiero po zatrzymaniu
- **SS2** (Safe Stop 2) — hamowanie po rampie → SOS (Safe Operating Stop — napęd zasilony, trzyma pozycję) — gdy oś musi utrzymać pozycję po zatrzymaniu
- **SBC** (Safe Brake Control) — certyfikowane załączenie hamulca mechanicznego przed odcięciem momentu
- Typowo: **SS1 + SBC** łącznie — najpierw hamowanie elektryczne, potem hamulec, potem STO

> ℹ️ **SLS** (Safely Limited Speed), **SDI** (Safe Direction), **SOS** (Safe Operating Stop) — to nie są funkcje zatrzymania, lecz **monitorowania/ograniczania podczas pracy** napędu. Szczegóły → pytanie 8.4.

> 💡 **Na rozmowie:** pytanie „dlaczego STO nie zawsze jest wystarczające jako Safe State?" → odpowiedź: osie pionowe, duże masy inercyjne, procesy wymagające kontrolowanego hamowania.

📚 **Źródła:**
- `docs/chapters/08_napedy_safety.md` — szczegóły STO/SS1/SBC (pytania 8.1–8.4)
- `docs/kb/kb_S08_napedy_safety.md` — STO w V90, podłączenie dwukanałowe
- `archive/slownik_v7.md` — definicje STO/SS1/SS2 z mapowaniem na EN 60204-1
- Normy: IEC 61800-5-2 §6.2 (funkcje Safety napędów), EN 60204-1 §9.2.2 (kategorie zatrzymania 0/1/2)

*[ZWERYFIKOWANE — IEC 61800-5-2 §6.2 (STO/SS1/SBC); EN 60204-1 §9.2.2 (kategorie zatrzymania); `archive/slownik_v7.md`; `docs/kb/kb_S08_napedy_safety.md`]*
### 6.5. Jak konfigurujesz substitute values dla F-DO i jaką wartość wybrać dla zaworu, siłownika i napędu? 🟡
Substitute value to wartość logiczna wyjścia F-DO nadawana automatycznie podczas passivacji lub gdy F-CPU akceptuje błąd bezpieczeństwa. Konfigurowana w TIA Portal → właściwości modułu F-DO → „Substitute value for outputs".
- Domyślnie: 0 (false) dla wszystkich kanałów — to zazwyczaj poprawne
- Zawór bezpieczeństwa (NC — normalnie zamknięty): substitute value = 0 → zawór zamknięty ✓
- Siłownik pneumatyczny: zależy od logiki bezpiecznej pozycji — z reguły 0 = bezpieczna
- Napęd STO: substitute value = 0 → F-DO = 0 → STO_enable usunięty → STO aktywne (brak momentu) ✓
- WYJĄTEK: zawór NO (normalnie otwarty) — substitute value = 0 → zawór OTWARTY (niespójne z intencją)
- Ważna zasada: Zawsze weryfikuj że substitute value 0 odpowiada fizycznie bezpiecznemu stanowi urządzenia

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. substitute value F-DO](https://support.industry.siemens.com/cs/document/109751404/)]*
