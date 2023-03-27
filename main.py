import requests
import os
import json

#Get Keys from key file
key_file = open('keys.txt')
keys = {}
for x in key_file.readlines():
    split = x.replace("\n", "").split(" = ")
    keys[split[0]] = split[1]
key_file.close()

consumer_key = keys.get('consumer_key')
consumer_secret = keys.get('consumer_secret')
access_token = keys.get('access_token')
access_token_secret = keys.get('access_token_secret')
bearer_token = keys.get('bearer_token')

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

query = "#despejozero OR #direitodemoradia -is:retweet"
max_results = 10

url = "https://api.twitter.com/2/tweets/search/all"
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "User-Agent": "v2FilteredStreamPython",
}

params = {
    "query": query,
    "max_results": max_results,
    "tweet.fields": "created_at,public_metrics,author_id",
    "start_time": "2022-09-01T00:00:00Z",
    "end_time": "2022-09-10T23:59:59Z",
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

json_response = response.json()

for tweet in json_response["data"]:
    print(tweet)