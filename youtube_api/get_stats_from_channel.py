import requests
import pandas as pd
import import_handle

def print_channel_info(response_json):
    if response_json:
        items = response_json.get('items', [])
        if items:
             channel = items[0]
             snippet = channel['snippet']
             statistics = channel['statistics']
             print("Channel Title:", snippet.get('title'))
             print("Description:", snippet.get('description'))
             print("Custom URL:", snippet.get('customUrl'))
             print("Published At:", snippet.get('publishedAt'))
             print("Thumbnails:", snippet.get('thumbnails'))
             print("Default Language:", snippet.get('defaultLanguage'))
             print("Localized:", snippet.get('localized'))
             print("Country:", snippet.get('country'))
             print("View Count:", statistics.get('viewCount'))
             print("Comment Count:", statistics.get('commentCount'))
             print("Subscriber Count:", statistics.get('subscriberCount'))
             print("Hidden Subscriber Count:", statistics.get('hiddenSubscriberCount'))
             print("Video Count:", statistics.get('videoCount'))

def get_channel_info(api_key, channel_id):
    base_url = 'https://www.googleapis.com/youtube/v3/channels?'
    url = base_url + 'key={}&id={}&part=snippet,statistics'.format(api_key, channel_id)

    response = requests.get(url)
    if response.status_code == 200:
        response_json =  response.json()
        #print_channel_info(response_json)
        items = response_json.get('items', [])
        df = import_handle.json_to_dataframe(items, 1)  # flatten the json and convert it into a dataframe
        import_handle.save_df('test1', 'a', df)  # save the dataframe to a csv file

    else:
        print("Error accessing the API, please check your API key and channel id")
        return None


api_key = "AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM"
channel_id = "UCxvwz3pGrKIgTXD-RbapM2w"

channel_info = get_channel_info(api_key, channel_id)