<!-- Źródło: knowledge_base_delta_v11.md -->

## SEKCJA: 8. Napędy Safety — SINAMICS z wbudowanym Safety

### Jakie funkcje bezpieczeństwa są wbudowane w serwowzmacniacz Sinamics V90 i jak należy je podłączyć?
Serwowzmacniacz Sinamics V90 jest wyposażony w funkcję bezpieczeństwa STO (Safe Torque Off), która zapewnia bezpieczne zdjęcie momentu obrotowego z napędu.
- Funkcja STO jest realizowana poprzez terminale STO+, STO1 i STO2.
- Domyślnie terminale te są zmostkowane, co oznacza, że funkcja STO jest nieaktywna w trybie bezpieczeństwa.
- W docelowej aplikacji sygnały STO należy podłączyć dwukanałowo do układu bezpieczeństwa, takiego jak przekaźnik bezpieczeństwa lub programowalny sterownik bezpieczeństwa (PLC Safety), aby zapewnić bezpieczne zatrzymanie napędu.
*Źródło: transkrypcje ControlByte*

