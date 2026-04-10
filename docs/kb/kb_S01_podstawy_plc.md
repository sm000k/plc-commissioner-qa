<!-- Źródło: knowledge_base_controlbyte.md -->

## 1. Podstawy PLC i automatyki

### Czym jest automatyka i jakie są jej główne obszary zastosowań?
Odpowiedź — Automatyka to dziedzina zajmująca się zagadnieniami sterowania procesami technologicznymi i przemysłowymi, dążąca do minimalizacji udziału człowieka. Różni się od automatyzacji, która dostarcza metody i rozwiązania ułatwiające eliminację udziału człowieka w różnych procesach, w tym biznesowych.
- **Obszary zastosowań:**
    - Linie produkcyjne (fabryki).
    - Przemysł górniczy, mineralny i metalurgiczny (kopalnie, platformy wiertnicze, huty, cementownie).
    - Infrastruktura publiczna (oczyszczalnie ścieków, stacje uzdatniania wody, przepompownie, gazownie, ciepłownie, elektrownie, sieci telekomunikacyjne).
    - Automatyka budynkowa (inteligentne domy, HVAC, oświetlenie).
    - Transport (automatyka kolejowa: systemy kontroli trakcji, sterowanie HVAC i oświetleniem w taborze).
    - Przemysł stoczniowy (systemy sterowania balastem).
    - Systemy wojskowe (sterowanie artylerią przeciwlotniczą).
*Praktyk: [Automatyk potrafi automatyzować procesy technologiczne i przemysłowe, ale nie biznesowe. Automatyka może być składową automatyzacji całego biznesu, np. automatyzacja linii produkcyjnych.]*

### Jakie są główne rodziny sterowników PLC Siemens i do jakich zastosowań są dedykowane?
Odpowiedź — Siemens oferuje różne rodziny sterowników PLC, dostosowane do aplikacji o różnej skali i złożoności, od prostych zadań po najbardziej wymagające systemy.
- **LOGO!**: Najmniejszy sterownik, nazywany przekaźnikiem programowalnym lub modułem logicznym.
    - **Zastosowanie:** Proste maszyny, nieskomplikowana automatyka procesowa (przepompownie, oczyszczalnie), automatyka budynkowa.
    - **Cena:** Moduł CPU około 400-500 zł, moduł rozszerzenia (8 wejść/wyjść) około 350 zł.
    - **Możliwości:** Możliwość rozszerzania o wejścia/wyjścia cyfrowe i analogowe, ale nie do zaawansowanych aplikacji napędowych czy kompletnych regulatorów PID.
- **S7-1200**: Kompaktowe sterowniki ze zintegrowanymi wejściami i wyjściami.
    - **Zastosowanie:** Małe i średnie aplikacje, łączące dobrą wydajność z niską ceną.
    - **Cena:** Jednostka CPU z możliwością rozbudowy (1212C) około 800 zł, (1214C) około 1200 zł. Moduł rozszerzenia (16 wejść/16 wyjść) około 850 zł.
    - **Możliwości:** Modułowa konstrukcja, port PROFINET, płytka sygnałowa, moduły rozszerzeń DI/DO/AI/AO, moduły technologiczne (np. wagowe), moduły komunikacyjne (RS232, RS485, PROFIBUS, AS-i, IO-Link, GSM), wbudowane szybkie wejścia/wyjścia (do enkoderów, silników krokowych/serwo), wersje failsafe.
- **S7-1500**: Dedykowane do najbardziej wymagających aplikacji.
    - **Zastosowanie:** Charakteryzują się największą mocą obliczeniową, zaawansowanymi funkcjami technologicznymi i komunikacyjnymi.
    - **Cena:** Podstawowa jednostka CPU 1511 około 2400 zł. Moduł rozszerzenia (16 wejść/16 wyjść) około 1400 zł.
*Praktyk: [Dla początkujących w programowaniu PLC, S7-1200 jest polecany ze względu na niższą cenę. Po opanowaniu S7-1200, przejście na S7-1500 nie powinno stanowić problemu. Sterowniki S7-1200 posiadają wbudowany serwer WWW do diagnostyki i wyświetlania własnych stron.] [PLC] [TIA Portal]*

### Jakie są podstawowe języki programowania sterowników PLC zgodne z normą IEC 61131-3?
Odpowiedź — Norma IEC 61131-3 definiuje ujednolicone języki programowania dla sterowników PLC, co ułatwia programowanie i obsługę sprzętu różnych producentów.
- **Języki graficzne:**
    - **LAD (Ladder Diagram):** Przeniesienie idei układów stycznikowych i przekaźnikowych. Składa się ze styków (NO, NC) i cewek. [PLC]
    - **FBD (Function Block Diagram):** Budowanie logiki programu poprzez strukturę bloków logicznych. [PLC]
    - *Charakterystyka:* Programowanie polega na przeciąganiu elementów graficznych. Graficznie zajmują duży obszar roboczy.
- **Języki tekstowe:**
    - **IL (Instruction List) / STL (Statement List - Siemens):** Język niskiego poziomu, odpowiednik asemblera dla PLC. Daje duże możliwości, ale wymaga skupienia na akumulatorze, rejestrach i stosie. [PLC]
    - **ST (Structured Text) / SCL (Structured Control Language - Siemens):** Język wysokiego poziomu, podobny do Pascala, Basic, C. Posiada instrukcje warunkowe (IF, CASE), pętle (FOR, WHILE, REPEAT). Umożliwia implementację zaawansowanych algorytmów, obliczeń matematycznych, operacji na wektorach, tablicach, macierzach. Charakteryzuje się dużą przejrzystością kodu. [PLC] [TIA Portal]
- **Języki grafów strukturalnych:**
    - **SFC (Sequential Function Chart):** Język grafów strukturalnych, składający się z kroków, tranzycji i akcji. Przydatny przy budowaniu sekwencyjnych układów sterowania. [PLC]
*Praktyk: [Język SCL jest certyfikowany według normy IEC 61131-3, co czyni go dobrym wyborem do zaawansowanych projektów. Programowanie w SCL jest znacznie szybsze niż w językach graficznych dla skomplikowanych algorytmów.] [TIA Portal]*

### Jakie są kluczowe aspekty pamięci sterownika PLC Siemens S7-1200/1500?
Odpowiedź — Pamięć sterownika PLC jest podzielona na obszary o różnych właściwościach, co pozwala na efektywne zarządzanie programem i danymi, uwzględniając trwałość i szybkość dostępu.
- **Pamięć ładowania (Load Memory):**
    - **Typ:** Pamięć trwała (nieulotna), np. karta pamięci typu Flash lub wbudowana kość pamięci (S7-1200).
    - **Zawartość:** Skompilowane bloki programowe (kod maszynowy), bloki danych, konfiguracja sprzętowa.
    - **Działanie:** Dane są kopiowane z pamięci ładowania do pamięci roboczej podczas fazy startupu sterownika.
- **Pamięć robocza (Work Memory):**
    - **Typ:** Pamięć ulotna (RAM).
    - **Działanie:** Sterownik wykonuje większość działań w tym obszarze. Dane są tracone po zdjęciu zasilania.
- **Pamięć systemowa:**
    - **Typ:** Część pamięci roboczej.
    - **Zawartość:** Pamięć bitowa M (zmienne z tablicy tagów), timery i liczniki systemowe, lokalna pamięć tymczasowa L (zmienne tymczasowe), aktualny obraz procesu wejść i wyjść.
- **Pamięć Retentive (nieulotna):**
    - **Typ:** Specjalny obszar pamięci nieulotnej w sterowniku.
    - **Działanie:** W przypadku utraty zasilania, sterownik przez chwilę podtrzymuje pracę i przepisuje część danych z pamięci roboczej do pamięci Retentive, co pozwala na zachowanie wybranych danych (np. parametry, aktualny stan maszyny).
*Praktyk: [Ważne jest, aby świadomie decydować, które dane mają być retentywne, aby zachować stan maszyny po zaniku zasilania. Ograniczona żywotność pamięci trwałej i długi czas zapisu/odczytu sprawiają, że pamięć RAM jest preferowana do bieżących operacji.] [PLC] [TIA Portal]*

### Jakie są kluczowe elementy budowy i montażu sterownika Siemens S7-1200?
Odpowiedź — Sterowniki S7-1200 charakteryzują się modułową konstrukcją, co pozwala na elastyczne rozszerzanie funkcjonalności i łatwy montaż w szafie sterowniczej.
- **Montaż:**
    - Jednostka CPU i moduły (oprócz płytki sygnałowej) montowane są na szynie DIN (TH35/TS35).
    - Montaż: zahaczenie górnej części, wciśnięcie ruchem obrotowym w dół, zablokowanie klipsem.
    - Demontaż: odblokowanie klipsa, podciągnięcie sterownika ruchem obrotowym do góry.
- **Płytka sygnałowa (Signal Board):**
    - Montowana od frontu CPU po usunięciu zaślepki. Wsuwana wertykalnie w gniazdo Gold pinowe.
    - Pozwala na proste rozszerzenie funkcjonalności sterownika.
- **Moduły rozszerzeń (SM - Signal Modules):**
    - Przyłączane z prawej strony sterownika. Po usunięciu zaślepki, moduł wpinany jest ruchem obrotowym na szynę i utwierdzany klipsem.
    - Suwak na froncie modułu służy do wsunięcia złącza do modułu z lewej strony.
- **Moduły komunikacyjne (CM/CP - Communication Modules/Processors):**
    - Przyłączane z lewej strony sterownika. Nie posiadają suwaka.
    - Posiadają odstające złącze sygnałowe i montowane są przy pomocy dwóch mechanicznych kołków ustalających.
    - Montaż: zaczepienie na szynie DIN w pewnej odległości, następnie zsunięcie modułu i sterownika względem siebie, co powoduje połączenie kształtowe i wsunięcie złącza.
- **Przewód rozszerzający:**
    - Umożliwia przyłączenie dodatkowych modułów wejść/wyjść na kolejnej szynie DIN, gdy skończy się miejsce obok CPU.
- **Złącza sterownika S7-1200:**
    - **X10:** Zasilanie sterownika i wejścia cyfrowe (pod górną klapką).
    - **X11:** Sygnały analogowe (pod górną klapką).
    - **X12:** Wyjścia cyfrowe (pod dolną klapką po prawej stronie).
    - **X50:** Slot na kartę pamięci Micro SD (preformatowane karty Siemensa).
- **Diody sygnalizacyjne:**
    - **RUN/STOP, ERROR, MAINTENANCE:** Na górze po lewej stronie, sygnalizują pracę sterownika.
    - **Stan wejść/wyjść:** Po prawej stronie (wejścia), na dole (wyjścia).
    - **LINK, RX/TX:** Po lewej stronie, sygnalizują stan połączenia sieciowego.
*Praktyk: [Przy każdym przyłączu na sterowniku S7-1200 znajduje się opis (np. 3L+, 3M, .0, .1), co ułatwia identyfikację zacisków. Sterownik 1211C nie może być rozbudowany o dodatkowe moduły wejść/wyjść bezpośrednio, ale może łączyć się z modułami zewnętrznymi po sieci.] [PLC]*

