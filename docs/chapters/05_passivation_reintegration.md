## 5. PASSIVATION, REINTEGRATION, ACK

### 5.1. Co to jest passivation i co się dzieje z wyjściami/wejściami?  🔴

<span style="color:#c0392b">**Passivation**</span> to stan błędu modułu F — wszystkie wyjścia przyjmują **substitute value** (zwykle `0`),
a wejścia raportowane są do F-CPU jako wartość bezpieczna (`0`).

**Przyczyny passivation:**
- Urwanie kabla lub zwarcie *(wykryte przez pulse testing)*
- Przekroczenie `discrepancy time` (ocena 1oo2)
- Utrata komunikacji PROFIsafe *(przekroczenie `F-monitoring time`)*
- Błąd wewnętrzny modułu
- Błąd spójności danych Safety

**W danych procesowych:** `PASS_OUT = TRUE` w F-DB modułu → widoczny w Watch Table

**Sekwencja sygnałów — passivation i reintegracja F-I/O:**
![Passivation timing diagram: PASS_OUT, ACK_REQ, ACK_REI, wartości procesowe](images/safety/05a_passivation_p189.png)

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), str. 189 — schemat passivation/reintegration](https://support.industry.siemens.com/cs/document/109751404/)]*
### 5.2. Dlaczego moduł nie wraca automatycznie po usunięciu błędu?

Celowo — zasada **"no silent recovery"** w systemach Safety.
Operator musi potwierdzić że sytuacja jest bezpieczna zanim maszyna wznowi pracę.

**Mechanizm reintegracji:**
1. Usuwasz przyczynę błędu *(naprawiasz kabel, naprawiasz czujnik)*
2. Moduł ustawia `ACK_REQ = TRUE` → widoczny w Watch Table
3. Operator naciska **"Reset Safety"** na HMI/kasecie
4. Generowany jest impuls na `ACK_REI` *(zbocze narastające, 1 cykl PLC)* — zmienna reintegracji F-I/O
5. Moduł reintegruje się → `PASS_OUT = FALSE`

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. Reintegracja F-I/O — ACK_REQ/ACK_REI](https://support.industry.siemens.com/cs/document/109751404/); [SIMATIC Safety Getting Started (Entry ID: pochodna A5E02714463, str. 42-43)](https://support.industry.siemens.com/cs/document/109779336/)]*
### 5.3. Moduł nie wychodzi z passivation — co sprawdzasz?

**Checklista:**
- [ ] Błąd fizyczny faktycznie usunięty? *(sprawdź kabel / czujnik multimetrem)*
- [ ] Brak aktywnych błędów w diagnostyce TIA Portal?
- [ ] Sygnał `ACK_REI` (reintegracja F-I/O) podany jako **impuls** *(zbocze)*, nie poziom stały?
- [ ] F-CPU w trybie **Safety mode activated** *(nie deactivated)*?
- [ ] `F-monitoring time` nie przekroczony *(przeciążona sieć PROFINET)*?
- [ ] Brak drugiego ukrytego błędu na innym kanale modułu?

> ⚠️ **S7-1200/S7-1500:** tradycyjny bit `QBAD` zastąpiony przez **value status**
> — logika odwrócona: `FALSE` = aktywne wartości zastępcze | `TRUE` = dane prawidłowe

---

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. QBAD/value status](https://support.industry.siemens.com/cs/document/109751404/)]*
### 5.4. Co to jest ACK_REQ, ACK_NEC i ACK_REI w praktyce?  🔴

W systemie Safety Siemens istnieją **dwa niezależne mechanizmy resetu**, które łatwo pomylić. Każdy ma swoją zmienną i swój kontekst. Najprościej zrozumieć je na konkretnym scenariuszu.

---

**Scenariusz: operator zrywa kabel E-STOP → naprawa → powrót do pracy**

**Krok 1 — Awaria:** Kabel do kanału E-STOP się zrywa. Moduł F-DI wykrywa wire break → **passivation** modułu → wyjścia F-DO = 0 → maszyna stoi.

**Krok 2 — Moduł mówi „potrzebuję resetu":** W F-I/O DB modułu pojawia się `ACK_REQ = TRUE`. To **wyjście informacyjne** (read-only) — moduł sam je ustawia, programista go nie steruje. Widoczne w Watch Table TIA Portal. Oznacza: „błąd usunięty, ale czekam na potwierdzenie operatora".

**Krok 3 — Reintegracja modułu F-I/O (ACK_REI):** Operator naciska przycisk „Reset" na kasecie → program Safety generuje **impuls** (zbocze narastające, 1 cykl PLC) na zmiennej `ACK_REI` w F-I/O DB tego modułu → moduł F-DI reintegruje się → `PASS_OUT = FALSE` → moduł znów przekazuje dane procesowe zamiast substitute values.

**Krok 4 — Reset funkcji Safety (ACK_NEC):** Moduł już działa, ale **blok ESTOP1** w programie Safety nadal blokuje wyjścia (bo E-STOP był aktywny). Blok ESTOP1 ma wejście `ACK_NEC` — operator musi nacisnąć przycisk „Reset Safety" → program generuje **impuls** na `ACK_NEC` → blok ESTOP1 zwalnia wyjście `Q` → maszyna może ruszyć.

---

**Podsumowanie — 3 zmienne, 3 różne role:**

| Zmienna | Co robi | Kto ją ustawia | Gdzie żyje | Kiedy potrzebna |
|---------|---------|----------------|------------|-----------------|
| `ACK_REQ` | **Informuje:** „moduł/blok czeka na reset" | Moduł F-I/O lub blok F automatycznie | F-I/O DB / wyjście bloku F | Zawsze po passivation — sprawdzaj w Watch Table |
| `ACK_REI` | **Reintegruje moduł F-I/O** po passivation | Programista (impuls z przycisku Reset) | F-I/O DB modułu (np. `"F-DI_1".ACK_REI`) | Po każdym błędzie sprzętowym (wire break, zwarcie, utrata PROFIsafe) |
| `ACK_NEC` | **Resetuje funkcję Safety** w bloku F | Programista (impuls z przycisku Reset Safety) | Wejście bloku ESTOP1 / SF_GuardMonitoring / SF_TwoHandControl | Po zadziałaniu funkcji Safety (E-STOP, osłona, kurtyna) |

**Kluczowa różnica:**
- `ACK_REI` = „naprawiłem kabel, moduł może wrócić do pracy" (**warstwa sprzętowa**)
- `ACK_NEC` = „sytuacja jest bezpieczna, maszyna może ruszyć" (**warstwa logiki Safety**)
- W praktyce operator naciska **jeden przycisk „Reset"**, a program Safety generuje oba impulsy we właściwej kolejności: najpierw `ACK_REI` (reintegracja modułu), potem `ACK_NEC` (reset funkcji)

**Zbiorcza reintegracja — ACK_GL:**
Zamiast ustawiać `ACK_REI` osobno dla każdego modułu F-I/O, możesz użyć bloku `ACK_GL` — generuje zbiorczy impuls reintegracji dla **wszystkich** modułów F-I/O w grupie F-runtime jednocześnie. Stosuj po awarii sieci PROFINET lub wymianie modułu, gdy wiele F-I/O wymaga reintegracji naraz.

```
// LAD — typowa logika resetu:
"Reset_Button": --|P|-- "ACK_GL_DB".ACK_GLOB    ← reintegracja WSZYSTKICH F-I/O
"Reset_Button": --|P|-- "ESTOP1_DB".ACK_NEC      ← reset funkcji E-STOP
```

> ⚠️ **KRYTYCZNE:** Zarówno `ACK_REI` jak i `ACK_NEC` muszą być **impulsami** (zbocze narastające, 1 cykl PLC). Sygnał stały `TRUE` = błąd programu Safety → F-CPU może odrzucić kompilację lub zgłosić Runtime Error.

📚 **Źródła:**
- [`sources/pdfs/extracted/safety_getting_started_en-US_extracted.txt`](sources/pdfs/extracted/safety_getting_started_en-US_extracted.txt) (str. 30–31) — Step 11: Programming ACK_GL for reintegration, parametr ACK_GLOB
- [`sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt`](sources/pdfs/extracted/21064024_E-Stop_SIL3_1500F_DOC_V7_0_1_en_extracted.txt) (str. 8) — ACK_GL instruction, events causing passivation
- [`sources/pdfs/extracted/safety_getting_started_en-US_extracted.txt`](sources/pdfs/extracted/safety_getting_started_en-US_extracted.txt) (str. 25) — SF_GuardMonitoring: ACK_NEC, ACK_REQ, ACK input
- Norma: EN ISO 13849-1 §6.3.5 (wymaganie ręcznego resetu po zadziałaniu funkcji Safety)
