import os
import argparse
import json
import threading

from dotenv import load_dotenv
from ytmp3 import download_song, get_youtube_url
from spotify.client import SpotifyClient


load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Thread entry for each download.
def download_runner(track):
    print("Starting runner for", track["name"])
    artists = [x["name"] for x in track["artists"]]
    url = get_youtube_url(track["name"], artists)

    # Download song from youtube URL.
    download_song(track["name"], url)

# CLI arguments.
parser = argparse.ArgumentParser(
    prog="Spotify downloader",
    description="Download playlists from Spotify",
)
parser.add_argument("playlist_id")

# Read from args.
args = parser.parse_args()
playlist_id = args.playlist_id

# Setup Spotify API client.
spotify = SpotifyClient(client_id, client_secret)

# Get tracks from spotify playlist.
tracks = spotify.get_playlist_tracks(playlist_id)
print(json.dumps(tracks, indent=2))

if len(tracks) == 0:
    print("No tracks in playlist")
    exit(1)

BATCH_SIZE = 5

batch_num = 0
done = False

while True:
    print(f"STARTING BATCH {batch_num}, ({BATCH_SIZE} downloads)")
    
    threads = list()
    for i in range(BATCH_SIZE):
        song_idx = (batch_num * BATCH_SIZE) + i
        
        if song_idx >= len(tracks):
            done = True
            continue
        
        # Start all threads.
        track = tracks[song_idx]
        x = threading.Thread(target=download_runner, args=(track,))
        threads.append(x)
        x.start()

    print("Joining all runners")
    for thread in threads:
        x.join()
        
    batch_num += 1
