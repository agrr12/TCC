

from sklearn.cluster import AgglomerativeClustering
import numpy as np
import analysis_API as AP
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt



# Perform Agglomerative Clustering based on the similarity matrix
# Note: Since the matrix is a similarity matrix, we might need to convert it into a distance matrix,
# which can be achieved by subtracting it from 1 (assuming values are between 0 and 1).
#clustering = AgglomerativeClustering(affinity='precomputed', linkage='average')
#distance_matrix = 1 - a
#labels = clustering.fit_predict(a)
#print("\nCluster Labels:")
#print(labels)

path ='/home/agrr/ProjectsPy/TCC/project/CSVs/comparison_metrics/AWARP_hou_w100.csv'
c1 = 'User1'
c2 = 'User2'
# Using the same distance_matrix from before
for x in ['AWARP']:
    a = AP.create_comparison_matrix(path, c1, c2, x)
    Z = linkage(a, method='average')
    plt.figure(figsize=(10, 9))
    dendrogram(Z)
    plt.savefig(f'Analysis/Dendograms/small/awarp_hours_{x}_dendogram_small.png')
    plt.clf()
    plt.figure(figsize=(100, 90))
    dendrogram(Z)
    plt.savefig(f'Analysis/Dendograms/large/awarp_hours_{x}_dendogram_large.png')
