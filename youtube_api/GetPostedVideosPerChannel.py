import requests
import json
import import_handle

import requests
import json


def get_all_comments(video_id, api_key):
    """
    Fetches all comments from a specific YouTube video.

    This function uses the YouTube Data API to retrieve all comments from a given video.
    It performs an initial request to get the first set of comments and then continues
    making requests for additional comments while the 'nextPageToken' field is present in
    the response data. Each comment is then processed and saved to a dataframe.

    Parameters
    ----------
    video_id : str
        The ID of the YouTube video for which to fetch comments.
    api_key : str
        The API key to use for authentication with the YouTube Data API.

    Returns
    -------
    list
        A list of all comments from the specified YouTube video. Each comment is represented as a JSON object.

    Raises
    ------
    HTTPError
        If an error occurs during the HTTP request to the YouTube Data API.
    """
    url = f"https://www.googleapis.com/youtube/v3/commentThreads"
    comments = []

    first_params = {
        'key': api_key,
        'textFormat': 'plainText',
        'part': 'snippet',
        'videoId': video_id,
        'maxResults': 100
    }

    result = requests.get(url, params=first_params)
    result.raise_for_status()  # Ensure the request succeeded
    data = result.json()

    for item in data['items']:
        comments.append(item)
        df = import_handle.json_to_dataframe(item, 3)  # flatten the json and convert it into a dataframe
        import_handle.save_df('test2', 'a', df)

    while 'nextPageToken' in data:
        next_params = first_params.copy()
        next_params['pageToken'] = data['nextPaxgeToken']
        result = requests.get(url, params=next_params)
        result.raise_for_status()  # Ensure the request succeeded
        data = result.json()

        for item in data['items']:
            df = import_handle.json_to_dataframe(item, 2)  # flatten the json and convert it into a dataframe
            import_handle.save_df('test2', 'a', df)
            comments.append(item)

    return comments

api_key = 'AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM'  # Replace this with your API key
video_id = '1PiqkX8IxUI'  # Replace this with your video ID
a=get_all_comments(video_id, api_key)
