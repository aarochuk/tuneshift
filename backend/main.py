from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests, os
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/spotifyAuth")
def spotifyAuth():
    scope = "user-library-read playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri=URI,
            client_id=ID,
            client_secret=SECRET,
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
            redirect_uri=URI,
            client_id=ID,
            client_secret=SECRET,
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
    print(response)
    return response

@app.route("/addApplePlaylist", methods=['POST'])
def addApplePlaylist():
    playlist = request.get_json()['playlist']
    idd = request.get_json()['id']
    response = requests.get(playlist)
    playlist_site = response.text

    soup = BeautifulSoup(playlist_site, 'html.parser')
    data = soup.find_all(name='script')[0].text
    data = json.loads(data)
    song_names = [x['name'] for x in data['track']]

    scope = "user-library-read playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri=URI,
            client_id=ID,
            client_secret=SECRET,
            show_dialog=True,
            cache_path=".cache"
        )
    )

    #user_id = auth.current_user()['id']

    song_uri = []

    # Finds all the songs and adds them to the Uri list
    for i in range(len(song_names)):
        q = song_names[i]
        if auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'] == []:
            continue
        else:
            res = auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'][0]
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
            idd += 1
            song_uri.append(response)

    # Creates a new playlist for the user on Spotify
    
    #new_playlist = auth.user_playlist_create(user_id, f'{playlist_name}', public=False)
    #playlist_id = new_playlist['id']

    # Adds the songs to the created playlists using the list of song uris
    #auth.playlist_add_items(playlist_id, song_uri)
    print(song_uri)
    return song_uri

@app.route("/addBillboard", methods=["POST"])
def addBillboard():
    date = request.get_json()['date']
    idd = request.get_json()['id']

    response = requests.get(f'https://www.billboard.com/charts/hot-100/{date}/')
    billboard = response.text

    soup = BeautifulSoup(billboard, 'html.parser')
    songs = [x.text.replace("\n", "").replace("\t", "") for x in soup.select(".o-chart-results-list-row .lrv-a-unstyle-list > li > h3")]
    art_ = [x.text.replace("\n", "").replace("\t", "") for x in soup.select(".o-chart-results-list-row .lrv-a-unstyle-list > li > span")]
    artists = []
    num = 0
    for i in range(len(art_)):
        if num%7 == 0:
            artists.append(art_[i])
        num += 1

    music = []

    for i in range(len(songs)):
        music.append((songs[i], artists[i]))

    scope = "user-library-read playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri=URI,
            client_id=ID,
            client_secret=SECRET,
            show_dialog=True,
            cache_path=".cache"
        )
    )

    song_uri = []

    for i in music:
        q = i[0] + ' ' + i[1]
        if auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'] == []:
            continue
        else:
            res = auth.search(q=q, type='track', limit=1, offset=0)['tracks']['items'][0]
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
            idd += 1
            song_uri.append(response)
        
    print(song_uri)
    return song_uri

@app.route("/createPlaylist", methods=["POST"])
def createPlaylist():
    playlist_name = request.get_json()['playlist_name']
    songs = request.get_json()['songs']

    scope = "playlist-modify-private"
    auth = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            redirect_uri=URI,
            client_id=ID,
            client_secret=SECRET,
            show_dialog=True,
            cache_path=".cache"
        )
    )

    user_id = auth.current_user()['id']
    new_playlist = auth.user_playlist_create(user_id, f'{playlist_name}', public=False)
    playlist_id = new_playlist['id']
    song_uri = [l['uri'] for l in songs]
    print(songs)
    print(song_uri)
    # Adds the songs to the created playlists using the list of song uris
    auth.playlist_add_items(playlist_id, song_uri)
    return "successful"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
