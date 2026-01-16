# Analiza Wyników

W ramach eksperymentu przeprowadzono testy porównawcze dwóch klasyfikatorów: klasycznego **Crisp k-NN** oraz rozmytego **Fuzzy k-NN**. Oba algorytmy uruchomiono z parametrem sąsiedztwa $k=3$ (oraz $m=2.0$ dla wersji rozmytej) na zbiorach danych poddanych wcześniej normalizacji Min-Max. W celu wizualizacji granic decyzyjnych zastosowano redukcję wymiarowości metodą PCA (Principal Component Analysis).


### Zbiór Iris (Łatwa separowalność)

Wyniki liczbowe:

**Dokładność Crisp:** 93.33%

**Dokładność Fuzzy:** 93.33%

**Macierz pomyłek Crisp:**
```
[[15  0  0]
 [ 0 15  0]
 [ 0  3 12]]
```

**Macierz pomyłek Fuzzy:**
```
[[15  0  0]
 [ 0 15  0]
 [ 0  3 12]]
```
**Wizualizacja:**

![Porównanie dla Iris](docs/imgs/plot_iris_comparison.png)

**Analiza wizualna:** Wizualizacja PCA (Rys. 1) pokazuje, że klasy w zbiorze Iris są bardzo dobrze odseparowane (szczególnie klasa Setosa). Granice między klasami Versicolor i Virginica są stosunkowo wyraźne.

**Wniosek:** W przypadku danych liniowo separowalnych lub o bardzo małym poziomie szumu, narzut obliczeniowy logiki rozmytej nie przynosi wymiernych korzyści. Algorytm klasyczny radzi sobie tutaj doskonale, a wersja rozmyta osiąga identyczny wynik, de facto redukując się do działania klasycznego (ponieważ wagi dla bliskich sąsiadów dążą do 1, a punkty błędnie sklasyfikowane leżały zbyt głęboko w obszarze innej klasy, by wagi mogły zmienić decyzję).

### Zbiór Wine (Średnia złożoność)

Wyniki liczbowe:

**Dokładność Crisp:** 94.44%

**Dokładność Fuzzy:** 94.44%

**Macierz pomyłek Crisp:**
```
[[18  0  0]
 [ 1 18  2]
 [ 0  0 15]]
```
**Macierz pomyłek Fuzzy:**
```
[[18  0  0]
 [ 1 18  2]
 [ 0  0 15]]
```

**Wizualizacja:**

![Porównanie dla Wine](docs/imgs/plot_wine_comparison.png)

**Analiza wizualna:** Zbiór Wine charakteryzuje się większą liczbą wymiarów (13 cech). Po rzutowaniu do 2D widać, że strefy przynależności do klas są bardziej zwarte, ale granice są nieregularne.

**Wniosek:** Mimo że teoretycznie Fuzzy k-NN wygładza granice decyzyjne, w tym konkretnym podziale danych (train/test split) oba modele zachowały się identycznie. Błędy wystąpiły w klasie środkowej, która została pomylona z klasami sąsiednimi. Wskazuje to, że w zbiorze testowym nie znalazły się próbki "remisowe" lub leżące w takiej odległości od sąsiadów, gdzie wagi $1/d^2$ przeważyłyby nad prostym głosowaniem większościowym.
### Zbiór Glass (Trudna separowalność, wysoki szum)

Wyniki liczbowe:

**Dokładność Crisp:** 70.77%

**Dokładność Fuzzy:** 72.31% (+1.54 p.p.)

**Macierz pomyłek Crisp:**
```
[[15  5  1  0  0  0]
 [ 2 19  1  0  1  0]
 [ 3  1  1  0  0  0]
 [ 0  1  0  1  0  2]  <-- Klasa 4 (indeks 3): 1 trafienie
 [ 0  0  0  0  2  1]
 [ 0  1  0  0  0  8]]
```

**Macierz pomyłek Fuzzy:**
``` 
[[15  5  1  0  0  0]
 [ 2 19  1  0  1  0]
 [ 3  1  1  0  0  0]
 [ 0  0  0  2  0  2]  <-- Klasa 4 (indeks 3): 2 trafienia (Poprawa!)
 [ 0  0  0  0  2  1]
 [ 0  1  0  0  0  8]]
```
**Wizualizacja:**

![Porównanie dla Glass](docs/imgs/plot_glass_comparison.png)

**Analiza wizualna:** Jest to najtrudniejszy z badanych zbiorów. Klasy chemiczne szkła nakładają się na siebie (overlapping), a dane zawierają punkty odstające (outliers).

**Wniosek:** To tutaj ujawnia się przewaga podejścia rozmytego. Model Fuzzy osiągnął wyższą dokładność (72.31% vs 70.77%), poprawnie klasyfikując dodatkową próbkę w trudnej klasie (widoczna poprawa w 4. wierszu macierzy). Wynika to z dwóch czynników
1) Odporność na szum: W klasycznym k-NN pojedynczy punkt szumu (outlier) znajdujący się blisko granicy innej klasy może „przegłosować” wynik, tworząc błędną wyspę decyzyjną.
2) Wagi odległości: W Fuzzy k-NN, nawet jeśli $k=3$ sąsiadów jest z różnych klas (np. dwa z klasy A i jeden z klasy B), ale ten jeden z klasy B jest bardzo blisko badanej próbki (mały dystans euklidesowy), otrzyma on znacznie większą wagę ($w \approx 1/d^2$). Pozwala to na poprawną klasyfikację w gęstych, zachodzących na siebie obszarach.

## Podsumowanie i wnioski 

Na podstawie przeprowadzonych badań sformułowano następujące wnioski dotyczące wyższości systemów rozmytych nad klasycznymi (Crisp) w zadaniach klasyfikacji:

1) **Niejednoznaczność danych (Ambiguity):** Gdy granice między klasami nie są ostre (jak w zbiorze Glass), logika rozmyta pozwala modelować niepewność. Zamiast binarnej decyzji, system analizuje stopień przynależności, co jest bliższe rzeczywistej naturze zjawisk w świecie fizycznym.
2) **Problem remisów i małego K:** Wersja Crisp przy małym $k$ jest podatna na losowe rozstrzyganie remisów. W Fuzzy k-NN o wyniku decyduje precyzyjna suma wag, co pozwoliło na uzyskanie lepszego wyniku w najtrudniejszym zbiorze danych (Glass).
3) **Wiarygodność decyzji (Confidence Level):** Choć w tym badaniu mierzono accuracy (które jest metryką typu Crisp), największą zaletą Fuzzy k-NN jest informacja zwrotna.
   - **Crisp:** Zwraca: „To jest klasa A”.
   - **Fuzzy:** Zwraca wektor: „85% szans na klasę A, 15% na klasę B”.W systemach krytycznych (np. medycyna, sterowanie) taka informacja jest kluczowa – pozwala systemowi wstrzymać się od decyzji, gdy pewność (membership) jest niska dla wszystkich klas.

Wersja rozmyta (Fuzzy) zyskuje przewagę nad wersją klasyczną (Crisp) w środowiskach zaszumionych, przy nakładających się klasach oraz tam, gdzie kluczowa jest informacja o stopniu pewności klasyfikacji, a nie tylko sama etykieta końcowa.