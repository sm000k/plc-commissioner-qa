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
STO (Safe Torque Off) jako Safe State napędu oznacza zablokowanie impulsów bramkowania tranzystorów — napęd nie może generować momentu obrotowego, nawet przy zasilaniu energetycznym. Zatrzymanie OFF1/OFF2 to kontrolowane wyhamowanie przez falownik z możliwością ponownego załączenia bez potwierdzenia.
- STO: brak momentu → wolne wybieganie jeśli nie ma hamulca mechanicznego (niebezpieczne na siłowniku pionowym!)
- OFF1: hamowanie po rampie (p1121 ⚠️ DO WERYFIKACJI w dokumentacji SINAMICS), potem wyłączenie impulsów — napęd można ponownie uruchomić sygnałem ON
- OFF2: natychmiastowe wyłączenie impulsów (jak STO, ale sterowane programem, nie Safety)
- Safe State = STO → w konfiguracji F-DO parametr „substitute value" = 0 dla wyjścia STO
- Dla osi pionowych (roboty, podnośniki): jako Safe State użyj SS1 (Stop + STO po rampie) lub SBC

*[ZWERYFIKOWANE - IEC 61800-5-2 §6.2 (STO/SS1/SBC — Safe Torque Off jako Safe State); [SINAMICS Safety Integrated product page](https://www.siemens.com/global/en/products/drives/sinamics/safety-integrated.html)]*
### 6.5. Jak konfigurujesz substitute values dla F-DO i jaką wartość wybrać dla zaworu, siłownika i napędu? 🟡
Substitute value to wartość logiczna wyjścia F-DO nadawana automatycznie podczas passivacji lub gdy F-CPU akceptuje błąd bezpieczeństwa. Konfigurowana w TIA Portal → właściwości modułu F-DO → „Substitute value for outputs".
- Domyślnie: 0 (false) dla wszystkich kanałów — to zazwyczaj poprawne
- Zawór bezpieczeństwa (NC — normalnie zamknięty): substitute value = 0 → zawór zamknięty ✓
- Siłownik pneumatyczny: zależy od logiki bezpiecznej pozycji — z reguły 0 = bezpieczna
- Napęd STO: substitute value = 0 → F-DO = 0 → STO_enable usunięty → STO aktywne (brak momentu) ✓
- WYJĄTEK: zawór NO (normalnie otwarty) — substitute value = 0 → zawór OTWARTY (niespójne z intencją)
- Ważna zasada: Zawsze weryfikuj że substitute value 0 odpowiada fizycznie bezpiecznemu stanowi urządzenia

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. substitute value F-DO](https://support.industry.siemens.com/cs/document/109751404/)]*
