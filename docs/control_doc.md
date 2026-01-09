# Część I: Adaptacyjny system sterowania głośnością nawigacji (Interval Type-2 Fuzzy Logic)

### 1. Wstęp i Cel Projektu

Celem projektu jest zaprojektowanie i zaimplementowanie inteligentnego systemu sterowania głośnością komunikatów nawigacji dla roweru elektrycznego/miejskiego. W warunkach ruchu drogowego rowerzysta narażony jest na silnie zmienne warunki akustyczne. Przy dużych prędkościach dominuje szum wiatru, natomiast podczas postoju (np. na światłach) istotny staje się hałas otoczenia lub, przeciwnie, cisza osiedlowa.

Manualna regulacja głośności podczas jazdy odrywa uwagę i ręce od kierownicy, co stwarza bezpośrednie zagrożenie bezpieczeństwa. Klasyczne systemy sterowania (np. liniowe podgłaśnianie w funkcji prędkości) okazują się niewystarczające w sytuacjach nietypowych, takich jak wolna jazda w głośnym korku ulicznym. Z tego względu zaproponowano system adaptacyjny oparty na logice rozmytej, który automatycznie dostosowuje poziom dźwięku, zapewniając słyszalność komunikatów bez generowania "hałasu akustycznego" dla otoczenia.

### 2. Zastosowanie Uogólnień Zbiorów Rozmytych (Teoria)

[Tu miejsce na wsad teoretyczny od TN: Opis Interval Type-2 Fuzzy Logic, definicja Footprint of Uncertainty (FOU) oraz uzasadnienie matematyczne użycia uogólnień.]

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