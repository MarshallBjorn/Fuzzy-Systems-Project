import numpy as np
from collections import Counter

class CrispKNN:
    def __init__(self, k=3):
        """
        Inicjalizacja klasycznego k-NN.
        :param k: Liczba sąsiadów do rozważenia.
        """
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        """
        Trening modelu
        :param X: Cechy treningowe (np. poziom szumu).
        :param y: Etykiety (np. poziom głośności).
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)

    def predict(self, X):
        """
        Przewidywanie klas dla nowych danych.
        """
        X = np.array(X)
        predictions = [self._predict_single(x) for x in X]
        return np.array(predictions)

    def _predict_single(self, x):
        # 1. Oblicz dystans euklidesowy między x a wszystkimi punktami treningowymi
        distances = [np.sqrt(np.sum((x_train - x) ** 2)) for x_train in self.X_train]

        # 2. Posortuj dystanse i wybierz indeksy k najmniejszych
        k_indices = np.argsort(distances)[:self.k]

        # 3. Pobierz etykiety najbliższych sąsiadów
        k_nearest_labels = [self.y_train[i] for i in k_indices]

        # 4. Głosowanie większościowe (Crisp vote)
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]