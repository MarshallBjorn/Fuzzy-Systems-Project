import numpy as np
import matplotlib.pyplot as plt
import os
from knn_crisp import CrispKNN


DATA_DIR = '../data'


def generate_mock_data(n_samples=50):
    """
    Generuje sztuczne dane:
    Cecha X: Poziom szumu w dB (np. 40-100 dB)
    Etykieta y: Poziom głośności nawigacji (0: Cicho, 1: Średnio, 2: Głośno)
    """
    np.random.seed(42)
    X = np.random.uniform(40, 100, n_samples).reshape(-1, 1)
    y = []

    for szum in X:
        if szum < 60:
            y.append(0)  # Cicho
        elif szum < 80:
            y.append(1)  # Średnio
        else:
            y.append(2)  # Głośno

    noise_indices = np.random.choice(n_samples, 5, replace=False)
    y = np.array(y)
    y[noise_indices] = np.random.randint(0, 3, 5)

    return X, y


def main():
    # 1. Przygotowanie danych
    print("Generowanie danych syntetycznych...")
    X, y = generate_mock_data(60)

    # Podział na trening i test (80% / 20%)
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]


    # 2. Uruchomienie Crisp k-NN
    k = 5
    print(f"Uruchamianie Crisp k-NN z k={k}...")
    knn = CrispKNN(k=k)
    knn.fit(X_train, y_train)
    predictions = knn.predict(X_test)

    # 3. Ewaluacja
    accuracy = np.mean(predictions == y_test)
    print(f"\n--- WYNIKI ---")
    print(f"Rzeczywiste klasy: {y_test}")
    print(f"Przewidziane klasy: {predictions}")
    print(f"Dokładność (Accuracy): {accuracy * 100:.2f}%")

    # 4. Przykładowa predykcja dla konkretnego szumu
    new_noise = [[55], [75], [95]]  # 55dB, 75dB, 95dB
    new_preds = knn.predict(new_noise)
    mapping = {0: "Cicho", 1: "Średnio", 2: "Głośno"}

    print("\n--- TESTY JEDNOSTKOWE ---")
    for noise, pred in zip(new_noise, new_preds):
        print(f"Szum: {noise[0]} dB -> Sugerowana głośność: {mapping[pred]}")


if __name__ == "__main__":
    main()