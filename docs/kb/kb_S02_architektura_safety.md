<!-- Źródło: knowledge_base_controlbyte.md -->

## 2. Architektura SIMATIC Safety Integrated

### Jakie są podstawowe komponenty i zasady programowania sterowników bezpieczeństwa Pilz PNOZmulti?
Odpowiedź — Pilz PNOZmulti to programowalny sterownik bezpieczeństwa, który umożliwia łatwe i intuicyjne tworzenie logiki bezpieczeństwa dla maszyn, wykorzystując dedykowane bloki funkcyjne i graficzne środowisko programowania.
- **Programowanie:**
    - Odbywa się za pomocą oprogramowania PNOZmulti Configurator.
    - Program jest podzielony na strony, co ułatwia organizację.
    - Wykorzystuje dedykowane bloki funkcyjne do obsługi elementów bezpieczeństwa (np. ML DH M gate, ML 2 D H M dla rygli, wejścia dwukanałowe).
    - Logika ryglowania i odryglowania jest zaimplementowana w specjalnych blokach.
- **Konfiguracja sprzętowa:**
    - W zakładce "Open Hardware Configuration" można zobaczyć jednostkę główną, dodatkowe moduły wejść/wyjść oraz urządzenia sieciowe (np. panel PMI, czytniki RFID podłączone przez switch).
    - Mapowanie zmiennych i wejść/wyjść odbywa się w zakładce "I O List".
- **Połączenie i diagnostyka:**
    - Połączenie ze sterownikiem odbywa się kablem Ethernet.
    - Adres IP i maska podsieci są dostępne w menu Ethernet -> info.
    - Opcja "Scan Network" pozwala wykryć sterownik w sieci.
    - W "Project Manager" należy wprowadzić Order number i Serial number sterownika, aby uzyskać dostęp.
    - Dostępne są trzy poziomy dostępu: pełna edycja, podgląd, zmiana parametrów.
    - Tryb "online Dynamic Program Display" podświetla aktywne sygnały na zielono, co ułatwia diagnostykę.
*Praktyk: [Programowanie PNOZmulti jest bardzo przyjazne użytkownikowi dzięki dedykowanym blokom. Diagnostyka w trybie online jest prosta, ponieważ aktywne sygnały są wizualnie wyróżnione.] [Safety]*


---
### 🔗 Dokumentacja Siemens online
- [SIMATIC Safety Integrated — przegląd systemu](https://www.siemens.com/global/en/products/automation/systems/industrial/safety-integrated.html)
- [SIMATIC Safety — konfiguracja i programowanie (Entry ID: 104547937)](https://support.industry.siemens.com/cs/document/104547937/)
- [Pilz PNOZmulti Configurator — strona produktowa](https://www.pilz.com/en-INT/products/controllers/small-controllers/pnozmulti-2)
