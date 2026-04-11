<!-- Źródło: knowledge_base_controlbyte.md -->

## 5. Passivation, Reintegration, ACK

### Czym jest pasywacja kanału w systemie bezpieczeństwa i jak przebiega reintegracja?
Odpowiedź — Pasywacja kanału to stan, w którym moduł bezpieczeństwa wyłącza dany kanał wejściowy lub wyjściowy z powodu wykrycia awarii, aby zapobiec niebezpiecznym sytuacjom. Reintegracja to proces przywracania kanału do normalnego działania po usunięciu awarii.
- **Pasywacja:**
    - **Przyczyny:** Zwarcie do potencjału 0 V, zwarcie międzykanałowe, błąd rozbieżności sygnału ("Discrepancy failure").
    - **Skutek:** Kanał zostaje wyłączony, a w przypadku wejść bezpieczeństwa, wyjścia bezpieczeństwa (np. styczniki) zostają rozłączone, prowadząc maszynę do bezpiecznego stanu.
    - **Diagnostyka:** Błędy są widoczne w buforze diagnostycznym sterownika PLC (np. "Overload or internal sensor supply short circuit to ground").
- **Reintegracja (Reintegration):**
    - **Warunki:** Po usunięciu przyczyny awarii (np. odłączeniu zwarcia, przywróceniu ciągłości obwodu).
    - **Sygnalizacja:** Diody na module mogą migać naprzemiennie (czerwona i zielona), sygnalizując możliwość resetu.
    - **Reset:** Wymaga aktywacji funkcji resetu. W niektórych konfiguracjach (parametr "Reintegration after discrepancy error" ustawiony na "Test zero signal necessary") konieczne jest najpierw wymuszenie stanu zerowego na czujniku (np. wciśnięcie E-STOP), a dopiero potem reset.
    - **ACK (Acknowledge) Requested:** Sygnał wskazujący, że system oczekuje na potwierdzenie (reset) po wystąpieniu błędu.
*Praktyk: [Po usunięciu zwarcia, błąd "outgoing event" pojawia się w buforze diagnostycznym, a następnie aktywny jest błąd związany z pasywacją kanałów, wymagający resetu. Reset funkcji bezpieczeństwa jest inny niż reset reintegracji kanałów safety.] [Safety]*


---
### 🔗 Dokumentacja Siemens online
- [SIMATIC Safety — programowanie F-CPU (Entry ID: 104547937)](https://support.industry.siemens.com/cs/document/104547937/)
- [E-Stop SIL3 — passivation i reintegration (Entry ID: 21064024)](https://support.industry.siemens.com/cs/document/21064024/)
