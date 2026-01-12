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
* Twarde głosowanie: Każdy z wybranych sąsiadów oddaje głos na swoją własną klasę.W tym podejściu głos każdego sąsiada jest równy. Nie ma znaczenia, czy sąsiad jest tuż obok, czy znajduje się na granicy zasięgu – jego głos liczy się jako "1".
* Decyzja: Nowy obiekt zostaje przypisany do tej kategorii, która zebrała najwięcej głosów. W przypadku remisu decyduje zazwyczaj kolejność znalezienia sąsiadów.

### 3 Algorytm rozmyty (Fuzzy kNN)

(do uzupełnienia o fuzzy)

### 4. Porównanie obu algorytmów

### 4.1 Wiarygodność danych
W wersji klasycznej (Crisp) istnieje ryzyko błędu, jeśli wśród najbliższych sąsiadów znajdą się tzw. punkty odstające (szum). Wyobraź sobie sytuację, gdzie badany punkt jest bardzo blisko jednego punktu klasy A, ale nieco dalej otaczają go trzy punkty klasy B. Wersja klasyczna wybierze klasę B (bo 3 głosy przeciw 1), mimo że punkt A jest znacznie bliżej i bardziej wiarygodny.

(do uzupełnienia o fuzzy)

### 4.2 Niejednoznaczność

W wersji klasycznej często zdarzają się sytuacje sporne (np. 2 głosy na TAK, 2 głosy na NIE). Algorytm musi wtedy wybierać lub brać pierwszy wynik z brzegu.

(do uzupełnienia o fuzzy)

## 5. Podsumowanie