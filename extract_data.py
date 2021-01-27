import json
import requests
from secrets import spotify_user_id, playlist_id
from refresh import Refresh

refresh_token = "AQD3Smys7vdX4mXFs4s0wcbT9Wh_1rmlWBqqRIxnGRRu5C5xYajr_R_pTpev_lLhbrQr-eAOI241n4HhQRtCiOM-vWRvqRKTv5Cn4oxMhaZuMcRqzGTzX3GcQbTdEZ7Sa6k"
base_64 = "MmVmMDRiOTE2MmE2NGE5Y2FlMmMyOTgxYTVlNDNhODg6OTQ4MDBlOTMxYjg1NDRiMGExNTY5YjUxYjhlZmJlMDA="
spotify_user_id = "4mcxmynlhuq6obusoyetg3w2n"


class SpotifyHistory(object):
    def __init__(self):
        self.spotify_user_id = spotify_user_id
        self.spotify_access_token = ""

    def find_songs(self):
        print("Finding recently played...")

        query = "https://api.spotify.com/v1/me/player/recently-played"

        response = requests.get(query, headers={"Content-Type": "application/json",
                                                "Authorization": "Bearer {}".format(self.spotify_access_token)}, params={"limit": 50})

        response_json = response.json()

        for i in response_json["items"]:
            self.tracks += i["track"]["uri"] + ","
            print(i["track"]["name"])
        self.tracks = self.tracks[:-1]
        self.replace_songs()

    def start(self):
        print("Refreshing token....")
        refreshCaller = Refresh()
        self.spotify_access_token = refreshCaller.refresh()
        self.find_songs()


a = SpotifyHistory()
a.start()
