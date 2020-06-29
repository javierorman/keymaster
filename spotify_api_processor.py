"""
Spotify represents keys (C, C#/Db, D, etc.) and modes (Minor, Major) with numbers:
Keys: 0 -> C, 1 -> C#/Db, 2 -> D, etc.
Modes: 0 -> Minor, 1 -> Major
"""
def real_key_and_mode(key, mode):
        keys = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F',
                'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']
        modes = ['Minor', 'Major']
        return f"{keys[key]} {modes[mode]}"

def get_playlist_id(playlist_uri):
    playlist_id = playlist_uri.split(':')[2]
    return playlist_id
