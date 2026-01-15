import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.decomposition import PCA
from knn_crisp import CrispKNN
from knn_fuzzy import FuzzyKNN

DATASETS = ['iris', 'wine', 'glass']
K_NEIGHBORS = 3
M_FUZZY = 2.0
STEP = 0.05

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
IMGS_DIR = os.path.join(BASE_DIR, 'docs', 'imgs')


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


def generate_decision_plot(dataset_name, X_full, y_full):
    print(f"   [Plot] Generowanie wykresu dla {dataset_name}...")

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_full)

    crisp_2d = CrispKNN(k=K_NEIGHBORS)
    crisp_2d.fit(X_pca, y_full)

    fuzzy_2d = FuzzyKNN(k=K_NEIGHBORS, m=M_FUZZY)
    fuzzy_2d.fit(X_pca, y_full)

    x_min, x_max = X_pca[:, 0].min() - 1, X_pca[:, 0].max() + 1
    y_min, y_max = X_pca[:, 1].min() - 1, X_pca[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, STEP),
                         np.arange(y_min, y_max, STEP))

    mesh_points = np.c_[xx.ravel(), yy.ravel()]

    Z_crisp = crisp_2d.predict(mesh_points).reshape(xx.shape)
    Z_fuzzy = fuzzy_2d.predict(mesh_points).reshape(xx.shape)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    unique_y = np.unique(y_full)
    cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF', '#FFFFAA', '#FFAAFF', '#AAFFFF'][:len(unique_y)])
    cmap_bold = ListedColormap(['#FF0000', '#008000', '#0000FF', '#CCCC00', '#FF00FF', '#00CCCC'][:len(unique_y)])

    titles = [f'Crisp KNN (k={K_NEIGHBORS})', f'Fuzzy KNN (k={K_NEIGHBORS}, m={M_FUZZY})']
    predictions = [Z_crisp, Z_fuzzy]

    for i, ax in enumerate(axes):
        ax.pcolormesh(xx, yy, predictions[i], cmap=cmap_light, shading='auto', alpha=0.6)
        ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y_full, cmap=cmap_bold, edgecolor='k', s=25)
        ax.set_title(titles[i])
        ax.set_xlabel('PCA 1')
        ax.set_ylabel('PCA 2')

    plt.suptitle(f"Porównanie granic decyzyjnych: {dataset_name.capitalize()}", fontsize=16)
    plt.tight_layout()

    save_path = os.path.join(IMGS_DIR, f"plot_{dataset_name}_comparison.png")
    plt.savefig(save_path)
    plt.close()
    print(f"   [Plot] Zapisano: {save_path}")


def run_full_pipeline():
    results = []

    os.makedirs(IMGS_DIR, exist_ok=True)

    print(f"{'=' * 60}")
    print(f"START TESTÓW I WIZUALIZACJI (k={K_NEIGHBORS}, m={M_FUZZY})")
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

        fuzzy_model = FuzzyKNN(k=K_NEIGHBORS, m=M_FUZZY)
        fuzzy_model.fit(X_train, y_train)
        fuzzy_preds = fuzzy_model.predict(X_test)
        fuzzy_acc = accuracy_score(y_test, fuzzy_preds)

        cm_crisp = confusion_matrix(y_test, crisp_preds)
        cm_fuzzy = confusion_matrix(y_test, fuzzy_preds)

        print(f"   [Stats] Crisp Acc: {crisp_acc:.2%}")
        print(f"   [Stats] Fuzzy Acc: {fuzzy_acc:.2%}")
        print(f"   [Stats] Macierz Crisp:\n{cm_crisp}")
        print(f"   [Stats] Macierz Fuzzy:\n{cm_fuzzy}")

        results.append({
            "Zbiór": ds_name.capitalize(),
            "Crisp Acc": f"{crisp_acc:.4f}",
            "Fuzzy Acc": f"{fuzzy_acc:.4f}",
            "Różnica": f"{fuzzy_acc - crisp_acc:+.4f}"
        })

        X_full = np.vstack((X_train, X_test))
        y_full = np.concatenate((y_train, y_test))

        generate_decision_plot(ds_name, X_full, y_full)
        print(f"{'-' * 60}\n")

    print("=== PODSUMOWANIE ZBIORCZE ===")
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))


if __name__ == "__main__":
    run_full_pipeline()