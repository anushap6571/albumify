import os
import dotenv
from flask import Flask, render_template, request, redirect, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

dotenv.load_dotenv()
client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
redirect_uri = 'http://localhost:5000/callback'
scope = 'playlist-read-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = scope,
    cache_handler = cache_handler,
    show_dialog = True
)

# create an instance of a spotify client
sp = Spotify(auth_manager = sp_oauth)


@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return render_template('home.html')

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return render_template('home.html')
 

@app.route('/get_album')
def get_album():
    users_playlists = []
    user_id = sp.current_user()['id']
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
            users_playlists.append(playlist)

    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in users_playlists]
   # playlists_html = '\n'+ ([f'{name}: {url}' for name, url in playlists_info])
    return render_template('playlists-list.html', list = playlists_info)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug = True)