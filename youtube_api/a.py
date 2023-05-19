import requests
import json
from datetime import datetime, timedelta

# Set up your credentials
API_KEY = 'AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM'

# Define the channel ID
channel_id = 'UCx7RxEQ9HspwurWnR5qum4Q'

# Define the time window
start_date = datetime(2022, 1, 1).isoformat() + 'Z'
end_date = datetime(2022, 12, 31).isoformat() + 'Z'

# Construct the URL to get the videos within the time window
videos_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&type=video&maxResults=50&key={API_KEY}&publishedAfter={start_date}&publishedBefore={end_date}'

# Make the request to get the videos within the time window
response = requests.get(videos_url)
videos_data = json.loads(response.text)

print(videos_data)

# Iterate over the videos in the response
for item in videos_data['items']:
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    published_at = item['snippet']['publishedAt']

    # Print video information
    print('Video ID:', video_id)
    print('Title:', title)
    print('Published At:', published_at)
    print('---')
