from bs4 import BeautifulSoup
import requests, os, spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

date = input('What data would you want to travel back to? Enter the date in YYYY-MM-DD: ')

response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}')
billboard = response.text

soup = BeautifulSoup(billboard, 'html.parser')

songs = soup.find_all(name='span', class_='chart-element__information__song')
songs = [x.text for x in songs]

artists = soup.find_all(name='span', class_='chart-element__information__artist')
artists = [x.text for x in artists]

music = []

for i in range(len(songs)):
    music.append((songs[i], artists[i]))


auth = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_ID,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = auth.current_user()["id"]

song_uri = []

for i in music:
    q = i[0] + ' ' + i[1]
    if auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'] == []:
        continue
    else:
        song_uri.append(auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'][0]['uri'])

new_playlist = auth.user_playlist_create(user_id, f'{date} Billboard Hot 100', public=False)
playlist_id = new_playlist['id']
auth.playlist_add_items('6mpPSaogl0uVqoBNuDBP4H', song_uri)