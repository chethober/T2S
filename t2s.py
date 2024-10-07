from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaDocument
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import re

# Replace with your  credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone = 'YOUR_PHONE_NUMBER'

SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
SPOTIFY_REDIRECT_URI = 'YOUR_SPOTIFY_REDIRECT_URI'
SPOTIFY_USERNAME = 'YOUR_SPOTIFY_USERNAME'

# Spotify Authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-modify-public",
    username=SPOTIFY_USERNAME
))

# Function to search for a track on Spotify using track and artist
def search_spotify_track(track_name, artist_name):
    query = f"track:{track_name} artist:{artist_name}"
    result = sp.search(q=query, limit=1, type='track')
    if result['tracks']['items']:
        return result['tracks']['items'][0]['id']
    return None

# Function to find an existing playlist by name
def find_playlist_by_name(playlist_name):
    playlists = sp.user_playlists(SPOTIFY_USERNAME)
    
    # Iterate through the user's playlists to find a match
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            print(f"Found existing playlist: {playlist_name}")
            return playlist['id']
    
    return None

# Function to create a Spotify playlist if it doesn't exist
def get_or_create_spotify_playlist(playlist_name):
    # First, try to find an existing playlist with the given name
    playlist_id = find_playlist_by_name(playlist_name)
    
    if not playlist_id:
        # If not found, create a new playlist
        playlist = sp.user_playlist_create(SPOTIFY_USERNAME, playlist_name, public=True)
        print(f"Created new playlist: {playlist_name}")
        return playlist['id']
    
    # If found, return the existing playlist ID
    return playlist_id

# Function to get all track IDs in a playlist
def get_tracks_in_playlist(playlist_id):
    existing_tracks = []
    results = sp.playlist_tracks(playlist_id)

    if results:
        while results:
            for item in results['items']:
                track = item['track']
                existing_tracks.append(track['id'])
            results = sp.next(results) if results['next'] else None

    return existing_tracks

# Function to add a track to a Spotify playlist, checking if it's already there
def add_track_to_playlist(playlist_id, track_id, existing_tracks):
    if track_id not in existing_tracks:
        sp.playlist_add_items(playlist_id, [track_id])
        print(f" + Added track to playlist: {track_id}")
    else:
        print(f" = Track already exists in playlist: {track_id}")

# Function to add tracks from Spotify links found in messages
def add_spotify_links_to_playlist(chat, playlist_id):
    with client:
        for message in client.iter_messages(chat):
            if message.message:
                spotify_links = re.findall(r'(https?://open.spotify.com/[^\s]+)', message.message)
                for link in spotify_links:
                    try:
                        # Extract Spotify track ID from the link and add to playlist
                        track_id = link.split("/")[-1].split("?")[0]  # Extract ID from the URL
                        add_track_to_playlist(playlist_id, track_id, get_tracks_in_playlist(playlist_id))
                        print(f" + Added Spotify link to playlist: {link}")
                    except Exception as e:
                        print(f" ! Failed to add track from link: {link}, error: {e}")

# Connect to Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Function to fetch music from chat and add to Spotify playlist
def fetch_music_and_add_to_spotify(chat):
    with client:
        # Get the chat entity (could be a username or chat ID)
        entity = client.get_entity(chat)

        # Get or create a Spotify playlist with the chat's title
        playlist_name = entity.title if hasattr(entity, 'title') else entity.username
        playlist_id = get_or_create_spotify_playlist(playlist_name)

        # Get existing tracks in the playlist to avoid duplicates
        existing_tracks = get_tracks_in_playlist(playlist_id)
        consecutive_existing = 0  # Counter for consecutive existing tracks

        # Iterate through messages in the chat
        for message in client.iter_messages(entity):
            if message.media and isinstance(message.media, MessageMediaDocument):
                if message.file and 'audio' in message.file.mime_type:
                    # Extract the artist (performer) and track title
                    artist_name = message.file.performer if message.file.performer else 'Unknown Artist'
                    track_name = message.file.title if message.file.title else message.file.name
                    
                    if artist_name != 'Unknown Artist' and track_name:
                        print(f" ? Found track: {track_name} by {artist_name}")

                        # Search for the track on Spotify using "track - artist" format
                        track_id = search_spotify_track(track_name, artist_name)
                        if track_id:
                            if track_id not in existing_tracks:
                                add_track_to_playlist(playlist_id, track_id, existing_tracks)
                                consecutive_existing = 0  # Reset the counter
                            else:
                                print(f" = Track already exists in playlist: {track_name} by {artist_name}")
                                consecutive_existing += 1
                        else:
                            print(f" - Track not found on Spotify: {track_name} by {artist_name}")
                    else:
                        print(f" ! Metadata not available for the file: {message.file.name}")

            # Break the process if 5 consecutive existing tracks are found
            if consecutive_existing >= 5:
                print(" * Other Tracks Already Added")
                break

        # After processing audio files, check for Spotify links in the chat and add those tracks
        add_spotify_links_to_playlist(chat, playlist_id)

# Fetch music files from a Telegram chat (accepts username or chat ID)
fetch_music_and_add_to_spotify('mus_bros')  # Replace 'me' with the chat username or chat ID
