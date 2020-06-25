    import os 
    from flask import Flask, request, render_template, redirect
    from spotify_auth import request_tokens, auth_request
    import script
    from client import SpotifyClientAPI

    client_id = os.getenv('spotify_client_id')
    client_secret = os.getenv('spotify_client_secret')
    REDIRECT_URI = os.getenv('REDIRECT_URI')

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
        client = SpotifyClientAPI(
            client_id=client_id, client_secret=client_secret, access_token=access_token)
        script.script(client=client, playlist_uri=authorization.playlist_uri)
        return redirect('/success')


    @app.route('/success')
    def success():
        return render_template('success.html')


    if __name__ == '__main__':
        app.run(debug=True)