import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd

next_page_token = 'EAAaB1BUOkNLeE4'
playlist_id = 'UUVFbXI6Gu8U2f9Gjtxw4A-Q'
api_key = IH.get_api_key(0)
path = 'CSVs/ChannelVideos'
name = 'UOL'


def continue_playlist_import_from_token(api_key, playlist_id, path, file_name, next_page_token):
    base_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    first_url = f'{base_url}?key={api_key}&playlistId={playlist_id}&part=snippet&maxResults=50&pageToken={next_page_token}'
    url = first_url
    min_date = datetime.strptime('2022-09-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    while True:
        response = requests.get(url)
        try:
            response.raise_for_status()  # Raise an HTTPError if the request fails
            data = response.json()
            items = data['items']
            df = IH.json_to_dataframe(items, 2)
            datas = pd.to_datetime(df['snippet.publishedAt'], format='%Y-%m-%dT%H:%M:%SZ')
            if datas.max()<min_date:
                break
            print(datas.max(),file_name)
            try:
                df['nextPageToken'] = data['nextPageToken']
            except Exception :
                df['nextPageToken'] = None

            IH.save_df(path, file_name, 'a', df)
            if 'nextPageToken' not in data:
                print('No more pages left')
                break
            else:
                next_page_token = data['nextPageToken']
                url = first_url + '&pageToken={}'.format(next_page_token)
                # To avoid exceeding quota with too many requests
                time.sleep(1)
        except requests.HTTPError as err:
            print(f"HTTP Error occurred: {err}")
            raise

get_playlist_items(api_key, playlist_id, path, 'UOL', next_page_token)