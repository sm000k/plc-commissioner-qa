<!-- Źródło: knowledge_base_controlbyte.md -->

## 14. PROFINET — topologia, diagnostyka i zaawansowane funkcje

### Jakie są podstawowe cechy i zastosowania sieci PROFINET w automatyce przemysłowej?
Odpowiedź — PROFINET to przemysłowy protokół Ethernet, który jest standardem w automatyce Siemens, zapewniającym szybką i niezawodną komunikację między sterownikami PLC, panelami HMI, napędami i innymi urządzeniami.
- **Zastosowanie:**
    - Komunikacja między sterownikami S7-1200/1500 a panelami HMI.
    - Sterowanie serwonapędami (np. SINAMICS V90) za pomocą telegramów PROFINET.
    - Łączenie modułów rozszerzeń (np. zewnętrznych modułów I/O) ze sterownikiem S7-1200.
- **Wbudowany port:** Sterowniki S7-1200 posiadają wbudowany port Ethernetowy obsługujący protokół PROFINET.
- **Konfiguracja w TIA Portal:**
    - Połączenie logiczne między sterownikiem PLC a panelem HMI w zakładce `Devices & networks`.
    - Urządzenia muszą znajdować się w tej samej podsieci (np. PLC 192.168.0.1, HMI 192.168.0.2).
    - Wybór odpowiedniego drivera komunikacyjnego (np. SIMATIC S7-1200).
- **Telegramy PROFINET [Sinamics]:**
    - W SINAMICS V90 wybiera się odpowiedni telegram w zależności od wymaganej funkcjonalności napędu.
    - S7-1200 współpracuje z telegramami 1, 2 lub 3.
    - S7-1500 może używać telegramu 102.
*Praktyk: [W przypadku urządzeń Siemens, konfiguracja komunikacji PROFINET między PLC a HMI jest bardzo prosta, ponieważ odbywa się z poziomu jednego projektu w TIA Portal.] [PROFINET] [TIA Portal] [HMI] [Sinamics]*

### Jakie są rodzaje i funkcje przemysłowych switchy Ethernet, oraz ich znaczenie w sieciach PROFINET?
Odpowiedź — Przemysłowe switche Ethernet są kluczowymi komponentami sieci PROFINET, zapewniającymi niezawodną i stabilną komunikację w trudnych warunkach przemysłowych, z różnymi funkcjonalnościami w zależności od potrzeb aplikacji.
- **Rodzaje switchy [PROFINET]:**
    - **Niezarządzalne (Plug & Play):** Proste w użyciu, nie wymagają konfiguracji.
        - **Compaрта ETU-0800/1600:** 8/16 portów Fast Ethernet (10/100 Mb/s), Auto-negocjacja, Full-duplex, Auto-MDI/MDIX. Metalowa obudowa IP30, odporność EMC, redundantne zasilanie 12-48 V DC, styk przekaźnikowy Fault.
        - **Compaрта LETU-0500:** 5 portów Fast Ethernet, obudowa z poliwęglanu IP30. Wspiera Quality of Service (QoS) dla priorytetów pakietów PROFINET.
        - **Compaрта EGU-0702-SFP-T:** Gigabitowy (10/100/1000 Mb/s) z 2 portami SFP (światłowód 100/1000). Backplane 14 Gb/s, Jumbo Frames 12.2 KB. Odporność na ekstremalne temperatury (-40 do 75°C).
        - **Compaрта PGU-1002-SFP-24:** Gigabitowy z 8 portami PoE+ (do 30W/port, budżet 200W) i 2 portami SFP.
    - **Zarządzalne:** Oferują pełną kontrolę nad siecią, zaawansowane funkcje i diagnostykę.
        - **Compaрта ETM-0800:** 8 portów Fast Ethernet. Funkcje L2: VLAN, QoS, RSTP (redundancja), kontrola dostępu (Port Access Control), SNMP, LACP (agregacja łączy), IGMP Snooping (kontrola ruchu multicast). Port konsoli RS232, USB do backupu konfiguracji. Wersje T (rozszerzona temp. -40°C) i CP (odporność na korozję).
        - **Compaрта EGM-1204-SFP:** Gigabitowy z 8 portami RJ45 i 4 slotami SFP. Obsługuje ERPS G.8032 (ring z czasem przełączania <50 ms). Pełen pakiet zarządzania siecią.
        - **Compaрта CBGM-0602-SFP:** 4 porty Gigabit Ethernet z PoE++ (do 90W/port) i 2 porty SFP. DIP switche do konfiguracji PoE. Wskaźnik obciążenia mocy PoE. Funkcje L2: DHCP Snooping, 802.1X (kontrola dostępu).
- **Wspólne cechy przemysłowych switchy [PROFINET]:**
    - **Odporność mechaniczna:** Metalowa obudowa (IP30), montaż na szynie DIN.
    - **Odporność środowiskowa:** Szeroki zakres temperatur pracy (-10 do 65°C, -40 do 75°C), brak wentylatorów.
    - **Odporność EMC:** Zgodność z normami EN (wyładowania elektrostatyczne, zakłócenia radiowe, szybkie zakłócenia impulsowe, przepięcia, zakłócenia przewodzone).
    - **Zasilanie:** Redundantne zasilanie DC (np. 12-48 V DC, 48-57 V DC), przekaźnik Fault (sygnalizacja awarii zasilania/urządzenia).
    - **Architektura:** Non-blocking (wszystkie porty pracują jednocześnie bez blokowania ruchu).
    - **MAC entries:** Duża liczba wpisów MAC (np. 16k) do obsługi rozbudowanych sieci.
*Praktyk: [W sieciach PROFINET, Quality of Service (QoS) w switchach jest kluczowe, aby pakiety PROFINET miały priorytet, nawet przy dużym ruchu. Redundancja zasilania i przekaźnik Fault są ważne dla ciągłości pracy w przemyśle.] [PROFINET]*

### Czym jest protokół ISO on TCP i do czego służy w komunikacji HMI-PLC?
Odpowiedź — ISO on TCP to protokół komunikacyjny, który umożliwia niskopoziomową wymianę danych bezpośrednio z pamięci sterownika PLC, wykorzystując standardowe instrukcje GET i PUT.
- **Zasada działania:**
    - Wykorzystuje protokół TCP/IP.
    - Pozwala na bezpośredni dostęp do obszarów pamięci sterownika PLC.
    - Instrukcje GET służą do odczytu danych z PLC.
    - Instrukcje PUT służą do zapisu danych do PLC.
- **Zastosowanie w HMI-PLC:**
    - Panel HMI (np. IDEC HG2J) może komunikować się ze sterownikiem Siemens S7-1200 za pomocą ISO on TCP.
    - Umożliwia szybką i efektywną wymianę danych między panelem a sterownikiem, np. do sterowania przyciskami, wyświetlania statusów LED, czy wartości prędkości.
*Praktyk: [W panelu IDEC HG2J, protokół ISO on TCP jest wykorzystywany do połączenia ze sterownikami Siemens S7-1200/1500, co pozwala na łatwe mapowanie zmiennych z pamięci sterownika do obiektów wizualizacji na panelu.] [HMI] [PROFINET]*


---
### 🔗 Dokumentacja Siemens online
- [PROFINET — przegląd technologii](https://www.siemens.com/global/en/products/automation/industrial-communication/profinet.html)
- [SCALANCE — switche przemysłowe](https://www.siemens.com/global/en/products/automation/industrial-communication/industrial-ethernet/scalance.html)
- [PROFINET diagnostyka — Application Example (Entry ID: 109484728)](https://support.industry.siemens.com/cs/document/109484728/)
