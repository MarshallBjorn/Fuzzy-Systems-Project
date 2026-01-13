# Część II: Teoretyczny opis różnić algorytmów kNN oraz Fuzzy kNN
### 1. Wstęp
Zaimplementowany system opiera się na podejściu tzw. uczenia leniwego (ang. lazy learning). Oznacza to, że system nie tworzy abstrakcyjnego modelu (np. drzewa decyzyjnego czy sieci neuronowej) podczas fazy treningu. Zamiast tego, zapamiętuje on cały zbiór danych treningowych.

Prawdziwa praca (obliczenia) rozpoczyna się dopiero w momencie, gdy system otrzymuje nowy, nieznany obiekt i musi zdecydować, do jakiej kategorii on należy. Decyzja podejmowana jest na podstawie analizy obiektów, które w przestrzeni cech znajdują się najbliżej badanego punktu.


### 2. Standardowy algorytm K-NN

Wersja klasyczna (Crisp kNN) opiera się na tzw. twardej decyzji.
Główną cechą jest że ten system zakłada, że ilość znaczy jakość. Jeśli wokół danego obiektu jest więcej punktów klasy A, to prawdopodobnie ten obiekt również należy do klasy A, niezależnie od dokładnego rozmieszczenia tych punktów.

Jako miarę podobieństwa między badaną próbką x a próbką treningową xj wykorzystano odległość Euklidesową.

### 2.1 Działanie algorytmu
Gdy system otrzymuje nowy obiekt do sklasyfikowania:

* Skanowanie przestrzeni: Algorytm przegląda wszystkie zapamiętane punkty ze zbioru treningowego i mierzy odległość (w linii prostej) od nowego obiektu do każdego z nich.
* Wybór sąsiedztwa: Spośród wszystkich punktów wybierana jest określona liczba (k) tych, które znajdują się fizycznie najbliżej.
* Twarde głosowanie: Każdy z wybranych sąsiadów oddaje głos na swoją własną klasę. W tym podejściu głos każdego sąsiada jest równy. Nie ma znaczenia, czy sąsiad jest tuż obok, czy znajduje się na granicy zasięgu – jego głos liczy się jako "1".
* Decyzja: Nowy obiekt zostaje przypisany do tej kategorii, która zebrała najwięcej głosów. W przypadku remisu decyduje zazwyczaj kolejność znalezienia sąsiadów.

### 3. Algorytm rozmyty (Fuzzy kNN)
Algorytm Fuzzy k-NN stanowi rozszerzenie klasycznego podejścia k-NN o elementy logiki rozmytej. W przeciwieństwie do wersji Crisp, algorytm ten nie podejmuje decyzji zero-jedynkowej, lecz opisuje przynależność obiektu do każdej klasy w sposób ciągły, za pomocą wektora przynależności.

Zamiast stwierdzenia, że obiekt należy lub nie należy do danej klasy, Fuzzy k-NN określa w jakim stopniu obiekt należy do poszczególnych klas. Suma wszystkich stopni przynależności wynosi 1, co umożliwia interpretację ich jako rozkładu pewności.

Kluczowym elementem algorytmu jest uwzględnienie odległości sąsiadów. Im bliżej znajduje się dany sąsiad, tym większy wpływ ma on na końcową decyzję. Stopień tego wpływu kontrolowany jest przez parametr rozmycia m (m > 1), który decyduje o tym, jak silnie algorytm różnicuje bliskich i dalszych sąsiadów.

### 3.1 Działanie algorytmu
Proces klasyfikacji nowego obiektu w algorytmie Fuzzy k-NN przebiega następująco:

* Obliczenie odległości: Podobnie jak w wersji klasycznej, obliczana jest odległość euklidesowa pomiędzy nowym obiektem a wszystkimi punktami zbioru treningowego.
* Wybór k sąsiadów: Spośród wszystkich punktów wybieranych jest k najbliższych sąsiadów.
* Wyznaczenie wag: Dla każdego sąsiada obliczana jest waga zależna od odległości. Wagi są odwrotnie proporcjonalne do odległości (z uwzględnieniem parametru m), co sprawia, że bliższe punkty mają znacznie większy wpływ na wynik.
* Agregacja przynależności: Wagi są sumowane osobno dla każdej klasy, tworząc wektor przynależności.
* Normalizacja: Wektor przynależności jest normalizowany tak, aby suma jego elementów wynosiła 1.
* Decyzja końcowa: Jeśli wymagane jest przypisanie „twardej” klasy, wybierana jest klasa o najwyższym stopniu przynależności (argmax).

Dodatkowo, w przypadku idealnego dopasowania (odległość równa zero), algorytm przypisuje obiektowi pełną przynależność do klasy identycznej próbki treningowej, eliminując ryzyko niestabilności numerycznej.

### 4. Porównanie obu algorytmów

### 4.1 Wiarygodność danych
W wersji klasycznej (Crisp) istnieje ryzyko błędu, jeśli wśród najbliższych sąsiadów znajdą się tzw. punkty odstające (szum). Wyobraź sobie sytuację, gdzie badany punkt jest bardzo blisko jednego punktu klasy A, ale nieco dalej otaczają go trzy punkty klasy B. Wersja klasyczna wybierze klasę B (bo 3 głosy przeciw 1), mimo że punkt A jest znacznie bliżej i bardziej wiarygodny.

W algorytmie Fuzzy k-NN problem ten jest w dużej mierze ograniczony. Dzięki zastosowaniu wag zależnych od odległości, bliższy sąsiad ma znacznie większy wpływ na wynik niż dalsze punkty. W opisanej sytuacji punkt klasy A, znajdujący się bardzo blisko badanego obiektu, otrzyma wysoką wagę, co może przeważyć nad większą liczbą dalszych sąsiadów klasy B. Dzięki temu algorytm jest bardziej odporny na szum i obserwacje odstające.

### 4.2 Niejednoznaczność
W wersji klasycznej często zdarzają się sytuacje sporne (np. 2 głosy na TAK, 2 głosy na NIE). Algorytm musi wtedy wybierać lub brać pierwszy wynik z brzegu.

Fuzzy k-NN naturalnie radzi sobie z takimi przypadkami, ponieważ nie wymusza jednoznacznej decyzji na wczesnym etapie. Zamiast tego zwraca stopnie przynależności do wszystkich klas, co pozwala:

* ocenić poziom niepewności klasyfikacji,
* wykryć obiekty leżące na granicach klas,
* wykorzystać wyniki w dalszych etapach systemu decyzyjnego.

Dopiero na końcu, jeśli jest to konieczne, można dokonać twardej decyzji, wybierając klasę o największej przynależności, zachowując jednocześnie informację o alternatywnych możliwościach.

## 5. Podsumowanie
