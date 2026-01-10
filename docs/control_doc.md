# Część I: Adaptacyjny system sterowania głośnością nawigacji (Interval Type-2 Fuzzy Logic)

### 1. Wstęp i Cel Projektu

Celem projektu jest zaprojektowanie i zaimplementowanie inteligentnego systemu sterowania głośnością komunikatów nawigacji dla roweru elektrycznego/miejskiego. W warunkach ruchu drogowego rowerzysta narażony jest na silnie zmienne warunki akustyczne. Przy dużych prędkościach dominuje szum wiatru, natomiast podczas postoju (np. na światłach) istotny staje się hałas otoczenia lub, przeciwnie, cisza osiedlowa.

Manualna regulacja głośności podczas jazdy odrywa uwagę i ręce od kierownicy, co stwarza bezpośrednie zagrożenie bezpieczeństwa. Klasyczne systemy sterowania (np. liniowe podgłaśnianie w funkcji prędkości) okazują się niewystarczające w sytuacjach nietypowych, takich jak wolna jazda w głośnym korku ulicznym. Z tego względu zaproponowano system adaptacyjny oparty na logice rozmytej, który automatycznie dostosowuje poziom dźwięku, zapewniając słyszalność komunikatów bez generowania "hałasu akustycznego" dla otoczenia.

### 2. Zastosowanie Uogólnień Zbiorów Rozmytych (Teoria)

Tradycyjne zbiory rozmyte typu pierwszego (Type-1 Fuzzy Sets) charakteryzują się precyzyjnie zdefiniowanymi funkcjami przynależności, gdzie dla każdego elementu $x$ przypisana jest jedna, konkretna wartość stopnia przynależności $\mu(x) \in [0, 1]$. W rzeczywistych systemach sterowania, takich jak adaptacja głośności w ruchu ulicznym, często mamy do czynienia z niepewnością, której zbiory typu pierwszego nie są w stanie w pełni zamodelować. Źródłami tej niepewności mogą być szumy pomiarowe czujników (np. mikrofonu owiewanego wiatrem) lub subiektywność w definiowaniu pojęć lingwistycznych (np. granica między "cicho" a "umiarkowanie").

Aby rozwiązać ten problem, w projekcie zastosowano **Logikę Rozmytą Typu 2 (Interval Type-2 Fuzzy Logic System - IT2FLS)**.

#### 2.1. Interval Type-2 Fuzzy Sets i Footprint of Uncertainty (FOU)

Zbiór rozmyty typu 2 można interpretować jako zbiór, którego funkcja przynależności jest sama w sobie rozmyta. W przypadku interwałowym (Interval Type-2), stopień przynależności dla danego wejścia nie jest pojedynczą liczbą, lecz przedziałem wartości.

Kluczowym pojęciem jest tutaj **Ślad Niepewności (Footprint of Uncertainty - FOU)**. FOU to obszar ograniczony przez dwie funkcje przynależności typu 1:
*   **Górna Funkcja Przynależności (Upper Membership Function - UMF),** oznaczana jako $\bar{\mu}(x)$,
*   **Dolna Funkcja Przynależności (Lower Membership Function - LMF),** oznaczana jako $\underline{\mu}(x)$.

Dla każdego argumentu $x$, stopień przynależności jest przedziałem:
$$ \mu_{\tilde{A}}(x) = [\underline{\mu}(x), \bar{\mu}(x)] $$

Obszar FOU reprezentuje całą niepewność zawartą w definicji zbioru. Im szerszy FOU, tym większa tolerancja systemu na niedokładności danych wejściowych.

#### 2.2. Uzasadnienie Matematyczne i Praktyczne

Zastosowanie uogólnień w postaci IT2FLS w sterowniku głośności wynika z następujących przesłanek:

1.  **Modelowanie szumu:** W warunkach jazdy rowerem odczyt poziomu hałasu (dB) jest silnie zaszumiony (np. porywy wiatru). W logice typu 1, chwilowa zmiana wartości wejściowej mogłaby spowodować nagłe przełączenie reguły. W logice typu 2, dzięki FOU, małe fluktuacje mieszczą się wewnątrz "grubości" funkcji przynależności, co stabilizuje wyjście sterownika.
2.  **Gładkość powierzchni sterowania:** Systemy IT2FLS generują zazwyczaj gładsze powierzchnie sterowania w okolicach przełączeń reguł niż systemy typu 1. Wynika to z procesu redukcji typu (Type-Reduction), który uśrednia wnioskowanie z górnych i dolnych funkcji przynależności.
3.  **Robustness (Odporność):** Matematycznie udowodniono, że systemy IT2FLS potrafią aproksymować złożone funkcje sterowania przy mniejszej liczbie reguł niż systemy typu 1, zachowując przy tym większą odporność na błędy modelowania.

W kontekście projektu, użycie IT2FLS pozwala na uniknięcie zjawiska "skakania" głośności przy niestabilnych odczytach z mikrofonu, co bezpośrednio przekłada się na komfort i bezpieczeństwo użytkownika.

### 3. Projekt Systemu Sterowania

#### 3.1. Zmienne Lingwistyczne

System operuje na dwóch zmiennych wejściowych i jednej wyjściowej. Zakresy (Universum) dobrano na podstawie typowej charakterystyki jazdy rowerem miejskim oraz parametrów akustycznych.

##### Wejście 1: Prędkość (Speed)
- **Zakres:** 0 – 50 km/h
- **Termy** (Zbiory):
  1. `Low` (Wolna jazda / Manewrowanie / Postój)
  2. `Medium` (Typowa prędkość podróżna)
  3. `High` (Szybka jazda / Zjazd)

##### Wejście 2: Hałas (Noise)
- **Zakres**: 40 – 100 dB
- **Termy** (Zbiory):
  1. `Quiet` (Cicha ulica / Park)
  2. `Moderate` (Umiarkowany ruch miejski)
  3. `Loud` (Duży ruch / Silny wiatr / Ciężarówki)

##### Wyjście: Głośność Nawigacji (Volume)
- **Zakres**: 0 – 100 % (Wysterowanie głośnika)
- **Termy** (Zbiory): 
  1. `Low`
  2. `Medium`
  3. `High`

#### 3.2. Funkcje Przynależności i Optymalizacja Systemu (Tuning)

Kluczowym aspektem projektu było dobranie odpowiedniego kształtu funkcji przynależności. Wstępne testy z wykorzystaniem funkcji trójkątnych dla wartości środkowych (Medium) wykazały niestabilność sterowania – w punktach przejściowych między regułami następowały gwałtowne spadki wartości sterującej (tzw. oscylacje lub "rogi" na charakterystyce).

Aby wyeliminować ten problem i zapewnić wymaganą płynność sterowania (Smooth Control), w finalnym rozwiązaniu zastosowano funkcje trapezowe (Trapezoidal Membership Functions) dla wszystkich zbiorów rozmytych. Trapezoidalny kształt zapewnia szersze jądro (obszar o przynależności 1.0), co stabilizuje odpowiedź układu przy niewielkich fluktuacjach wejścia. Dodatkowo, wykorzystując właściwości Interval Type-2 Fuzzy Logic, zwiększono stopień nakładania się (overlap) Dolnych Funkcji Przynależności (LMF). Zabieg ten wyeliminował martwe strefy, w których sterownik traciłby pewność decyzyjną.

#### 3.3. Baza Reguł (FAM)

Zdefiniowano kompletną bazę 9 reguł wnioskowania typu Mamdani:

| **Prędkość \ Hałas** | **Quiet** | **Moderate** | **Loud** |
|----------------------|-----------|--------------|----------|
| **Low**              | Low       | Low          | Medium   |
| **Medium**           | Low       | Medium       | High     |
| **High**             | Medium    | High         | High     |

### 4. Analiza Empiryczna i Wyniki

Zgodnie z wymaganiami projektowymi (ocena adekwatności rozwiązania), przeprowadzono weryfikację działania sterownika poprzez symulację dynamiczną oraz analizę powierzchni sterowania.

#### 4.1. Symulacja Scenariusza Drogowego

Wygenerowano scenariusz testowy o czasie trwania 60 sekund, odwzorowujący rzeczywisty przejazd. Scenariusz obejmuje: ruszanie z miejsca, nagły incydent akustyczny przy stałej prędkości (np. przejazd pojazdu uprzywilejowanego) oraz jazdę z dużą prędkością.

![image](/Users/oleksijnavrockij/Documents/UR/SR/Fuzzy-Systems-Project/docs/imgs/plotSimulation.png)
Rys. 1. Przebieg zmiennych wejściowych (góra) oraz odpowiedź sterownika (dół) w czasie.

**Analiza wyników symulacji:**
Na podstawie wykresu (Rys. 1) można stwierdzić poprawność działania algorytmu:

W przedziale 10s – 20s (linia pomarańczowa) następuje gwałtowny wzrost hałasu przy zachowaniu stałej prędkości. System reaguje natychmiastowym podniesieniem głośności (linia zielona) do poziomu ok. 80%, co gwarantuje przebicie się komunikatu przez hałas tła.

Charakterystyka zmian jest płynna. Nie występują niepożądane skoki typu "włącz/wyłącz", które mogłyby dezorientować użytkownika. Jest to efekt zastosowania logiki rozmytej, która interpoluje wynik pomiędzy regułami.

#### 4.2. Charakterystyka Powierzchniowa (Control Surface)

W celu zbadania globalnej spójności reguł i braku uchybień w logice, wygenerowano trójwymiarową powierzchnię sterowania układu.

![image](/Users/oleksijnavrockij/Documents/UR/SR/Fuzzy-Systems-Project/docs/imgs/plotSurface.png)
Rys. 2. Powierzchnia sterowania (Control Surface) dla układu Interval Type-2.

**Wnioski:**
Wygenerowana powierzchnia sterowania wykazuje cechę monotoniczności oraz gładkości. Nie występują lokalne minima (tzw. "dziury" w sterowaniu), gdzie głośność spadałaby mimo wzrostu parametrów wejściowych. "Płaskowyże" (płaskie obszary na wykresie) wskazują na stabilność systemu w stanach ustalonych, co jest bezpośrednią zasługą zastosowania szerokiego obszaru niepewności (FOU) w logice Type-2.

### 5. Podsumowanie

Zaprojektowany adaptacyjny układ sterowania głośnością spełnia założenia projektowe. Część praktyczna wykazała, że zastosowanie uogólnień teorii zbiorów rozmytych (Interval Type-2 Fuzzy Logic) pozwoliło na stworzenie systemu odpornego na szum pomiarowy i zapewniającego wyższą kulturę pracy niż klasyczne rozwiązania progowe. Otrzymane wyniki empiryczne (symulacja i powierzchnia sterowania) jednoznacznie potwierdzają adekwatność i stabilność zaproponowanego rozwiązania.