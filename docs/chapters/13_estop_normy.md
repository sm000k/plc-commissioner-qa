## 13. E-STOP — NORMY, IMPLEMENTACJA I OBLICZENIA BEZPIECZEŃSTWA


### 13.1. Jakie są kategorie zatrzymania wg EN 60204-1 i jak wpływają na wybór STO vs SS1?  🔴

| Kategoria | Opis zatrzymania | Odpowiednik Safety | Kiedy stosujesz |
|-----------|-----------------|-------------------|-----------------|
| **Kat. 0** | Natychmiastowe odcięcie zasilania napędów — wybieg swobodny | <span style="color:#c0392b">**STO**</span> (Safe Torque Off) | Wybieg akceptowalny i bezpieczny (lekkie masy) |
| **Kat. 1** | Hamowanie z rampą do zatrzymania, następnie odcięcie zasilania | <span style="color:#c0392b">**SS1**</span> (Safe Stop 1) | Inercja maszyny wyklucza bezpieczny wybieg (prasy, obrabiarki, dźwigi) |
| **Kat. 2** | Hamowanie z rampą, napęd pozostaje zasilony i monitoruje pozycję | <span style="color:#c0392b">**SS2 → SOS**</span> | Oś musi trzymać pozycję po zatrzymaniu (ramiona robotów, pionowe slide) |

> ⚠️ **Norma:** EN 60204-1 wymaga by e-stop realizował kategorię **0 lub 1** — nie 2, chyba że analiza ryzyka uzasadnia inaczej.

*[ZWERYFIKOWANE - EN 60204-1 §9.2.2 (kategorie zatrzymania); IEC 61800-5-2 §6.2 (STO/SS1/SS2 definicje); [E-Stop SIL 3 Application Example (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/)]*
### 13.2. Co to jest LSafe_EStop i gdzie go znajdziesz w TIA Portal?  🟡

`LSafe_EStop` to certyfikowany przez TÜV blok funkcjonalny z biblioteki LSafe (STEP 7 Safety Advanced). Realizuje kompletną logikę e-stopu: odcięcie wyjścia aktuatora, blokada restartu, sekwencja ACK i monitorowanie styczników.

**Wejścia kluczowe:**
- `eStop` (BOOL, **NC** — FALSE = e-stop wciśnięty)
- `start/stop`, `acknowledge` (impuls)
- `feedback1/feedback2` (zwrotne styki pomocnicze NC) + `feedbackTime` (max czas reakcji)
- `actuatorVS` (value status F-DO)

**Wyjścia:**
- `actuator` (BOOL — steruje F-DO → styczniki)
- `acknowledgeRequestedEStop` (TRUE = wymagane ACK)
- `eStopReleased` (TRUE = e-stop odblokowany)
- `fault` (błąd logiki lub zacięty styk)

**Lokalizacja w TIA Portal:** `Safety Advanced → Libraries → LSafe → LSafe_EStop`
Blok musi być wywołany z Safety OB (`F_MAIN` lub Safety Main OB).

> 💡 **Oba kanały e-stopu** (2×NC) podłączone do pary kanałów F-DI z ewaluacją 1oo2 — sam moduł F-DI dostarcza jeden bezpieczny sygnał BOOL do bloku (kanały nie są widoczne osobno w programie).

**Struktura programu Safety z blokiem LSafe_EStop:**
![Safety program: OB123 → Main Safety → LSafe_EStop + ACK_GL](images/safety/07b_estop_mode_of_op_p6.png)

**Okablowanie sprzętowe E-Stop (CPU 1516F + F-DI + F-DQ z dwoma kanałami):**
![E-Stop hardware setup: S7-1516F, F-DI, F-DQ, dwukanałowe połączenie przycisku](images/safety/07c_estop_hw_setup_p10.png)

*[ZWERYFIKOWANE - [E-Stop SIL 3 Application Example (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/) — rozdz. LSafe_EStop, okablowanie F-DI; [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/)]*
### 13.3. Co to jest feedback circuit (obwód sprzężenia zwrotnego styczników) i dlaczego jest wymagany dla SIL 3 / PL e?  🟡

Feedback circuit to monitorowanie stanu styków pomocniczych (NC, pozytywnie sterowanych) styczników wykonawczych podłączone z powrotem na wejście DI lub F-DI.
Cel: wykrywanie zgrzania (welding) lub zacięcia styku stycznika. Zgrzany styk = kontakt NC pozostaje otwarty mimo odcięcia cewki → feedback = niezgodność → maszyna nie może wystartować.
Dla Cat.4 / PL e / SIL 3 wymagana jest REDUNDANCJA ścieżki wyłączania (2 styczniki szeregowo lub równolegle) PLUS monitoring feedback obydwu — bez tego system nie spełnia DC ≥ 99% w podsystemie Reaction.
Parametr feedbackTime w LSafe_EStop definiuje max czas w którym stycznik musi się przełączyć po komendzie (typowo 100–300ms ⚠️ DO WERYFIKACJI — wartość zależy od rodzaju stycznika, sprawdź w dokumentacji producenta).
Połączenie styczników: pozytywne otwarcie (EN 60947-5-1) — jeśli cewka odcięta, styk NC jest MECHANICZNIE zmuszony do otwarcia nawet przy zgrzaniu. Wymagane przez normy w obwodach Safety.

*[ZWERYFIKOWANE - EN 60947-5-1 §4.5 (pozytywne otwarcie); ISO 13849-1 Tablica K.1 (DC dla monitorowania sprzężenia zwrotnego); [E-Stop SIL 3 Application Example (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/) — rozdz. feedback circuit]*
### 13.4. Co to są CCF (Common Cause Failure) i jakie środki są wymagane dla Cat.4?  🟢

CCF (Common Cause Failure / Usterka wspólnej przyczyny) to scenariusz gdzie JEDNA przyczyna (np. przepięcie, temperatura, EMC, błąd montażu) uszkadza oba kanały redundantnego systemu jednocześnie — co pozbawia system odporności na błędy.
ISO 13849-1 Tablica F.1 wymaga minimum 65 punktów CCF dla architektury Cat.3 i Cat.4. Punkty przyznawane za środki zapobiegawcze, m.in.: separacja/oddzielenie tras kablowych, stosowanie różnych technologii czujników, ochrona przed EMC, uwzględnienie warunków środowiskowych, procedury testowania ⚠️ DO WERYFIKACJI: dokładne wartości punktowe w ISO 13849-1 Tablica F.1 (zależą od wydania normy).
W praktyce: prowadź kable kanału 1 i 2 w osobnych trasach, stosuj różnych producentów czujników (diverse redundancy), zachowuj separację przestrzenną.
Siemens F-DI realizuje diagnostykę cross-circuit (zwarcie między kanałami) i pulse-testing — ale CCF środki leżą po stronie projektu i montażu, nie CPU.

*[ZWERYFIKOWANE - ISO 13849-1 Tablica F.1 (CCF punkty, wartości ⚠️ DO WERYFIKACJI w wydaniu normy); [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/) — rozdz. CCF; [E-Stop SIL 3 Application Example (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/)]*
### 13.5. Czy można łączyć przyciski e-stop szeregowo do jednego wejścia F-DI?

Tak, ale z ograniczeniami. EN ISO 13850 i IEC 62061 dopuszczają szeregowe połączenie e-stopów TYLKO jeśli można wykluczyć jednoczesne naciśnięcie dwóch e-stopów ORAZ jednoczesne wystąpienie awarii i naciśnięcia.
Problem: przy szeregowym połączeniu nie wiadomo KTÓRY e-stop zadziałał → brak diagnostyki granularnej. Siemens zaleca oddzielne kanały F-DI per e-stop dla szybszej lokalizacji usterek i lepszej diagnostyki ProDiag/HMI.
Praktyczny kompromis Siemens (wg doc. 21064024): każdy e-stop na osobnej parze kanałów F-DI z 1oo2 evaluation → każdy e-stop widoczny osobno w diagnostyce TIA Portal i na HMI.
Jeśli szeregowo: każde zadziałanie to osobna "supplementary safety function" — analiza ryzyka musi obejmować wszystkie e-stopy indywidualnie.

---

*[ZWERYFIKOWANE - EN ISO 13850 §5.4 (szeregowe połączenie e-stopów); IEC 62061 §7.3 (analiza ryzyka per funkcja Safety); [E-Stop SIL 3 Application Example (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/) — rozdz. okablowanie wielu przycisków e-stop]*

### 13.6. Jak wygląda obliczenie PFHD (Probability of Dangerous Failure per Hour) dla funkcji Safety E-Stop z F-CPU S7-1500F?

**PFHD** to prawdopodobieństwo niebezpiecznej awarii na godzinę — podstawowa miara ilościowa bezpieczeństwa funkcjonalnego. Dla osiągnięcia PL e / SIL 3 sumaryczne PFHD wszystkich podsystemów musi być < 10⁻⁷ (< 1×10⁻⁷ /h).

**Podział na podsystemy (z Application Example Siemens, Entry ID: 21064024):**

Funkcja Safety E-Stop dzieli się na 3 podsystemy, każdy oceniany osobno:

| Podsystem | Komponenty | PFHD | PL |
|-----------|-----------|------|-----|
| **Detection** (detekcja) | Przycisk E-Stop (B10=100.000, 20% dangerous) + F-DI (DC≥99%, 1oo2) | 9,06×10⁻¹⁰ | PL e |
| **Evaluation** (ewaluacja) | CPU 1516F (2,00×10⁻⁹) + ET200MP F-DI (1,00×10⁻⁹) + F-DQ (2,00×10⁻⁹) | 5,00×10⁻⁹ | PL e |
| **Reaction** (reakcja) | 2 styczniki (B10=1.000.000, 73% dangerous, Cat.4, DC≥99%) | 1,45×10⁻⁹ | PL e |
| **SUMA** | — | **7,35×10⁻⁹** | **PL e** |

**Kluczowe parametry wejściowe:**
- **B10** — liczba cykli do 10% awaryjności (producent podaje w karcie katalogowej)
- **Percentage of dangerous failures** — jaki % awarii jest niebezpieczny (E-Stop: 20%, stycznik: 73%)
- **DC (Diagnostic Coverage)** — ≥99% wymagane dla Cat.4/PL e. Realizowane przez: cross-comparison w F-DI (detekcja) i redundantną ścieżkę wyłączania + dynamiczny monitoring styczników (reakcja)
- **CCF ≥ 65 punktów** — wymagane środki przeciw usterkom wspólnej przyczyny wg ISO 13849-1 Tablica F.1

**Narzędzie do obliczeń:** Safety Evaluation w TIA Selection Tool (online) — wprowadzasz komponenty, parametry B10, DC, architekturę → narzędzie oblicza PFHD per podsystem i sumę.

**Praktyka commissioning:** Nie musisz obliczać PFHD samodzielnie — jako commissioner weryfikujesz, czy zastosowane komponenty i architektura odpowiadają obliczeniom z projektu Safety. Sprawdź: czy zastosowano właściwe styczniki (B10 z karty), czy feedback circuit jest podłączony (DC≥99%), czy CCF measures są spełnione (separacja kabli, różne trasy).

> Źródło: Siemens Application Example „Emergency Stop up to PL e / SIL 3 with F-S7-1500", Entry ID: 21064024, V7.0.1, tabele 3-3 do 3-8 [ZWERYFIKOWANE]

### 13.7. Co to jest DC (Diagnostic Coverage) i jak jest osiągane w poszczególnych podsystemach E-Stop?

**DC (Diagnostic Coverage / Pokrycie diagnostyczne)** to miara procentowa zdolności systemu do wykrywania niebezpiecznych awarii zanim doprowadzą do utraty funkcji Safety. DC ≥ 99% jest wymagane dla najwyższych poziomów bezpieczeństwa (Cat.4 / PL e / SIL 3).

**DC w podsystemie Detection (detekcja — E-Stop + F-DI):**
- Realizowane przez **cross-comparison w module F-DI** — moduł porównuje sygnały z dwóch kanałów (1oo2 evaluation). Rozbieżność → discrepancy error → passivation
- E-Stop z pozytywnym otwieraniem (EN 60947-5-1) zapewnia, że mechaniczne zacięcie jest wykrywalne przez drugi kanał
- DC ≥ 99% — cross-comparison wykrywa praktycznie wszystkie awarie w torze detekcji

**DC w podsystemie Evaluation (ewaluacja — F-CPU + F-I/O):**
- Realizowane przez **wewnętrzną diagnostykę F-CPU** — dual-channel processing, program diversification, self-tests
- Wartość PFHD podawana przez Siemens w Safety Evaluation TIA Selection Tool (np. CPU 1516F: 2,00×10⁻⁹)
- Commissioner nie konfiguruje DC ewaluacji — jest wbudowane w F-CPU

**DC w podsystemie Reaction (reakcja — styczniki):**
- Realizowane przez **redundantną ścieżkę wyłączania** (2 styczniki) + **dynamiczny feedback monitoring** (styki pomocnicze NC podłączone do F-DI/DI, monitorowane przez LSafe_EStop → parametr feedbackTime)
- Zgrzany styk jednego stycznika → feedback = niezgodność → blokada restartu → system wykrywa awarię
- DC ≥ 99% wymaga ZARÓWNO redundancji (2 styczniki) JAK I feedback monitoringu — same 2 styczniki bez monitoringu to DC < 99%

**Praktyka commissioning:** Podczas acceptance testu sprawdź: (1) oba kanały E-Stop podłączone i przetestowane (cross-comparison w F-DI), (2) feedback z obu styczników podłączony i monitorowany, (3) feedbackTime ustawiony odpowiednio do typu stycznika (typowo 100–300 ms ⚠️ DO WERYFIKACJI — zależy od producenta stycznika).

> Źródło: Siemens Application Example Entry ID: 21064024, tabele 3-3 i 3-6 — DC≥99% przez cross-comparison i redundant switch-off path [ZWERYFIKOWANE]

### 13.8. Jak wygląda obliczenie czasów odpowiedzi (response time) w funkcji Safety E-Stop i co na nie wpływa?

**Czas odpowiedzi Safety (Safety Response Time)** to czas od wykrycia zagrożenia (naciśnięcie E-Stop) do osiągnięcia stanu bezpiecznego (odcięcie momentu napędu). Jest sumą opóźnień w całym łańcuchu Safety.

**Składowe czasu odpowiedzi:**

| Składowa | Typowy zakres | Źródło opóźnienia |
|---------|--------------|-------------------|
| Czas reakcji F-DI | 2–12 ms | Filtrowanie wejścia + czas cyklu aktualizacji F-I/O |
| Czas cyklu F-runtime group | 10–100 ms | Czas przetwarzania programu Safety (zależy od rozmiaru programu) |
| Czas komunikacji PROFIsafe (round-trip) | 2–20 ms | Zależy od topologii sieci, send clock PROFINET, liczby urządzeń |
| Czas reakcji F-DQ | 1–5 ms | Czas przełączenia wyjścia Safety |
| Czas mechaniczny stycznika | 10–30 ms | Czas otwarcia styku (z karty katalogowej producenta) |
| **Suma (worst case)** | **25–167 ms** | — |

**Czynniki wpływające:**
- **F-monitoring time** — nie jest częścią normalnego czasu odpowiedzi, ale wpływa na worst-case w przypadku utraty komunikacji
- **Czas cyklu F-runtime group** — najważniejszy parametr do optymalizacji. Ustawisz go w Safety Administration → F-runtime group → Max cycle time
- **Filtr wejścia F-DI** — zbyt długi filtr debounce na wejściu F-DI zwiększa czas reakcji

**Narzędzie Siemens:** Arkusz kalkulacyjny Excel do obliczenia response time dostępny na support.automation.siemens.com (Entry ID: 49368678). Wprowadzasz parametry sieci i konfiguracji → arkusz oblicza worst-case response time.

**Praktyka commissioning:** Czas odpowiedzi musi być krótszy niż czas dobiegu maszyny do zatrzymania (wynikający z analizy ryzyka). Jeśli obliczony response time > czas wymagany → skróć cykl F-runtime, zmniejsz filtr wejścia F-DI, upewnij się, że PROFINET send clock jest optymalny. Dokumentuj obliczony response time w protokole Safety Acceptance Test.

> Źródło: Siemens Application Example Entry ID: 21064024 + arkusz kalkulacyjny Entry ID: 49368678 (referencja w SIMATIC Safety - Konfiguracja i programowanie, s.654) [ZWERYFIKOWANE]
