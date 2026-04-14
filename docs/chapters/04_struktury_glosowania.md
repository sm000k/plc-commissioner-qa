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

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/); IEC 61508-2 §7.4.4 (struktury redundancji); EN ISO 13849-1 Aneks K (architektury 1oo1, 1oo2, 2oo2)]*
### 4.2. Kiedy wybierasz 1oo2 a kiedy 2oo2?  🟡

**1oo2** gdy priorytet to **bezpieczeństwo** (zatrzymanie przy pierwszym sygnale):
- Osłony maszyn, e-stopy przy prasach
- Wyższy SIL, akceptowalne fałszywe zatrzymania

**2oo2** gdy priorytet to **dostępność** (unikanie fałszywych stopów):
- Procesy chemiczne gdzie zatrzymanie jest bardzo kosztowne
- Jedno "głuche" zadziałanie nie jest katastrofą

> ⚠️ Przy 2oo2: uszkodzenie jednego kanału *(zepsuty, ale nie zgłaszający błędu)* może spowodować że system nie zadziała gdy będzie potrzeba.

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/); EN ISO 13849-1 §6.2.9 (common cause failure — 2oo2); IEC 62061 §6.7.6]*
### 4.3. Jak 1oo2 jest realizowane w module F-DI Siemens?

Dwa sygnały z dwóch czujników podłączone na dwa kanały tego samego modułu F-DI (lub dwóch osobnych modułów). Moduł F-DI porównuje oba sygnały:
- Oba zgodne → OK
- Różnica przekracza `discrepancy time` → błąd → <span style="color:#c0392b">**passivation**</span> lub alarm

> 💡 Ewaluację 1oo2 wykonuje **sam moduł F-DI sprzętowo** — odciążając F-CPU. Wynik trafia do programu Safety jako jeden bezpieczny sygnał BOOL.

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. F-DI channel evaluation 1oo2](https://support.industry.siemens.com/cs/document/109751404/)]*
### 4.4. Jak monitorowana jest rozbieżność sygnałów w strukturze 1oo2 i jakie awarie wykrywa moduł F-DI? 🔴

Monitoring rozbieżności (discrepancy monitoring) to kluczowy mechanizm diagnostyczny struktury głosowania 1oo2 — porównuje sygnały z dwóch niezależnych kanałów i wykrywa, gdy przestają się zgadzać. Jest to podstawa bezpieczeństwa dla urządzeń elektromechanicznych (E-STOP, wyłączniki krańcowe, osłony) i czujników tranzystorowych.

**Discrepancy time i mechanizm wykrywania:**
- **Discrepancy time** = maksymalny czas, przez jaki kanały 1oo2 mogą mieć różne stany logiczne bez wygenerowania błędu. Konfiguracja: TIA Portal → właściwości F-DI → zakładka „Input" → „Discrepancy time [ms]".
- Po przekroczeniu discrepancy time → moduł F-DI zgłasza **„Discrepancy failure"** w buforze diagnostycznym (wskazując kanał awarii) → **passivation** kanału lub całego modułu (zależnie od parametru „Behavior after channel fault") → wyjścia F-DO przyjmują substitute values (0).
- **Dobór czasu:** Zbyt krótki → fałszywe passivation (np. styki E-STOP nie przełączają się idealnie jednocześnie). Zbyt długi → większa zwłoka w wykryciu awarii (np. zespawanego styku). Praktyka: przetestuj czujnik kilkanaście razy i dobierz na podstawie wyników. Typowe wartości: 10–200 ms.

**Trzy scenariusze awarii wykrywane w 1oo2:**

| Awaria | Komunikat diagnostyczny | Zakres passivation | LED na module |
|--------|------------------------|-------------------|---------------|
| Zwarcie do M (0V) | „Overload or internal sensor supply short circuit to ground" | Kanał lub moduł (parametr) | Kanał: czerwona |
| Zwarcie międzykanałowe (cross-circuit) | „Internal sensor supply short circuit to P" / „Short-circuit of two encoder supplies" | **Zawsze cały moduł** | Moduł: czerwona |
| Rozbieżność sygnału (discrepancy) | „Discrepancy failure" | Kanał lub moduł (parametr) | Miganie czerwona/zielona (po usunięciu przyczyny) |

**Reintegracja po discrepancy — parametr „Reintegration after discrepancy error":**
- **Automatic** — reintegracja natychmiast po zgodności kanałów.
- **Test zero signal necessary** — po błędzie operator musi najpierw wymusić stan 0 na obu kanałach (np. wcisnąć E-STOP, a potem odciągnąć), dopiero wtedy możliwy jest reset. Bez tego diody zgłaszają błąd i reintegracja jest zablokowana.
- Opcja „Test zero signal necessary" jest szczególnie istotna przy starszych urządzeniach (styki zużyte po latach pracy → sporadyczne błędy rozbieżności) — wymusza fizyczne potwierdzenie stanu bezpiecznego.

> ⚠️ **Uwaga:** Reset reintegracji kanałów F-DI (ACK_GL / operator acknowledge) to **nie to samo** co reset funkcji bezpieczeństwa (np. E-STOP reset w programie Safety). To dwa odrębne mechanizmy z różną logiką programowania.

📚 **Źródła:**
- [`sources/pdfs/extracted/SIMATIC Safety - Konfiguracja i programowanie (2)_extracted.txt`](sources/pdfs/extracted/SIMATIC%20Safety%20-%20Konfiguracja%20i%20programowanie%20(2)_extracted.txt) (str. 54–55) — parametry Discrepancy behavior, Reintegration after discrepancy error, Behavior after channel fault
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 22) — discrepancy time, passivation events
- [`transcripts/controlbyte/NA_Jak działa PLC Safety - Wykrywanie zwarć do 0V, rozbieżności w ocenie 1oo2.txt`](transcripts/controlbyte/NA_Jak%20działa%20PLC%20Safety%20-%20Wykrywanie%20zwarć%20do%200V,%20rozbieżności%20w%20ocenie%201oo2.txt) — demonstracja scenariuszy awarii 1oo2, konfiguracja discrepancy time i reintegracji
- Norma: EN ISO 13849-1 §6.2.9 (monitoring rozbieżności w Cat.3/Cat.4)

### 4.5. Jak moduł F-DI ET200SP wykrywa zwarcie między kanałami (cross-circuit detection) w obwodzie 1oo2? 🟡

Cross-circuit detection wykrywa zwarcie przewodu kanału A do kanału B w parze 1oo2 — awarię groźną, bo degrada dwukanałowy obwód do jednokanałowego (1oo1) bez widocznych objawów.

**Mechanizm — impulsy VS\* z przesunięciem czasowym:**
- Moduł F-DI ma dwa niezależne wyjścia sensor supply: **VS0** (zasilanie kanałów 0–3) i **VS2** (zasilanie kanałów 8–11). To są wyjścia zasilania czujnika generujące krótkie impulsy testowe (VS\* pulse testing).
- VS0 i VS2 wysyłają impulsy w **różnych oknach czasowych** (nigdy jednocześnie):
  - Okno T1: VS0 wysyła impuls → kanał A widzi impuls, kanał B — cisza
  - Okno T2: VS2 wysyła impuls → kanał B widzi impuls, kanał A — cisza
- **Kanały spięte (cross-circuit):** impuls VS0 pojawia się na wejściu kanału B w oknie T1 (zamiast T2) → moduł wykrywa impuls w złym oknie → błąd cross-circuit → **passivation całego modułu**

**Konfiguracja w TIA Portal:**
- Właściwości modułu F-DI → „Short-circuit test" → **Activate** (osobno per sensor supply 0 i sensor supply 2)
- **Domyślnie wyłączone** — trzeba aktywować, aby osiągnąć DC ≥ 99% wymagane dla Cat.4 / PL e / SIL 3
- Wymagane prawidłowe okablowanie: czujnik kanału A zasilany z VS0, czujnik kanału B z VS2 — nigdy oba z tego samego VS

> 💡 Szczegółowy opis VS\* pulse testing, wykrywania zwarć do L+/M i schematy okablowania → patrz pytanie 3.1 i 3.2.

📚 **Źródła:**
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 11–12) — aktywacja short-circuit test dla sensor supply 0 i 2, konfiguracja kanałów E-STOP
- [`sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt`](sources/pdfs/extracted/39198632_Wiring_Example_en_extracted.txt) — schematy okablowania F-DI z VS0/VS2
- Norma: EN ISO 13849-1 (DC ≥ 99% dla Cat.4)
