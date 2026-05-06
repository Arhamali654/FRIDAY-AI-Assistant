import spotipy
from spotipy.oauth2 import SpotifyOAuth
import subprocess
import time
import os
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI

sp = None
SPOTIFY_PATH = r"C:\Users\arham\AppData\Roaming\Spotify\Spotify.exe"
CACHE_PATH   = r"F:\JARVIS\.spotify_cache"

def init_spotify():
    global sp
    try:
        auth_manager = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state user-read-currently-playing",
            cache_path=CACHE_PATH,
            open_browser=True
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
        return True
    except Exception as e:
        print(f"[Spotify] Init error: {e}")
        return False

def ensure_spotify_open():
    if os.path.exists(SPOTIFY_PATH):
        subprocess.Popen(SPOTIFY_PATH)
        time.sleep(5)

def get_active_device():
    try:
        devices = sp.devices()
        if not devices or not devices["devices"]:
            ensure_spotify_open()
            time.sleep(5)
            devices = sp.devices()
        if devices and devices["devices"]:
            for device in devices["devices"]:
                if device["is_active"]:
                    return device["id"]
            return devices["devices"][0]["id"]
    except Exception as e:
        print(f"[Spotify] Device error: {e}")
    return None

def play_music(query: str = None) -> str:
    global sp
    if sp is None:
        if not init_spotify():
            return "Could not connect to Spotify."

    try:
        device_id = get_active_device()
        if not device_id:
            return "No Spotify device found. Please open Spotify app first and try again."

        if query and query.strip():
            results = sp.search(q=query, limit=1, type="track")
            tracks = results["tracks"]["items"]
            if tracks:
                track = tracks[0]
                track_name = track["name"]
                artist = track["artists"][0]["name"]
                sp.start_playback(device_id=device_id, uris=[track["uri"]])
                time.sleep(1)
                return f"Playing {track_name} by {artist}."
            else:
                return f"Could not find {query} on Spotify."
        else:
            sp.start_playback(device_id=device_id)
            return "Resuming Spotify playback."

    except Exception as e:
        err = str(e)
        if "NO_ACTIVE_DEVICE" in err:
            ensure_spotify_open()
            return "Spotify is opening. Please try again in a few seconds."
        elif "Premium" in err:
            return "Spotify Premium is required. Please check your account."
        return f"Spotify error: {err}"

def pause_music() -> str:
    global sp
    if sp is None:
        init_spotify()
    try:
        sp.pause_playback()
        return "Spotify paused."
    except Exception as e:
        return f"Could not pause: {str(e)}"

def next_song() -> str:
    global sp
    if sp is None:
        init_spotify()
    try:
        sp.next_track()
        time.sleep(1)
        current = sp.current_playback()
        if current and current["item"]:
            name   = current["item"]["name"]
            artist = current["item"]["artists"][0]["name"]
            return f"Playing {name} by {artist}."
        return "Skipped to next song."
    except Exception as e:
        return f"Could not skip: {str(e)}"

def previous_song() -> str:
    global sp
    if sp is None:
        init_spotify()
    try:
        sp.previous_track()
        time.sleep(1)
        current = sp.current_playback()
        if current and current["item"]:
            name   = current["item"]["name"]
            artist = current["item"]["artists"][0]["name"]
            return f"Playing {name} by {artist}."
        return "Went to previous song."
    except Exception as e:
        return f"Could not go back: {str(e)}"

def current_song() -> str:
    global sp
    if sp is None:
        init_spotify()
    try:
        current = sp.current_playback()
        if current and current["item"]:
            name   = current["item"]["name"]
            artist = current["item"]["artists"][0]["name"]
            return f"Currently playing {name} by {artist}."
        return "Nothing is playing right now."
    except Exception as e:
        return f"Could not get current song: {str(e)}"

def handle_music_command(command: str) -> str:
    cmd = command.lower()

    if "pause" in cmd or "stop" in cmd:
        return pause_music()
    elif "next" in cmd or "skip" in cmd:
        return next_song()
    elif "previous" in cmd or "prev" in cmd or "back" in cmd:
        return previous_song()
    elif "what" in cmd and ("playing" in cmd or "song" in cmd):
        return current_song()
    elif "play" in cmd:
        query = cmd.replace("play", "").replace("song", "").replace("music", "").replace("friday", "").replace("spotify", "").strip()
        return play_music(query if query else None)
    else:
        return play_music()
