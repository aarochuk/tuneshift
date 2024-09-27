from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests, os

app = Flask(__name__)
CORS(app, supports_credentials=True)

# make the authentication and use of the api proper

@app.route("/spotifyAuth")
def spotifyAuth():
    scope = "user-library-read playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri="http://localhost:3000",
            client_id="5fd6c7ca63044657ae73acff0ee3d798",
            client_secret="62b4d40d59d34729a4824aab5eebe999",
            show_dialog=True,
            cache_path=".cache"
        )
    )
    return auth.me()

@app.route("/addSong", methods=['POST'])
def addSong():
    song = request.get_json()['song']
    idd = request.get_json()['id']
    scope = "user-library-read playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri="http://localhost:3000",
            client_id="5fd6c7ca63044657ae73acff0ee3d798",
            client_secret="62b4d40d59d34729a4824aab5eebe999",
            show_dialog=True,
            cache_path=".cache"
        )
    )
    res = {} 
    if auth.search(q=song, type='track', limit=1, offset=0)['tracks']['items'] != []:
        res = auth.search(q=song, type='track', limit=1, offset=0)['tracks']['items'][0]

    millis = int(res['duration_ms'])
    seconds=(res['duration_ms']/1000)%60
    seconds = int(seconds)
    minutes=(res['duration_ms']/(1000*60))%60
    minutes = int(minutes)

    response = {
        "id": idd,
        "artists": [x['name'] for x in res['artists']],
        "img": res['album']['images'][0]['url'],
        "album": res['album']['name'],
        "title": res['name'],
        "time": str(minutes)+":"+str(seconds).rjust(2, "0"),
        "uri": res['uri'],
        "link": res['external_urls']['spotify']
    }

    return response

@app.route("/addApplePlaylist")
def addApplePlaylist():
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
    return {"state": 1}

@app.route("/addBillboard")
def addBillboard():
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

@app.route("/removesong")
def removeSong():
    return "remove song"

@app.route("/createPlaylist")
def createPlaylist():
    return "create playlist"
    


@app.route("/logout")
def logout():
    return "log out"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
