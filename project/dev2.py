import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt
#62_CNNbrasil
#48_alexandreGarcia
#1_felintoMotoVlog
#2_EDUARDOBOLSONARO

import YT_API_handler as YT
api_key = IH.get_api_key(2)

#path2 = 'C:\\Users\\agrri\PycharmProjects\TCC\project\CSVs\ChannelVideos'
#path = 'C:\\Users\\agrri\PycharmProjects\TCC\project\Analysis\HighCommenters\JairBolsonaro\comments_3_JairBolsonaro.csv'

path = 'CSVs\ChannelVideos'

def add_channel_to_channel_csv(api_key, channel_name, channel_id):
    json = YT.get_channel_info(api_key, channel_id)
    IH.write_json(f'JSONs/Channels/', channel_name + "_info", json)
    data = json['items']
    df_c = IH.json_to_dataframe(data, 0)
    IH.save_df('CSVs/', 'channels_info', 'a', df_c)

channel_name='ptbrasil'
#channel_id='UC0xqLnPTcFVf8MXaIoHPeDw'
playlist_id = 'UU0xqLnPTcFVf8MXaIoHPeDw'
YT.get_playlist_items(api_key, playlist_id, path, channel_name)