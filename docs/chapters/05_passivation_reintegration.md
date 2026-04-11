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

| Zmienna | Kierunek | Kontekst | Opis |
|---------|----------|----------|------|
| `ACK_REQ` | Wyjście bloku F | F-FB / F-I/O | Auto `TRUE` gdy moduł/blok wymaga resetu — widoczny w Watch Table |
| `ACK_NEC` | Wejście bloku F | Safety-FB (ESTOP1, Two-hand, GuardMonitoring) | Impuls *(zbocze narastające)* potwierdzający usunięcie błędu w logice Safety |
| `ACK_REI` | Wejście F-I/O DB | Reintegracja modułów F-I/O po passivation | Impuls reintegracji konkretnego modułu F-I/O |

**Schemat logiki Reset Safety (LAD):**
```
Reset_HMI: --|P|-- [ACK_NEC]   ← impuls z przycisku, tylko 1 cykl PLC
```

> ⚠️ `ACK_NEC` **nie może być** sygnałem stałym `TRUE` — tylko impuls zboczowy!

> 💡 **Zbiorcza reintegracja całej stacji:** blok `ACK_GL` *(STEP 7 Safety Advanced)*
> generuje zbiorczy impuls do **wszystkich** F-I/O w grupie runtime jednocześnie.
> Stosuj po wymianie modułu lub awarii sieci PROFINET całej stacji.

*[ZWERYFIKOWANE - [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404), rozdz. ACK_NEC, ACK_REI, ACK_GL — impuls reintegracji](https://support.industry.siemens.com/cs/document/109751404/)]*
