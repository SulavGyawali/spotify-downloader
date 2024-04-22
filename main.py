import os 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import pytube 
import moviepy.editor as mp
from sys import argv
from threading import Thread

# Load environment variables from .env file
load_dotenv()
clien_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_auth():
    # Get client ID and secret from environment variables
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    # Create a Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    return spotify

def get_playlist_tracks(playlist_id):
    spotify = get_auth()
    results = spotify.playlist_tracks(playlist_id)
    return results

def get_youtube_video(query):
    results = pytube.Search(query)
    return results.results[0]

def download_video(yt, title):
    yt.streams.get_highest_resolution().download(filename=f"{title}.mp4")

def convert_to_mp3(video, title,folder):
    clip = mp.VideoFileClip(video)
    clip.audio.write_audiofile(f"{folder}/{title}.mp3")
    clip.close()
    os.remove(video)

def download_track(track, folder):
    try:
        track_name = track["track"]["name"]
        yt_result =  get_youtube_video(f"{track_name}")
        download_video(yt_result, track_name)
        convert_to_mp3(f"{track_name}.mp4", track_name, folder)
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
        #get auth
        spotify = get_auth()
        # Get tracks from a playlist
        try:
            playlist_id = argv[1]
            folder = argv[2]
            os.mkdir(folder)
        
        except IndexError:
            print("Please provide a playlist ID and folder name as arguments.")
            return
        
        tracks = get_playlist_tracks(playlist_id)

        for track in tracks["items"]:
            Thread(target=download_track, args=(track, folder)).start()
            


if __name__ == "__main__":
    main()
