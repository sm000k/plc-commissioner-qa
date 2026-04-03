## 20. SCHEMATY ELEKTRYCZNE — CZYTANIE, ANALIZA I PRAKTYKA COMMISSIONING

### 20.1. Co to jest schemat elektryczny i jakie rodzaje schematów spotykasz na obiekcie?

**Schemat elektryczny** to graficzna dokumentacja techniczna przedstawiająca połączenia elektryczne, aparaturę łączeniową i urządzenia w instalacji — bez niego nie uruchomisz, nie zdiagnozujesz i nie naprawisz maszyny.

**Rodzaje schematów w automatyce przemysłowej:**

| Typ schematu | Co pokazuje | Kiedy używasz |
|--------------|-------------|---------------|
| **Schemat ideowy (zasadniczy)** | Logika obwodu — styczniki, zabezpieczenia, styki, cewki. Nie pokazuje fizycznego ułożenia | Analiza działania, programowanie PLC, troubleshooting |
| **Schemat montażowy** | Fizyczne rozmieszczenie aparatów w szafie, numery zacisków, korytka kablowe | Montaż szafy sterowniczej |
| **Schemat połączeń (okablowania)** | Trasa kabli, numery żył, przekroje, oznaczenia | Okablowanie w terenie, podłączanie czujników i napędów |
| **Schemat blokowy** | Uproszczony przegląd — CPU, I/O, napędy, sieci PROFINET | Koncepcja systemu, ofertowanie, przegląd architektury |

**Oznaczenia aparatów wg IEC 81346 (dawniej DIN 40719):**
- `-Q1`, `-Q3`, `-Q4` — wyłączniki, styczniki (np. Q3 = trójkąt, Q4 = gwiazda)
- `-F1`, `-F3` — zabezpieczenia (bezpiecznik, przekaźnik termiczny)
- `-K1`, `-K2` — przekaźniki pomocnicze
- `-M1` — silnik
- `-A1` — sterownik PLC / moduł elektroniczny
- `-S1`, `-S2` — przyciski (STOP, START)

**Czytanie schematu — procedura na obiekcie:**
1. Zacznij od **obwodu mocy** (grube linie): zasilanie → zabezpieczenie (-F) → stycznik (-Q/-K) → silnik (-M)
2. Przejdź do **obwodu sterowania** (cienkie linie): przyciski (-S) → cewki styczników → blokady
3. Sprawdź **referencje krzyżowe**: styk `-KM1` w obwodzie mocy → cewka `-KM1` w obwodzie sterowania (numer strony/wiersza na schemacie)
4. Zweryfikuj **blokady**: wzajemne wykluczenie styczników, kolejność załączania, styki NC

> 💡 **Na obiekcie:** przy przejmowaniu nieznanej maszyny — zawsze zacznij od schematu ideowego obwodu mocy. Zidentyfikuj styczniki, zabezpieczenia, silnik i porównaj z fizyczną szafą. Dopiero potem analizuj logikę sterowania.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, norma IEC 81346 / EN 60204-1*

---

### 20.2. Jak czytasz schemat rozruchu gwiazda-trójkąt (Y/Δ) i jakie elementy musisz na nim zidentyfikować?

**Rozruch Y/Δ** to najczęstszy układ łagodnego rozruchu silnika asynchronicznego w starszych instalacjach. Na schemacie identyfikujesz:

**Obwód mocy — 3 styczniki + zabezpieczenie:**

| Oznaczenie | Element | Rola na schemacie |
|------------|---------|-------------------|
| **KM_L** (K1 / -Q1) | Stycznik liniowy (główny) | Zasila uzwojenia: L1/L2/L3 → U1/V1/W1 |
| **KM_Y** (K2 / -Q4) | Stycznik gwiazdowy | Zwiera końce uzwojeń (U2, V2, W2) = punkt Y |
| **KM_Δ** (K3 / -Q3) | Stycznik trójkątowy | Łączy U2→V1, V2→W1, W2→U1 (pełne napięcie) |
| **-F3** | Przekaźnik termiczny | Między stycznikiem a silnikiem — ochrona przeciążeniowa |

**Sekwencja załączania (widoczna na schemacie sterowania):**
1. START → KM_L + KM_Y zamykają się → silnik rusza w gwieździe (prąd ~1/3 DOL)
2. Timer odmierza 3–10 s → KM_Y otwiera się
3. Przerwa 50–100 ms (rozpad łuku) → KM_Δ zamyka się → pełna prędkość
4. **Blokada:** styk NC KM_Y w obwodzie KM_Δ i vice versa — ZAWSZE obecna

**Co sprawdzasz na schemacie przy commissioning:**
- Czy KM_Y i KM_Δ mają **blokadę mechaniczną** (symbol sprzęgła między stycznikami)
- Czy **przekaźnik termiczny** (-F) jest za stycznikiem głównym, a nie za gwiazdą (błąd montażowy = brak ochrony w Δ)
- Czy silnik ma **6 zacisków** (U1/V1/W1 + U2/V2/W2) — 3-zaciskowy nie nadaje się do Y/Δ
- Czy tabliczka silnika potwierdza napięcie Δ = napięcie sieci (np. 400V/Δ przy sieci 3×400V)

**Schemat obwodu mocy — rozruch gwiazda-trójkąt:**

![Schemat Y/Δ obwód mocy](images/electrical/stern_dreieck_schaltung.png)

*Rys. 20.2a — Obwód mocy Y/Δ: K1 = stycznik sieciowy (Netz), K2 = gwiazdowy (Stern), K3 = trójkątowy (Dreieck), M 3~ = silnik 6-zaciskowy. Źródło: Wikimedia Commons, Public Domain*

**Tabliczka zaciskowa silnika — gwiazda (Y) i trójkąt (Δ):**

![Tabliczka zaciskowa Y/Δ](images/electrical/svorkovnice_star_delta.png)

*Rys. 20.2b — Tabliczka zaciskowa: lewo = Y (mostki pionowe), prawo = Δ (mostki skośne). Źródło: Wikimedia Commons, Public Domain*

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1 §9*

---

### 20.3. Jak czytasz schemat rewersji silnika (zmiana kierunku obrotów) i co MUSISZ sprawdzić?

**Rewersja** = zamiana dwóch faz (np. L1↔L3). Na schemacie widzisz dwa styczniki z krzyżowym połączeniem.

**Identyfikacja na schemacie:**

| Oznaczenie | Element | Schemat połączeń |
|------------|---------|-----------------|
| **KM_F** (KM1) | Stycznik Forward | L1→U, L2→V, L3→W (kolejność prosta) |
| **KM_R** (KM2) | Stycznik Reverse | L3→U, L2→V, L1→W (L1↔L3 zamienione) |

**3 warstwy blokady (ZAWSZE na schemacie):**
1. **Mechaniczna** — symbol sprzęgła między KM_F i KM_R (Siemens: `3RA1934-1A`)
2. **Elektryczna** — styk NC KM_F w obwodzie cewki KM_R i odwrotnie
3. **Programowa (PLC)** — wzajemne wykluczenie w logice

**Czas martwy przy zmianie kierunku** (widoczny jako timer na schemacie sterowania):
- Min. 100–300 ms między wyłączeniem jednego a włączeniem drugiego
- Rozpad łuku + demagnetyzacja uzwojeń

**Co sprawdzasz na schemacie przy commissioning:**
- Czy krzyżowanie faz jest na **schemacie mocy** (nie w sterowniku!)
- Czy **blokada mechaniczna** jest narysowana — sam styk NC NIE wystarczy wg EN 60204-1
- Czy jest **feedback** (styk pomocniczy) do PLC — potwierdzenie prawdziwego stanu stycznika
- Gotowe zestawy Siemens `3RA2` / `3RA1` mają blokadę fabryczną

**Schemat kompletnego układu rewersyjnego:**

![Schemat rewersji](images/electrical/motor_reverse_3phase.jpg)

*Rys. 20.3a — Układ rewersyjny: QS1 = rozłącznik, FU = bezpieczniki, KM1/KM2 = styczniki z krzyżowaniem L1↔L3, blokada elektryczna wzajemna (styki NC). Źródło: Wikimedia Commons, CC BY-SA 3.0*

![Schemat mocy rewersji](images/electrical/demarrage_direct_2sens.png)

*Rys. 20.3b — Obwód mocy rewersji: Q2 = rozłącznik, KM1/KM2, F1 = termiczny, M = silnik. Źródło: Wikimedia Commons, CC BY-SA 3.0*

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1 §9.3*

---

### 20.4. Co to jest układ samopodtrzymania na schemacie i jak go rozpoznajesz?

**Układ samopodtrzymania** (latching / self-holding) to podstawowy obwód sterowania — impuls START uruchamia stycznik, a jego własny styk pomocniczy NO podtrzymuje zasilanie cewki po zwolnieniu przycisku.

**Schemat klasyczny — jak go czytasz:**

```
L (24V) ─── [S1 STOP NC] ─┬─ [S2 START NO] ─── [Cewka KM]
                           └─ [KM styk NO] ──┘
N (0V) ──────────────────────────────────────────────────
```

**Identyfikacja na schemacie:**
- **S1 (STOP)** = styk NC — normalnie zamknięty, przerywa obwód po naciśnięciu
- **S2 (START)** = styk NO — normalnie otwarty, zamyka obwód na chwilę
- **KM (styk pomocniczy NO)** = równolegle do S2 — to on „trzyma" po zwolnieniu START
- **Cewka KM** = symbol prostokąta z oznaczeniem na końcu obwodu

**Dlaczego STOP jest NC (normalnie zamknięty):**
- EN 60204-1 + EN ISO 13849-1: stan bezpieczny = brak sygnału
- Zerwanie przewodu do STOP → obwód otwarty → maszyna staje (fail-safe)
- Na schemacie: STOP ZAWSZE jest pierwszy w łańcuchu (przed START)

**Realizacja w PLC (LAD):**
```
|  I0.0    I0.1         Q0.0  |
|--[START]--+--[STOP NC]--(KM)|
|  Q0.0     |                 |
|--[KM]-----+                 |
```

**Co sprawdzasz:**
- Czy STOP jest NC i jest PRZED START w obwodzie
- Czy styk samopodtrzymania jest równoległy do START (nie szeregowy)
- Czy jest tylko JEDEN styk samopodtrzymania (dwa = pułapka logiczna)

![Układ samopodtrzymania z timerem](images/electrical/delta_star_switching.jpg)

*Rys. 20.4 — Obwód sterowania z samopodtrzymaniem: S1=STOP NC, S2=START NO, K1=stycznik z samopodtrzymaniem, K2=timer. Źródło: Wikimedia Commons, CC BY-SA 3.0*

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1*

---

### 20.5. Jak czytasz schemat Dahlandera (silnik dwubiegowy) i czym różni się od Y/Δ na schemacie?

**Silnik Dahlander** = 2 prędkości (stosunek 1:2) przez zmianę konfiguracji uzwojeń. Na schemacie wygląda podobnie do Y/Δ, ale logika jest inna.

**Kluczowa różnica Y/Δ vs Dahlander:**

| Cecha | Rozruch Y/Δ | Dahlander |
|-------|-------------|-----------|
| Cel | Łagodny rozruch → pełna prędkość | Dwie prędkości robocze |
| Styczniki | 3 (liniowy + Y + Δ) — sekwencja | 3 (główny + wolny + szybki) — wybór |
| Timer | Tak (przełączenie po rozruchu) | Nie (operator wybiera prędkość) |
| Silnik | 6 zacisków, jedna prędkość | 6 zacisków, dwie prędkości |

**Identyfikacja na schemacie Dahlandera (3 styczniki):**

| Oznaczenie | Funkcja | Połączenie |
|------------|---------|------------|
| **KM1** | Główny (zawsze zamknięty) | L1/L2/L3 → silnik |
| **KM2** | Wolna (Δ) | Zasila U1/V1/W1, U2/V2/W2 otwarte |
| **KM3** | Szybka (YY) | Zasila U2/V2/W2, zwiera U1/V1/W1 |

**Co sprawdzasz na schemacie:**
- Blokada między KM2 i KM3 (jak w rewersji — mechaniczna + elektryczna)
- Osobny przekaźnik termiczny dla każdej prędkości (różne prądy znamionowe)
- Przerwa 50–100 ms przy zmianie biegu (timer na schemacie sterowania)

**Schemat Dahlander z wentylacją:**

![Schemat Dahlander](images/electrical/dahlander_ventilation.jpg)

*Rys. 20.5a — Schemat mocy Dahlander Y/YY z wentylacją. Źródło: Wikimedia Commons, CC BY-SA 4.0*

![Dahlander Δ/YY](images/electrical/dahlander_TDD.jpg)

*Rys. 20.5b — Połączenia uzwojeń Δ/YY. Źródło: Wikimedia Commons, CC BY-SA 4.0*

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60034-8*

---

### 20.6. Jak wygląda na schemacie blokada elektryczna i mechaniczna między stycznikami i po co ją sprawdzasz?

**Blokada wzajemna** to zabezpieczenie przed jednoczesnym zadziałaniem dwóch wykluczających się styczników — jej brak = zwarcie lub uszkodzenie silnika.

**Jak rozpoznajesz na schemacie:**

**1. Blokada elektryczna:**
- Styk NC jednego stycznika w obwodzie cewki drugiego
- Na schemacie: w linii cewki KM_R widzisz styk opisany KM_F (NC) — i odwrotnie

```
Obwód cewki KM_F:  ──[S1 START_F]──[NC KM_R]──(Cewka KM_F)
Obwód cewki KM_R:  ──[S2 START_R]──[NC KM_F]──(Cewka KM_R)
```

**2. Blokada mechaniczna:**
- Symbol sprzęgła/dźwigni między dwoma stycznikami (przerywana linia łącząca)
- Siemens: `3RA1934-1A` (dla 3RT1), `3RA1944-2A` (dla 3RT2)
- Na schemacie montażowym: blok mechaniczny między obudowami

**3. Blokada programowa (PLC):**
- Wzajemne wykluczenie w kodzie — ale NIGDY jako jedyna warstwa

**Gdzie blokada jest obowiązkowa:**
- Rewersja silnika (KM_F / KM_R)
- Rozruch Y/Δ (KM_Y / KM_Δ)
- Przełączanie źródeł zasilania (sieć / agregat)
- Dowolne dwa styczniki, których jednoczesne załączenie powoduje zwarcie

**Co sprawdzasz na obiekcie:**
1. Otwórz szafę — czy fizycznie widzisz moduł blokady między stycznikami?
2. Schemat: czy styki NC są narysowane w obu obwodach (wzajemnie)?
3. PLC: czy program ma wykluczenie + czy jest timer martwej strefy?

> ⚠️ Przy audycie Safety: sam schemat elektryczny nie wystarczy — sprawdź fizycznie czy moduł mechaniczny jest zamontowany. EN 60204-1 §9 wymaga blokady sprzętowej.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1 §9.3, IEC 60947-4-1*

---

### 20.7. Jak wygląda schemat rozruchu Y/Δ sterowanego przez PLC i jak go programujesz w TIA Portal?

**Kompletny schemat Y/Δ z PLC — mapowanie I/O:**

**Wyjścia PLC → styczniki:**

| Wyjście | Element | Opis |
|---------|---------|------|
| Q0.0 | KM_L (liniowy) | Zasila U1/V1/W1 |
| Q0.1 | KM_Y (gwiazda) | Zwiera U2/V2/W2 |
| Q0.2 | KM_Δ (trójkąt) | Łączy skrzyżowanie U2→V1, V2→W1, W2→U1 |

**Wejścia PLC ← sprzężenia zwrotne:**

| Wejście | Sygnał | Po co |
|---------|--------|-------|
| I0.0 | START (NO) | Impuls rozruchu |
| I0.1 | STOP (NC) | Zatrzymanie — fail-safe |
| I0.2 | FB_KM_L | Potwierdzenie załączenia stycznika głównego |
| I0.3 | FB_KM_Y | Potwierdzenie gwiazdy |
| I0.4 | FB_KM_Δ | Potwierdzenie trójkąta |
| I0.5 | THERMAL_FAULT (NC) | Przekaźnik termiczny — 0 = wyzwolony |

**Program SCL w TIA Portal (maszyna stanów):**

```scl
CASE YD_State OF
    0: // STOP
        KM_L := FALSE; KM_Y := FALSE; KM_D := FALSE;
        IF Start AND NOT Fault_Thermal THEN
            KM_L := TRUE; KM_Y := TRUE;
            Timer_YD(IN:=TRUE, PT:=T#6S);
            YD_State := 1;
        END_IF;

    1: // GWIAZDA
        IF Timer_YD.Q THEN
            KM_Y := FALSE;
            Timer_Gap(IN:=TRUE, PT:=T#100MS);
            YD_State := 2;
        END_IF;

    2: // PRZERWA (gap Y→Δ)
        IF Timer_Gap.Q THEN
            KM_D := TRUE;
            YD_State := 3;
        END_IF;

    3: // TRÓJKĄT — praca nominalna
        IF NOT Stop OR Fault_Thermal THEN
            KM_L := FALSE; KM_D := FALSE;
            YD_State := 0;
        END_IF;
END_CASE;

// Blokada programowa — nigdy jednocześnie
IF KM_Y THEN KM_D := FALSE; END_IF;
IF KM_D THEN KM_Y := FALSE; END_IF;
```

**Diagnostyka typowych problemów:**

| Objaw | Co sprawdzasz na schemacie/PLC |
|-------|-------------------------------|
| Silnik nie startuje | FB_KM_L = 0? → sprawdź bezpiecznik, termiczny |
| Wyłączenie przy Y→Δ | Timer_Gap za krótki → wydłuż do 150–200 ms |
| Nie przyspiesza w Y | Timer_YD za krótki → wydłuż do 5–8 s |
| Termiczny wyzwala po starcie | I_set za nisko lub klasa 10 zamiast 20 |
| KM_Y i KM_Δ jednocześnie | Brak blokady mechanicznej → zamontuj 3RA1934-1A |

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1*

---

### 20.8. Jak na schemacie rozpoznajesz obwód bezpieczeństwa (Safety) i czym różni się od standardowego obwodu sterowania?

**Obwód Safety** na schemacie jest wyraźnie oddzielony od standardowego sterowania — rozpoznajesz go po:

**Oznakowanie na schemacie:**
- Linia przerywana lub kolorowe obramowanie wydzielające strefę Safety
- Symbole z oznaczeniem „F-" (F-DI, F-DO, F-CPU)
- Dwukanałowe podłączenie czujników (dwie linie do jednego elementu)
- Oznaczenie PL/SIL przy elementach (np. „SIL 3", „PL e")

**Typowe elementy Safety na schemacie:**

| Element | Oznaczenie | Jak wygląda na schemacie |
|---------|------------|--------------------------|
| E-Stop | -S_ES / -SB1 | Przycisk z symbolem grzyba + dwukanałowe NC |
| Kurtyna | -B1 / AOPD | Blok z OSSD1/OSSD2 (dwa wyjścia) |
| Elektrorygiel | -S_LOCK | Styk NC + cewka ryglowania |
| F-DI | -A_FDI | Moduł z kanałami Ch0/Ch1 (dwukanałowe) |
| F-DO | -A_FDO | Moduł z wyjściami + PP/PM switching |
| Przekaźnik Safety | -K_SF | Podwójny styk (kanał 1 + kanał 2) |

**Kluczowe różnice od standardowego obwodu:**

| Cecha | Standard | Safety |
|-------|----------|--------|
| Okablowanie czujnika | 1 przewód → 1 wejście | 2 kanały → 2 wejścia (1oo2) |
| Sygnał STOP/E-Stop | NC (1 styk) | NC dwukanałowy (2 styki rozdzielone fizycznie) |
| Feedback stycznika | Opcjonalny | Obowiązkowy (EDM — External Device Monitoring) |
| Zasilanie czujników | Wspólne | Rozdzielone T1/T2 (test pulses) z F-DI |

**Co sprawdzasz na obiekcie:**
1. Dwukanałowość: na schemacie dwa osobne przewody od e-stop do F-DI (nie wspólny!)
2. Feedback: styk NO stycznika wraca do F-DI jako potwierdzenie otwarcia
3. Separacja tras kablowych: kanał 1 i kanał 2 prowadzone osobno (nie w jednym kablu)
4. Oznaczenia: numery F-address na schemacie muszą zgadzać się z konfiguracją TIA Portal

> 💡 **Schemat Safety jest dowodem** — audytor TÜV/UDT porównuje schemat z fizycznym okablowaniem i konfiguracją TIA Portal. Niezgodność = blokada odbioru maszyny.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej, EN 60204-1, IEC 62061*