import os 
from flask import Flask, request, render_template, redirect
from itertools import product
from spotify_auth import request_tokens, auth_request
from api_client import SpotifyClientAPI
from db_client import DBClient

client_id = os.getenv('spotify_client_id')
client_secret = os.getenv('spotify_client_secret')
REDIRECT_URI = os.getenv('REDIRECT_URI')
DATABASE_URL = os.getenv('DATABASE_URL')

app = Flask(__name__, template_folder='templates')


"""
Ask user for plalist URI, e.g. 'spotify:playlist:63kEKf0LebJO2iq9REryiW'
"""
@app.route('/')
def home():
    return render_template('home.html')


"""
Retrieve playlist URI from user input
Direct browser to Spotify authorization page
"""
@app.route('/authorization', methods=['POST'])
def authorization():
    authorization.playlist_uri = request.form['playlist_uri']
    auth_url = auth_request(client_id=client_id, redirect_uri=REDIRECT_URI)
    return redirect(auth_url)


"""
1. Receive access code from Spotify's API
2. Use access code to request access token
3. Create client object to communicate with API
4. Run script
"""
@app.route('/callback')
def process():
    code = request.args['code']
    access_token = request_tokens(code=code, redirect_uri=REDIRECT_URI, client_id=client_id, client_secret=client_secret)
    
    api_client = SpotifyClientAPI(client_id=client_id, client_secret=client_secret, access_token=access_token)
    db_client = DBClient(DATABASE_URL=DATABASE_URL)

    playlist_id = api_client.get_playlist_id(playlist_uri=authorization.playlist_uri)
    playlist_name = api_client.get_playlist_info(playlist_id=playlist_id, fields='name')['name']
    playlist_tracks = api_client.get_playlist_tracks(playlist_id=playlist_id)
    
    db_client.create_table()

    for item in playlist_tracks['items']:
        track_id = item['track']['id']
        track_uri = item['track']['uri']
        track_features = api_client.get_track_features(track_id=track_id, track_uri=track_uri)
        db_client.insert_track_features(track_features=track_features)

    list_keys = list(range(12))
    list_modes = list(range(2))
    
    for key, mode in list(product(list_keys, list_modes)):
        track_uris = db_client.list_track_uris_by_key_and_mode(key=key, mode=mode)
        new_playlist_id = api_client.create_playlist(
            pl_name=f"{playlist_name}: {api_client.real_key_and_mode(key=key, mode=mode)}")
        api_client.add_songs_to_playlist(new_playlist_id, track_uris)

    db_client.close_conn()

    return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
