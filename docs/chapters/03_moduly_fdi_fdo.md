## 3. MODUŁY F-DI / F-DO — OKABLOWANIE I PARAMETRY

### 3.1. Co to jest F-DI i jak różni się od standardowego DI?  🔴

F-DI (Fail-safe Digital Input) to moduł wejść bezpieczeństwa certyfikowany do SIL 3 / PL e. W porównaniu ze standardowym DI posiada trzy dodatkowe mechanizmy diagnostyczne, które standardowy DI nie ma:

**1. VS\* pulse testing — ciągły autotest okablowania (= „self-test kanałów w tle")**

VS\* (Versorgung Sensor) to zasilanie czujnika z modułu F-DI, które zamiast stałego 24 V wysyła **krótkie impulsy testowe**. Moduł analizuje wzorzec impulsów powracających na wejście i wykrywa usterki:
- **Przerwa przewodu (wire break)** — brak jakiegokolwiek sygnału zwrotnego (obwód otwarty)
- **Zwarcie do L+ (24 V)** — stały sygnał wysoki bez pulsacji (przewód podciągnięty do zasilania)
- **Zwarcie do M (0 V / masa)** — stały sygnał niski (przewód ściągnięty do masy)

Testowanie odbywa się **w tle, cyklicznie, bez przerywania procesu** — impulsy są tak krótkie, że czujnik (np. styk NC E-Stop) działa normalnie. To właśnie jest „self-test kanałów" — nie jest to osobna funkcja, lecz bezpośredni efekt działania VS\* pulse testing.

**2. Cross-circuit detection — wykrywanie zwarcia MIĘDZY kanałami 1oo2**

Cross-circuit to zwarcie przewodu kanału A do przewodu kanału B tego samego czujnika dwukanałowego (1oo2). Przyczyna: kabel wielożyłowy przygnieciony lub przetarty → izolacja przebita → kanały A i B połączone elektrycznie.

**Dlaczego to groźne:** Zwarcie międzykanałowe sprawia, że oba kanały zawsze pokazują identyczną wartość — nawet jeśli jeden styk E-Stop jest uszkodzony (np. spawany). System „myśli", że ma dwa niezależne kanały, a w rzeczywistości obwód jest zdegradowany do jednokanałowego (1oo1). Drugi błąd (uszkodzenie drugiego styku) nie zostanie wykryty → E-Stop nie zadziała. [ZWERYFIKOWANE — Siemens 21064024: „Without cross-circuit detection this would lead to, for example, a 2-channel emergency stop circuit not to trigger a shut-down even if only one normally-closed contact is faulty (second error)"]

**Jak moduł F-DI to wykrywa:** Dwa wyjścia sensor supply (VS0 i VS2) generują impulsy testowe **z różnym przesunięciem czasowym** (nie jednocześnie). Kanał A jest zasilany z VS0, kanał B z VS2:
- **Kanały niezależne** → odpowiedzi wracają z różnymi fazami (VS0 w swoim oknie, VS2 w swoim) → OK
- **Kanały spięte** → impuls z VS0 pojawia się na wejściu kanału B w oknie czasowym przypisanym do VS0 (a nie VS2) → moduł wykrywa cross-circuit → passivation

**Konfiguracja w TIA Portal:** Właściwości modułu F-DI → „Short-circuit test" → Activate (osobno per sensor supply 0 i sensor supply 2). **Domyślnie wyłączone** — trzeba aktywować, aby uzyskać DC ≥ 99% wymagane dla Cat.4 / PL e / SIL 3. [ZWERYFIKOWANE — Siemens 21064024, str. 12: „The short circuit tests for the channels 0 and 8 are activated."]

**3. Obsługa 1oo2 z discrepancy time + komunikacja PROFIsafe**

- Ewaluacja dwukanałowa 1oo2 z konfigurowalnym discrepancy time (monitorowanie rozbieżności między kanałami)
- Komunikacja z F-CPU przez PROFIsafe z CRC — integralność danych gwarantowana na poziomie protokołu
- Ewaluację 1oo2 wykonuje **sam moduł** F-DI (nie obciąża F-CPU) [ZWERYFIKOWANE — Siemens Safety Integrated broszura: „Ewaluację 1oo2 wejść failsafe wykonują moduły wejściowe"]

**Podsumowanie:** VS\* pulse testing, cross-circuit detection i self-test to **ten sam mechanizm sprzętowy** widziany z różnych perspektyw — VS\* to sposób działania (impulsy), cross-circuit to jedna z wykrywanych usterek, a self-test to fakt że dzieje się to ciągle w tle. Aktywacja parametru „Short-circuit test" w TIA Portal włącza zarówno cross-circuit detection jak i detekcję zwarć do L+/M.

Moduły: ET 200SP F-DI, ET 200MP F-DI, S7-1200 SM 1226 F-DI.

📚 **Źródła:**
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 12, 17) — konfiguracja short-circuit test, definicja cross-circuit
- [`sources/pdfs/extracted/SIMATIC Safety Integrated – wszystko w jednym sterowniku PLC_extracted.txt`](sources/pdfs/extracted/SIMATIC%20Safety%20Integrated%20–%20wszystko%20w%20jednym%20sterowniku%20PLC_extracted.txt) — broszura: testy failsafe zwarć, przerw, cross-circuit
- Normy: EN ISO 13849-1 (Cat.4 / PL e), IEC 62061 (SIL 3), IEC 61508
### 3.2. Co to jest VS* (pulse testing) i jak wykrywa usterki?  🔴

VS\* (Versorgung Sensor / Sensor Supply) to wyjście zasilające na module F-DI, które wysyła **krótkie impulsy testowe** zamiast stałego 24 V. Czujnik zasilany jest tymi impulsami, a sygnał wraca na wejście z tą samą charakterystyką pulsacji. To jest ten sam mechanizm, który stoi za „self-testem kanałów" i „cross-circuit detection" opisanymi w pytaniu 3.1.

**Moduł analizuje wzorzec impulsów i rozróżnia 4 stany usterek:**

| Usterka | Co widzi moduł | Mechanizm |
|---------|----------------|-----------|
| **Przerwa przewodu (wire break)** | Brak jakiegokolwiek sygnału zwrotnego | Obwód otwarty → impulsy nie wracają |
| **Zwarcie do M (0 V / masa)** | Stały sygnał niski (0 V) | Przewód ściągnięty do masy → impulsy zanikają |
| **Zwarcie do L+ (24 V)** | Stały sygnał wysoki bez pulsacji | Przewód podciągnięty do zasilania → brak przerw między impulsami |
| **Cross-circuit (zwarcie międzykanałowe)** | Impuls z VS0 pojawia się na wejściu kanału B w złym oknie czasowym | Kanał A i B spięte elektrycznie → utrata niezależności kanałów 1oo2 |

**Mechanizm cross-circuit detection w szczegółach:**
Moduł F-DI ma dwa niezależne wyjścia sensor supply: **VS0** (dla kanałów 0–3) i **VS2** (dla kanałów 4–7 / 8–11 zależnie od modelu). VS0 i VS2 generują impulsy w **różnych oknach czasowych** — nigdy jednocześnie:
1. W oknie T1: VS0 wysyła impuls → kanał A (np. DI0.0) widzi impuls, kanał B (np. DI0.4) — cisza
2. W oknie T2: VS2 wysyła impuls → kanał B widzi impuls, kanał A — cisza
3. Jeśli kanały A i B są spięte (cross-circuit): w oknie T1 **oba** kanały widzą impuls VS0 → moduł wykrywa impuls na kanale B w złym oknie czasowym → błąd cross-circuit → passivation

**Kluczowe:** VS\* pulse testing zapewnia DC ≥ 99% (Diagnostic Coverage) — warunek konieczny do Cat.4 / PL e (ISO 13849-1) lub SIL 3 (IEC 62061 / IEC 61508). [ZWERYFIKOWANE — Siemens 39198632, normy ISO 13849-1 i IEC 62061]

**Konfiguracja w TIA Portal:** Właściwości modułu F-DI → „Short-circuit test" → Activate (osobno per sensor supply 0 i sensor supply 2). Domyślnie wyłączone — trzeba aktywować! [ZWERYFIKOWANE — Siemens 21064024, str. 12]

> ⚠️ **Wyjątek — kurtyny (OSSD):** Kurtyny bezpieczeństwa mają **własne impulsy testowe** na wyjściach OSSD1/OSSD2. Nie podłączaj VS\* do OSSD — w TIA Portal ustaw „Sensor supply" kanału na „None/Disabled", inaczej impulsy F-DI zablokują sygnał z kurtyny.

![ET 200 F-DI: cross-circuit, wire break i short-circuit detection](images/safety/01d_safety_brochure_p4.png)

*[ZWERYFIKOWANE - [Siemens Wiring Examples for F-I/O (Entry ID: 39198632)](https://support.industry.siemens.com/cs/document/39198632/); [E-Stop SIL3 Application (Entry ID: 21064024, str. 10-12)](https://support.industry.siemens.com/cs/document/21064024/)]*
### 3.3. Dlaczego czujniki Safety podłącza się jako NC (normalnie zamknięty)?  🔴

Zasada bezpieczna (fail-safe): zerwanie kabla, przepalenie bezpiecznika, uszkodzenie czujnika → obwód otwarty → sygnał 0 → system Safety traktuje to jako zadziałanie i zatrzymuje maszynę.
Przy NO (normalnie otwartym): zerwanie kabla = brak sygnału = maszyna nie wie o zagrożeniu → niebezpieczeństwo.
NC to zasada 'fail-safe by design' wymagana przez normy bezpieczeństwa.

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/); EN ISO 13849-1 §6.2.5 (wymogi dla sygnalizacji NC w obwodach bezpiecznych)]*
### 3.4. Co to jest discrepancy time i jak go konfigurujesz?  🟡

Discrepancy time to maksymalny czas w którym dwa kanały czujnika 1oo2 mogą pokazywać różne wartości bez generowania błędu. Przykład: przy otwieraniu osłony mechanicznej jeden styk reaguje 15ms wcześniej niż drugi — to normalne i fizyczne.
Konfigurujesz w TIA Portal: właściwości modułu F-DI → parametry kanału → Discrepancy time (typowo 10–200ms w zależności od czujnika).
Zbyt krótki → fałszywe błędy. Zbyt długi → późne wykrycie uszkodzenia.

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. parametry F-DI](https://support.industry.siemens.com/cs/document/109751404/)]*
### 3.5. Co to jest substitute value na F-DO i kto decyduje o jego wartości?

Substitute value to wartość którą przyjmuje wyjście F-DO po przejściu modułu w passivation (stan błędu). Konfigurujesz w TIA Portal we właściwościach kanału F-DO: wartość 0 lub 1.
Decyduje inżynier projektu na podstawie analizy bezpieczeństwa — nie Siemens. Przykłady: napęd → 0 (stop), zawór bezpieczeństwa → może być 1 (pozostaje otwarty), pompa chłodząca → może być 1 (chłodzi nadal).

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. F-DO substitute values](https://support.industry.siemens.com/cs/document/109751404/)]*
### 3.6. Co to jest pm switching i pp switching — różnica?  🟡

Pm switching i pp switching to dwa sposoby okablowania bezpiecznego odcięcia zasilania grupy standardowych modułów wyjściowych (DQ/AQ) przez moduł F-PM-E w stacji ET 200SP. Różnica dotyczy tego, **które linie zasilania obciążenia (Load supply) są przełączane** przez F-PM-E.

**Problem, który rozwiązują:** Na linii produkcyjnej masz dziesiątki standardowych modułów DQ sterujących zaworami, silnikami, lamp­kami. Przy E-Stop lub innej funkcji Safety musisz **bezpiecznie odciąć zasilanie** tym wyjściom. Wymiana wszystkich DQ na moduły F-DQ jest droga. Zamiast tego F-PM-E odcina **zasilanie obciążenia** (Load supply) całej grupy standardowych modułów — wszystkie wyjścia w grupie natychmiast tracą napięcie i przechodzą w stan bezpieczny (0 V).

**pm switching (plus-minus) — odcięcie obu linii:**
- F-PM-E przełącza **obie** linie zasilania obciążenia: **P (+24V)** i **M (0V)**
- Aktuator podłączony jest między wyjściem P a wyjściem M modułu DQ — a obie te linie przechodzą przez F-PM-E
- **Wymaga wydzielonego zasilania obciążenia (Load supply)** odizolowanego galwanicznie od zasilania elektroniki (Electronic supply) — widoczne na schemacie jako osobny zasilacz 24V DC
- **Zaleta:** pełna izolacja galwaniczna → nawet jeśli przewód wyjścia DQ dotknie zewnętrznego potencjału (np. zwarcie do obcego L+), aktuator i tak nie dostanie napięcia, bo M jest również odcięte
- **Zastosowanie:** gdy wymagana jest ochrona przed zwarciami do zewnętrznych potencjałów (np. linie z napięciem >24V w pobliżu, wymóg EN 60204-1)
- **Osiągalny poziom:** do SIL 2 / Cat.3 / PL d (z dwoma F-PM-E) lub SIL 1 / Cat.2 / PL c (z jednym F-PM-E)

**pp switching (plus-plus) — odcięcie dwóch kanałów P:**
- F-PM-E przełącza **dwa niezależne kanały po stronie P (+24V)** — podaje dwa sygnały P1 i P2 do grupy modułów
- Linia M (0V) jest **wspólnym powrotem** (common M) — NIE jest przełączana przez F-PM-E
- **Nie wymaga** osobnej izolacji galwanicznej zasilania obciążenia od elektroniki (prostsze okablowanie)
- **Wada:** linia M pozostaje aktywna po odcięciu → jeśli przewód wyjścia DQ ma zwarcie do aktywnego L+ za F-PM-E, aktuator może nadal dostać napięcie przez tę ścieżkę. Dlatego wymóg Siemens: **„measures must be taken to protect the wiring from the PP output via all standard modules in the switch-off group to the actuator against short circuits to wires still active after safe switch off"** (EN 60204-1) [ZWERYFIKOWANE — Siemens 39198632, str. 5]
- **Zastosowanie:** gdy okablowanie jest krótkie/chronione i nie ma ryzyka zwarć do obcych potencjałów — prostsze, tańsze rozwiązanie
- **Osiągalny poziom:** do SIL 2 / Cat.3 / PL d (z dwoma F-PM-E) lub SIL 1 / Cat.2 / PL c (z jednym F-PM-E)

| Cecha | pm switching | pp switching |
|-------|-------------|-------------|
| Co przełącza F-PM-E | P **i** M (obie linie) | Dwa kanały P (tylko plus) |
| Linia M | Odcięta przez F-PM-E | Wspólna, nie odcinana |
| Izolacja galwaniczna Load/Electronic | **Wymagana** | Nie wymagana |
| Ochrona przed zwarciami do obcych potencjałów | Wbudowana (M odcięte) | Wymaga dodatkowych środków (EN 60204-1) |
| Złożoność okablowania | Wyższa (osobny zasilacz) | Niższa |
| Typowe zastosowanie | Linie z wyższym napięciem w pobliżu | Proste aplikacje, krótkie trasy kablowe |

**pm-switching — schemat ET 200SP:**
![pm-switching ET 200SP via F-PM-E](images/safety/06a_wiring_pm_switching_p6.png)

**pp-switching — schemat ET 200SP:**
![pp-switching ET 200SP via F-PM-E](images/safety/06b_wiring_pp_switching_p7.png)

📚 **Źródła:**
- [`sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt`](sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt) (str. 5–7) — Fig. 2-1 pm switching, Fig. 2-2 pp switching, wymogi PP Switch Off
- Norma: EN 60204-1 (środki ochrony okablowania przed zwarciami)

### 3.7. Co to jest F-PM-E i do czego służy?

F-PM-E (Fail-safe Power Module E) to moduł Safety w systemie ET 200SP, który umożliwia **bezpieczne odcięcie zasilania obciążenia (Load supply) grupy standardowych modułów wyjściowych** (DQ, AQ) — bez konieczności wymiany tych modułów na drogie moduły F-DQ.

**Problem, który rozwiązuje:**
Standardowe moduły DQ nie mają certyfikatu Safety — nie mogą samodzielnie realizować funkcji bezpieczeństwa. Ale na jednej stacji ET 200SP możesz mieć 10–20 modułów DQ sterujących zaworami i napędami. Wymiana ich wszystkich na F-DQ to ogromny koszt. F-PM-E rozwiązuje to inaczej: **odcina zasilanie na poziomie grupy** — jeden moduł F-PM-E obsługuje wszystkie standardowe DQ w swoim segmencie napięciowym (voltage segment).

**Jak to działa krok po kroku:**
1. F-PM-E jest montowany w szynie ET 200SP **przed** grupą standardowych modułów DQ/AQ
2. Zasilanie obciążenia (Load supply 24V DC) przechodzi **przez** F-PM-E do modułów w grupie
3. W normalnej pracy F-PM-E przepuszcza zasilanie → DQ działają normalnie
4. F-CPU (przez program Safety) nakazuje F-PM-E odciąć zasilanie → **wszystkie wyjścia** grupy tracą napięcie → aktuatory przechodzą w stan bezpieczny (0 V)
5. F-PM-E realizuje to w konfiguracji **pm switching** (odcina P i M) lub **pp switching** (odcina dwa kanały P) — patrz pytanie 3.6

**Osiągalny poziom bezpieczeństwa:**
- **2× F-PM-E** (redundancja) → do **SIL 2 / Cat.3 / PL d**
- **1× F-PM-E** → do **SIL 1 / Cat.2 / PL c**

**Ograniczenia i wymagania:**
- Standardowe DQ w grupie **nie wykonują** same funkcji Safety — bezpieczeństwo zapewnia wyłącznie F-PM-E odcinając zasilanie
- Tylko moduły z listy dopuszczonej przez Siemens (FAQ 39198632) mogą być użyte w grupie Safety
- Diagnostyka procesu (czy aktuator rzeczywiście się wyłączył) musi być realizowana pośrednio — przez monitorowanie procesu lub feedback z czujników do F-DI
- Moduły standardowe DI **nie mogą** być używane do odczytu sygnałów Safety — wymagane F-DI

**Praktyka commissioning:** W TIA Portal F-PM-E konfiguruje się w hardware config jako moduł Safety w stacji ET 200SP. Przypisujesz mu F-address, ustawiasz tryb (pm/pp), a w programie Safety F-CPU sterujesz wyjściem F-PM-E tak jak zwykłym F-DO (TRUE = zasilanie włączone, FALSE = odcięte).

📚 **Źródła:**
- [`sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt`](sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt) (str. 4–7) — wymagania, schematy pm/pp switching
- [`docs/chapters/03_moduly_fdi_fdo.md`](docs/chapters/03_moduly_fdi_fdo.md) — pytanie 3.6 (pm vs pp switching), 3.8 (alternatywy: Safety Relay, F-DO+przekaźnik)
### 3.8. Jak bezpiecznie wyłączyć standardowe moduły wyjść przez Safety?

Trzy główne metody (wg dokumentu Siemens 39198632):
- Safety Relay (np. 3SK1) — zewnętrzny przekaźnik bezpieczeństwa odcina zasilanie grupy DQ. Niezależne od PLC.
- F-PM-E (pm lub pp switching) — moduł F-PM-E w tej samej stacji ET200 odcina zasilanie grupy standardowych DQ (SIL2/Cat.3/PLd).
- F-DO + zewnętrzny przekaźnik — F-DO steruje cewką przekaźnika który odcina zasilanie modułów standardowych. Feedback z przekaźnika do DI.
Ważne: standardowe moduły DI nie mogą być używane do odczytu sygnałów Safety — wymagane F-DI.

**Schematy okablowania — Safety Relay i ET200MP/S7-1500:**
![Figure 3-1: Safety Relay (3SK1) PM-switching, ET200MP S7-1500 — DQ odcięte przez przekaźnik do SIL1/Cat.2/PLc i SIL2/Cat.3/PLd](images/safety/06e_wiring_et200mp_p10.png)

*[ZWERYFIKOWANE - [Siemens Wiring Examples for F-I/O (Entry ID: 39198632), Fig. 3-1 (Safety Relay PM-switching), Fig. 3-2 (F-PM-E), Fig. 3-3 (F-DO + przekaźnik)](https://support.industry.siemens.com/cs/document/39198632/)]*
### 3.9. Jak F-CPU reaguje na typowe awarie wejść dwukanałowych (1oo2)?

Moduł F-DI, skonfigurowany do oceny dwukanałowej (1oo2), monitoruje sygnały z dwóch niezależnych kanałów i reaguje na różne typy awarii. **Wszystkie trzy poniższe awarie powodują passivation** — różnica polega na zakresie (kanał vs cały moduł), co zależy od parametru „Behavior after channel fault" w TIA Portal:
- `Passivate channel` — passivation tylko dotkniętego kanału (pozostałe kanały działają dalej)
- `Passivate the entire module` — passivation całego F-I/O (domyślne dla ET 200SP)

**1. Zwarcie do potencjału 0 V (M):**
  - **Passivation:** ✅ Tak — awaria kanału → passivation kanału lub modułu (wg parametru). Wyjścia Safety przyjmują substitute values (0).
  - **Błąd diagnostyczny:** "Overload or internal sensor supply short circuit to ground".
  - **LED:** Kanał świeci na czerwono.
  - **Reset:** Po usunięciu zwarcia → reintegracja (ręczna lub automatyczna, wg parametru „Channel failure acknowledge").

**2. Zwarcie międzykanałowe (cross-circuit):**
  - **Passivation:** ✅ Tak — awaria **modułu** (nie kanału!) → passivation **całego modułu** niezależnie od parametru „Behavior after channel fault". Cross-circuit oznacza utratę niezależności kanałów → moduł nie może gwarantować poprawnej ewaluacji 1oo2.
  - **Błąd diagnostyczny:** "Internal sensor supply short circuit to P" lub "Short-circuit of two encoder supplies".
  - **LED:** Cały moduł świeci na czerwono (nie pojedynczy kanał).
  - **Reset:** Po usunięciu zwarcia → wymagany ACK_GL lub reset ręczny.

**3. Rozbieżność sygnału (Discrepancy failure):**
  - **Passivation:** ✅ Tak — awaria kanału → passivation kanału lub modułu (wg parametru). Discrepancy = jeden kanał zmienił stan, a drugi nie w czasie discrepancy time.
  - **Przyczyna:** Utrata ciągłości obwodu w jednym z kanałów (np. uszkodzenie styku w E-STOP, kurtynie bezpieczeństwa, skanerze) lub zespawany styk → kanały nie zmieniają się jednocześnie.
  - **Błąd diagnostyczny:** "Discrepancy failure" — wskazany jest kanał, na którym wykryto rozbieżność.
  - **LED:** Diody migają naprzemiennie (czerwona i zielona) po usunięciu przyczyny → gotowość do reintegracji.
  - **Reset:** Zależy od parametru „Reintegration after discrepancy error":
    - `Automatic` — reintegracja natychmiast po zgodności kanałów
    - `Test zero signal necessary` — operator musi najpierw wymusić stan 0 na obu kanałach (np. wcisnąć E-STOP), dopiero potem reset

| Awaria | Passivation? | Zakres | LED |
|--------|-------------|--------|-----|
| Zwarcie do M (0V) | ✅ Tak | Kanał lub moduł (parametr) | Kanał: czerwona |
| Cross-circuit | ✅ Tak | **Zawsze cały moduł** | Moduł: czerwona |
| Discrepancy | ✅ Tak | Kanał lub moduł (parametr) | Miganie czerwona/zielona (po usunięciu) |

**Praktyczne wskazówki:**
- W przypadku błędu rozbieżności z parametrem "Test zero signal necessary" — operator musi najpierw wymusić stan zerowy na czujniku (np. wcisnąć E-STOP), a dopiero potem może zresetować układ. Jest to ważne dla starszych urządzeń, które mogą generować fałszywe błędy rozbieżności.
- Parametr „Behavior after channel fault" (`Passivate channel` vs `Passivate the entire module`) ma krytyczne znaczenie: passivation kanału pozwala utrzymać pozostałe kanały modułu aktywne, ale zwiększa czas pracy F-runtime group. [ZWERYFIKOWANE — SIMATIC Safety Konfiguracja, str. 54-55]

📚 **Źródła:**
- [`sources/pdfs/extracted/SIMATIC Safety - Konfiguracja i programowanie (2)_extracted.txt`](sources/pdfs/extracted/SIMATIC%20Safety%20-%20Konfiguracja%20i%20programowanie%20(2)_extracted.txt) (str. 54–55) — passivation kanału vs modułu, parametr „Behavior after channel fault"
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 22) — examples of events that cause passivation, ACK_GL
- `docs/kb/kb_S03_moduly_fdi_fdo.md` — knowledge base sekcji
- Źródło: transkrypcje ControlByte

### 3.10. Jakie parametry są kluczowe przy konfiguracji wejść dwukanałowych w sterowniku bezpieczeństwa?

Prawidłowa konfiguracja parametrów wejść dwukanałowych (1oo2) w module F-DI jest niezbędna do niezawodnego działania systemu Safety i uniknięcia fałszywych passivation. W TIA Portal kluczowe parametry ustawia się we właściwościach kanału F-DI (Hardware Configuration → moduł F-DI → Properties).

**1. Evaluation mode (tryb oceny)**
- Dla wejść dwukanałowych wybierasz ocenę **1oo2 (one out of two)** — moduł F-DI porównuje sygnały z dwóch niezależnych kanałów (np. DI0.0 i DI0.4) i traktuje je jako jeden sygnał logiczny.
- Ewaluację 1oo2 wykonuje sam moduł F-DI (nie F-CPU) — wynik trafia do F-CPU przez PROFIsafe jako jeden bit z value status.

**2. Discrepancy time (czas rozbieżności)**
- **Definicja:** Maksymalny dopuszczalny czas, w którym dwa kanały mogą pokazywać różne wartości bez wygenerowania błędu.
- **Dobór:** Zbyt krótki → fałszywe błędy i passivation kanałów (np. przy E-STOP, wyłącznikach krańcowych, których styki NC nie przełączają się idealnie jednocześnie). Zbyt długi → większa zwłoka w wykryciu rzeczywistej awarii (np. zespawanego styku).
- **Praktyka:** Najlepiej określić na podstawie testów — wciśnij E-STOP kilkanaście razy i sprawdź, czy nie generuje discrepancy fault. Typowe wartości: 10–200 ms w zależności od typu czujnika.

**3. Reintegration after discrepancy error (reintegracja po błędzie rozbieżności)**
- **Automatic** — reintegracja następuje automatycznie, gdy oba kanały wrócą do zgodności.
- **Test zero signal necessary** — po błędzie rozbieżności operator musi najpierw wymusić stan zerowy na obu kanałach (np. wcisnąć E-STOP, a następnie go odciągnąć), dopiero potem możliwy jest reset. Bez wymuszenia stanu niskiego diody zgłaszają błąd i reintegracja jest zablokowana.
- **Znaczenie praktyczne:** Urządzenia z kilkuletnim stażem mogą generować sporadyczne błędy rozbieżności (zużyte styki). Opcja „Test zero signal necessary" wymusza fizyczne potwierdzenie stanu bezpiecznego przed powrotem do pracy — zwiększa bezpieczeństwo, ale wymaga interwencji operatora.

**Procedura diagnostyczna przy discrepancy fault:**
1. Diody na module F-DI świecą na czerwono → brak możliwości reintegracji
2. Sprawdź bufor diagnostyczny — błąd „Discrepancy failure" wskazuje kanał z awarią
3. Jeśli aktywna opcja „Test zero signal necessary" → wymuś stan 0 na czujniku (np. wciśnij E-STOP)
4. Po wymuszeniu stanu 0 i zwolnieniu → diody migają naprzemiennie (czerwona/zielona) = gotowość do resetu
5. Naciśnij przycisk reset → reintegracja kanałów → normal operation

📚 **Źródła:**
- [`sources/pdfs/extracted/SIMATIC Safety - Konfiguracja i programowanie (2)_extracted.txt`](sources/pdfs/extracted/SIMATIC%20Safety%20-%20Konfiguracja%20i%20programowanie%20(2)_extracted.txt) (str. 54–55) — parametry Discrepancy behavior, Reintegration after discrepancy error
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 22) — discrepancy time, cross-circuit monitoring
- [`transcripts/controlbyte/NA_Jak działa PLC Safety - Wykrywanie zwarć do 0V, rozbieżności w ocenie 1oo2.txt`](transcripts/controlbyte/NA_Jak%20działa%20PLC%20Safety%20-%20Wykrywanie%20zwarć%20do%200V,%20rozbieżności%20w%20ocenie%201oo2.txt) — demonstracja parametrów 1oo2, discrepancy time, test zero signal
- Norma: EN ISO 13849-1 (wymagania dla ewaluacji dwukanałowej Cat.3/Cat.4)

---

