import requests
import import_handle


def get_video_info(api_key, video_id):
    base_url = 'https://www.googleapis.com/youtube/v3/videos?'
    url = base_url + 'key={}&id={}&part=snippet,contentDetails,statistics'.format(api_key, video_id)

    response = requests.get(url)
    if response.status_code == 200:
        response_json =  response.json()
        #print_channel_info(response_json)
        items = response_json.get('items', [])
        import_handle.json_to_dataframe(items, 1)  # flatten the json and convert it into a dataframe
        #import_handle.save_df('test1', 'a', df)  # save the dataframe to a csv file
    else:
        print("Error accessing the API, please check your API key and video id")
        return None


api_key = "AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM"
video_id = "zlQTFzlFZnc"

video_info = get_video_info(api_key, video_id)

if video_info:
    items = video_info.get('items', [])
    if items:
        video = items[0]
        snippet = video['snippet']
        content_details = video['contentDetails']
        statistics = video['statistics']

        print("Title:", snippet.get('title'))
        print("Description:", snippet.get('description'))
        print("Published At:", snippet.get('publishedAt'))
        print("Channel ID:", snippet.get('channelId'))
        print("Channel Title:", snippet.get('channelTitle'))
        print("Tags:", snippet.get('tags'))
        print("Category ID:", snippet.get('categoryId'))
        print("Live Broadcast Content:", snippet.get('liveBroadcastContent'))

        print("Duration:", content_details.get('duration'))
        print("Dimension:", content_details.get('dimension'))
        print("Definition:", content_details.get('definition'))
        print("Caption:", content_details.get('caption'))
        print("Licensed Content:", content_details.get('licensedContent'))
        print("Content Rating:", content_details.get('contentRating'))
        print("Projection:", content_details.get('projection'))

        print("View Count:", statistics.get('viewCount'))
        print("Like Count:", statistics.get('likeCount'))
        print("Dislike Count:", statistics.get('dislikeCount'))
        print("Favorite Count:", statistics.get('favoriteCount'))
        print("Comment Count:", statistics.get('commentCount'))
