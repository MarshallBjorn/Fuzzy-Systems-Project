import numpy as np
import os
import csv
from knn_crisp import CrispKNN

DATASET_NAME = 'iris'

TRAIN_FILE = os.path.join('..', 'data', f'{DATASET_NAME}_train.csv')
TEST_FILE = os.path.join('..', 'data', f'{DATASET_NAME}_test.csv')


def load_dataset(filename):
    if not os.path.exists(filename):
        print(f"BŁĄD: Nie znaleziono pliku {filename}")
        return None, None

    data_points = []
    labels = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        try:
            next(reader)

            for row in reader:
                if not row: continue

                features = [float(x) for x in row[:-1]]
                label = float(row[-1])

                data_points.append(features)
                labels.append(label)

        except ValueError as e:
            print(f"Błąd parsowania w pliku {filename}. Czy plik ma nagłówek? {e}")
            return None, None

    return np.array(data_points), np.array(labels)


def main():
    print(f"Uruchamianie Crisp k-NN dla zbioru: {DATASET_NAME.upper()} ---")

    # 1. Wczytanie danych
    print(f"Wczytywanie danych treningowych z: {TRAIN_FILE}")
    X_train, y_train = load_dataset(TRAIN_FILE)

    print(f"Wczytywanie danych testowych z: {TEST_FILE}")
    X_test, y_test = load_dataset(TEST_FILE)

    if X_train is None or X_test is None:
        print("Przerwano z powodu błędu wczytywania danych.")
        return

    print(f"Wymiary treningowe: {X_train.shape}")
    print(f"Wymiary testowe: {X_test.shape}")

    # 2. Uruchomienie Crisp k-NN
    k = 3
    print(f"\nUczenie modelu k-NN (k={k})...")
    knn = CrispKNN(k=k)
    knn.fit(X_train, y_train)

    # 3. Predykcja
    print("Rozpoczynam klasyfikację zbioru testowego...")
    predictions = knn.predict(X_test)

    # 4. Ewaluacja
    accuracy = np.mean(predictions == y_test)

    print(f"\n--- WYNIKI ({DATASET_NAME}) ---")
    print(f"Pierwsze 10 rzeczywistych: {y_test[:10]}")
    print(f"Pierwsze 10 przewidzianych: {predictions[:10]}")

    print(f"\nDokładność (Accuracy): {accuracy * 100:.2f}%")

    # Wyliczanie błędów
    errors = np.sum(predictions != y_test)
    print(f"Liczba błędów: {errors} na {len(y_test)} przykładów.")


if __name__ == "__main__":
    main()