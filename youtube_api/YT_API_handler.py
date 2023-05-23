import requests
import import_handle

def print_video_info(response_json):
    items = response_json.get('items', [])
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
def get_video_info(api_key, video_id):
    base_url = 'https://www.googleapis.com/youtube/v3/videos?'
    url = base_url + 'key={}&id={}&part=snippet,contentDetails,statistics'.format(api_key, video_id)

    response = requests.get(url)
    if response.status_code == 200:
        response_json =  response.json()
        #print_video_info(response_json)
        return response_json.get('items', [])
        #import_handle.json_to_dataframe(items, 1)  # flatten the json and convert it into a dataframe
        #import_handle.save_df('test1', 'a', df)  # save the dataframe to a csv file
    else:
        print("Error accessing the API, please check your API key and video id")
        return None

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
        response_json = response.json()
        print_channel_info(response_json)
        return response_json.get('items', [])
        #df = import_handle.json_to_dataframe(items, 1)  # flatten the json and convert it into a dataframe
        ##usar threadimport_handle.save_df('Canais', 'a', df)  # save the dataframe to a csv file

    else:
        print("Error accessing the API, please check your API key and channel id")
        return None

def write_channel_list_from_videoid_list(video_id_list):
    for x in list_NEWS:
        items = get_video_info('AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM', x)
        video = items[0]
        channelID = video['snippet']
        channelInfo = get_channel_info('AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM', channelID.get('channelId'))
        df = import_handle.json_to_dataframe(channelInfo, 1)  # flatten the json and convert it into a dataframe
        import_handle.save_df('Canais', 'a', df)  # save the dataframe to a csv file

if __name__ == '__main__':
    list_NEWS = {'Band Jornalismo': 'iYVk1CeIs60',
                 'UOL': 'WsA2SRdkIFM',
                 'Folha de S.Paulo': 'k9c3LbZxXKs',
                 'Gazeta do Povo': 'dsvFw0_l14c',
                 'Jornalismo TV Cultura': 'jSlG0No9muY',
                 'g1': 'MVeRuwkig18',
                 'SBT News': 'oZ03eKeROuE',
                 'Rádio BandNews FM': 'ClU5zXko0cw',
                 'CNN Brasil': 'fvWJTGN4-Ts',
                 'Jovem Pan News': 'eabTH5yhfAk',
                 'Poder360': 'n1cPJuoqAC8'}

    listLEFT = ['UCO5aa6kx60','mIPXf00WRaQ']
    listRIGHT = ['3-NbDp9i2GM','Zst1asVFk88']
    dic = {}
    for x in list_NEWS:
        try:
            video = get_video_info('AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM', x)[0]
            snippet = video['snippet']
            print("Channel Title:", snippet.get('channelTitle'))
            dic[snippet.get('channelTitle')] = x
        except:
            print("CAN'T RETRIEVE" , x)
    print(dic)
    #write_channel_list_from_videoid_list(list_NEWS)