import os
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import spotipy


BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]

billboard_list = []
artists_list = []
track_links = []

user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
input_year = user_input[0:4]
print("Please wait. Loading...")

response = requests.get(url=f"{BILLBOARD_URL}{user_input}/")
html = response.text

soup = BeautifulSoup(html, "html.parser")
song_one = soup.find(
    name="h3",
    class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 "
           "u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-"
           "230@tablet-only u-letter-spacing-0028@tablet",
    id="title-of-a-story"
)

# artist_one = soup.find(
#     name="span",
#     class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max "
#            "u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@"
#            "tablet-only u-font-size-20@tablet"
# )
try:
    billboard_list.append(song_one.text.strip())
except AttributeError:
    print("Please enter a valid date.")
# artists_list.append(artist_one.text.strip())

else:
    song_list = soup.find_all(
        name="h3",
        class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-"
               "16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@"
               "tablet-only",
        id="title-of-a-story"
    )

    # artist_list = soup.find_all(
    #     name="span",
    #     class_="c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max "
    #            "u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@"
    #            "tablet-only"
    # )
    # print(artist_list)
    for song_title in song_list:
        name = song_title.text.strip()
        billboard_list.append(name)
    print("Finished collating data...")
    # for artist in artist_list:
    #     name = artist.text.strip()
    #     artists_list.append(name)

    # sp = spotipy.Spotify(auth="AQDyS0rEvmDeeV6UYGeWXJv2MkQXe8L6y77oOf6Qu1mmLEYvBih-9VPo8C-wiS2v0kjOhK2knJk6VvoKqKlr97ZPdEqi50DseN4GK8GX7DRNJzd90E06zufYYmCoPbuVChc")
    sp = spotipy.Spotify(auth=f"{AUTH_TOKEN}")
    spotipy_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="https://example.com",
        scope="playlist-modify-private",
        cache_path="token.txt"
    )

    # spotipy_oauth.get_access_token(code=None, as_dict=True, check_cache=True)
    print("Account accessed...")
    username = sp.current_user()["id"]
    # print(username)
    # print(billboard_list)
    # print(artists_list)

    print("Preparing playlist...")
    for index in range(0, len(billboard_list)):
        search_response = sp.search(
            q=f"track:{billboard_list[index]} year:{input_year}",
            limit=1
        )
        # pprint(search_response)
        try:
            track_link = search_response["tracks"]["items"][0]["external_urls"]["spotify"]
        except IndexError:
            pass
        else:
            track_links.append(track_link)

    playlist_response = sp.user_playlist_create(
        user=username,
        name=f"{user_input} Billboard Top 100",
        public=False,
        collaborative=False,
        description=""
    )

    playlist_id = playlist_response["id"]

    sp.playlist_add_items(playlist_id=playlist_id, items=track_links)
    print("Playlist created!")
