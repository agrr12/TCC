import json
import time
from datetime import datetime

import requests
import pandas as pd
import import_handle as IH
import YT_API_handler as YT



playlist_id = 'UUk5BcU1rOy6hepflk7_q_Pw'
df = pd.read_csv('CSVs/channels_info.csv')


for _,row in df.iterrows():
    #playlist_id = json.loads(row['contentDetails'].replace('"\'', '').replace('\'"', ''))['relatedPlaylists']['uploads']
    playlist_id = eval(row['contentDetails'])['relatedPlaylists']['uploads']
    name = eval(row['snippet'])['title'].replace(' ', '')
    print(name, playlist_id)

#YT.get_playlist_items(api_key, playlist_id, 'CSVs/', 'Meteoro')