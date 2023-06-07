import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd

import YT_API_handler as YT
api_key = IH.get_api_key(0)
#YT.get_video_comments(api_key, 'P4-NzPnlnGw', 'a', 'test248')

df = pd.read_csv('C:\\Users\\agrri\PycharmProjects\TCC\youtube_api\CSVs\ChannelVideos\FranciscoMelloOficial.csv')


start_date = datetime.strptime('2022-10-01T00:00:00Z', '%Y-%m-%dT%H:%M:%S%z')
end_date = datetime.strptime('2022-11-01T00:00:00Z', '%Y-%m-%dT%H:%M:%S%z')

df['dates'] = pd.to_datetime(df['snippet.publishedAt'])

df_filtered = df[(df['dates'] >= start_date) & (df['dates'] < end_date)]

videoCount = 0

for _,row in df_filtered.iterrows():
    if videoCount<=-1:
        videoCount += 1
        continue
    else:
        print("Getting video",str(videoCount))
        channel_name = row['snippet.channelTitle'].replace(" ", "")
        fileName = f"video{str(videoCount)}_comments_{channel_name}"
        videoID = row['snippet.resourceId.videoId']
        YT.get_video_comments(api_key, videoID, f'CSVs/Comments/{channel_name}/', fileName)
        print("Got video", str(videoCount))
        videoCount+=1