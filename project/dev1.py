import json
import time
from datetime import datetime
import analysis_API as AN

import requests
import pandas as pd
import import_handle as IH
import YT_API_handler as YT
import os



folder_path = 'CSVs\Comments\EDUARDOBOLSONARO'  # Replace with the actual folder path

from itertools import combinations

def get_combinations(comment_folder_path):
    # Get the values of the column as a list
    # Iterate over all files in the folder
    edges = {}
    for file_name in os.listdir(comment_folder_path)[0:10]:
        if os.path.isfile(os.path.join(comment_folder_path, file_name)):
            print(file_name)
            df = pd.read_csv(os.path.join(comment_folder_path, file_name))
            df_id = df['authorChannelId'].unique().tolist()
            comb = list(combinations(df_id, 2))
            sorted_combinations = [tuple(sorted(combo)) for combo in comb]
            for item in sorted_combinations:
                if item in edges:
                    edges[item] += 1
                else:
                    edges[item] = 1
    # Use the combinations function to get all 2-element combinations
    return edges


dic = get_combinations(folder_path)
for x in dic:
    if dic[x] > 3:
        print(x, dic[x])

import networkx as nx
import matplotlib.pyplot as plt
# Initialize the Graph
G = nx.Graph()


# Add edges from the dictionary to the graph
for nodes, weight in dic.items():
    G.add_edge(nodes[0], nodes[1], weight=weight)

nx.write_pajek(G, "graph.net")
nx.draw(G, with_labels=False, node_color='skyblue', node_size=800)
plt.show()