import base64
import requests
import datetime
from datetime import datetime
from urllib.parse import urlencode

client_id = ""  # input client id
client_secret = ""  # input secret key
refresh_token = " "  # input refresh token
spotify_user_id = ""  # input spotify user id


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = ""
    client_secret = ""
    refresh_token = ""

    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.spotify_user_id = spotify_user_id

    def get_clients_credentials(self):
        """
        Return a base64 encoded string

        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_header(self):
        client_creds_b64 = self.get_clients_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {"grant_type": "refresh_token",
                "refresh_token": self.refresh_token}

    def perform_auth(self):
        # perform authentication and request for new token if it has expired
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        valid_request = r.status_code in range(
            200, 299)  # to know if its valid
        if not valid_request:
            raise Exception("Could not authenticate clients")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": f"Bearer {access_token}"
                   }
        return headers

    def get_recently_played(self):
        # Convert time to Unix timestamp in miliseconds
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
        # Download all songs you've listened to "after yesterday", which means in the last 24 hours
        endpoint = "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
            time=yesterday_unix_timestamp)
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers, params={"limit": 50})
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
