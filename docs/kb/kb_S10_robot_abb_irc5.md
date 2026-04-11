<!-- Źródło: knowledge_base_delta_v11.md -->

## SEKCJA: 10. Robot ABB IRC5 — integracja z PLC

### Jakie protokoły komunikacyjne i format danych są wykorzystywane do integracji robota ABB IRC5 z PLC Siemens?
Integracja robota ABB z kontrolerem IRC5 ze sterownikiem PLC Siemens może być realizowana za pośrednictwem protokołu TCP lub UDP, z wykorzystaniem standardu XML do przesyłania danych.
- Komunikacja odbywa się z częstotliwością około 250 Hz (cykl co 4 ms) dzięki modułowi "Robot Reference Interface".
- **TCP (Transmission Control Protocol):** Wybierany, gdy kluczowe jest otrzymanie każdej ramki danych, nawet kosztem powtórnego wysyłania.
- **UDP (User Datagram Protocol):** Wybierany, gdy nie jest istotne otrzymanie każdej ramki (może zostać utracona), ale ważna jest aktualna wartość i ciągłość nadawania.
- Dane są przesyłane w formacie XML, który jest językiem znaczników umożliwiającym reprezentowanie informacji za pomocą struktury elementów i atrybutów.
*Źródło: transkrypcje ControlByte*

### Jakie są kluczowe elementy struktury telegramu XML wysyłanego z robota ABB IRC5 do PLC?
Telegram XML wysyłany z robota ABB IRC5 do PLC zawiera ustrukturyzowane dane dotyczące stanu i położenia robota, wykorzystując elementy i atrybuty.
- Głównymi częściami dokumentu XML są elementy, takie jak `RobData` (element nadrzędny/root), `RobMode`, `Ts_act`, `P_act`, `J_act`, `Ts_des`, `P_des`, `J_des`.
- Elementy mogą zawierać tekst (np. `RobMode` z wartością "Auto") lub atrybuty (np. `RobData` z atrybutami `Id` i `Ts` zawierającymi wartości w cudzysłowie).
- Możliwe jest zagnieżdżanie elementów, gdzie `RobData` zawiera inne elementy, które z kolei posiadają atrybuty informujące o aktualnym położeniu i orientacji robota.
- Telegram jest kodowany w standardzie UTF-8, który jest rozszerzonym kodowaniem obejmującym znaki ASCII.
*Źródło: transkrypcje ControlByte*

### Jak przebiega proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens?
Proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens obejmuje odbiór danych, konwersję znaków i ekstrakcję informacji z elementów i atrybutów XML.
- Sterownik PLC odbiera ramkę danych za pośrednictwem protokołu TCP.
- Odebrane bajty są dekodowane jako zmienne typu `character` (char), reprezentujące znaki w formacie ASCII/UTF-8.
- Następnie, z wykorzystaniem odpowiednich funkcji (np. z biblioteki LString), następuje dekodowanie poszczególnych pól dla elementów w znacznikach XML.
- Odczytywane są wartości atrybutów, które stanowią zmienne robota, takie jak położenie i orientacja.
- Do symulacji i testowania komunikacji można wykorzystać narzędzia takie jak PLCSIM Advanced i Node-RED, który generuje przykładowe telegramy XML.
*Źródło: transkrypcje ControlByte*


---
### 🔗 Dokumentacja online
- [ABB IRC5 — strona produktowa](https://new.abb.com/products/robotics/controllers/irc5)
- [ABB RobotStudio — narzędzie offline](https://new.abb.com/products/robotics/robotstudio)
- [Siemens PLCSIM Advanced — symulacja komunikacji](https://support.industry.siemens.com/cs/document/109795016/)
