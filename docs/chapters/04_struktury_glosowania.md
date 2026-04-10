## 4. STRUKTURY GŁOSOWANIA — 1oo1/1oo2/2oo2/2oo3


### 4.1. Wyjaśnij notację XooY i podaj przykład każdej architektury.  🟡

XooY = **X z Y**: ile (X) z dostępnych (Y) kanałów musi zadziałać aby system zareagował.

| Architektura | Definicja | Dostępność | Bezpieczeństwo | Typowe zastosowanie |
|-------------|-----------|-----------|---------------|---------------------|
| **1oo1** | 1 czujnik — wystarczy | Wysoka | Podstawowe | SIL1, proste maszyny |
| **1oo2** | 2 czujniki — wystarczy JEDEN | Niska (fałszywe stopy) | Wysokie | E-stopy, osłony — SIL2/3 |
| **2oo2** | 2 czujniki — wymagane OBA | Wysoka | Niższe (cichy błąd!) | Procesy ciągłe, kosztowne stopy |
| **2oo3** | 3 czujniki — wymagane 2 z 3 | Balans | Balans | Przemysł procesowy, ciśnienie/temp. |

> ⚠️ **2oo2 pułapka:** uszkodzenie jednego czujnika (sygnalizuje ciągle OK) → system może nie zadziałać gdy potrzeba. Wymagany monitoring DC!

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 4.2. Kiedy wybierasz 1oo2 a kiedy 2oo2?  🟡

**1oo2** gdy priorytet to **bezpieczeństwo** (zatrzymanie przy pierwszym sygnale):
- Osłony maszyn, e-stopy przy prasach
- Wyższy SIL, akceptowalne fałszywe zatrzymania

**2oo2** gdy priorytet to **dostępność** (unikanie fałszywych stopów):
- Procesy chemiczne gdzie zatrzymanie jest bardzo kosztowne
- Jedno "głuche" zadziałanie nie jest katastrofą

> ⚠️ Przy 2oo2: uszkodzenie jednego kanału *(zepsuty, ale nie zgłaszający błędu)* może spowodować że system nie zadziała gdy będzie potrzeba.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 4.3. Jak 1oo2 jest realizowane w module F-DI Siemens?

Dwa sygnały z dwóch czujników podłączone na dwa kanały tego samego modułu F-DI (lub dwóch osobnych modułów). Moduł F-DI porównuje oba sygnały:
- Oba zgodne → OK
- Różnica przekracza `discrepancy time` → błąd → <span style="color:#c0392b">**passivation**</span> lub alarm

> 💡 Ewaluację 1oo2 wykonuje **sam moduł F-DI sprzętowo** — odciążając F-CPU. Wynik trafia do programu Safety jako jeden bezpieczny sygnał BOOL.

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 4.4. Jak F-CPU reaguje na błąd rozbieżności sygnału (Discrepancy Failure) w konfiguracji 1oo2?
Moduł F-DI wykrywa błąd rozbieżności sygnału, gdy jeden z dwóch kanałów skonfigurowanych w ocenie 1oo2 straci ciągłość obwodu lub sygnały nie zadziałają równocześnie w określonym czasie. Jest to podstawowa funkcja diagnostyczna dla urządzeń elektromechanicznych i czujników z wyjściami tranzystorowymi.
- Błąd "Discrepancy failure" jest zgłaszany w buforze diagnostycznym PLC, wskazując kanał awarii.
- Po usunięciu przyczyny błędu (np. ponownym podłączeniu obwodu), diody modułu naprzemian migają na czerwono i zielono, sygnalizując możliwość resetu reintegracji.
- Discrepancy time (np. 50 ms) musi być precyzyjnie dobrany, aby uniknąć fałszywych błędów lub zbyt długiej zwłoki w wykryciu awarii.
*Źródło: transkrypcje ControlByte*

### 4.5. Jakie są scenariusze awaryjne wykrywane przez moduł F-DI w układzie dwukanałowym 1oo2?
Moduł F-DI w układzie dwukanałowym 1oo2 jest w stanie wykryć różne scenariusze awaryjne, które mogą prowadzić do niebezpiecznych sytuacji, zapewniając wysoką diagnostykę.
- **Zwarcie do potencjału 0 V (zwarcie do masy):** Moduł zgłasza błąd "Overload or internal sensor supply short circuit to ground", pasywuje kanał i rozłącza styczniki.
- **Zwarcie międzykanałowe (do P):** Moduł zgłasza błąd "Internal sensor supply short circuit to P" lub "Short-circuit of two encoder supplies", cały moduł zapala się na czerwono.
- **Rozbieżność sygnału (Discrepancy failure):** Wykrywana, gdy jeden z kanałów straci ciągłość obwodu lub sygnały nie zadziałają równocześnie, co jest kluczowe dla urządzeń z mechanicznymi stykami (E-STOP, wyłączniki krańcowe) lub wyjściami tranzystorowymi.
*Źródło: transkrypcje ControlByte*

### 4.6. Jak parametr "Reintegration after discrepancy error" wpływa na obsługę błędu rozbieżności sygnału?
Parametr "Reintegration after discrepancy error" w konfiguracji modułu safety określa, czy po wystąpieniu błędu rozbieżności sygnału wymagane jest doprowadzenie sygnału do stanu zerowego przed wykonaniem resetu.
- Jeśli wybrano opcję "Test zero signal necessary", operator musi wymusić stan zerowy na czujniku (np. wcisnąć i odciągnąć E-STOP) zanim możliwy będzie reset reintegracji.
- Ten parametr jest istotny dla sposobu obsługi stanowiska przez operatora, szczególnie w przypadku starszych urządzeń, które mogą generować sporadyczne błędy rozbieżności.
- Reset reintegracji kanałów safety w sterowniku PLC jest odrębny od resetu funkcji bezpieczeństwa, który wymaga innej logiki programowania.
*Źródło: transkrypcje ControlByte*

### 4.7. Co to jest discrepancy time (czas rozbieżności) w F-DI 1oo2 i co się dzieje gdy zostanie przekroczony? 🔴
Discrepancy time (czas rozbieżności) to maksymalny czas, przez jaki oba kanały 1oo2 mogą mieć różne wartości logiczne bez wywołania błędu. Parametr konfigurowany w TIA Portal dla każdego F-DI z oceną 1oo2.
- Domyślnie: 100 ms — oba sygnały muszą zmienić stan w tym oknie
- Przekroczenie → F-DI przechodzi w stan pasywny (passivation), wyjście F-DO = substitute value
- Typowa przyczyna: mechaniczne opóźnienie styku bezpieczeństwa lub błąd okablowania
- Konfiguracja: właściwości modułu F-DI → zakładka „Input" → „Discrepancy time [ms]"
- W diagnostyce: alarm rozbieżności widoczny w buforze diagnostycznym CPU (F_LADDR.DIAG) ⚠️ DO WERYFIKACJI: konkretny numer kodu alarmu — sprawdź w SIMATIC Safety System Manual lub buforze diagnostycznym TIA Portal online

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 4.8. Jak moduł F-DI ET200SP wykrywa zwarcie między kanałami (cross-circuit detection) w obwodzie 1oo2? 🟡
Detekcja cross-circuit (zwarcia między kanałami) to mechanizm pozwalający wykryć zwarcie przewodu kanału 1 do kanału 2 dzięki testowym impulsom wyjść testowych (T-signal).
- T1 i T2 generują impulsy testowe z różną fazą (wzajemnie rozłączne)
- Wejścia odczytują sygnał z powrotem przez czujnik
- Zwarcie między kanałami = impuls T1 pojawia się na wejściu kanału 2 → błąd cross-circuit
- Wymaga okablowania z wyjść testowych (T1, T2) przez czujnik do wejść (DI0.0, DI0.1)
- Nie działa przy PM-switching bez wyjść testowych (wtedy detekcja cross-circuit jest ograniczona)

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
