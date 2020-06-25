import os
import psycopg2

DATABASE_URL = os.getenv('DATABASE_URL')

def connect_db():
    try:
        connect_db.conn = psycopg2.connect(f"""{DATABASE_URL}""")
    except:
        print("Unable to connect to the database")

    connect_db.conn.autocommit = True
    connect_db.cur = connect_db.conn.cursor()

def create_table():
    connect_db.cur.execute("""
        DROP TABLE IF EXISTS orig_playlist;
        CREATE TABLE orig_playlist (
        track_uri VARCHAR(100),
        key INT,
        mode INT
        );
    """)

def get_playlist_id(playlist_uri):
    playlist_id = playlist_uri.split(':')[2]
    return playlist_id

def get_playlist_name(playlist_id, client, fields):
    pl_info = client.get_playlist_info(playlist_id, fields)
    return pl_info['name']

def get_tracks_from_playlist(client, playlist_id):
    pl_tracks = client.get_playlist_tracks(playlist_id)
    return pl_tracks

def make_list_of_tracks(playlist_tracks):
    list_of_tracks = []
    for item in playlist_tracks['items']:
        track_dict = {}
        track_dict['name'] = item['track']['name']
        track_dict['id'] = item['track']['id']
        track_dict['uri'] = item['track']['uri']
        list_of_tracks.append(track_dict)
    return list_of_tracks

def get_track_info_insert_into_table(list_of_tracks, client):
    for track in list_of_tracks:
        track_id = track['id']
        track_uri = track['uri']
        track_features = client.get_audio_features(track_id)
        key = track_features['key']
        mode = track_features['mode']
        connect_db.cur.execute(f"""INSERT INTO orig_playlist
                VALUES ({track_uri!r}, {key}, {mode});""")


"""
Spotify represents keys (C, C#/Db, D, etc.) and modes (Minor, Major) with numbers:
Keys: 0 -> C, 1 -> C#/Db, 2 -> D, etc.
Modes: 0 -> Minor, 1 -> Major
"""
def real_key_and_mode(key, mode):
    keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
    modes = ['Minor', 'Major']
    return f"{keys[key]} {modes[mode]}"

def list_track_uris_by_key_and_mode(key, mode):
    track_uris = []
    connect_db.cur.execute(f"""SELECT track_uri
        FROM orig_playlist
        WHERE key = {key}
        AND mode = {mode};
        """)
    track_uris_tuples = connect_db.cur.fetchall()
    if len(track_uris_tuples) != 0:
        for item in track_uris_tuples:
            track_uris.append(item[0])
    return track_uris

def create_new_playlists_add_tracks(client, playlist_name):
    num_keys = 12
    num_modes = 2
    for key in range(num_keys):
        for mode in range(num_modes):
            track_uris = list_track_uris_by_key_and_mode(key=key, mode=mode)
            new_playlist_id = client.create_playlist(
                pl_name=f"{playlist_name}: {real_key_and_mode(key=key, mode=mode)}")                            
            response = client.add_songs_to_playlist(new_playlist_id, track_uris)
            # print(response)    

def script(client, playlist_uri):
    connect_db()
    conn = connect_db.conn
    cur = connect_db.cur
    create_table()

    playlist_id = get_playlist_id(playlist_uri=playlist_uri)
    playlist_name = get_playlist_name(playlist_id=playlist_id, client=client, fields='name')
    playlist_tracks = get_tracks_from_playlist(client=client, playlist_id=playlist_id)
    list_of_tracks = make_list_of_tracks(playlist_tracks=playlist_tracks)
    get_track_info_insert_into_table(list_of_tracks=list_of_tracks, client=client)
    create_new_playlists_add_tracks(client=client, playlist_name=playlist_name)
    
    conn.close()
