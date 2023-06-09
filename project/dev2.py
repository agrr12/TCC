import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd
import os

#62_CNNbrasil
#48_alexandreGarcia
#1_felintoMotoVlog
#2_EDUARDOBOLSONARO

import YT_API_handler as YT
api_key = IH.get_api_key(2)

path = 'C:\\Users\\agrri\PycharmProjects\TCC\project\CSVs\ChannelVideos'


def find_high_commenters(videos_path):
    for file_name in os.listdir(videos_path):
        if file_name.replace(" ", "").replace(".csv", "") not in ('UOL'):#in ("JornaldaRecord",'PlantãoBrasil'):
            continue
        print(file_name, 'STARTING')
        path_output = os.path.join('CSVs', 'Comments',file_name.replace(" ", "").replace(".csv", ""))
        #if os.path.exists(f'{path_output}'):
        #    print(file_name, 'ALREADY DOWNLOADED')
        #    continue
        if os.path.isfile(os.path.join(videos_path, file_name)):
            df = pd.read_csv(os.path.join(videos_path, file_name))
            start_date = datetime.strptime('2022-10-01T00:00:00Z', '%Y-%m-%dT%H:%M:%S%z')
            end_date = datetime.strptime('2022-11-01T00:00:00Z', '%Y-%m-%dT%H:%M:%S%z')
            df['dates'] = pd.to_datetime(df['publishedAt'])
            df_filtered = df[(df['dates'] >= start_date) & (df['dates'] < end_date)]
            videoCount = 0
            print(file_name, 'DOWNLOADING')
            for _,row in df_filtered.iterrows():
                if videoCount<=875:
                    videoCount += 1
                    continue
                else:
                    print("Getting video",str(videoCount), "of", file_name.replace(" ", "").replace(".csv", ""))
                    channel_name = row['channelTitle'].replace(" ", "")
                    fileName = f"video{str(videoCount)}_comments_{channel_name}"
                    videoID = row['videoId']
                    YT.get_video_comments(api_key, videoID, f'CSVs/Comments/{channel_name}/', fileName)
                    print("Got video", str(videoCount))
                    videoCount+=1
            print(file_name, 'FINISHED')

find_high_commenters(path)