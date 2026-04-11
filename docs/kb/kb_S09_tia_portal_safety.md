<!-- Źródło: knowledge_base_controlbyte.md -->

## 9. TIA Portal — Safety praktyka

### Jakie są możliwości sterowników S7-1200 w zakresie bezpieczeństwa?
Odpowiedź — Sterowniki S7-1200 oferują wersje failsafe, które pozwalają na realizację funkcji bezpieczeństwa maszyn, integrując logikę bezpieczeństwa z kontrolą standardową w jednym systemie.
- **Wersje Failsafe:**
    - Dostępne są sterowniki S7-1200 w wersji failsafe (np. 1212FC, 1214FC, 1215FC).
    - Umożliwiają realizację funkcji bezpiecznego zatrzymania maszyny lub linii technologicznej.
- **Integracja:**
    - W połączeniu z dedykowanymi modułami wejściowymi i wyjściowymi failsafe, można zbudować kompletny układ bezpieczeństwa dla maszyny.
*Praktyk: [Użycie sterowników failsafe S7-1200 pozwala na uproszczenie architektury systemu bezpieczeństwa, ponieważ standardowa i bezpieczna logika są zarządzane przez ten sam sterownik.] [Safety] [TIA Portal]*

### Jakie są możliwości programowania sterowników bezpieczeństwa Pilz PNOZmulti w TIA Portal?
Odpowiedź — Transkrypcje nie wspominają o bezpośrednim programowaniu Pilz PNOZmulti w TIA Portal. PNOZmulti jest programowany za pomocą dedykowanego oprogramowania PNOZmulti Configurator.

### Jakie są kluczowe elementy konfiguracji i obsługi rygli bezpieczeństwa Pilz PSENmlock w systemach bezpieczeństwa?
Odpowiedź — Rygle bezpieczeństwa Pilz PSENmlock to zaawansowane urządzenia do kontroli dostępu, które oferują wysoką siłę trzymania, rozbudowaną diagnostykę i funkcje ucieczkowe, a ich integracja odbywa się poprzez cyfrowe sygnały I/O.
- **Typy rygli Pilz:**
    - **PSENmlock mini:** Podstawowe aplikacje, max. Kategoria 3, Performance Level D. Diody LED wskazują status zaryglowania.
    - **PSENslock 2:** Elektrorygiel magnetyczny, zabudowany wewnątrz osłony. Składa się z jednostki głównej i aktuatora przyciąganego elektromagnesem. Pozwala osiągnąć Performance Level E przy częstym testowaniu. Odporny na uszkodzenia mechaniczne aktuatorów.
    - **PSENmlock:** Wysoka siła trzymania (do 7500 N).
        - **Wizualizacja:** Diody sygnalizacyjne z trzech stron.
        - **Odryglowanie:** Gniazda na froncie i z boku do odryglowania specjalnym narzędziem.
        - **Funkcja ucieczkowa:** Wewnętrzna klamka do odryglowania w przypadku zatrzaśnięcia operatora w strefie niebezpiecznej.
        - **Montaż:** Dedykowany do profili systemowych 40 mm, śruby antymanipulacyjne.
        - **Połączenie:** Możliwość łączenia szeregowego za pomocą dedykowanych złączek i trójników.
        - **Odporność:** IP67.
        - **Zasilanie:** Ryglowany i odryglowywany impulsowo (brak ciągłego zasilania cewki, mniejsze zużycie energii, brak grzania).
        - **Performance Level:** Najwyższy możliwy Performance Level E dla monitorowania i ryglowania osłon.
        - **Sygnały:** Posiada tylko cyfrowe sygnały wejściowe i wyjściowe, co umożliwia wpięcie do każdego układu sterowania bezpieczeństwa (np. PNOZmulti).
- **Integracja z kasetą sterującą Pilz PIT i czytnikiem RFID (Key in Pocket):**
    - **Sekwencja pracy operatora:**
        1. Wprowadzenie tagu RFID do czytnika.
        2. Logowanie do systemu przyciskiem.
        3. Zwolnienie elektrorygla.
        4. Wejście do maszyny (serwis, prace nastawcze).
        5. Przed opuszczeniem strefy niebezpiecznej i zresetowaniem rygla, naciśnięcie przycisku "Blind spot" (potwierdzenie braku personelu).
        6. Ponowne wprowadzenie tagu RFID.
        7. Naciśnięcie przycisku "zamknij elektrorygiel".
        8. Wylogowanie.
        9. Maszyna jest w 100% zabezpieczona.
*Praktyk: [Elektrorygiel PSENmlock z klamką jest idealny do systemów, gdzie operator może zostać zatrzaśnięty w strefie niebezpiecznej. Impulsowe ryglowanie/odryglowywanie to zaleta w kontekście zużycia energii i temperatury pracy.] [Safety]*


---
### 🔗 Dokumentacja Siemens online
- [SIMATIC Safety — Getting Started (Entry ID: 104547937)](https://support.industry.siemens.com/cs/document/104547937/)
- [TIA Portal — Safety Administration](https://www.siemens.com/global/en/products/automation/industry-software/automation-software/tia-portal.html)
- [Pilz PSENmlock — strona produktowa](https://www.pilz.com/en-INT/products/sensors/safety-locking-devices/psenmlock)
