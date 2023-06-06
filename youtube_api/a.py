import json
import time
from datetime import datetime

import requests
import pandas as pd
import import_handle as IH
import YT_API_handler as YT
import os



#playlist_id = 'UUk5BcU1rOy6hepflk7_q_Pw'
df = pd.read_csv('CSVs/channels_info.csv')
api_key = IH.get_api_key(0)

for _,row in df.iterrows():
    playlist_id = eval(row['contentDetails'])['relatedPlaylists']['uploads']
    name = eval(row['snippet'])['title'].replace(' ', '')
    print(name,'STARTED')
    test_path = os.path.join('CSVs/ChannelVideos', name)
    if os.path.exists(f'{test_path}.csv'):
        print(name, 'ALREADY DOWNLOADED')
        continue
    YT.get_playlist_items(api_key, playlist_id, 'CSVs/ChannelVideos', name)
    print(name, 'CONCLUDED')
