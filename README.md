### Telegram to Spotify Bot

The script will extract music from any Telegram chat. It automatically adds the tracks to a Spotify playlist created with the chat's name. You can replace `'me'` with a specific chat username or chat ID in the `fetch_music_and_add_to_spotify()` function call. The script will automatically find and add tracks from any Spotify links shared in the chat messages. It will:
1. **Search for audio files** in a Telegram chat, extract their metadata (track and artist), and add them to a Spotify playlist.
2. **Automatically create a Spotify playlist** with the name of the Telegram chat if one does not already exist.
3. **Handle Spotify links** found in chat messages and add those tracks to the playlist as well.
4. **Break after finding consecutive existing tracks** in the playlist to avoid redundant searching.
5. **Return "NO NEW SONGS"** if no new tracks are added to the playlist.


### Requirements

1. **Python** (Version 3.8+)
2. **Libraries**:
   - `telethon`: For connecting to Telegram and fetching messages.
   - `spotipy`: For interacting with Spotify's API.
   - `re`: For searching Spotify URLs in chat messages.

### Installation Steps

1. **Clone the Project**:

   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/telegram-spotify-bot.git
   cd telegram-spotify-bot
   ```

2. **Install Required Libraries**:

   You need to install the required libraries to interact with Telegram and Spotify. Use `pip` to install dependencies:
   ```bash
   pip install telethon spotipy
   ```

3. **Create Spotify Developer App**:

   To interact with the Spotify API, you must create an application in the Spotify Developer Dashboard:
   - Visit: https://developer.spotify.com/dashboard/applications
   - Create a new app and note down the `Client ID`, `Client Secret`, and set your **Redirect URI** (e.g., `http://localhost:8080`).

4. **Configure Your Credentials**:

   In the script, replace the following placeholders with your real credentials:
   ```python
   api_id = 'YOUR_API_ID'
   api_hash = 'YOUR_API_HASH'
   phone = 'YOUR_PHONE_NUMBER'

   SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
   SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
   SPOTIFY_REDIRECT_URI = 'YOUR_SPOTIFY_REDIRECT_URI'
   SPOTIFY_USERNAME = 'YOUR_SPOTIFY_USERNAME'
   ```

5. **Run the Script**:

   You can now run the script to start fetching tracks and adding them to your Spotify playlist:
   ```bash
   python3 t2s.py
   ```

6. **Authenticate Spotify**:

   The script will open a URL in your browser for Spotify authentication. After you log in, Spotify will redirect you back, and the script will continue.