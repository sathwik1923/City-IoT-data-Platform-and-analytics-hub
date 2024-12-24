import pandas as pd
from sklearn.datasets import make_classification
from imblearn.under_sampling import NearMiss
from collections import Counter
import matplotlib.pyplot as plt

# Generate a synthetic imbalanced dataset
X, y = make_classification(n_classes=2, class_sep=2, weights=[0.1, 0.9], n_informative=3, n_redundant=1, flip_y=0, n_features=20, n_clusters_per_class=1, n_samples=1000, random_state=10)

# Convert to DataFrame for ease of use
df = pd.DataFrame(X)
df['target'] = y

# Split features and target
X = df.drop('target', axis=1)
y = df['target']

# Display original class distribution
print(f'Original dataset shape: {Counter(y)}')

# Apply NearMiss
nm = NearMiss(version=1)  # You can change to version=2 or version=3
X_resampled, y_resampled = nm.fit_resample(X, y)

# Display resampled class distribution
print(f'Resampled dataset shape: {Counter(y_resampled)}')

# Visualize original and resampled data distribution
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Original data distribution
axs[0].bar(Counter(y).keys(), Counter(y).values(), color=['blue', 'orange'])
axs[0].set_title('Original Data Distribution')
axs[0].set_xticks([0, 1])
axs[0].set_xticklabels(['Class 0', 'Class 1'])

# Resampled data distribution
axs[1].bar(Counter(y_resampled).keys(), Counter(y_resampled).values(), color=['blue', 'orange'])
axs[1].set_title('Resampled Data Distribution')
axs[1].set_xticks([0, 1])
axs[1].set_xticklabels(['Class 0', 'Class 1'])

plt.show()
