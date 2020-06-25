import requests
import json

class SpotifyClientAPI():
    def __init__(self, client_id, client_secret, access_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

    # Set up headers for API calls
    def get_resource_header(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        return headers

    # Get User ID: https://developer.spotify.com/documentation/web-api/reference/users-profile/get-current-users-profile/
    def get_user_id(self):
        endpoint = 'https://api.spotify.com/v1/me'
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        response = r.json()
        user_id = response['id']
        return user_id

    # API calls
    def get_audio_features(self, track_id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/audio-features/{track_id}"
        r = requests.get(endpoint, headers=headers)
        # print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_tracks(self):
        headers = self.get_resource_header()
        endpoint = 'https://api.spotify.com/v1/me/tracks'
        r = requests.get(endpoint, headers=headers)
        # print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_playlist_info(self, playlist_id, fields=None):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        if fields is None:
            lookup_url = endpoint
        else:
            lookup_url = f"{endpoint}?fields={fields}"
        r = requests.get(endpoint, headers=headers)
        # print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_playlist_tracks(self, playlist_id):
        headers = self.get_resource_header()
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.get(endpoint, headers=headers)
        # print(r.status_code)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def create_playlist(self, pl_name):
        user_id = self.get_user_id()
        token = self.access_token
        request_body = json.dumps({
            "name": f"{pl_name}",
            "public": False
        })
        endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        r = requests.post(endpoint, data=request_body, headers=headers)
        # print(r.status_code)
        response_json = r.json()
        return response_json["id"]

    def add_songs_to_playlist(self, playlist_id, track_uris):
        access_token = self.access_token
        request_data = json.dumps({
            "uris": track_uris
        })
        print(request_data)
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        r = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        # print(r.status_code)
        response = r.json()
        return response
