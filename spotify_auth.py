from urllib.parse import quote
import requests
import json

def auth_request(client_id, redirect_uri):
    endpoint = 'https://accounts.spotify.com/authorize'
    scope = 'playlist-modify-private'
    query_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope,
        'show_dialog': 'true'
    }
    url_args = '&'.join([f'{key}={quote(value)}' for key, value in query_params.items()])
    return f'{endpoint}?{url_args}'


def request_tokens(code, redirect_uri, client_id, client_secret):
    endpoint = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': str(code),
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(endpoint, data=data)
    response = json.loads(response.text)
   
    access_token = response['access_token']
    token_type = response['token_type']
    scope = response['scope']
    expires_in = response['expires_in']
    refresh_token = response['refresh_token']
   
    return access_token
