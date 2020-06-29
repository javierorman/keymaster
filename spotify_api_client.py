import requests
import json

class SpotifyClientAPI():
    def __init__(self, client_id, client_secret, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    def build_get_requests_headers(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return headers

    def build_post_requests_headers(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        return headers

    def get_user_id(self):
        endpoint = 'https://api.spotify.com/v1/me'
        headers = self.build_get_requests_headers()
        r = requests.get(endpoint, headers=headers)
        response = r.json()
        user_id = response['id']
        return user_id

    def get_tracks(self):
        headers = self.build_get_requests_headers()
        endpoint = 'https://api.spotify.com/v1/me/tracks'
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_track_features(self, track_id, track_uri):
        track_features = {}
        track_features['track_uri'] = track_uri

        headers = self.build_get_requests_headers()
        endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}

        track_features['key'] = r.json()['key']
        track_features['mode'] = r.json()['mode']
        return track_features

    def get_playlist_info(self, playlist_id, fields=None):
        headers = self.build_get_requests_headers()
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        if fields:
            lookup_url = f"{endpoint}?fields={fields}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_playlist_tracks(self, playlist_id):
        headers = self.build_get_requests_headers()
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def create_playlist(self, playlist_name):
        headers = self.build_post_requests_headers()
        data = json.dumps({
            "name": f"{playlist_name}",
            "public": False
        })
        endpoint = f"https://api.spotify.com/v1/users/{self.get_user_id()}/playlists"
        r = requests.post(endpoint, data=data, headers=headers)
        response_json = r.json()
        return response_json["id"]

    def add_songs_to_playlist(self, playlist_id, track_uris):
        headers = self.build_post_requests_headers()
        data = json.dumps({
            "uris": track_uris
        })
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.post(endpoint, data=data, headers=headers)
        response = r.json()
        return response


