import pandas as pd

import pandas as pd
import os


def json_to_dataframe(json_object, max_unnest_level):
    df = pd.json_normalize(json_object, max_level=max_unnest_level)
    return df

def save_df(path, save_mode, dataframe):
    file_exists = os.path.exists(f'{path}.csv')
    dataframe.to_csv(f'{path}.csv', index=False, mode=save_mode, header=not file_exists)

