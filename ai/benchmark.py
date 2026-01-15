import os
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
from knn_crisp import CrispKNN
from knn_fuzzy import FuzzyKNN

DATASETS = ['iris', 'wine', 'glass']
K_NEIGHBORS = 3
M_FUZZY = 2.0

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


def load_data(dataset_name):
    train_path = os.path.join(DATA_DIR, f"{dataset_name}_train.csv")
    test_path = os.path.join(DATA_DIR, f"{dataset_name}_test.csv")

    if not os.path.exists(train_path) or not os.path.exists(test_path):
        print(f"Pominięto {dataset_name}: brak plików w folderze data/")
        return None, None, None, None

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train = train_df.drop(columns=['target']).values
    y_train = train_df['target'].values

    X_test = test_df.drop(columns=['target']).values
    y_test = test_df['target'].values

    return X_train, y_train, X_test, y_test


def print_confusion_matrix(y_true, y_pred, title):
    cm = confusion_matrix(y_true, y_pred)
    print(f"\n--- Macierz Pomyłek: {title} ---")
    print(cm)
    return cm


def run_benchmark():
    results = []

    print(f"{'=' * 60}")
    print(f"START TESTÓW PORÓWNAWCZYCH (k={K_NEIGHBORS}, m={M_FUZZY})")
    print(f"{'=' * 60}\n")

    for ds_name in DATASETS:
        print(f"ZBIÓR DANYCH: {ds_name.upper()}")

        X_train, y_train, X_test, y_test = load_data(ds_name)
        if X_train is None:
            continue

        crisp_model = CrispKNN(k=K_NEIGHBORS)
        crisp_model.fit(X_train, y_train)
        crisp_preds = crisp_model.predict(X_test)

        crisp_acc = accuracy_score(y_test, crisp_preds)
        print_confusion_matrix(y_test, crisp_preds, "Crisp KNN")

        fuzzy_model = FuzzyKNN(k=K_NEIGHBORS, m=M_FUZZY)
        fuzzy_model.fit(X_train, y_train)
        fuzzy_preds = fuzzy_model.predict(X_test)

        fuzzy_acc = accuracy_score(y_test, fuzzy_preds)
        print_confusion_matrix(y_test, fuzzy_preds, "Fuzzy KNN")

        results.append({
            "Zbiór": ds_name.capitalize(),
            "Crisp Acc": f"{crisp_acc:.4f}",
            "Fuzzy Acc": f"{fuzzy_acc:.4f}",
            "Różnica": f"{fuzzy_acc - crisp_acc:+.4f}"
        })

        print(f"\nWyniki dla {ds_name}:")
        print(f"  > Crisp Accuracy: {crisp_acc:.2%}")
        print(f"  > Fuzzy Accuracy: {fuzzy_acc:.2%}")
        print(f"{'-' * 60}\n")

    print("=== PODSUMOWANIE ZBIORCZE ===")
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))


if __name__ == "__main__":
    run_benchmark()