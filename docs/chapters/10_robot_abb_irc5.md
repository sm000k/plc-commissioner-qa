## 10. ROBOT ABB IRC5 — INTEGRACJA Z PLC

### 10.1. Jak przebiega komunikacja Siemens PLC z robotem ABB IRC5?  🟡

Przez PROFINET: Siemens PLC = IO-Controller, robot ABB IRC5 = IO-Device.
Konfiguracja: 1) W RobotStudio konfigurujesz PROFINET slave i sygnały I/O w pliku EIO.cfg. 2) Eksportujesz GSDML z IRC5. 3) W TIA Portal importujesz GSDML — robot widoczny jak każde urządzenie PROFINET. 4) Mapujesz adresy wejść/wyjść. 5) Ustawiasz IP robota i nazwę PROFINET zgodną z RobotStudio.

*[ZWERYFIKOWANE - ABB Application Manual: PROFINET Device (Ref. 3HAC050996-001); [PROFINET — technologia Siemens](https://www.siemens.com/global/en/products/automation/industrial-communication/profinet.html)]*
### 10.2. Co to jest GSDML i jak go instalujesz w TIA Portal?

GSDML (General Station Description Markup Language) to plik XML opisujący urządzenie PROFINET — jego moduły I/O, parametry, obsługiwane adresy.
Instalacja: TIA Portal → Options → Manage general station description files → Install → wskazujesz plik GSDML.
Plik GSDML dla ABB IRC5 znajdziesz w folderze instalacji RobotStudio lub w IRC5 controller disk.

*[ZWERYFIKOWANE - ABB Application Manual: PROFINET Device (Ref. 3HAC050996-001); IEC 61158 (GSDML standard PROFINET)]*
### 10.3. Jak PLC wysyła numer programu do robota i jak robot go odczytuje?

Po stronie robota (EIO.cfg): definiujesz Group Input (GI) — np. GI_ProgramNumber, 8 bitów, zmapowany na bajt z PROFINET.
Po stronie PLC (TIA Portal): piszesz wartość INT (np. 5) do obszaru wyjść PROFINET przypisanego do robota.
Po stronie RAPID (kod robota): nrProgram := GInput(GI_ProgramNumber); a następnie SELECT nrProgram → IF 1 → MoveL pos1 → IF 2 → MoveL pos2 itd.

*[ZWERYFIKOWANE - ABB RAPID Reference Manual (3HAC049903-001) — GInput/GOutput — Group I/O signals; ABB Application Manual: PROFINET Device (3HAC050996-001)]*
### 10.4. Jak działa przesyłanie offsetu pozycji z PLC do RAPID?

PLC wysyła wartość offsetu (np. X, Y w mm×10 jako INT, żeby uniknąć przecinka) przez Group Input PROFINET.
W RAPID: offsetX := GInput(GI_OffsetX) / 10.0;
Dodajesz do pozycji bazowej: targetPos := Offs(basePos, offsetX, offsetY, 0);
MoveL targetPos, v100, fine, tool1;
Metoda stosowana przy systemach wizyjnych i zmiennych pozycjach detali.

*[ZWERYFIKOWANE - ABB RAPID Reference Manual (3HAC049903-001) — Offs() function; ABB Application Note: Vision-guided robot positioning via PROFINET I/O]*
### 10.5. Jak debugujesz brak komunikacji PROFINET między PLC a robotem?

Kolejność sprawdzania:
- Czy robot ma poprawne IP i nazwę PROFINET (zgodne z TIA Portal)?
- Ping z PLC do IP robota — czy odpowiada?
- W TIA Portal diagnostyka PROFINET — czy urządzenie widoczne w sieci?
- W RobotStudio — czy interfejs PROFINET aktywny, czy sygnały skonfigurowane?
- Czy GSDML wersja pasuje do wersji RobotWare (starsze RW → starszy GSDML)?
- Czy nie ma duplikatu nazwy PROFINET w sieci?

---

*[ZWERYFIKOWANE - ABB Application Manual PROFINET Device (3HAC050996-001), rozdz. troubleshooting; [PROFINET diagnostyka — Application Example Siemens (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/)]*
### 10.6. Jakie protokoły komunikacyjne i format danych są wykorzystywane do integracji robota ABB IRC5 z PLC Siemens?
Integracja robota ABB z kontrolerem IRC5 ze sterownikiem PLC Siemens może być realizowana za pośrednictwem protokołu TCP lub UDP, z wykorzystaniem standardu XML do przesyłania danych.
- Komunikacja odbywa się z częstotliwością około 250 Hz (cykl co 4 ms) dzięki modułowi "Robot Reference Interface".
- **TCP (Transmission Control Protocol):** Wybierany, gdy kluczowe jest otrzymanie każdej ramki danych, nawet kosztem powtórnego wysyłania.
- **UDP (User Datagram Protocol):** Wybierany, gdy nie jest istotne otrzymanie każdej ramki (może zostać utracona), ale ważna jest aktualna wartość i ciągłość nadawania.
- Dane są przesyłane w formacie XML, który jest językiem znaczników umożliwiającym reprezentowanie informacji za pomocą struktury elementów i atrybutów.
*Źródło: transkrypcje ControlByte*

### 10.7. Jakie są kluczowe elementy struktury telegramu XML wysyłanego z robota ABB IRC5 do PLC?
Telegram XML wysyłany z robota ABB IRC5 do PLC zawiera ustrukturyzowane dane dotyczące stanu i położenia robota, wykorzystując elementy i atrybuty.
- Głównymi częściami dokumentu XML są elementy, takie jak `RobData` (element nadrzędny/root), `RobMode`, `Ts_act`, `P_act`, `J_act`, `Ts_des`, `P_des`, `J_des`.
- Elementy mogą zawierać tekst (np. `RobMode` z wartością "Auto") lub atrybuty (np. `RobData` z atrybutami `Id` i `Ts` zawierającymi wartości w cudzysłowie).
- Możliwe jest zagnieżdżanie elementów, gdzie `RobData` zawiera inne elementy, które z kolei posiadają atrybuty informujące o aktualnym położeniu i orientacji robota.
- Telegram jest kodowany w standardzie UTF-8, który jest rozszerzonym kodowaniem obejmującym znaki ASCII.
*Źródło: transkrypcje ControlByte*

### 10.8. Jak przebiega proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens?
Proces dekodowania telegramu XML z robota ABB w sterowniku PLC Siemens obejmuje odbiór danych, konwersję znaków i ekstrakcję informacji z elementów i atrybutów XML.
- Sterownik PLC odbiera ramkę danych za pośrednictwem protokołu TCP.
- Odebrane bajty są dekodowane jako zmienne typu `character` (char), reprezentujące znaki w formacie ASCII/UTF-8.
- Następnie, z wykorzystaniem odpowiednich funkcji (np. z biblioteki LString), następuje dekodowanie poszczególnych pól dla elementów w znacznikach XML.
- Odczytywane są wartości atrybutów, które stanowią zmienne robota, takie jak położenie i orientacja.
- Do symulacji i testowania komunikacji można wykorzystać narzędzia takie jak PLCSIM Advanced i Node-RED, który generuje przykładowe telegramy XML.
*Źródło: transkrypcje ControlByte*

