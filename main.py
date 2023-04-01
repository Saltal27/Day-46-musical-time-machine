from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


MY_SPOTIFY_USER_ID = os.environ.get("MY_SPOTIFY_USER_ID")

# Setting up Spotify API credentials
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"

# asking the user for the desired date
date = input("Which year do you want to travel to?\n"
             "Type the date in this format YYY-MM-DD (e.g. 2008-01-27):"
             " \033[3m [Make sure not to make any typos]\033[0m\n")

# getting hold of the site html code
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_code = response.text

# preparing the soup
soup = BeautifulSoup(billboard_code, "html.parser")

# scraping the top 100 shots
top_shots = soup.find_all(name='div', class_='o-chart-results-list-row-container')
top_100_shots_list = []
for shot in top_shots:
    title_tag = shot.find(name="h3")
    song_title = title_tag.get_text().strip()
    top_100_shots_list.append(song_title)

# authenticating Python project with Spotify using Client ID/ Client Secret
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

# creating a Spotipy object
sp = spotipy.Spotify(auth_manager=auth_manager)

# getting current user information, including user ID
# user_info = sp.current_user()
# user_id = user_info["id"]
# print(user_id)

# creating a new private playlist
new_playlist = sp.user_playlist_create(
    user=MY_SPOTIFY_USER_ID,
    name=f"{date} Billboard 100",
    public=False,
)
playlist_id = new_playlist["id"]

# searching for the songs URIs
songs_uris_list = []
for song in range(100):
    search = sp.search(q=top_100_shots_list[song], limit=1, offset=0, type='track', market=None)
    first_song_uri = search["tracks"]["items"][0]["uri"]
    songs_uris_list.append(first_song_uri)

# adding the songs to the list
for _ in range(len(songs_uris_list)):
    sp.playlist_add_items(playlist_id=playlist_id, items=[songs_uris_list[_]], position=None)
