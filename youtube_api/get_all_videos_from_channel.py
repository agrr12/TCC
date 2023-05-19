import requests
import datetime
import time


def get_videos(api_key, channel_id, from_date, to_date):
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    first_url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(api_key,
                                                                                                        channel_id)

    url = first_url
    videos = []

    while True:
        response = requests.get(url)
        result = response.json()
        if response.status_code != 200:
            print("Error accessing the API, please check your API key and channel id")
            break

        for item in result['items']:
            try:
                video_id = item['id']['videoId']
                published_at = item['snippet']['publishedAt']

                # converting the string to datetime object
                published_at_obj = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")

                # filtering based on the date
                if published_at_obj.date() >= from_date and published_at_obj.date() <= to_date:
                    videos.append(item)

            except KeyError:
                pass

        try:
            # get the next page token
            next_page_token = result['nextPageToken']
            url = first_url + '&pageToken={}'.format(next_page_token)

        except KeyError:
            # if there is no next page token
            break

    return videos


api_key = 'AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM'
channel_id = 'UCx7RxEQ9HspwurWnR5qum4Q'

from_date = datetime.date(2022, 1, 1)  # start date
to_date = datetime.date(2023, 1, 1)  # end date

videos = get_videos(api_key, channel_id, from_date, to_date)

for video in videos:
    print(video['snippet']['title'])
    print(video['snippet']['publishedAt'])
