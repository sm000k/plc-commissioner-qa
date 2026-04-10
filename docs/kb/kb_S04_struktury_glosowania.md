<!-- Źródło: knowledge_base_controlbyte.md -->

## 4. Struktury głosowania (1oo1 / 1oo2 / 2oo2 / 2oo3)

### Co oznacza struktura głosowania "1oo2" w kontekście bezpieczeństwa?
Odpowiedź — Struktura głosowania "1oo2" (one out of two) oznacza, że system bezpieczeństwa monitoruje dwa niezależne sygnały z jednego urządzenia lub funkcji bezpieczeństwa, a do zadziałania funkcji bezpieczeństwa wystarczy, że jeden z tych sygnałów zmieni stan na bezpieczny.
- **Zasada działania:**
    - Oba kanały są aktywne i monitorowane.
    - Jeśli jeden z kanałów straci ciągłość obwodu lub zgłosi błąd, system wykrywa rozbieżność sygnału ("Discrepancy failure").
    - W przypadku zwarcia do 0V lub zwarcia międzykanałowego, system również reaguje, pasywując kanał lub zgłaszając błąd modułu.
- **Cel:** Zwiększenie niezawodności i diagnostyki w porównaniu do pojedynczego kanału (1oo1). System jest w stanie wykryć uszkodzenie jednego z kanałów, zanim doprowadzi to do niebezpiecznej sytuacji.
*Praktyk: [W przypadku E-STOP lub wyłączników krańcowych, jeśli jeden styk się uszkodzi, a drugi jest redundantny, sterownik safety wykryje uszkodzenie urządzenia i może spowodować pasywację kanałów wejściowych.] [Safety]*

<!-- Źródło: knowledge_base_delta_v11.md -->

## SEKCJA: 4. Struktury głosowania (1oo1 / 1oo2 / 2oo2 / 2oo3)

### Jak sterownik safety reaguje na błąd rozbieżności sygnału (Discrepancy Failure) w konfiguracji 1oo2?
Sterownik safety wykrywa błąd rozbieżności sygnału, gdy jeden z dwóch kanałów skonfigurowanych w ocenie 1oo2 straci ciągłość obwodu lub sygnały nie zadziałają równocześnie w określonym czasie. Jest to podstawowa funkcja diagnostyczna dla urządzeń elektromechanicznych i czujników z wyjściami tranzystorowymi.
- Błąd "Discrepancy failure" jest zgłaszany w buforze diagnostycznym PLC, wskazując kanał awarii.
- Po usunięciu przyczyny błędu (np. ponownym podłączeniu obwodu), diody modułu naprzemian migają na czerwono i zielono, sygnalizując możliwość resetu reintegracji.
- Czas rozbieżności (np. 50 ms) musi być precyzyjnie dobrany, aby uniknąć fałszywych błędów lub zbyt długiej zwłoki w wykryciu awarii.
*Źródło: transkrypcje ControlByte*

### Jakie są scenariusze awaryjne wykrywane przez moduł safety w układzie dwukanałowym 1oo2?
Moduł safety w układzie dwukanałowym 1oo2 jest w stanie wykryć różne scenariusze awaryjne, które mogą prowadzić do niebezpiecznych sytuacji, zapewniając wysoką diagnostykę.
- **Zwarcie do potencjału 0 V (zwarcie do masy):** Moduł zgłasza błąd "Overload or internal sensor supply short circuit to ground", pasywuje kanał i rozłącza styczniki.
- **Zwarcie międzykanałowe (do P):** Moduł zgłasza błąd "Internal sensor supply short circuit to P" lub "Short-circuit of two encoder supplies", cały moduł zapala się na czerwono.
- **Rozbieżność sygnału (Discrepancy failure):** Wykrywana, gdy jeden z kanałów straci ciągłość obwodu lub sygnały nie zadziałają równocześnie, co jest kluczowe dla urządzeń z mechanicznymi stykami (E-STOP, wyłączniki krańcowe) lub wyjściami tranzystorowymi.
*Źródło: transkrypcje ControlByte*

### Jak parametr "Reintegration after discrepancy error" wpływa na obsługę błędu rozbieżności sygnału?
Parametr "Reintegration after discrepancy error" w konfiguracji modułu safety określa, czy po wystąpieniu błędu rozbieżności sygnału wymagane jest doprowadzenie sygnału do stanu zerowego przed wykonaniem resetu.
- Jeśli wybrano opcję "Test zero signal necessary", operator musi wymusić stan zerowy na czujniku (np. wcisnąć i odciągnąć E-STOP) zanim możliwy będzie reset reintegracji.
- Ten parametr jest istotny dla sposobu obsługi stanowiska przez operatora, szczególnie w przypadku starszych urządzeń, które mogą generować sporadyczne błędy rozbieżności.
- Reset reintegracji kanałów safety w sterowniku PLC jest odrębny od resetu funkcji bezpieczeństwa, który wymaga innej logiki programowania.
*Źródło: transkrypcje ControlByte*

