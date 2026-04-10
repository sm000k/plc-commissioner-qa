<!-- Źródło: knowledge_base_controlbyte.md -->

## 3. Moduły F-DI / F-DO — okablowanie i parametry

### Jak sterownik bezpieczeństwa reaguje na typowe awarie wejść dwukanałowych (1oo2)?
Odpowiedź — Sterownik bezpieczeństwa, skonfigurowany do oceny dwukanałowej (1oo2), monitoruje sygnały z dwóch niezależnych kanałów i reaguje na różne typy awarii, aby zapewnić bezpieczny stan maszyny.
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
*Praktyk: [W przypadku błędu rozbieżności, jeśli parametr "Reintegration after discrepancy error" jest ustawiony na "Test zero signal necessary", operator musi najpierw wymusić stan zerowy na czujniku (np. wcisnąć E-STOP), a dopiero potem może zresetować układ. Jest to ważne dla starszych urządzeń, które mogą generować fałszywe błędy rozbieżności.] [Safety]*

### Jakie parametry są kluczowe przy konfiguracji wejść dwukanałowych w sterowniku bezpieczeństwa?
Odpowiedź — Prawidłowa konfiguracja parametrów wejść dwukanałowych jest niezbędna do zapewnienia niezawodnego działania systemu bezpieczeństwa i uniknięcia niepotrzebnych błędów.
- **Ocena (Evaluation):**
    - Dla wejść dwukanałowych często stosuje się ocenę "one out of two" (1oo2).
- **Czas rozbieżności (Discrepancy time):**
    - **Definicja:** Maksymalny dopuszczalny czas między zmianą stanu sygnałów na dwóch kanałach wejściowych.
    - **Znaczenie:** Należy go dobrać precyzyjnie. Zbyt mały czas może generować niepotrzebne błędy i pasywację kanałów (np. przy E-STOP, wyłącznikach krańcowych). Zbyt długi czas zwiększa zwłokę w wykryciu sytuacji awaryjnej.
    - **Dobór:** Najlepiej określić go na podstawie testów.
- **Reintegracja po błędzie rozbieżności (Reintegration after discrepancy error):**
    - **Opcja "Test zero signal necessary":** W przypadku błędu rozbieżności, aby zresetować kanały, należy najpierw doprowadzić do stanu zerowego sygnał z czujnika (np. wcisnąć E-STOP, a następnie go odciągnąć).
    - **Znaczenie praktyczne:** Ten parametr wpływa na sposób obsługi stanowiska przez operatora. Urządzenia z kilkuletnim stażem mogą generować błędy rozbieżności, a ta opcja wymusza fizyczne potwierdzenie stanu bezpiecznego.
*Praktyk: [W przypadku błędu rozbieżności, jeśli "Test zero signal necessary" jest aktywne, diody zgłaszają błąd i brak możliwości reintegracji, dopóki nie zostanie wymuszony stan niski na obu kanałach, a dopiero potem można nacisnąć przycisk reset.] [Safety]*

