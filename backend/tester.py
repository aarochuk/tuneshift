import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read playlist-modify-private"

auth = SpotifyOAuth(
        scope=scope,
        redirect_uri="http://localhost:3000",
        client_id="5fd6c7ca63044657ae73acff0ee3d798",
        client_secret="62b4d40d59d34729a4824aab5eebe999",
        show_dialog=True,
        cache_path=".cache"
    )
per = spotipy.client.Spotify(auth_manager=auth)
print(per.me())