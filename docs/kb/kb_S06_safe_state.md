<!-- Źródło: knowledge_base_controlbyte.md -->

## 6. Safe State — bezpieczny stan

### Czym jest funkcja STO (Safe Torque Off) i jak jest implementowana w napędach SINAMICS V90?
Odpowiedź — STO (Safe Torque Off) to funkcja bezpieczeństwa, która zapewnia bezpieczne odłączenie momentu obrotowego od silnika, uniemożliwiając jego niekontrolowany ruch. Jest to podstawowa funkcja bezpieczeństwa w napędach, która nie wymaga odłączenia zasilania od wzmacniacza.
- **Zasada działania:**
    - Funkcja STO jest wbudowana w serwowzmacniacz SINAMICS V90.
    - Odpowiada za bezpieczne zdjęcie momentu obrotowego z napędu, co oznacza, że silnik nie może generować siły ani ruchu.
    - Zasilanie serwowzmacniacza pozostaje włączone, co pozwala na szybsze wznowienie pracy po usunięciu zagrożenia.
- **Implementacja w SINAMICS V90:**
    - Serwowzmacniacz V90 posiada dedykowane terminale do podłączenia funkcji STO: STO+, STO1 i STO2.
    - Domyślnie terminale te są zmostkowane, co oznacza, że funkcja STO jest nieaktywna (moment jest dostępny).
    - W docelowej aplikacji sygnały STO należy podłączyć dwukanałowo do układu bezpieczeństwa (przekaźnika bezpieczeństwa lub programowalnego sterownika bezpieczeństwa), który będzie realizował bezpieczne zatrzymanie napędu.
*Praktyk: [Podłączenie STO do układu bezpieczeństwa jest kluczowe dla zapewnienia zgodności z normami. Brak prawidłowego podłączenia STO oznacza, że napęd nie jest bezpiecznie wyłączany w przypadku zagrożenia.] [Safety] [Sinamics]*

