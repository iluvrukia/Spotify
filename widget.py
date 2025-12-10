import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print("DEBUG: starting widget.py")

# ====== CONFIG PUT YOUR REAL VALUES HERE ======
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "https://iluvrukia.github.io/callback/"

SCOPE = "user-read-currently-playing user-read-playback-state"
# ================================================


def create_spotify_client():
    print("DEBUG: creating Spotify client...")
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=True,
        cache_path=".cache-spotify-widget"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("DEBUG: Spotify client created.")
    return sp


def get_now_playing(sp):
    print("DEBUG: calling current_playback()...")
    try:
        playback = sp.current_playback()
        print("DEBUG: playback =", playback)
    except Exception as e:
        print("DEBUG: error from Spotify API:", e)
        return "Error talking to Spotify", str(e)

    if not playback or not playback.get("is_playing"):
        return "Nothing playing", "Start a song in Spotify and wait a few seconds."

    item = playback.get("item") or {}
    track = item.get("name", "Unknown track")
    artists = ", ".join(a["name"] for a in item.get("artists", []))
    return track, artists


# ================== UI SETUP ==================
root = tk.Tk()
root.title("Spotify Now Playing (Python)")
root.geometry("420x110")
root.attributes("-topmost", True)

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

status_label = ttk.Label(frame, text="Initializing...", font=("Segoe UI", 9, "italic"))
status_label.pack(anchor="w", pady=(0, 5))

track_label = ttk.Label(frame, text="", font=("Segoe UI", 11, "bold"))
track_label.pack(anchor="w")

artist_label = ttk.Label(frame, text="", font=("Segoe UI", 9))
artist_label.pack(anchor="w")

sp = None  # will hold Spotify client

print("DEBUG: UI created, about to check CLIENT_ID/SECRET.")

# Simple guard so we don't silently fail
if CLIENT_ID == "CLIENT_ID" or CLIENT_SECRET == "CLIENT_SECRET":
    status_label.config(text="ERROR: Put your CLIENT_ID and CLIENT_SECRET in widget.py")
    print("ERROR: CLIENT_ID / CLIENT_SECRET are still placeholders.")
else:
    status_label.config(text="Waiting for Spotify login in browser...")
    sp = create_spotify_client()


def update():
    if sp is None:
        # No client, so nothing to do
        root.after(5000, update)
        return

    title, artists = get_now_playing(sp)
    track_label.config(text=title)
    artist_label.config(text=artists)
    if title == "Nothing playing":
        status_label.config(text="Connected. No track is currently playing.")
    elif title.startswith("Error"):
        status_label.config(text="Error from Spotify. See terminal.")
    else:
        status_label.config(text="Connected to Spotify. Updating every 5 seconds.")

    root.after(5000, update)


print("DEBUG: starting update loop.")
update()
print("DEBUG: entering Tk mainloop.")
root.mainloop()
print("DEBUG: mainloop exited.")

