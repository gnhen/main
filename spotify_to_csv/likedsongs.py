"""Export Spotify Liked Songs (Saved Tracks) to a CSV file."""

import csv
import os
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
OUTPUT_FILE = "liked_songs.csv"
SCOPE = "user-library-read"
PAGE_SIZE = 50  # Spotify's max page size for this endpoint


def get_spotify_client() -> spotipy.Spotify:
    """Authenticate with Spotify and return a ready-to-use client."""
    if not CLIENT_ID or not CLIENT_SECRET:
        sys.exit(
            "Missing Spotify credentials. Set SPOTIPY_CLIENT_ID and "
            "SPOTIPY_CLIENT_SECRET environment variables before running."
        )
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_all_liked_songs(sp: spotipy.Spotify) -> list:
    """Page through the Liked Songs library and return a list of track dicts."""
    tracks = []
    offset = 0

    while True:
        response = sp.current_user_saved_tracks(limit=PAGE_SIZE, offset=offset)
        items = response.get("items", [])
        if not items:
            break

        for item in items:
            track = item.get("track") or {}
            if not track:
                continue  # skip local files / unavailable tracks

            artists = ", ".join(a["name"] for a in track.get("artists", []))
            album = track.get("album", {}).get("name", "")
            release_date = track.get("album", {}).get("release_date", "")
            duration_ms = track.get("duration_ms", 0)
            duration = f"{duration_ms // 60000}:{(duration_ms // 1000) % 60:02d}"
            spotify_url = track.get("external_urls", {}).get("spotify", "")

            tracks.append(
                {
                    "Date Added": item.get("added_at", ""),
                    "Track Name": track.get("name", ""),
                    "Artist(s)": artists,
                    "Album": album,
                    "Release Date": release_date,
                    "Duration": duration,
                    "Spotify Link": spotify_url,
                    "Track ID": track.get("id", ""),
                }
            )

        offset += PAGE_SIZE
        print(f"Fetched {len(tracks)} tracks so far...")

    return tracks


def write_csv(tracks: list, filename: str) -> None:
    """Write track dicts to a CSV file."""
    if not tracks:
        print("No liked songs found, nothing to write.")
        return

    fieldnames = list(tracks[0].keys())
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tracks)

    print(f"Done. Wrote {len(tracks)} liked songs to {filename}")


def main():
    sp = get_spotify_client()
    tracks = fetch_all_liked_songs(sp)
    write_csv(tracks, OUTPUT_FILE)


if __name__ == "__main__":
    main()
