"""Patch: add encoder questions Q1.15, Q16.12, Q16.13 to qa_draft_v11.md"""

path = 'docs/qa_draft_v11.md'
content = open(path, encoding='utf-8').read()

# ============================================================
# Q1.15 — after Q1.14 (before section 2 header)
# ============================================================
Q115 = """
### 1.15. Czym jest enkoder i jaka jest różnica między inkrementalnym a absolutnym?  🟡

**Enkoder** (przetwornik obrotowo-impulsowy) to czujnik zamieniający ruch mechaniczny (kąt/pozycję) na sygnał elektryczny odczytywany przez napęd lub PLC.

| Cecha | Inkrementalny | Absolutny |
|-------|---------------|-----------|
| **Sygnał wyjściowy** | Impulsy zliczane od punktu startowego | Unikalna wartość liczbowa = aktualna pozycja |
| **Po zaniku zasilania** | Traci pozycję — wymaga referencjonowania (homing) | Zachowuje pozycję *(absolutny)* |
| **Homing (referencja)** | Wymagany po każdym starcie | Nie wymagany *(single-turn)* lub nie wymagany *(multi-turn)* |
| **Interfejsy** | TTL (A/B/Z), HTL, sin/cos 1 Vpp | SSI, EnDat 2.1/2.2, HIPERFACE, HIPERFACE DSL |
| **Rozdzielczość** | 100 – 65 536 imp/obrót (PPR) | 12 – 25 bit/obrót |
| **Koszt** | Niższy | Wyższy |
| **Zastosowanie** | Przenośniki, wentylatory, proste osie | Roboty, osie pionowe, serwosystemy |

**Single-turn vs Multi-turn (absolutne):**
- **Single-turn:** unikalny kod dla 1 pełnego obrotu (0°–360°). Po przekręceniu o >1 obrót — traci pozycję absolutną.
- **Multi-turn:** dodatkowy mechanizm (getriebe optyczny lub zasilanie bateryjne) liczy pełne obroty. Np. 17 bit (131 072 poz/obrót) + 12 bit multi-turn (4096 obrotów) = ponad 536 mln unikalnych pozycji.

> ⚠️ **Osie pionowe i roboty:** zawsze absolutny enkoder multi-turn — po zaniku zasilania maszyna wie dokładnie gdzie jest ramię bez potrzeby homing. Inkrementalny = homing po każdym resecie = niebezpieczne przy obciążeniu.

> 💡 **Na rozmowie:** pytanie o enkodery często pojawia się razem z SLS/SDI — wspomnij że do tych funkcji Safety wymagane są enkodery certyfikowane (HIPERFACE Safety, EnDat Safety).

"""

INSERT_BEFORE_S2 = "\n---\n\n## 2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED"
if INSERT_BEFORE_S2 in content:
    content = content.replace(
        INSERT_BEFORE_S2,
        Q115 + "\n---\n\n## 2. ARCHITEKTURA SIMATIC SAFETY INTEGRATED",
        1
    )
    print("Q1.15 inserted OK")
else:
    print("Q1.15 insertion point NOT FOUND")

# ============================================================
# Q16.12 and Q16.13 — after Q16.11 (before section 17)
# ============================================================
BEFORE_S17 = "*Źródło: transkrypcje ControlByte*\n\n---\n\n## 17. REALNE SCENARIUSZE COMMISSIONING"

Q1612 = """
### 16.12. Jakie są parametry enkoderów inkrementalnych i absolutnych — rozdzielczość, co mogą i czego nie mogą?  🟡

**Enkoder inkrementalny — kluczowe parametry:**

| Parametr | Typowe wartości | Opis |
|----------|----------------|------|
| **PPR** *(Pulses Per Revolution)* | 100 / 512 / 1024 / 2048 / 4096 / 8192 | Impulsy na jeden pełny obrót osi enkodera |
| **Napięcie zasilania** | 5 V DC (TTL) / 12–24 V DC (HTL) | TTL = linie różnicowe, HTL = sygnał push-pull |
| **Sygnały** | A, B (faza 90°), Z (indeks/zerowy) | A+B → kierunek i liczba impulsów; Z → punkt odniesienia |
| **Max częstotliwość** | do 500 kHz (HTL) / do 1 MHz (TTL) | Limit dla modułu licznikowego lub wejścia HSC |
| **Ochrona** | IP54–IP67 | Zależnie od producenta i montażu |

**Enkoder absolutny — kluczowe parametry:**

| Parametr | Typowe wartości | Opis |
|----------|----------------|------|
| **Rozdzielczość single-turn** | 12–25 bit | 17 bit = 131 072 pozycji/obrót (typowy HIPERFACE/EnDat) |
| **Rozdzielczość multi-turn** | 12 bit dodatkowe | 4096 pełnych obrotów liczonych niezależnie |
| **Interfejs** | SSI, EnDat 2.1/2.2, HIPERFACE, HIPERFACE DSL | Patrz Q16.13 |
| **Czas odpowiedzi** | do 8 µs (EnDat 2.2) | Limit dla krótkiego czasu cyklu napędu |
| **Diagnostyka** | temperatura, błędy wewnętrzne | Dostępna przez EnDat 2.2 i HIPERFACE DSL |

**Co mogą:**
- Precyzyjne pozycjonowanie do ±1 impulsu (inkrementalny) lub ±0.003° przy 17 bit (absolutny)
- Pomiar prędkości: $n = (f \times 60) / PPR$ [rpm]
- Multi-turn absolutny: śledzenie pozycji przez wiele obrotów bez zasilania bateryjnego
- Diagnostyka wewnętrzna (temperatura, błędy — EnDat 2.2, HIPERFACE DSL)
- Synchronizacja osi (`TO_ExternalEncoder` w TIA Portal) — wałek wirtualny, master-slave

**Czego nie mogą:**
- **Inkrementalny:** nie pamięta pozycji po zaniku zasilania → **zawsze wymaga homing** po resecie
- **Inkrementalny:** nie ma jednoznacznej pozycji absolutnej → niebezpieczne przy osiach pionowych z obciążeniem
- **Absolutny single-turn:** zlicza tylko jeden obrót → po >360° traci pozycję absolutną
- **Standard enkodery:** nie są certyfikowane Safety → **nie można ich używać dla SLS/SDI** (wymagają enkoder Safety: HIPERFACE Safety lub EnDat Safety)
- **HTL przy dużej prędkości:** ograniczona częstotliwość (~500 kHz) → przy dużej prędkości i wysokim PPR może dochodzić do utraty impulsów

> ⚠️ **Safety funkcje SLS/SDI:** SINAMICS wymaga enkodera certyfikowanego Safety (HIPERFACE Safety lub EnDat Safety) wbudowanego w silnik — standardowy enkoder przemysłowy nie spełnia wymagań IEC 61800-5-2 dla „safe encoder feedback".

> 💡 **Przelicznik rozdzielczości:** enkoder 1024 PPR z interpolacją ×4 (A, /A, B, /B) daje **4096 kroków/obrót** — to standardowe zachowanie modułu HSC lub SINAMICS przy zliczaniu czterech zboczy.

"""

Q1613 = """
### 16.13. Jakie są interfejsy enkoderów i jak konfigurujesz enkoder w SINAMICS i TIA Portal?  🟡

**Przegląd interfejsów:**

| Interfejs | Typ sygnału | Napięcie | Kierunek | Typowe zastosowanie |
|-----------|------------|----------|----------|---------------------|
| **TTL (A/B/Z)** | Cyfrowy różnicowy | 5 V DC | Jednostronny | S7-1200 HSC, proste osi, tanie aplikacje |
| **HTL (A/B/Z)** | Cyfrowy push-pull | 12–24 V DC | Jednostronny | Środowisko przemysłowe, odporność na EMC |
| **Sin/Cos 1 Vpp** | Analogowy sinusoidalny | 5 V / 12 V | Jednostronny | G120 z CU240E, wysoka rozdzielczość przez interpolację |
| **SSI** | Szeregowy synchroniczny | 5 V / 12 V | Jednostronny | Absolutne enkoderzy starszej generacji |
| **EnDat 2.1/2.2** | Szeregowy, dwukierunkowy | 5 V DC | Dwukierunkowy | S120, SIMOTION, nowoczesne SINAMICS — wysoka dynamika |
| **HIPERFACE** | Sin/Cos + RS-485 | 7–12 V DC | Dwukierunkowy | Silniki Siemens 1FK7/1FT7 (classic) |
| **HIPERFACE DSL** | Cyfrowy, tylko 2 żyły | 5 V DC | Dwukierunkowy | V90 z 1FG/1FK7 — kabel enkodera = kabel mocy |

**Konfiguracja w SINAMICS Startdrive:**

| Parametr | Opis | Przykładowe wartości |
|----------|------|---------------------|
| `p0400` | Typ enkodera | 0=brak, 1=TTL/HTL inkr., 4=SSI, 9=EnDat 2.2, 11=HIPERFACE sin/cos |
| `p0404` | Liczba PPR (impulsy/obrót) | 1024, 2048, 4096, 8192 |
| `p0406` | Napięcie zasilania enkodera | 0=5V, 1=12V, 2=24V |
| `p0408` | Liczba bitów SSI | 10–30 bit |
| `p0418` | Współczynnik interpolacji sin/cos | 1024 lub 2048 |
| `p0431` | Korekta offsetu enkodera (fine adjust) | Wartość w impulsach |

**Konfiguracja Technology Object (TIA Portal Motion Control):**
1. TIA Portal → Technology objects → wybrany TO (`TO_PositioningAxis` lub `TO_ExternalEncoder`)
2. Zakładka `Encoder` → `Encoder type`: Incremental / Absolute
3. Ustaw: `Data exchange type` (np. PROFIdrive, analog sin/cos, HSC module)
4. `Encoder resolution`: podaj PPR lub ilość bitów
5. Dla `TO_ExternalEncoder`: wskaż moduł HSC (S7-1200) lub interfejs sieciowy enkodera (ET200S counting module)

**Wejście HSC (High Speed Counter) w S7-1200/S7-1500 dla enkoderów TTL/HTL:**
- S7-1200: wbudowane HSC (`HSC1–HSC6`) — max **100 kHz** na kanał; moduł SB 1221 High Speed zwiększa do **200 kHz**
- S7-1500T: moduł TM PosInput (6ES7138-6AA01) dla enkoderów sin/cos / TTL do 1 MHz

> ⚠️ **PROFINET enkoder z Technology Object:** telegram `102` (z enkoderem) wymaga że SINAMICS odbiera pozycję z wbudowanego enkodera przez Startdrive, następnie przesyła ją do CPU przez PROFINET jako część PZD telegramu. Telegramy `1` i `20` **nie zawierają** danych enkodera — tylko prędkość!

> 💡 **HIPERFACE DSL:** jeden kabel do serwosilnika zawiera jednocześnie zasilanie silnika (3 fazy + PE) i sygnał enkodera DSL — brak osobnego kabla enkodera. Stosowany w Sinamics V90 z silnikami 1FK7. Upraszcza montaż ale wymaga specjalnego kabla (Siemens Motion Connect 500).

"""

if BEFORE_S17 in content:
    content = content.replace(
        BEFORE_S17,
        "*Źródło: transkrypcje ControlByte*\n" + Q1612 + Q1613 + "\n---\n\n## 17. REALNE SCENARIUSZE COMMISSIONING",
        1
    )
    print("Q16.12 and Q16.13 inserted OK")
else:
    print("Q16.12/16.13 insertion point NOT FOUND")
    idx = content.find("*Źródło: transkrypcje ControlByte*\n\n---\n\n## 17.")
    if idx > 0:
        print("Found at:", idx)
        print(repr(content[idx:idx+100]))

open(path, 'w', encoding='utf-8').write(content)
print("Done — all encoder questions added")
