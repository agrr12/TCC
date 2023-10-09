import os

import analysis_API as AN
import threading
from multiprocessing import Process, Manager
import pandas as pd

r = 'C:\\Users\\agrri\PycharmProjects\TCC\sources\Comment'
columns_to_extract = ['id', 'authorChannelId', 'publishedAt', 'textOriginal', 'videoId']
all_dataframes = []

# Iterate through directories
for dir in os.listdir(r):
    print(dir)
    # Ensure that the item being read is a directory before proceeding
    if os.path.isdir(os.path.join(r, dir)):

        # Iterate through files in the directory
        for idx, file in enumerate(os.listdir(os.path.join(r, dir))):

            # Ensure that the item being read is a file before proceeding
            if os.path.isfile(os.path.join(r, dir, file)) and file.endswith('.csv'):
                df = pd.read_csv(os.path.join(r, dir, file))

                # Extracting the specified columns if they exist in the dataframe
                cols = [col for col in columns_to_extract if col in df.columns]
                subset_df = df[cols]

                # Store each subset dataframe in a list to concatenate later
                all_dataframes.append(subset_df)

# Concatenate all the subset dataframes into a single dataframe
final_df = pd.concat(all_dataframes, ignore_index=True)
final_df = final_df.replace(to_replace="\n", value=" ", regex=True)
final_df = final_df.replace(to_replace="\"", value="\"\"", regex=True)
final_df.to_csv("combined_columns2.csv", encoding="utf-8-sig", index=False)