# Apple Playlist to Spotify Playlist

from bs4 import BeautifulSoup
import requests, os, spotipy
from spotipy import SpotifyOAuth

SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']

link_to_playlist = input('Input the link to the playlist you want to copy: ')
response = requests.get(link_to_playlist)
playlist_site = response.text

soup = BeautifulSoup(playlist_site, 'html.parser')

playlist_name = 'Apple: ' + soup.find(name='h1', id='page-container__first-linked-element').text
song_names = [x.text for x in soup.find_all(name='div', class_='songs-list-row__song-name') if x.text != '']
artist_span = [x.span for x in soup.select(selector='div.songs-list-row__song-container div.songs-list-row__song-wrapper div.songs-list-row__by-line')]
artist_names = [x.a.text for x in artist_span]

auth = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope='playlist-modify-private',
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri='https://www.google.com/',
        show_dialog=True,
        cache_path='token.txt'
    ))

user_id = auth.current_user()['id']

song_uri = []

# Finds all the songs and adds them to the Uri list
for i in range(len(song_names)):
    q = song_names[i] + ' ' + artist_names[i]
    if auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'] == []:
        continue
    else:
        song_uri.append(auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'][0]['uri'])

# Creates a new playlist for the user on Spotify
new_playlist = auth.user_playlist_create(user_id, f'{playlist_name}', public=False)
playlist_id = new_playlist['id']

# Adds the songs to the created playlists using the list of song uris
auth.playlist_add_items(playlist_id, song_uri)

