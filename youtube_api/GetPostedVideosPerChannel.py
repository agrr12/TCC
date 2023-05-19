import requests
import json

# Defina suas credenciais
API_KEY = 'AIzaSyAX7qsfII35cqKaIo_Wr8RZQcdyujnfOSM'

# Defina o ID do canal
channel_id = 'UClNb35LAT7Ob9GrZx1oJDxQ'

# Construa a URL para obter a playlist de uploads do canal
playlist_url = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}'

# Faça a requisição GET para obter a playlist de uploads
playlist_response = requests.get(playlist_url)

print(playlist_response)

playlist_data = json.loads(playlist_response.text)
playlist_id = playlist_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
print(playlist_data['items'])
# Construa a URL para obter a lista de vídeos da playlist de uploads
videos_url = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=10&key={API_KEY}'
# Faça a requisição GET para obter a lista de vídeos
videos_response = requests.get(videos_url)
videos_data = json.loads(videos_response.text)

print(videos_response)


# Itere sobre os vídeos na resposta
for item in videos_data['items']:
    video_id = item['snippet']['resourceId']['videoId']
    title = item['snippet']['title']

    # Exiba o ID e o título do vídeo
    print('ID do vídeo:', video_id)
    print('Título:', title)
    print('---')
