import os
import sys
from itertools import product
from spotify_api_client import SpotifyClientAPI
import spotify_api_processor
from db_client import DBClient

client_id = os.getenv('spotify_client_id')
client_secret = os.getenv('spotify_client_secret')
DATABASE_URL = os.getenv('DATABASE_URL')

playlist_uri = sys.argv[1]
access_token = sys.argv[2]

api_client = SpotifyClientAPI(
    client_id=client_id, client_secret=client_secret, access_token=access_token)

db_client = DBClient(DATABASE_URL=DATABASE_URL)

playlist_id = spotify_api_processor.get_playlist_id(
    playlist_uri=playlist_uri)
playlist_name = api_client.get_playlist_info(
    playlist_id=playlist_id, fields='name')['name']
playlist_tracks = api_client.get_playlist_tracks(playlist_id=playlist_id)

db_client.create_table()

for item in playlist_tracks['items']:
    track_id = item['track']['id']
    track_uri = item['track']['uri']
    track_features = api_client.get_track_features(
        track_id=track_id, track_uri=track_uri)
    if track_features == {}:
        continue
    db_client.insert_track_features(track_features=track_features)

list_keys = list(range(12))
list_modes = list(range(2))

for key, mode in list(product(list_keys, list_modes)):
    track_uris = db_client.list_track_uris_by_key_and_mode(
        key=key, mode=mode)
    new_playlist_id = api_client.create_playlist(
        playlist_name=f"{playlist_name}: {spotify_api_processor.real_key_and_mode(key=key, mode=mode)}")
    api_client.add_songs_to_playlist(new_playlist_id, track_uris)

db_client.close_conn()
