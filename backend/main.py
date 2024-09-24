from flask import Flask
from flask_cors import CORS
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth
app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/spotifyAuth")
def spotifyAuth():
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id="5fd6c7ca63044657ae73acff0ee3d798", client_secret="62b4d40d59d34729a4824aab5eebe999", redirect_uri="http://localhost:3000"))

    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])
    return {'state':1}

@app.route("/addApplePlaylist")
def addApplePlaylist():
    return "apple playlist"

@app.route("/addBillboard")
def addBillboard():
    return "billboard"

@app.route("/logout")
def logout():
    return "log out"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
