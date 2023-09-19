import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import analysis_API as AP
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform


# Perform Agglomerative Clustering based on the similarity matrix
# Note: Since the matrix is a similarity matrix, we might need to convert it into a distance matrix,
# which can be achieved by subtracting it from 1 (assuming values are between 0 and 1).
#clustering = AgglomerativeClustering(affinity='precomputed', linkage='average')
#distance_matrix = 1 - a
#labels = clustering.fit_predict(a)
#print("\nCluster Labels:")
#print(labels)

def generate_dendogram_for_metrics(dataset_path, column1, column2, column3, output_path, metric, representation):
    matrix = AP.create_comparison_matrix(dataset_path, column1, column2, column3)
    condensed_dist_matrix = squareform(matrix, checks=False)
    labels = [row for row in matrix]
    if metric != 'AWARP':
        image_map = pd.read_csv('C:\\Users\\agrri\PycharmProjects\TCC\project\CSVs\image_map.csv', sep=';')
        dict_mapping = {}
        for x,y in image_map.iterrows():
            dict_mapping[str(y['imgNumber'])]=y['authorChannelId']
        labels = list(map(lambda x: dict_mapping[x.replace('.png', '')], labels))

    mapped_labels = [[str(index), labels[index]] for index in range(len(labels))]
    df_mapped_labels = pd.DataFrame(columns=['Index', 'authorChannelId'], data=mapped_labels)
    df_mapped_labels.to_csv(output_path+f'\\instance_maps\\{metric}_{representation}_instance_map.csv', index = False, header=True)
    matrix.to_csv(output_path+f'\\csv_matrixes\\{metric}_{representation}_matrix.csv', header=True)

    Z = linkage(matrix, method='average')
    plt.figure(figsize=(10, 9))
    dendrogram(Z)
    plt.savefig(f'{output_path}/small/{representation}_hours_{metric}_dendogram_small.png')
    plt.clf()
    plt.figure(figsize=(100, 90))
    dendrogram(Z)
    plt.savefig(f'{output_path}/large/{representation}_hours_{metric}_dendogram_large.png')


output = 'Analysis/Dendograms'

for x in ['hexbin', 'scatter']:
    path = f'CSVs\comparison_metrics\hours_{x}_comparison_metrics.csv'
    c1 = 'Image1'
    c2 = 'Image2'
    c4 = x
    for y in ['MSE', 'NRMSE', 'SSIM', 'PSNR', 'CK1_vp9']:
        c3 = y
        generate_dendogram_for_metrics(path, c1, c2, c3, output, c3, c4)

generate_dendogram_for_metrics('CSVs\comparison_metrics\AWARP_hou_w100.csv', 'User1', 'User2', 'AWARP', output, 'AWARP', 'AWARP')
