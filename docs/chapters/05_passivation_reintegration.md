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

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 5.2. Dlaczego moduł nie wraca automatycznie po usunięciu błędu?

Celowo — zasada **"no silent recovery"** w systemach Safety.
Operator musi potwierdzić że sytuacja jest bezpieczna zanim maszyna wznowi pracę.

**Mechanizm reintegracji:**
1. Usuwasz przyczynę błędu *(naprawiasz kabel, naprawiasz czujnik)*
2. Moduł ustawia `ACK_REQ = TRUE` → widoczny w Watch Table
3. Operator naciska **"Reset Safety"** na HMI/kasecie
4. Generowany jest impuls na `ACK_NEC` *(zbocze narastające, 1 cykl PLC)*
5. Moduł reintegruje się → `PASS_OUT = FALSE`

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 5.3. Moduł nie wychodzi z passivation — co sprawdzasz?

**Checklista:**
- [ ] Błąd fizyczny faktycznie usunięty? *(sprawdź kabel / czujnik multimetrem)*
- [ ] Brak aktywnych błędów w diagnostyce TIA Portal?
- [ ] Sygnał `ACK_NEC` podany jako **impuls** *(zbocze)*, nie poziom stały?
- [ ] F-CPU w trybie **RUN Safety** *(nie `LOCK`)*?
- [ ] `F-monitoring time` nie przekroczony *(przeciążona sieć PROFINET)*?
- [ ] Brak drugiego ukrytego błędu na innym kanale modułu?

> ⚠️ **S7-1200/S7-1500:** tradycyjny bit `QBAD` zastąpiony przez **value status**
> — logika odwrócona: `FALSE` = aktywne wartości zastępcze | `TRUE` = dane prawidłowe

---

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
### 5.4. Co to jest ACK_REQ i ACK_NEC w praktyce?  🔴

| Zmienna | Kierunek | Opis |
|---------|----------|------|
| `ACK_REQ` | Wyjście bloku F | Auto `TRUE` gdy moduł wymaga resetu — widoczny w Watch Table |
| `ACK_NEC` | Wejście bloku F | Impuls *(zbocze narastające)* potwierdzający usunięcie błędu |

**Schemat logiki Reset Safety (LAD):**
```
Reset_HMI: --|P|-- [ACK_NEC]   ← impuls z przycisku, tylko 1 cykl PLC
```

> ⚠️ `ACK_NEC` **nie może być** sygnałem stałym `TRUE` — tylko impuls zboczowy!

> 💡 **Zbiorcza reintegracja całej stacji:** blok `ACK_GL` *(STEP 7 Safety Advanced)*
> generuje zbiorczy impuls do **wszystkich** F-I/O w grupie runtime jednocześnie.
> Stosuj po wymianie modułu lub awarii sieci PROFINET całej stacji.

*[PRAWDOPODOBNE] — na podstawie wiedzy domenowej Siemens*
