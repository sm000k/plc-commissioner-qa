## 3. MODUŁY F-DI / F-DO — OKABLOWANIE I PARAMETRY

### 3.1. Co to jest F-DI i jak różni się od standardowego DI?  🔴

F-DI (Fail-safe Digital Input) to moduł wejść bezpieczeństwa. Różnice od standardowego:
- VS* (pulse testing) — impulsowe zasilanie do diagnostyki okablowania
- Obsługa dwukanałowych czujników Safety (1oo2) z discrepancy time
- Cross-circuit detection — wykrywanie zwarć między kanałami
- Komunikacja przez PROFIsafe z CRC do F-CPU
- Self-test kanałów w tle
Moduły ET200SP F-DI, ET200MP F-DI, ET200eco F-DI, S7-1200 SM 1226 F-DI.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.2. Co to jest VS* (pulse testing) i jak wykrywa usterki?  🔴

VS* to wyjście zasilające na module F-DI które wysyła krótkie impulsy testowe zamiast stałego napięcia. Czujnik zasilany jest tymi impulsami, a sygnał wraca na wejście razem z impulsami.
Moduł analizuje czy impulsy wróciły:
- Brak impulsów → zerwanie przewodu lub zwarcie do masy
- Impulsy cały czas bez przerwy → zwarcie do 24V
To mechanizm cross-circuit detection zapewniający Diagnostics Coverage (DC) bez dodatkowego okablowania. VS* z cross-circuit detection zapewnia DC ≥ 99% (Diagnostic Coverage) — warunek konieczny do osiągnięcia kategorii Cat.4 i Performance Level e (PL e) wymaganego przez SIL 3 per ISO 13849-1.

![ET 200 F-DI: cross-circuit, wire break i short-circuit detection](images/safety/01d_safety_brochure_p4.png)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.3. Dlaczego czujniki Safety podłącza się jako NC (normalnie zamknięty)?  🔴

Zasada bezpieczna (fail-safe): zerwanie kabla, przepalenie bezpiecznika, uszkodzenie czujnika → obwód otwarty → sygnał 0 → system Safety traktuje to jako zadziałanie i zatrzymuje maszynę.
Przy NO (normalnie otwartym): zerwanie kabla = brak sygnału = maszyna nie wie o zagrożeniu → niebezpieczeństwo.
NC to zasada 'fail-safe by design' wymagana przez normy bezpieczeństwa.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.4. Co to jest discrepancy time i jak go konfigurujesz?  🟡

Discrepancy time to maksymalny czas w którym dwa kanały czujnika 1oo2 mogą pokazywać różne wartości bez generowania błędu. Przykład: przy otwieraniu osłony mechanicznej jeden styk reaguje 15ms wcześniej niż drugi — to normalne i fizyczne.
Konfigurujesz w TIA Portal: właściwości modułu F-DI → parametry kanału → Discrepancy time (typowo 10–200ms w zależności od czujnika).
Zbyt krótki → fałszywe błędy. Zbyt długi → późne wykrycie uszkodzenia.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.5. Co to jest substitute value na F-DO i kto decyduje o jego wartości?

Substitute value to wartość którą przyjmuje wyjście F-DO po przejściu modułu w passivation (stan błędu). Konfigurujesz w TIA Portal we właściwościach kanału F-DO: wartość 0 lub 1.
Decyduje inżynier projektu na podstawie analizy bezpieczeństwa — nie Siemens. Przykłady: napęd → 0 (stop), zawór bezpieczeństwa → może być 1 (pozostaje otwarty), pompa chłodząca → może być 1 (chłodzi nadal).

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.6. Co to jest pm switching i pp switching — różnica?  🟡

pm switching (plus-minus): F-DO przełącza linię P (plus, 24V) do aktuatora. Masa (M) jest wspólna. Prostsze okablowanie, niższy koszt.
pp switching (plus-plus): F-DO przełącza obie linie P+ do aktuatora, bez wspólnej masy. Wyższy poziom bezpieczeństwa — zwarcie jednej linii do masy nie powoduje przypadkowego zadziałania. Używane przy wyższych wymaganiach SIL/PL.
F-PM-E (Power Module) w ET 200SP/S może realizować oba tryby.

**pm-switching — schemat ET 200SP:**
![pm-switching ET 200SP via F-PM-E](images/safety/06a_wiring_pm_switching_p6.png)

**pp-switching — schemat ET 200SP:**
![pp-switching ET 200SP via F-PM-E](images/safety/06b_wiring_pp_switching_p7.png)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.7. Co to jest F-PM-E i do czego służy?

F-PM-E (Fail-safe Power Module E) to moduł zasilający Safety w systemie ET 200SP/S. Umożliwia bezpieczne odcięcie zasilania grupy standardowych modułów DO przez sygnał Safety — bez ich fizycznej wymiany na moduły F.
Działanie: F-CPU nakazuje F-PM-E odciąć 24V dla grupy standardowych DQ → wszystkie wyjścia grupy idą na 0 (PM switching do SIL2/Cat.3/PLd).
Tańsze rozwiązanie niż wymiana wszystkich DQ na F-DQ.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.8. Jak bezpiecznie wyłączyć standardowe moduły wyjść przez Safety?

Trzy główne metody (wg dokumentu Siemens 39198632):
- Safety Relay (np. 3SK1) — zewnętrzny przekaźnik bezpieczeństwa odcina zasilanie grupy DQ. Niezależne od PLC.
- F-PM-E (pm lub pp switching) — moduł F-PM-E w tej samej stacji ET200 odcina zasilanie grupy standardowych DQ (SIL2/Cat.3/PLd).
- F-DO + zewnętrzny przekaźnik — F-DO steruje cewką przekaźnika który odcina zasilanie modułów standardowych. Feedback z przekaźnika do DI.
Ważne: standardowe moduły DI nie mogą być używane do odczytu sygnałów Safety — wymagane F-DI.

**Schematy okablowania — Safety Relay i ET200MP/S7-1500:**
![Figure 3-1: Safety Relay (3SK1) PM-switching, ET200MP S7-1500 — DQ odcięte przez przekaźnik do SIL1/Cat.2/PLc i SIL2/Cat.3/PLd](images/safety/06e_wiring_et200mp_p10.png)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 3.9. Jak F-CPU reaguje na typowe awarie wejść dwukanałowych (1oo2)?

Moduł F-DI, skonfigurowany do oceny dwukanałowej (1oo2), monitoruje sygnały z dwóch niezależnych kanałów i reaguje na różne typy awarii, aby zapewnić bezpieczny stan maszyny.
- **Zwarcie do potencjału 0 V (M):**
  - **Reakcja:** Kanał zostaje spaszywowany, styczniki rozłączone.
  - **Błąd diagnostyczny:** "Overload or internal sensor supply short circuit to ground".
  - **Reset:** Po usunięciu zwarcia, wymagany jest reset układu.
- **Zwarcie międzykanałowe:**
  - **Reakcja:** Cały moduł zapala się na czerwono, zgłaszając błąd.
  - **Błąd diagnostyczny:** "Internal sensor supply short circuit to P" lub "Short-circuit of two encoder supplies".
  - **Reset:** Po usunięciu zwarcia, wymagany jest reset układu.
- **Rozbieżność sygnału (Discrepancy failure):**
  - **Reakcja:** Pojawia się błąd "Discrepancy failure", wskazany jest kanał, na którym wystąpiła awaria.
  - **Przyczyna:** Utrata ciągłości obwodu w jednym z kanałów (np. uszkodzenie styku w E-STOP, kurtynie bezpieczeństwa, skanerze).
  - **Funkcja diagnostyczna:** Sprawdzenie równoczesności zadziałania sygnałów jest podstawową funkcją diagnostyczną dla urządzeń elektromechanicznych.
  - **Reset:** Po podłączeniu obwodu, diody migają naprzemiennie (czerwona i zielona), sygnalizując możliwość resetu/reintegracji.
Praktyczne wskazówki:
- W przypadku błędu rozbieżności, jeśli parametr "Reintegration after discrepancy error" jest ustawiony na "Test zero signal necessary", operator musi najpierw wymusić stan zerowy na czujniku (np. wcisnąć E-STOP), a dopiero potem może zresetować układ. Jest to ważne dla starszych urządzeń, które mogą generować fałszywe błędy rozbieżności.
*Źródło: transkrypcje ControlByte*

### 3.10. Jakie parametry są kluczowe przy konfiguracji wejść dwukanałowych w sterowniku bezpieczeństwa?

Prawidłowa konfiguracja parametrów wejść dwukanałowych jest niezbędna do zapewnienia niezawodnego działania systemu bezpieczeństwa i uniknięcia niepotrzebnych błędów.
- **Ocena (Evaluation):**
  - Dla wejść dwukanałowych często stosuje się ocenę "one out of two" (1oo2).
- **Discrepancy time (czas rozbieżności):**
  - **Definicja:** Maksymalny dopuszczalny czas między zmianą stanu sygnałów na dwóch kanałach wejściowych.
  - **Znaczenie:** Należy go dobrać precyzyjnie. Zbyt mały czas może generować niepotrzebne błędy i pasywację kanałów (np. przy E-STOP, wyłącznikach krańcowych). Zbyt długi czas zwiększa zwłokę w wykryciu sytuacji awaryjnej.
  - **Dobór:** Najlepiej określić go na podstawie testów.
- **Reintegracja po błędzie rozbieżności (Reintegration after discrepancy error):**
  - **Opcja "Test zero signal necessary":** W przypadku błędu rozbieżności, aby zresetować kanały, należy najpierw doprowadzić do stanu zerowego sygnał z czujnika (np. wcisnąć E-STOP, a następnie go odciągnąć).
  - **Znaczenie praktyczne:** Ten parametr wpływa na sposób obsługi stanowiska przez operatora. Urządzenia z kilkuletnim stażem mogą generować błędy rozbieżności, a ta opcja wymusza fizyczne potwierdzenie stanu bezpiecznego.
Praktyczne wskazówki:
- W przypadku błędu rozbieżności, jeśli "Test zero signal necessary" jest aktywne, diody zgłaszają błąd i brak możliwości reintegracji, dopóki nie zostanie wymuszony stan niski na obu kanałach, a dopiero potem można nacisnąć przycisk reset.
*Źródło: transkrypcje ControlByte*

---

