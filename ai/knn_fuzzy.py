import numpy as np

class FuzzyKNN:
    """
    Fuzzy k-NN classifier implementing class membership vectors.
    """

    def __init__(self, k=3, m=2.0, epsilon=1e-10):
        """
        :param k: number of nearest neighbors
        :param m: fuzziness parameter (m > 1), usually m = 2
        :param epsilon: small value to avoid division by zero
        """
        if m <= 1:
            raise ValueError("Parameter m must be > 1 for fuzzy k-NN")

        self.k = k
        self.m = m
        self.epsilon = epsilon
        self.X_train = None
        self.y_train = None
        self.classes_ = None
        self.class_to_index_ = None

    def fit(self, X, y):
        """
        Store training data and prepare class information.
        :param X: training feature matrix
        :param y: training labels
        """
        self.X_train = np.array(X)
        self.y_train = np.array(y)

        # Unique classes and mapping to indices
        self.classes_ = np.unique(self.y_train)
        self.class_to_index_ = {
            cls: idx for idx, cls in enumerate(self.classes_)
        }

    def predict(self, X):
        """
        Predict crisp class labels for input samples
        (argmax over membership vector).
        """
        memberships = self.predict_membership(X)
        class_indices = np.argmax(memberships, axis=1)
        return self.classes_[class_indices]

    def predict_membership(self, X):
        """
        Predict fuzzy membership vectors for input samples.
        :param X: input feature matrix
        :return: membership matrix of shape (n_samples, n_classes)
        """
        X = np.array(X)
        memberships = [self._predict_single_membership(x) for x in X]
        return np.array(memberships)

    def _predict_single_membership(self, x):
        """
        Compute the fuzzy membership vector for a single sample.
        """
        # 1. Compute Euclidean distances
        distances = np.linalg.norm(self.X_train - x, axis=1)

        # 2. Get k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        k_distances = distances[k_indices]
        k_labels = self.y_train[k_indices]

        # 3. Handle exact match (distance == 0)
        if np.any(k_distances < self.epsilon):
            membership = np.zeros(len(self.classes_))
            exact_label = k_labels[np.argmin(k_distances)]
            membership[self.class_to_index_[exact_label]] = 1.0
            return membership

        # 4. Compute fuzzy weights
        power = 2.0 / (self.m - 1.0)
        weights = 1.0 / ((k_distances + self.epsilon) ** power)

        # 5. Aggregate memberships per class
        membership = np.zeros(len(self.classes_))
        for w, label in zip(weights, k_labels):
            class_idx = self.class_to_index_[label]
            membership[class_idx] += w

        # 6. Normalize membership vector
        membership_sum = np.sum(membership)
        if membership_sum > 0:
            membership /= membership_sum

        return membership
