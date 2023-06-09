import import_handle as IH
import requests
import time
from datetime import datetime
import pandas as pd
import json
import os
#Costly Function in QUotas
def get_channel_videosIDs_timeframe(api_key, channel_id, start_date, end_date):
    """
    Retrieves the IDs of videos uploaded to a specified YouTube channel within a given timeframe.
    This function is HIGHLY COSTLY since it uses the SEARCH API.
    Each request costs 100 quotas.

    Args:
        api_key (str): The API key to authenticate with the YouTube Data API v3.
        channel_id (str): The ID of the YouTube channel from which to retrieve videos.
        start_date (str): The start of the timeframe within which to retrieve videos.
            The date must be in the format 'YYYY-MM-DDThh:mm:ssZ', representing a time in UTC.
        end_date (str): The end of the timeframe within which to retrieve videos.
            The date must be in the same format as start_date.

    Returns:
        dict: A dictionary containing all response data.

    Raises:
        HTTPError: If the GET request to the YouTube Data API v3 fails.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/search?'
    first_url = base_url+'key={}&channelId={}&part=id&order=date&maxResults=50&publishedAfter={}&publishedBefore={}'.format(
        api_key, channel_id, start_date, end_date)
    video_data = {}
    url = first_url
    while True:
        response = requests.get(url)
        try:
            response.raise_for_status()  # Raise an HTTPError if the request fails
            data = response.json()
            video_ids = [item['id']['videoId'] for item in data['items']]
            video_data.update({f'Page{data.get("nextPageToken", "End")}': video_ids})
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
    return video_data

#Costly Function in QUotas
def get_channelID_by_channelName(api_key, channel_name):
    """
    Retrieves the ID of a YouTube channel by the channel name.

    Args:
        api_key (str): The API key to authenticate with the YouTube Data API v3.
        channel_name (str): The name of the YouTube channel for which to retrieve the ID.

    Returns:
        str: The ID of the YouTube channel.

    Raises:
        HTTPError: If the GET request to the YouTube Data API v3 fails.
        IndexError: If the search did not return any results.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/search?'
    url = base_url + 'key={}&q={}&part=snippet&type=channel&maxResults=1'.format(api_key, channel_name)

    response = requests.get(url)
    try:
        response.raise_for_status()  # Raise an HTTPError if the request fails
        data = response.json()
        # The first (and only) item in the items list should be the channel
        channel = data['items'][0]
        channel_id = channel['id']['channelId']
        return channel_id
    except requests.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
        raise

def get_channel_info(api_key, channel_id):
    """
    Retrieves information about a YouTube channel using the YouTube Data API v3.

    Args:
        api_key (str): The API key to authenticate with the YouTube Data API v3.
        channel_id (str): The ID of the YouTube channel for which to retrieve information.

    Returns:
        dict: A dictionary representing the channel and containing various information about the channel,
        including 'snippet', 'brandingSettings', 'contentDetails', 'statistics', and 'status'.

    Raises:
        requests.HTTPError: If the GET request to the YouTube Data API v3 fails.

    """
    base_url = 'https://www.googleapis.com/youtube/v3/channels?'
    url = base_url + 'key={}&part=snippet,brandingSettings,contentDetails,statistics,status&id={}'.format(api_key, channel_id)
    response = requests.get(url)

    try:
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
        raise

def get_video_info(api_key, video_id):
    """
    Retrieves detailed information about a specific YouTube video.

    This function makes a GET request to the YouTube Data API v3
    to retrieve comprehensive details about a specified video.
    These details include ID, snippet, contentDetails, player,
    recordingDetails, statistics, status, and topicDetails.

    Note: The 'fileDetails', 'processingDetails', and 'suggestions'
    parts are only available to the video's owner.

    Args:
        api_key (str): The API key to authenticate with the YouTube Data API v3.
        channel_id (str): The ID of the video for which to retrieve information.

    Returns:
        dict: A dictionary containing all response data.

    Raises:
        HTTPError: If the GET request to the YouTube Data API v3 fails.

    """
    base_url = 'https://www.googleapis.com/youtube/v3/videos?'
    url = base_url + 'key={}&id={}&part=id,snippet,contentDetails,player,recordingDetails,statistics,status,topicDetails'.format(api_key,video_id)
    response = requests.get(url)
    try:
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except requests.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
        raise

def get_video_comments(api_key, video_id, path, file_name):
    """
    This function retrieves comments from a specified YouTube video and returns a list of them.

    It makes a series of requests to the YouTube Data API v3, collecting the comments from the
    video specified by `video_id` using the provided `api_key`. Pagination is handled within the
    function to retrieve comments from all pages of the API response.

    Parameters:
    api_key (str): The API key to access the YouTube Data API v3.
    video_id (str): The ID of the YouTube video from which to retrieve comments.

    Returns:
    json_list (list): A list of dictionaries where each dictionary represents a page of comments.
                      Each dictionary contains the data of each comment thread, including 'id', 'snippet',
                      and 'replies'.

    Raises:
    requests.HTTPError: If an HTTP error occurs while making the API request.
    """
    base_url = 'https://www.googleapis.com/youtube/v3/commentThreads?'
    first_url = base_url + 'part=id, snippet,replies&maxResults=100&videoId={}&key={}'.format(
        video_id, api_key)
    url = first_url
    column_names = ['kind', 'etag', 'id', 'snippet', 'replies']

    df_base = pd.DataFrame(columns=column_names)
    while True:
        response = requests.get(url)
        try:
            response.raise_for_status()  # Raise an HTTPError if the request fails
            data = response.json()
            items = data['items']
            if items == []: #Video with no comments
                print("No Comments on Video.")
                break
            df = pd.concat([df_base, IH.json_to_dataframe(items, 0)])
            full_expanded = IH.json_to_dataframe(items, 8)
            df['authorChannelId'] = full_expanded["snippet.topLevelComment.snippet.authorChannelId.value"]
            df['publishedAt'] = full_expanded["snippet.topLevelComment.snippet.publishedAt"]
            df['textOriginal'] = full_expanded["snippet.topLevelComment.snippet.textOriginal"]
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
                time.sleep(0.1)
            df = None
        except requests.HTTPError as err:
            status_code = err.response.status_code
            if status_code == 404:
                print("404 - Not Found Error")
                # Treatment for 404 error
                raise
            elif status_code == 403:
                print("403 - Forbidden Error")
                # Treatment for 403 error
                break
            else:
                print(f"HTTP Error occurred: {status_code}")
                # Default treatment for other HTTP errors
                raise
#Costly Function in QUotas
def search_channel_with_name_and_get_info(df, api_key):
    """
    Process a dataframe, retrieving channel information and saving it as JSON and CSV.
    This function is HIGHLY COSTLY since it uses the SEARCH API (get_channelID_by_channelName).
    Each request costs 100 quotas.

    Args:
        df (pandas.DataFrame): The dataframe containing channel information.
        api_key (str): The API key to authenticate with the YouTube Data API v3.
    """
    for _, row in df.iterrows():
        channel_name = row['Channel']
        print(channel_name)
        channel_id = get_channelID_by_channelName(api_key, channel_name)
        json = get_channel_info(api_key, channel_id)
        IH.write_json(f'JSONs/Channels/', channel_name + "_info", json)
        data = json['items']
        df_c = IH.json_to_dataframe(data, 0)
        IH.save_df('CSVs/', 'channels_info', 'a', df_c)
        time.sleep(0.5)

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
            if datas.max() < min_date:
                break
            print(datas.max(), file_name)
            try:
                df['nextPageToken'] = data['nextPageToken']
            except Exception:
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

def get_playlist_items(api_key, playlist_id, path, file_name):
    base_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    first_url = f'{base_url}?key={api_key}&playlistId={playlist_id}&part=snippet&maxResults=50'
    url = first_url
    min_date = datetime.strptime('2022-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    column_names = ['kind', 'etag', 'id', 'snippet', 'contentDetails', 'status']
    df_base = pd.DataFrame(columns=column_names)
    while True:
        response = requests.get(url)
        try:
            response.raise_for_status()  # Raise an HTTPError if the request fails
            data = response.json()
            items = data['items']
            full_expanded = IH.json_to_dataframe(items, 8)
            df = pd.concat([df_base, IH.json_to_dataframe(items, 0)])
            df['channelId'] = full_expanded["snippet.channelId"]
            df['channelTitle'] = full_expanded["snippet.channelTitle"]
            df['publishedAt'] = full_expanded["snippet.publishedAt"]
            df['playlistId'] = full_expanded["snippet.playlistId"]
            df['videoId'] = full_expanded["snippet.resourceId.videoId"]
            datas = pd.to_datetime(df['publishedAt'], format='%Y-%m-%dT%H:%M:%SZ')
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
                time.sleep(0.25)
        except requests.HTTPError as err:
            print(f"HTTP Error occurred: {err}")
            raise

def process_playlist_videos(df, api_key):
    for _, row in df.iterrows():
        playlist_id = eval(row['contentDetails'])['relatedPlaylists']['uploads']
        name = eval(row['snippet'])['title'].replace(' ', '')
        print(name, playlist_id, 'STARTED')
        test_path = os.path.join('CSVs/ChannelVideos', name)
        if os.path.exists(f'{test_path}.csv'):
            print(name, 'ALREADY DOWNLOADED')
            continue
        get_playlist_items(api_key, playlist_id, 'CSVs/ChannelVideos', name)
        print(name, playlist_id, 'CONCLUDED')

def process_video_comments(df, api_key, start_date, end_date):
    df['dates'] = pd.to_datetime(df['snippet.publishedAt'])
    df_filtered = df[(df['dates'] >= start_date) & (df['dates'] < end_date)]

    videoCount = 0

    for _, row in df_filtered.iterrows():
        print("Getting video", str(videoCount))
        channel_name = row['snippet.channelTitle'].replace(" ", "")
        fileName = f"video{str(videoCount)}_comments_{channel_name}"
        videoID = row['snippet.resourceId.videoId']
        get_video_comments(api_key, videoID, f'CSVs/Comments/{channel_name}/', fileName)
        print("Got video", str(videoCount))
        videoCount += 1
