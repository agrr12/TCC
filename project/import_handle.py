import pandas as pd
import os
from datetime import datetime
import json
import os

def add_timestamp(df):
    # Get current timestamp
    current_timestamp = datetime.now()

    # Add timestamp to a new column in the DataFrame
    df['extraction_date'] = current_timestamp

    return df

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def json_to_dataframe(json_object, max_unnest_level):
    df = pd.json_normalize(json_object, max_level=max_unnest_level)
    return df

def save_df(path, file_name, save_mode, dataframe, add_time=True):
    create_path_if_not_exists(path)
    full_path = os.path.join(path, file_name)
    file_exists = os.path.exists(f'{full_path}.csv')
    if add_time:
        dataframe = add_timestamp(dataframe)
    dataframe.to_csv(f'{full_path}.csv', index=False, mode=save_mode, header=not file_exists, encoding='utf-8', escapechar='\\')

def write_json(path, file_name, json_object):
    create_path_if_not_exists(path)
    full_path = os.path.join(path, file_name)
    with open(f'{full_path}.json', 'w') as json_file:
        json.dump(json_object, json_file)

def get_api_key(row_number):
    path = os.path.join('..', 'keys.txt')
    with open(path, 'r') as file:
        rows = file.readlines()
        rows = [row.strip() for row in rows]  # Remove leading/trailing whitespace

    return rows[row_number].split("=")[1]

if __name__ == '__main__':
    print(get_api_key(0))