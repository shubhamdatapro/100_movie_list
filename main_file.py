from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# access the billboard site

year_format = input("which year you want to travel to? Type the date in this format YYYY-MM-DD:")
url = f"https://www.billboard.com/charts/hot-100/{year_format}"
# print(year)
response = requests.get(url=url)
webpage_html = response.text

soup = BeautifulSoup(webpage_html, "html.parser")
song_names = [song.get_text() for song in soup.find_all(name="span", class_="chart-element__information__song "
                                                                            "text--truncate color--primary")]
# create a txt.file to having 100 songs title

with open("playlist.txt", mode="w") as file:
    for song in song_names:
        file.write(f"{song}\n")

# access the spotify:

spotify_Client_ID = "f1818b8001044a459b8a4e84dc218a20"
spotify_Client_Secret = "53eab63d42e84e73996713797335cddf"

# find user id

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=spotify_Client_ID,
        client_secret=spotify_Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

year = year_format.split("-")[0]

# create a list of spotify song uri. format should be like is "track:{song_name} year:{year}"
song_uris = []
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass  # print(f"{song} doesn't exist in Spotify. Skipped.")

# Creates a playlist for a user

playlist = sp.user_playlist_create(user=user_id, name=f"{year_format} Billboard 100", public=False, collaborative=False,
                                   description="")
playlist_id = playlist["id"]

# Adding songs found into the new playlist
add_tracks = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
print(add_tracks)



