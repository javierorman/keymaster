import os 
from flask import Flask, request, render_template, redirect
import subprocess
from spotify_auth import request_tokens, auth_request

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

    main_completed = subprocess.run(['python', 'main.py', authorization.playlist_uri, access_token])
    if main_completed.returncode != 0:
        return redirect('/failure')
    else:
        return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/failure')
def failure():
    return render_template('failure.html')

if __name__ == '__main__':
    app.run(debug=True)
