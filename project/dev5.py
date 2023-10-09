import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
import analysis_API as AP
from scipy.spatial.distance import squareform


# Load matrices
matrices = {
    'awarp': AP.create_comparison_matrix('CSVs/comparison_metrics/AWARP_hou_w100.csv', 'User1','User2','AWARP'),
    'scatter_MSE': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_scatter_comparison_metrics.csv', 'Image1','Image2','MSE'),
    'scatter_NRMSE': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_scatter_comparison_metrics.csv', 'Image1','Image2','NRMSE'),
    'scatter_SSIM': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_scatter_comparison_metrics.csv', 'Image1','Image2','SSIM'),
    #'scatter_PSNR': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_scatter_comparison_metrics.csv', 'Image1','Image2','PSNR'),
    'scatter_CK1': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_scatter_comparison_metrics.csv', 'Image1','Image2','CK1_vp9'),
    'hexbin_MSE': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_hexbin_comparison_metrics.csv', 'Image1','Image2','MSE'),
    'hexbin_NRMSE': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_hexbin_comparison_metrics.csv', 'Image1','Image2','NRMSE'),
    'hexbin_SSIM': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_hexbin_comparison_metrics.csv', 'Image1','Image2','SSIM'),
    #'hexbin_PSNR': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_hexbin_comparison_metrics.csv', 'Image1','Image2','PSNR'),
    'hexbin_CK1': AP.create_comparison_matrix('CSVs/comparison_metrics/hours_hexbin_comparison_metrics.csv', 'Image1','Image2','CK1_vp9'),
    'post_distribution_euclidean': AP.create_comparison_matrix('CSVs/comparison_metrics/metrics_post_distribution_merged.csv', 'author1','author2','euclidean_distance'),
    'post_distribution_manhattan': AP.create_comparison_matrix('CSVs/comparison_metrics/metrics_post_distribution_merged.csv', 'author1','author2','manhattan_distance'),
    'post_distribution_cosine': AP.create_comparison_matrix('CSVs/comparison_metrics/metrics_post_distribution_merged.csv', 'author1','author2','cosine_similarity'),
    'post_distribution_pearson': AP.create_comparison_matrix('CSVs/comparison_metrics/metrics_post_distribution_merged.csv', 'author1','author2','pearson_correlation')
}

# Convert similarity matrices to distance matrices where needed
matrices['scatter_SSIM'] = 1 - matrices['scatter_SSIM']
matrices['hexbin_SSIM'] = 1 - matrices['hexbin_SSIM']
matrices['post_distribution_cosine'] = 1 - matrices['post_distribution_cosine']
matrices['post_distribution_pearson'] = 1 - (matrices['post_distribution_pearson'] + 1) / 2

# Range of cluster sizes to test
cluster_sizes = range(2, 21)  # e.g., from 2 to 20 clusters

# Lists to store results
matrix_names = []
chosen_cluster_sizes = []
sil_scores = []
db_scores = []
ch_scores = []
used_linkages = []
labels = []
class_distribution = []

# Define potential linkage values (excluding 'ward' since we're using 'precomputed' affinity)
linkages = ['complete', 'average', 'single']

# Iterate through each matrix, then through each cluster size, and then through each linkage
for name, matrix in matrices.items():
    for size in cluster_sizes:
        for linkage in linkages:
            print(name, size, linkage)

            clusterer = AgglomerativeClustering(n_clusters=size, affinity='precomputed', linkage=linkage)
            cluster_labels = clusterer.fit_predict(matrix)

            # Extract instance names from the first column
            instances = matrix.index.tolist()
            # Assuming you have a list of labels corresponding to the order of the instances
            # Create a mapping of instance to cluster
            instance_to_cluster = dict(zip(instances, cluster_labels))
            sil_score = silhouette_score(matrix, cluster_labels)
            db_score = davies_bouldin_score(matrix, cluster_labels)
            ch_score = calinski_harabasz_score(matrix, cluster_labels)

            unique_labels= set(cluster_labels.tolist())
            occurrences = {num: cluster_labels.tolist().count(num) for num in unique_labels}

            matrix_names.append(name)
            chosen_cluster_sizes.append(size)
            class_distribution.append(occurrences)
            sil_scores.append(sil_score)
            db_scores.append(db_score)
            ch_scores.append(ch_score)
            used_linkages.append(linkage)
            labels.append(instance_to_cluster)

# Convert results into a DataFrame
results_df = pd.DataFrame({
    'Matrix_Name': matrix_names,
    'Number_of_Clusters': chosen_cluster_sizes,
    'Distribution_of_Clusters': class_distribution,
    'Linkage_Method': used_linkages,
    'Silhouette_Score': sil_scores,
    'Davies_Bouldin_Score': db_scores,
    'Calinski_Harabasz_Score': ch_scores,
    'labels': labels
})

# Save DataFrame to CSV
results_df.to_csv('clustering_metrics_results.csv', index=False)
