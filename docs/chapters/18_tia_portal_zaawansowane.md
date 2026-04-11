## 18. TIA PORTAL — ZAAWANSOWANE FUNKCJE

### 18.1. Co to są Project Libraries vs Global Libraries i kiedy używasz każdej?

Biblioteki TIA Portal umożliwiają wielokrotne użycie i wersjonowanie bloków, typów PLC, ekranów HMI i UDT.

| Cecha | Project Library | Global Library |
|-------|----------------|----------------|
| **Zakres** | Jeden projekt TIA Portal | Wiele projektów (plik `.al17`) |
| **Zastosowanie** | Standardy jednej linii/zakładu | Firmowe szablony wieloprojektowe |
| **Przykłady** | FB napędu specyficzny dla klienta | SICAR Tec Units, certyfikowane F-bloki |
| **Wersjonowanie** | Tak (w ramach projektu) | Tak (niezależnie od projektu) |
| **Udostępnianie** | Export/import między projektami | Otwierasz plik `.al17` bezpośrednio |

**Workflow:**
1. Rozwijaj i testuj elementy w **Global Library**
2. Insertuj do **Project Library** w docelowym projekcie
3. Deploy do programu PLC jako instancje

> 💡 **Wersjonowanie:** zmiana w Global Library (nowa wersja FB) → w każdym projekcie znajdziesz alert "Update available" — aktualizujesz selektywnie, nie przez przypadek.

*[ZWERYFIKOWANE - [TIA Portal Help: Global Libraries, Project Libraries, Library versioning](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); IEC 61131-3 §6.6 (program organization units, reuse)]*
### 18.2. Jak robisz partial download żeby nie resetować całego CPU?

TIA Portal rozróżnia typy downloadów — wybierz najmniej inwazyjny dla sytuacji:

| Typ downloadu | CPU w RUN? | Kiedy używać |
|---------------|-----------|-------------|
| **Software (only changes)** | ✅ Tak | Poprawka kodu, nowy blok — bez zmiany HW |
| **HW and SW (only changes)** | ⚠️ Krótki STOP | Nowy moduł IO, zmiana IP, zmiana konfiguracji |
| **All** | ❌ STOP wymagany | Pełne wgranie projektu — unikaj na produkcji |

**Procedura partial download:**
1. Skompiluj projekt `Compile → All` — brak błędów = warunek konieczny
2. `Compare offline/online` — sprawdź diff co faktycznie się różni przed downloadem
3. `Download to device → Software (only changes)` → zaznacz CPU → `Load`
4. Potwierdź synchronizację — TIA Portal pokaże listę zmienionych bloków

> ⚠️ **Safety partial download:** zmiany w programie Safety zawsze wymagają akceptacji F-signature przez uprawnionego użytkownika. Safety runtime przechodzi przez `LOCK → RUN` (~1s). Standard może działać, ale napędy Safety (STO) chwilowo nieaktywne.

> 💡 **Sprawdź przed:** `Online & Diagnostics → Compare` — zidentyfikuj różnice. Nieoczekiwane zmiany (np. ktoś edytował online) staną się widoczne zanim je nadpiszesz.

*[ZWERYFIKOWANE - [TIA Portal Help: Download to device, Partial download, Compare offline/online](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [SIMATIC Safety - Konfiguracja i programowanie (Entry ID: 109751404)](https://support.industry.siemens.com/cs/document/109751404/) — rozdz. Safety partial download procedure]*
### 18.3. Do czego służy OPC UA w TIA Portal i jak go aktywujesz?

**OPC UA** (Open Platform Communications Unified Architecture) to otwarte, bezpieczne API do integracji PLC z systemami SCADA, MES, ERP, chmurą i IT (Python, C#, Java). Kluczowe zalety nad S7-Protocol/Modbus: standaryzacja, szyfrowanie TLS 1.2, certyfikaty X.509, model obiektowy (nodes, methods, events).

**Aktywacja w TIA Portal:**
1. CPU properties → `OPC UA` → `Server` → `Enable OPC UA server`
2. Ustaw port (domyślny: `4840`) i certyfikat bezpieczeństwa
3. Wybierz węzły: `All tags` (wszystkie tagi PLC) lub `Selected DBs` (wybrane bloki danych)
4. Skonfiguruj `Security Policy`: `None` (dev), `Basic256Sha256` (produkcja)
5. Pobierz certyfikat serwera dla klienta — potrzebny do połączenia

**Typowe zastosowania:**
- WinCC Advanced/Unified → monitoring i SCADA
- Node-RED → dashboard prototypowy, IoT gateway
- Python `asyncua` library → analityka danych, integracja z chmurą
- Kepware / Ignition → integracja MES/ERP

> ⚠️ **Ograniczenia OPC UA:** opóźnienie ~10–50ms vs PROFINET RT <1ms. Nie używaj OPC UA do sterowania real-time — wyłącznie do monitoringu, parametryzacji, zbierania danych.

> 💡 **Security w produkcji:** zawsze włącz `Basic256Sha256` + certyfikaty. OPC UA bez szyfrowania to otwarta furtka do odczytu (i zapisu!) wszystkich tagów PLC.

*[ZWERYFIKOWANE - IEC 62541 (OPC UA standard — security, certificates); [TIA Portal Help: OPC UA Server configuration](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); [SIMATIC S7-1500 OPC UA (Siemens)](https://www.siemens.com/global/en/products/automation/systems/industrial/plc/simatic-s7-1500.html)]*
### 18.4. Czym jest SIMATIC ProDiag i jak konfigurujesz pierwsze monitory diagnostyczne? 🟡
ProDiag (Process Diagnostics) to narzędzie TIA Portal do tworzenia automatycznej diagnostyki maszynowej generując alarmy HMI wprost z warunków logicznych PLC bez programowania w blokach.
- Dostępny od: TIA Portal V14 SP1, dla S7-1500 i ET200SP z CPU
- Konfiguracja: Devices & Networks → CPU → ProDiag → Add monitor
- Monitor = warunek logiczny (np. „siłownik nie dosunął się w 5s") → automatyczny alarm HMI + log
- Typy monitorów: Supervision (stan), Process Monitor (czas reakcji), Travel movement (pozycja)
- Krok 1: Zdefiniuj warunek triggering (bool z programu PLC)
- Krok 2: Przypisz tekst alarmu (wielojęzyczny) i kategorie (Error, Warning, Info)
- Krok 3: Skompiluj → alarmy automatycznie pojawiają się w HMI bez dodatkowej konfiguracji WinCC
- Korzyść: czas od awarii do diagnozy przyczyny bez przeglądania kodu — operator widzi kontekst

---

*[ZWERYFIKOWANE - [TIA Portal ProDiag (Siemens)](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html); SIMATIC ProDiag dostępny od TIA Portal V14 SP1 dla S7-1500 i ET200SP CPU]*
