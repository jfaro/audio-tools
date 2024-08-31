import requests
import json

from spotify.token import get_access_token

SPOTIFY_API_URL = "https://api.spotify.com/v1"


class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str):
        self.token = get_access_token(client_id, client_secret)


    def get_artist_data(self, artist_id: str):
        url = f"{SPOTIFY_API_URL}/artists/{artist_id}"
        headers = { "Authorization": f"Bearer {self.token}" }
        response = requests.get(url, headers=headers)
        return json.loads(response.text)


    def get_playlist_tracks(self, playlist_id: str):
        url = f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks"
        headers = { "Authorization": f"Bearer {self.token}" }
        response = requests.get(url, headers=headers)
        print(response.text)
        parsed = json.loads(response.text)
        tracks = []
        for track in parsed["items"]:
            data = track["track"]
            artists = []
            for artist in data["artists"]:
                artists.append({
                    "id": artist["id"],
                    "name": artist["name"]
                })
            tracks.append({
                "id": data["id"],
                "name": data["name"],
                "artists": artists
            })
        return tracks
