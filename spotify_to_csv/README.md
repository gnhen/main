# Spotify Liked Songs Exporter

*this readme was created by AI*

Export your Spotify Liked Songs (Saved Tracks) library to a CSV file.

## Features

- Pulls every saved track, no size limit like Spotify's 10,000-song playlist cap
- Includes track name, artist(s), album, release date, duration, date added, and a direct Spotify link
- Caches your login so you only need to authenticate once

## Requirements

- Python 3.8+
- A Spotify account
- [`spotipy`](https://spotipy.readthedocs.io/)

## Setup

1. Install the dependency:

   ```bash
   pip install spotipy
   ```

2. Create a Spotify API app:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
   - Click **Create app**, and give it any name and description.
   - Under **Redirect URIs**, add:
     ```
     http://127.0.0.1:8888/callback
     ```
   - Save, then copy your **Client ID** and **Client Secret** from the app's settings page.

3. Set your credentials as environment variables:

   ```bash
   export SPOTIPY_CLIENT_ID="your_client_id_here"
   export SPOTIPY_CLIENT_SECRET="your_client_secret_here"
   export SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
   ```

   On Windows (PowerShell):

   ```powershell
   $env:SPOTIPY_CLIENT_ID="your_client_id_here"
   $env:SPOTIPY_CLIENT_SECRET="your_client_secret_here"
   $env:SPOTIPY_REDIRECT_URI="http://127.0.0.1:8888/callback"
   ```

## Usage

```bash
python export_liked_songs.py
```

The first run opens a browser window asking you to log in to Spotify and authorize the app. Spotipy caches the resulting token locally (`.cache`), so you won't need to log in again on future runs.

## Output

Writes `liked_songs.csv` to the current directory, one row per saved track:

| Column | Description |
|---|---|
| Date Added | When you liked the track (ISO 8601 timestamp) |
| Track Name | Song title |
| Artist(s) | Comma-separated list of artists |
| Album | Album name |
| Release Date | Original release date |
| Duration | Track length (mm:ss) |
| Spotify Link | Direct link to the track on Spotify |
| Track ID | Spotify's internal track ID |

## Notes

- Your credentials never leave your machine, this script only talks to Spotify's official Web API.
- Add `.cache` to your `.gitignore` if you fork or publish this repo, it holds your local auth token and shouldn't be committed.

## License

MIT
