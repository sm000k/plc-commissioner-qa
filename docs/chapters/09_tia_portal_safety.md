## 9. TIA PORTAL — SAFETY PRAKTYKA

### 9.1. Jak wygląda struktura programu Safety w TIA Portal?

Program Safety w TIA Portal składa się z:
- F-OB (Safety Main OB, np. Main_Safety_RTG1) — główny cykl Safety, odpowiednik OB1 dla Safety
- F-FB / F-FC — bloki logiki Safety programowane w F-LAD lub F-FBD
- F-DB — instancje bloków, generowane automatycznie przez TIA Portal
Kompilacja Safety generuje CRC dla każdego bloku i collective signature dla całości. Program Safety jest logicznie oddzielony od standardowego OB1.

### 9.2. Jak przekazujesz sygnał z obszaru F do standardowego OB?

Z F do standard: poprzez F-DB — zmienne wynikowe Safety są dostępne do odczytu ze standardowego programu. Przykład: F-DB.SafetyOK (BOOL) możesz odczytać w OB1 do wyświetlenia na HMI lub logowania.
Ze standard do F: przez dedykowane zmienne 'safe interlock' — standardowy program może pisać do specjalnych zmiennych które F-CPU traktuje jako niezaufane (nie używa do decyzji Safety).
Bezpośredni zapis ze standardowego do F-DB — zablokowany. Zalecany wzorzec Siemens (wg doc. 21064024): dwa globalne DB — DataFromSafety (zapisuje F-program, czyta standard) i DataToSafety (zapisuje standard, czyta F-program). Synchronizacja przez konsekwentne używanie tych DB eliminuje ryzyko niezamierzonego wpływu programu standardowego na logikę Safety.

### 9.3. Jak wgrywasz zmianę w programie Safety?  🟡

Modyfikujesz logikę F → kompilacja → TIA Portal ostrzega o zmianie F-signature → wymagane potwierdzenie zmiany (kliknięcie Accept lub hasło Safety) → wgranie do CPU (Download) → CPU weryfikuje collective signature → Safety RUN.
Każda zmiana jest logowana z datą i użytkownikiem w projekcie TIA Portal.

### 9.4. Co się dzieje gdy F-signature nie zgadza się po wgraniu?

F-CPU nie uruchamia programu Safety i zgłasza błąd 'F-signature mismatch'. Przyczyny: niekompletne wgranie, wgranie programu z innego projektu, ingerencja w F-DB.
Rozwiązanie: skompiluj projekt ponownie (Compile → Software) i wykonaj pełne wgranie (Download to device → All). Nie próbuj edytować F-DB ręcznie.

### 9.5. Jak czytasz diagnostykę F-modułu online w TIA Portal?  🟡

Online → w drzewie projektu rozwiń moduł F → Device diagnostics → zakładka Diagnostics.
Widzisz: status passivation (TAK/NIE), aktywne błędy kanałów (urwanie, zwarcie, discrepancy), status komunikacji PROFIsafe, liczniki błędów.
Alternatywnie: Watch Table z zmiennymi F-DB modułu (DIAG, PASS_OUT, ACK_REQ, QBAD).

### 9.6. Co to jest PLCSIM i jak pomaga w Safety?

PLCSIM to symulator TIA Portal umożliwiający testowanie programu PLC bez fizycznego sprzętu. Obsługuje również programy Safety — możesz symulować działanie F-CPU, testować logikę Safety, weryfikować ACK, passivation, reintegration.
Oszczędza czas commissioning bo błędy logiczne wyłapujesz przed wyjazdem do klienta. Nie zastępuje testów na prawdziwym sprzęcie dla certyfikacji — ale znacznie skraca czas FAT.

### 9.7. Co to jest Safety Matrix w TIA Portal i jak z niej korzystasz?  🟢

Safety Matrix (dostępna w STEP 7 Safety Advanced V15+) to graficzne narzędzie do definiowania logiki Safety w formie tabeli: **wiersze = zdarzenia wyzwalające** (triggery), **kolumny = funkcje bezpieczeństwa** (aktuatory/napędy). Przecięcie wiersza z kolumną określa czy dane zdarzenie aktywuje daną funkcję Safety.

**Kiedy używasz Safety Matrix:**
- Złożone maszyny z wieloma strefami Safety i zależnościami (np. e-stop strefy A wyłącza napędy A1, A2, A3, ale nie B — Safety Matrix to pokazuje na jeden rzut oka).
- Dokumentacja wymagana przez klienta lub rzeczoznawcę — matrix jest czytelna dla osób nie znających kodu LAD/FBD.
- Zamiast pisać ręcznie logikę AND/OR w F-FB, matrix generuje ją automatycznie.

**Praca z Safety Matrix w TIA Portal:**
1. W drzewie projektu: `Safety Administration → Safety Matrix → Add new Safety Matrix`.
2. W edytorze matrix: dodajesz kolumny (funkcje Safety: STO napędu, zawór bezp., blokada ryglowania) i wiersze (wyzwalacze: E-STOP, kurtyna, krańcówka).
3. W komórce przecięcia klikasz: `Active` (zadziała), `Not active` (ignoruje), `Deactivate` (dezaktywuje funkcję).
4. Opcjonalnie definiujesz warunki resetu per funkcja Safety: automatyczny lub wymagający ACK.
5. `Compile` — TIA Portal generuje automatycznie F-bloki z logiką odpowiadającą matrix.

**Ograniczenia:** Safety Matrix nie zastępuje pełnej logiki sekwencyjnej (np. muting z oknem czasowym, SS1 z rampą) — te programujesz nadal w F-FB. Matrix nadaje się dla logiki kombinacyjnej (A AND B → zatrzymaj napęd C).

**Na rozmowie:** Wspomnij, że matrix jest przydatna zarówno jako narzędzie projektowania, jak i dokumentacji do FAT/SAT — klient dostaje tabelę zamiast kodu.

### 9.8. Jak generujesz Safety Report / certyfikat Safety w TIA Portal i co zawiera?  🟢

Safety Report (raport Safety) to dokument generowany przez TIA Portal potwierdzający konfigurację i collective signature programu Safety — wymagany przy odbiorze maszyny i audycie bezpieczeństwa.

**Generowanie w TIA Portal:**
1. `Safety Administration` (lewy panel projektu) → `Safety program` → `Print / Save Safety program`.
2. Wybierz format: PDF lub wydruk (HTML).
3. TIA Portal generuje raport zawierający:

**Zawartość raportu Safety:**
- **Collective signature** (podpis zbiorczy) — unikalny skrót całego programu Safety. Zmiana czegokolwiek w logice = zmiana podpisu. Raport z podpisem jest dowodem że program nie był modyfikowany po certyfikacji.
- **Lista bloków F** z indywidualnymi F-signatures i datami ostatniej modyfikacji.
- **Lista F-peripherals** (moduły F-DI/F-DO/napędy Safety) z ich F-Address i F-monitoring time.
- **Parametry Safety** każdego modułu: discrepancy time, substitute values, ewaluacja kanałów.
- **Historia zmian** (Change log) — kto i kiedy modyfikował program Safety (TIA Portal śledzi zmiany per użytkownik).

**Kiedy generujesz raport:**
- Po zakończeniu kodowania Safety, przed FAT — jako baseline dla testów.
- Po każdej zmianie w Safety programie — nowy raport z nowym podpisem.
- Na żądanie klienta lub rzeczoznawcy TÜV/UDT.

**Ważne:** Raport Safety ≠ certyfikat bezpieczeństwa maszyny. To dokumentacja techniczna PLC. Certyfikat maszyny (CE, ocena ryzyka) wystawia producent maszyny lub notyfikowana jednostka — nie TIA Portal.

