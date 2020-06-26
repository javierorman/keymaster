import psycopg2

class DBClient():
    def __init__(self, DATABASE_URL):
        self.DATABASE_URL = DATABASE_URL
        try:
            self.conn = psycopg2.connect(f"""{self.DATABASE_URL}""")
        except:
            print("Unable to connect to the database")

        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            DROP TABLE IF EXISTS orig_playlist;
            CREATE TABLE orig_playlist (
            track_uri VARCHAR(100),
            key INT,
            mode INT
            );
        """)

    def insert_track_features(self, track_features):
        uri = track_features['track_uri']
        key = track_features['key']
        mode = track_features['mode']
        self.cur.execute(f"""INSERT INTO orig_playlist
                    VALUES ({uri!r}, {key}, {mode});""")

    def list_track_uris_by_key_and_mode(self, key, mode):
        track_uris = []
        self.cur.execute(f"""SELECT track_uri
            FROM orig_playlist
            WHERE key = {key}
            AND mode = {mode};
            """)
        track_uris_tuples = self.cur.fetchall()
        if len(track_uris_tuples) != 0:
            for item in track_uris_tuples:
                track_uris.append(item[0])
        return track_uris

    def close_conn(self):
        self.conn.close()