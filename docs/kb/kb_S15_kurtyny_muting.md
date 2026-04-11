<!-- Źródło: knowledge_base_controlbyte.md -->

## 15. Kurtyny bezpieczeństwa i Muting

### Jakie jest zastosowanie wyjść tranzystorowych z czujników bezpieczeństwa w systemach PLC Safety?
Odpowiedź — Wyjścia tranzystorowe z czujników bezpieczeństwa, takich jak kurtyny bezpieczeństwa czy skanery, są kluczowe dla systemów PLC Safety, ponieważ umożliwiają dwukanałowe monitorowanie i szybkie wykrywanie awarii.
- **Podłączenie:** Wyjścia tranzystorowe z czujników bezpieczeństwa podłącza się do wejść bezpieczeństwa sterownika PLC.
- **Wykrywanie awarii:**
    - Jeśli jedno z wyjść tranzystorowych ulegnie uszkodzeniu (np. spali się lub będzie miało zwarcie), układ bezpieczeństwa natychmiast wykryje sytuację awaryjną.
    - Jest to analogiczne do wykrywania rozbieżności sygnału ("discrepancy error") w przypadku styków mechanicznych.
*Praktyk: [W przypadku uszkodzenia jednego z wyjść tranzystorowych kurtyny bezpieczeństwa, sterownik safety natychmiast zgłosi błąd, co zapobiega dalszej pracy maszyny w niebezpiecznym stanie.] [Safety]*


---
### 🔗 Dokumentacja online
- [SICK deTec — kurtyny bezpieczeństwa](https://www.sick.com/ag/en/safety-light-curtains/c/g575862)
- [SIMATIC Safety — muting configuration (Entry ID: 104547937)](https://support.industry.siemens.com/cs/document/104547937/)
- [IEC 61496 — kurtyny świetlne (norma informacyjnie)](https://www.iso.org/standard/44998.html)
- [EN ISO 13855 — odległości bezpieczeństwa](https://www.iso.org/standard/42845.html)
