import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# Spotify credentials
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SCOPE = "user-library-read playlist-modify-private playlist-modify-public playlist-read-private"
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")


# Create API Client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri= REDIRECT_URI, scope=SCOPE))

def main():
    # Get user ID
    user_id = sp.me()['id']

    # Get 100 most recent liked songs
    liked_songs = []
    offset = 0
    for _ in range(2):
        liked_songs.extend(sp.current_user_saved_tracks(limit=50, offset= offset)['items'])
        offset+=50
        
    # Create or get the playlist
    playlist_id = create_or_get_playlist(user_id, "Liked Songs (Last 100)")

    # Remove existing tracks from the playlist
    sp.playlist_replace_items(playlist_id, [])

    # Add the most recently liked songs to the playlist
    track_uris = [track['track']['uri'] for track in liked_songs]
    sp.playlist_add_items(playlist_id, track_uris)

def create_or_get_playlist(user_id, playlist_name):
    playlists = sp.user_playlists(user_id)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist['id']

    # If the playlist doesn't exist, create it.
    playlist = sp.user_playlist_create(user_id, playlist_name, public=True)
    return playlist['id']

if __name__ == "__main__":
    main()