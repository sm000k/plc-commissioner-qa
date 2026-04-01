## 20. SCHEMATY ELEKTRYCZNE — SILNIKI I APARATURA ŁĄCZENIOWA

### 20.1. Co to jest silnik Dahlander (6 wyprowadzeń) i jak uzyskuje się dwa zakresy prędkości?

**Silnik Dahlander** (pol. *silnik z przełączaniem biegunów*) to trójfazowy silnik asynchroniczny z 6 wyprowadzeniami (U1, V1, W1 — niskiej prędkości; U2, V2, W2 — wysokiej prędkości), który dzięki zmianie połączenia uzwojeń uzyskuje dwie synchroniczne prędkości w stosunku **1:2**.

**Zasada działania:**
- Zmiana połączenia uzwojeń = zmiana liczby par biegunów (p) → zmiana prędkości synchronicznej: `n = 60·f / p`
- Stosunek prędkości zawsze **dokładnie 1:2** (np. 750/1500 rpm, 1000/2000 rpm przy 50 Hz)

**Połączenia uzwojeń:**

| Prędkość | Konfiguracja uzwojenia | Zasilanie | Zwarte wyprowadzenia |
|----------|------------------------|-----------|----------------------|
| Niska (więcej biegunów) | Trójkąt (Δ) | U1, V1, W1 | U2, V2, W2 — otwarte |
| Wysoka (mniej biegunów) | Podwójna gwiazda (YY) | U2, V2, W2 | U1, V1, W1 — zwarte razem |

**Schemat aparatury (3 styczniki):**
- **KM1** — główny (zawsze zamknięty gdy silnik pracuje)
- **KM2** — niskiej prędkości (Δ: zasila U1/V1/W1, U2/V2/W2 otwarte)
- **KM3** — wysokiej prędkości (YY: zasila U2/V2/W2, zwiera U1/V1/W1)
- **Blokada:** KM2 i KM3 MUSZĄ być wzajemnie blokowane (el. + mech.) — jednoczesne zadziałanie = zwarcie

**Sterowanie z PLC:**
```
Q0.0 = KM1 (główny)
Q0.1 = KM2 (niska prędkość)   -- wyklucza Q0.2
Q0.2 = KM3 (wysoka prędkość)  -- wyklucza Q0.1
```
- Przy zmianie z niskiej na wysoką: przerwa min. 50–100 ms (rozpad łuku na KM2 zanim zamknie KM3)
- Zabezpieczenie: dla każdej prędkości osobny przekaźnik termiczny (różne prądy znamionowe przy Δ i YY)

> ⚠️ **Moment przy zmianie biegów:** przejście Δ→YY powoduje chwilowy skok prądu — nie zmieniaj biegu pod obciążeniem zderzakowym. W razie potrzeby stosuj łagodny rozruch (soft-starter) lub przemiennik częstotliwości.

**Schemat połączeń uzwojeń Dahlander — konfiguracja Δ/YY (szybka/wolna prędkość):**

![Schemat Dahlander Δ/YY](images/electrical/dahlander_TDD.jpg)

*Rys. 20.1a — Połączenie uzwojeń silnika Dahlander: trójkąt (marcha rápida) i gwiazda-gwiazda (marcha lenta). Źródło: Wikimedia Commons, CC BY-SA 4.0*

**Schemat połączeń uzwojeń Dahlander — konfiguracja Y/YY:**

![Schemat Dahlander Y/YY](images/electrical/dahlander_DetaDeta.jpg)

*Rys. 20.1b — Połączenie uzwojeń silnika Dahlander: gwiazda/gwiazda-gwiazda. Źródło: Wikimedia Commons, CC BY-SA 4.0*

**Kompletny schemat sterowania silnikiem Dahlander z wentylacją:**

![Schemat sterowania Dahlander](images/electrical/dahlander_ventilation.jpg)

*Rys. 20.1c — Profesjonalny schemat obwodu mocy silnika Dahlander z wentylacją Y/YY — styczniki, przekaźniki termiczne, tabliczka zaciskowa. Źródło: Wikimedia Commons, CC BY-SA 4.0*

*Źródło: EN 60034-8, praktyka rozdzielnica automatyki przemysłowej*

---

### 20.2. Jak działa rozruch gwiazda-trójkąt (Y/Δ) i kiedy go stosujemy?

**Rozruch Y/Δ** to metoda łagodnego rozruchu silnika asynchronicznego, polegająca na etapowym przełączeniu uzwojeń: najpierw w gwiazdę (Y — niższe napięcie na uzwojeniu), potem w trójkąt (Δ — pełne napięcie).

**Parametry elektryczne:**

| Parametr | Bezpośredni (DOL) | Gwiazda (Y) | Trójkąt (Δ) |
|----------|-------------------|-------------|-------------|
| Napięcie na uzwojeniu | U_line | U_line / √3 ≈ 58% U_n | U_line = 100% U_n |
| Prąd rozruchowy sieciowy | ~6–8× I_n | ~2–2.7× I_n (1/3 DOL) | ~6–8× I_n |
| Moment rozruchowy | ~100% | ~33% | ~100% |

> ⚠️ **Moment = 1/3 przy starcie w Y:** silnik NIE nadaje się do rozruchu pod pełnym obciążeniem — stosuj tylko przy lekkim obciążeniu startowym (wentylatory, pompy odśrodkowe, sprężarki bez obciążenia startowego).

**Aparatura (3 elementy aparatury):**
- **KM_L** — główny liniowy (zasilanie L1/L2/L3 → U1/V1/W1 silnika)
- **KM_Y** — gwiazda (zwiera U2/V2/W2 = punkt gwiazdowy; uzwojenia w Y)
- **KM_Δ** — trójkąt (łączy U2→V1, V2→W1, W2→U1 = uzwojenia w Δ)
- **Blokada:** KM_Y i KM_Δ MUSZĄ być blokowane wzajemnie elektrycznie i mechanicznie

**Sekwencja rozruchu:**
1. PLC zamknij **KM_L** (główny)
2. PLC zamknij **KM_Y** (gwiazda) → silnik rusza z ~33% momentu, prąd ~2–3× I_n
3. Poczekaj na timer T1 (typowo 3–10 s, aż silnik osiągnie ~70–80% prędkości docelowej)
4. PLC otwórz **KM_Y** → odczekaj 50–100 ms (czas zaniku łuku)
5. PLC zamknij **KM_Δ** (trójkąt) → silnik na pełnej prędkości
6. Skok prądu przy przełączeniu: krótkotrwały ~4–6× I_n — niemalże jak DOL — to **chwilowe uderzenie prądowe** przy przejściu Y→Δ

**Warunki stosowania:**
- Silnik 6-wyprowadzeniowy (U1, V1, W1, U2, V2, W2)
- Napięcie znamionowe silnika = napięcie sieci (np. 400 V / Δ przy sieci 3×400 V)
- Obciążenie nie wymaga pełnego momentu rozruchowego

**Kiedy NIE stosować Y/Δ:**
- Duże obciążenie przy starcie (np. przenośniki taśmowe z ładunkiem) → stosuj soft-starter lub VFD
- Silnik 3-wyprowadzeniowy (tylko Δ lub tylko Y z fabryki) — brak możliwości przełączenia

**Schemat obwodu mocy — rozruch gwiazda-trójkąt:**

![Schemat Y/Δ obwód mocy](images/electrical/stern_dreieck_schaltung.png)

*Rys. 20.2a — Obwód mocy rozruchu Y/Δ: K1 = stycznik sieciowy (Netz), K2 = stycznik gwiazdowy (Stern), K3 = stycznik trójkątowy (Dreieck), M 3~ = silnik trójfazowy z 6 zaciskami (U1/V1/W1, U2/V2/W2). Źródło: Wikimedia Commons, Public Domain*

**Tabliczka zaciskowa silnika — połączenie gwiazda (Y) i trójkąt (Δ):**

![Tabliczka zaciskowa Y i Δ](images/electrical/svorkovnice_star_delta.png)

*Rys. 20.2b — Tabliczka zaciskowa silnika asynchronicznego: po lewej połączenie w gwiazdę (Y), po prawej w trójkąt (Δ). Źródło: Wikimedia Commons, Public Domain*

*Źródło: EN 60204-1 §9, praktyka szafy rozdzielniczej automotive*

---

### 20.3. Jak realizuje się zmianę kierunku obrotów silnika asynchronicznego?

**Zmiana kierunku** silnika trójfazowego to zamiana kolejności faz — wystarczy zamienić dowolne dwie fazy (np. L1↔L3, L2 pozostaje). Realizuje się to dwoma blokami stykowymi (stycznikami KM_F i KM_R) z rygorystyczną blokadą.

**Zasada:**

| Styk czynny | Fazy na silniku | Kierunek |
|-------------|-----------------|----------|
| KM_F (Forward/Prawy) | L1 → U, L2 → V, L3 → W | Prawoskrętny |
| KM_R (Reverse/Lewy) | L3 → U, L2 → V, L1 → W | Lewoskrętny |

*(Zamiana L1↔L3, L2 pozostaje — wynik: odwrócona kolejność faz)*

**Schemat aparatury:**

```
L1 ─┬── KM_F_styk ─┐
L2 ──────────────── Silnik (U, V, W)
L3 ─┴── KM_R_styk ─┘   (krzyżowe połączenie L1/L3 w KM_R)
```

**Trójstopniowa blokada (OBOWIĄZKOWA):**

1. **Blokada mechaniczna** — blokada mechaniczna Siemens `3RT1946-2G` montowana między dwoma zestawami stykowymi (fizycznie uniemożliwia jednoczesne zadziałanie)
2. **Blokada elektryczna** — styk NC (normalnie zamknięty) KM_F w obwodzie cewki KM_R i vice versa
3. **Blokada programowa (PLC)** — wzajemne wykluczenie w logice programu, np.:
   ```
   // SCL Siemens TIA Portal
   IF Forward AND NOT Reverse_FB THEN
       KM_F := TRUE;
       KM_R := FALSE;
   ELSIF Reverse AND NOT Forward_FB THEN
       KM_R := TRUE;
       KM_F := FALSE;
   END_IF;
   ```

**Czas martwy przy zmianie kierunku:**
- Min. 100–300 ms między wyłączeniem jednego a włączeniem drugiego stycznika
- Konieczny ze względu na rozpad łuku elektrycznego na styling i demagnetyzację uzwojeń silnika
- Przy PLC: zrealizuj timerem (TOF lub TON)

> ⚠️ **Zmiana pod napięciem:** zmiana kierunku gdy silnik kręci się z pełną prędkością = silny szok mechaniczny + prąd udarowy do 10× I_n. Zawsze zastosuj logikę: STOP → czekaj aż silnik się zatrzyma → START w przeciwnym kierunku (lub hamowanie dynamiczne).

> 💡 **Gotowe zestawy odwracające:** Siemens oferuje zestawy `3RA2` i `3RA1` z fabryczną blokadą mechaniczną — szybszy montaż i certyfikowana blokada.

**Schemat kompletnego układu rewersyjnego silnika trójfazowego:**

![Schemat rewersji silnika 3-fazowego](images/electrical/motor_reverse_3phase.jpg)

*Rys. 20.3a — Kompletny układ odwracania kierunku obrotów: QS1 = rozłącznik, FU1-3 = bezpieczniki, KM1/KM2 = styczniki z krzyżowym połączeniem faz (L1↔L3), PTT1 = termistor, SB1/SB2 = przyciski START, SB3 = STOP, styki NC KM1 i KM2 = blokada elektryczna wzajemna. Źródło: Wikimedia Commons, CC BY-SA 3.0*

**Uproszczony schemat mocy — rozruch bezpośredni dwukierunkowy:**

![Schemat mocy rewersji](images/electrical/demarrage_direct_2sens.png)

*Rys. 20.3b — Obwód mocy rewersji: Q2 = rozłącznik, KM1/KM2 = styczniki kierunkowe, F1 = przekaźnik termiczny, M = silnik. Źródło: Wikimedia Commons, CC BY-SA 3.0*

*Źródło: EN 60204-1, katalog Siemens SIRIUS aparatura łączeniowa*

---

### 20.4. Czym jest przekaźnik termiczny (bimetalowy) i jak go dobierasz do silnika?

**Przekaźnik termiczny** (termobimetalowy) to element zabezpieczający silnik przed przeciążeniem przez detekcję nadmiernego prądu — bimetale nagrzewają się proporcjonalnie do r.m.s. prądu i otwierają styk wyzwalający po osiągnięciu temperatury progowej.

**Zasada:**
- Bimetal = dwie warstwy metalu o różnym współczynniku rozszerzalności → ugięcie przy nagrzaniu
- Symuluje nagrzewanie silnika (model termiczny) — zabezpiecza przed długotrwałym przeciążeniem
- **NIE** chroni przed zwarciem (to zadanie bezpiecznika lub WS/wyłącznik silnikowy)

**Dobór przekaźnika termicznego:**

| Parametr | Wartość |
|----------|---------|
| Prąd nastawiania | I_set = I_n silnika (wartość z tabliczki znamionowej) |
| Zakres nastawy | Wybierz model o zakresie obejmującym I_n |
| Klasa wyzwalania | Class 10 (standard), Class 20 (ciężki rozruch), Class 30 (bardzo ciężki) |
| Typ | 1-fazowy (brak symetrii faz), 3-fazowy (asymetria faz, utrata fazy) |

**Siemens SIRIUS — wybór modelu:**
- `3RU2` — elektroniczny przekaźnik przeciążeniowy (dokładniejszy, klasy 5/10/20/30 przestawiane)
- `3RB3` — elektroniczny z czujnikiem termistorowym PTC (bezpośredni pomiar temperatury uzwojenia)
- `3RT` + `3RU2` jako zestaw (bezpośredni styk pomocniczy, mechaniczna blokada)

**Sygnały z przekaźnika do PLC:**
- Styk NC → obwód sterowania cewki KM (otwarcie = wyłączenie silnika)
- Styk NO → wejście PLC jako sygnał alarmu: `"TermalTrip"` → diagnostyka HMI

> ⚠️ **Reset po zadziałaniu:** po wyzwoleniu przekaźnik NIE resetuje się automatycznie — wymagany czas ostygnięcia (zwykle 3–5 min) + ręczny reset przyciskiem. Siemens 3RU2 ma tryb auto-reset (niezalecany = może uruchomić silnik bez wiedzy operatora).

*Źródło: Siemens Industry Catalog — SIRIUS Motor Starters 3RT/3RU, EN 60947-4-1*

---

### 20.5. Co to jest aparat różnicowoprądowy (RCD/RCCB) i czym różni się od bezpiecznika nadprądowego?

**Aparat różnicowoprądowy** (RCD — Residual Current Device, pol. *wyłącznik różnicowoprądowy*) to urządzenie ochronne wykrywające upływ prądu do ziemi przez porównanie sumy prądów w przewodach fazowych i zerowym.

**Zasada działania:**
- Wszystkie przewody (L1, L2, L3, N) przechodzą przez wspólny przekładnik prądowy (toroid)
- W stanie normalnym: ΣI = 0 (prąd wychodzący = powracający)
- Przy upływności: ΣI ≠ 0 → napięcie na cewce → wyzwolenie w ciągu <40 ms

**Wartości wrażliwości (czułości):**

| Prąd wyzwalający | Zastosowanie |
|-----------------|--------------|
| 10 mA | Ochrona osób w miejscach szczególnie niebezpiecznych (baseny, medycyna) |
| 30 mA | Ochrona przeciwporażeniowa (standard w instalacjach ogólnych, EN 60364) |
| 100 mA | Ochrona pożarowa urządzeń |
| 300 mA / 500 mA | Ochrona pożarowa obwodów zbiorczych |

**Typy RCD — kluczowe dla automatyki:**

| Typ | Wykrywany prąd upływu | Zastosowanie |
|-----|----------------------|--------------|
| Typ AC | Tylko sinusoidalny przemienny | Klasyczne obciążenia rezystancyjne/indukcyjne |
| Typ A | AC + pulsujący DC | Silniki z tyrystorami (falowniki 1-fazowe) |
| Typ B | AC + pulsujący DC + gładki DC | **Przemienniki częstotliwości VFD, UPS, ładowarki EV** |
| Typ F | Jak A + wysokoczęstotliwościowy | Falowniki z filtrem EMC |

> ⚠️ **RCD + VFD:** przemiennik częstotliwości generuje prądy upływu pojemnościowe (filtr EMC, kable ekranowane) → mogą wyzwalać RCD 30 mA bez powodu. Rozwiązania: (1) użyj RCD typ B 300 mA jako pożarowy, (2) zastosuj RCD selektywny (opóźniony), (3) RCD dedykowany do VFD (np. Siemens 5SV — Enhanced protection).

**RCD vs bezpiecznik/MCB:**

| Cecha | RCD (różnicowoprądowy) | MCB (nadprądowy) / bezpiecznik |
|-------|------------------------|-------------------------------|
| Czego broni | Upływu do ziemi (porażenie, pożar) | Przed przeciążeniem i zwarciem |
| Zasada | Pomiar różnicy prądów | Bimetale + wyzwalacz elektromagnetyczny |
| Prądy robocze | Nie ogranicza obciążenia | Odcina powyżej I_n |
| Stosowanie | Zawsze z MCB/bezpiecznikiem | Może pracować samodzielnie |

> 💡 **RCBO = RCD + MCB w jednym urządzeniu** — oszczędność miejsca w rozdzielnicy, jedno urządzenie łączy obie funkcje.

*Źródło: EN 60364-4-41 (ochrona przed porażeniem), EN 61008, katalog Siemens SENTRON*

---

### 20.6. Na czym polega blokada elektryczna i mechaniczna między dwoma stycznikami?

**Blokada wzajemna** (interlocking) to układ zabezpieczający przed jednoczesnym zadziałaniem dwóch styków wzajemnie wykluczających się — konieczna wszędzie tam, gdzie jednoczesne zadziałanie grozi zwarciem (Y/Δ, rewersja, przełączanie źródeł zasilania).

**Rodzaje blokad:**

**1. Blokada elektryczna (electrical interlock):**
- Styk NC (normalnie zamknięty) jednego stycznika wstawiony szeregowo do obwodu cewki drugiego
- Gdy KM_A jest pod napięciem → jego NC styk w obwodzie KM_B otwiera się → KM_B nie może zadziałać

```
Obwód KM_A:  [START_A] NC(KM_B) [Cewka KM_A]
Obwód KM_B:  [START_B] NC(KM_A) [Cewka KM_B]
```

**2. Blokada mechaniczna (mechanical interlock):**
- Fizyczna belka sprzęgająca dwie obudowy styków (montaż między nimi)
- Gdy jeden jest zamknięty, mechaniczna dźwignia fizycznie blokuje zadziałanie drugiego
- Siemens: moduły `3RA1934-1A` (dla 3RT1) lub `3RA1944-2A` (dla 3RT2)
- Nie zależy od obwodu elektrycznego — chroni nawet przy awarii sterowania

**3. Blokada programowa (software interlock):**
- Wzajemne wykluczenie bitów wyjściowych w programie PLC
- Najlepsza dla skrótu typowych błędów, ale tylko jako warstwa trzecia
- Sama w sobie NIEDOSTATECZNA — błąd w programie lub awaria CPU może ją ominąć

**Dlaczego wszystkie trzy warstwy?**
- EN 60204-1 §9 wymaga, aby blokada funkcji wzajemnie wykluczających była zrealizowana sprzętowo
- IEC 60947-4-1 — wymagania dla układów rewersyjnych

> ⚠️ **Kolejność hierarchii:** blokada mechaniczna > elektryczna > programowa. Przy audycie bezpieczeństwa sprawdzaj fizycznie, czy moduł mechaniczny jest zamontowany — sam schemat elektryczny nie wystarczy.

*Źródło: EN 60204-1 §9.3, Siemens Catalog SIRIUS D*

---

### 20.7. Czym różni się wyłącznik silnikowy (3RV) od bezpiecznika wkładkowego (wkładka topikowa)?

**Wyłącznik silnikowy** (Motor Circuit Breaker — MCB/MP, Siemens seria `3RV2`) to wielofunkcyjny wyłącznik chroniący silnik zarówno przed przeciążeniem jak i zwarciem, z możliwością wielokrotnego użycia.

**Porównanie:**

| Cecha | Wyłącznik silnikowy (3RV2) | Bezpiecznik wkładkowy (topikowy) |
|-------|---------------------------|----------------------------------|
| Zasada działania | Bimetal (przeciążenie) + elektromagnes (zwarcie) | Topliwy drucik/wkładka |
| Ponowne użycie | Tak — reset przyciskiem | Nie — wymiana wkładki po zadziałaniu |
| Nastawianie I | Tak — pokrętło I_set | Nie — stała klasa (gG, aM) |
| Sygnalizacja | Styk pomocniczy (NO/NC) do PLC | Brak (lub sygnalizator topikowy) |
| Ochrona przed utratą fazy | Tak (3-fazowy termobimetal) | Tak (osobna wkładka na fazę) |
| Montaż | Na szynie DIN, łączy się z KM | Na szynie DIN lub w listwach |
| Zastosowanie | Silniki do ~45 kW (3RV2) | Duże silniki, obwody główne |

**Klasy bezpieczników:**
- **gG** — ogólne przeznaczenie (ochrona przewodów i ogólnych odbiorników) — wolne topienie
- **aM** — motorowe (ochrona uzwojeń silnika) — szybkie przy zwarciu, toleruje prąd rozruchowy

**Dobór wyłącznika silnikowego 3RV2:**
- Nastaw `I_set` na I_n silnika z tabliczki znamionowej
- Klasa wyzwalania: 10 (standard) lub 20 (dla silników z ciężkim rozruchem Y/Δ)
- Sprawdź zdolność łączeniową (Ics) ≥ prąd zwarcia w punkcie instalacji

> 💡 **Siemens 3RV2 + 3RT2 = zestaw:** wyłącznik silnikowy + stycznik montowane razem na szynie DIN, łączą się łącznikiem mechanicznym bez dodatkowych przewodów — standardowe rozwiązanie w szafach automatyki.

*Źródło: Siemens Catalog SIRIUS D, EN 60947-2, IEC 60947-4-1*

---

### 20.8. Co to jest układ samopodtrzymania w schemacie elektrycznym i jak go realizujesz?

**Układ samopodtrzymania** (ang. *latching circuit / self-holding circuit*) to obwód sterowania, w którym krótki impuls przycisku START uruchamia odbiornik, a styk pomocniczy NO stycznika podtrzymuje jego własny obwód zasilania po zwolnieniu przycisku.

**Schemat klasyczny (obwód sterowniczy 230 VAC / 24 VDC):**

```
L (24V) ─── [STOP NC] ─┬─ [START NO] ─── [Cewka KM]
                        └─ [KM styk NO] ─┘
N (0V) ─────────────────────────────────────────────
```

**Działanie:**
1. `STOP` NC — normalnie zamknięty → prąd może płynąć
2. Naciśnij `START` NO → zamknięcie → prąd przez cewkę KM → KM zastyga (zamknięcie styku głównego + pomocniczego)
3. Zwolnij `START` → styk pomocniczy NO (KM) przejął zadanie podtrzymania → cewka nadal zasilona
4. Naciśnij `STOP` → otwarcie NC → cewka bez zasilania → KM opada → silnik wyłączony

**Sygnał STOP musi być NC (normalnie zamknięty):**
- Zgodnie z EN 60204-1 i EN ISO 13849-1 — stan bezpieczny = brak sygnału
- Uszkodzenie przewodu do STOP → otwarcie = maszyna się zatrzymuje (fail-safe)

**Realizacja w PLC (program LAD):**
```
Network 1:
  [I0.0 START] ──┬── [I0.1 STOP NC] ─── (Q0.0 KM)
  [Q0.0 KM] ─────┘
```

**Schemat układu samopodtrzymania z timerem (przełączenie Δ→Y):**

![Układ samopodtrzymania z timerem](images/electrical/delta_star_switching.jpg)

*Rys. 20.8 — Kompletny schemat: obwód mocy (F1, K1 stycznik główny, K2 timer) + obwód sterowania z samopodtrzymaniem (S1 STOP NC, S2 START NO, cewka K1 z samopodtrzymaniem, cewka K2 timer). Źródło: Wikimedia Commons, CC BY-SA 3.0*

**Integracja z PLC a klasyczny schemat:**
- Przy sterowaniu PLC: często rezygnuje się z hardware self-holding (PLC to realizuje programowo)
- Wymaganie bezpieczeństwa: obwód STOP w sprzęcie (HW) — np. PLC może się zawiesić, a Stop musi działać

*Źródło: EN 60204-1 §10, EN ISO 13849-1, praktyka automatyki przemysłowej*

---

### 20.9. Jak wygląda typowy schemat rozruchu Y/Δ sterowanego przez PLC — kolejność wyjść i blokady?

**Kompletna procedura commissioning i uruchomienia układu Y/Δ z PLC (TIA Portal):**

**Przypisanie wyjść PLC:**

| Wyjście PLC | Styk / Element | Opis |
|-------------|----------------|------|
| Q0.0 | KM_L (liniowy) | Zasila uzwojenia silnika (U1/V1/W1) |
| Q0.1 | KM_Y (gwiazda) | Zwiera U2/V2/W2 = punkt gwiazdowy |
| Q0.2 | KM_Δ (trójkąt) | Łączy U2/V2/W2 → U1/V1/W1 (skrzyżowanie) |

**Wejścia PLC (sprzężenie zwrotne):**

| Wejście PLC | Sygnał | Opis |
|-------------|--------|------|
| I0.0 | START | Przycisk Start (NO) |
| I0.1 | STOP | Przycisk Stop (NC) |
| I0.2 | FB_KM_L | Potwierdzenie załączenia KM_L (styk pomocniczy NO) |
| I0.3 | FB_KM_Y | Potwierdzenie załączenia KM_Y |
| I0.4 | FB_KM_Δ | Potwierdzenie załączenia KM_Δ |
| I0.5 | FAULT_THERMAL | Styk NC z przekaźnika termicznego |

**Sekwencja sterowania (SCL):**

```scl
// TIA Portal S7-1500 — rozruch Y/Delta
VAR_GLOBAL
    Timer_YD : TON;       // timer przełączenia Y→Δ
    Timer_Gap : TON;      // timer przerwy między KM_Y off a KM_D on
    Running : BOOL;
    YD_State : INT;       // 0=stop, 1=Y, 2=gap, 3=delta
END_VAR

CASE YD_State OF
    0: // STOP
        KM_L := FALSE; KM_Y := FALSE; KM_D := FALSE;
        IF Start AND NOT Fault_Thermal THEN
            KM_L := TRUE;
            KM_Y := TRUE;
            Timer_YD(IN:=TRUE, PT:=T#6S);
            YD_State := 1;
        END_IF;

    1: // Gwiazda (Y)
        IF Timer_YD.Q THEN
            KM_Y := FALSE;                     // wyłącz gwiazdę
            Timer_YD(IN:=FALSE);
            Timer_Gap(IN:=TRUE, PT:=T#100MS);  // przerwa 100ms
            YD_State := 2;
        END_IF;
        IF NOT Stop OR Fault_Thermal THEN YD_State := 0; END_IF;

    2: // Przerwa (gap) między Y a Δ
        IF Timer_Gap.Q THEN
            KM_D := TRUE;                      // zamknij trójkąt
            Timer_Gap(IN:=FALSE);
            YD_State := 3;
        END_IF;

    3: // Trójkąt (Δ) — praca nominalna
        IF NOT Stop OR Fault_Thermal THEN
            KM_L := FALSE; KM_D := FALSE;
            YD_State := 0;
        END_IF;
END_CASE;

// Blokada programowa — nigdy jednocześnie Y i Δ
IF KM_Y THEN KM_D := FALSE; END_IF;
IF KM_D THEN KM_Y := FALSE; END_IF;
```

**Diagnostyka typowych problemów:**

| Objaw | Przyczyna | Naprawa |
|-------|-----------|---------|
| Silnik nie startuje | KM_L nie zasila (brak FB_KM_L) | Sprawdź bezpieczniki, przekaźnik termiczny |
| Wyłączenie przy przełączeniu Y→Δ | Przerwa zbyt krótka → łuk → zwarcie | Wydłuż Timer_Gap do 150–200 ms |
| Ciągły prąd rozruchowy, nie przyspiesza | Zbyt krótki Timer_YD — przełączenie za wcześnie | Ustaw 5–8 s zamiast 3 s |
| Przekaźnik termiczny wyciąga | I_set za nisko lub klasa wyzwalania 10 zamiast 20 | Nastaw I_set = I_n, zmień na klasę 20 |
| KM_Δ i KM_Y wyzwalają jednocześnie | Brak blokady mechanicznej lub elektrycznej | Zamontuj 3RA1934-1A + sprawdź styki NC |

> 💡 **Monitoruj prąd online:** przy komisjonowaniu przyłącz multimetr cęgowy do fazy silnika — sprawdź prąd w Y (powinien być ~1/3 prądu w Δ). Jeśli prąd w Y jest równy prądowi Δ = uzwojenia podłączone jako 660V silnik na sieci 400V (błąd: silnik jest gwiazdowy z fabryki, a ty go prefabrykujesz w Y/Δ).

**Schemat rozruchu bezpośredniego jednokierunkowego (DOL) — porównanie z Y/Δ:**

![Schemat DOL](images/electrical/demarrage_direct.png)

*Rys. 20.9 — Rozruch bezpośredni (DOL): Q2 = rozłącznik, KM1 = stycznik, F1 = przekaźnik termiczny, M = silnik. W schemacie Y/Δ dochodzą dwa dodatkowe styczniki (KM_Y i KM_Δ). Źródło: Wikimedia Commons, CC BY-SA 3.0*

*Źródło: EN 60204-1, praktyka szafy rozdzielniczej commissioning, Siemens Industry*

---
