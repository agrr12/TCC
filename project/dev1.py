

from sklearn.cluster import AgglomerativeClustering
import numpy as np
import analysis_API as AP
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt


a = AP.create_comparison_matrix()
# Set numpy print options
np.set_printoptions(threshold=np.inf)

# Print the complete matrix
print(a)
# Perform Agglomerative Clustering based on the similarity matrix
# Note: Since the matrix is a similarity matrix, we might need to convert it into a distance matrix,
# which can be achieved by subtracting it from 1 (assuming values are between 0 and 1).
clustering = AgglomerativeClustering(n_clusters=2, affinity='precomputed', linkage='average')
distance_matrix = 1 - a
labels = clustering.fit_predict(a)
print("\nCluster Labels:")
print(labels)

# Using the same distance_matrix from before
Z = linkage(a, method='average')
plt.figure(figsize=(10, 7))
dendrogram(Z)
plt.title("Dendrogram")
plt.show()