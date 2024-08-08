import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import pprint

app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie'

# set a random secret key to sign the cookie
app.secret_key = 'YOUR_SECRET_KEY'

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = '11b314828c96417e9f75f58ad96e3ec6',
        client_secret = '5ebadf3dc8da4976950ddb35ac447085',
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

@app.route('/')
def login():
    #Spotifu oauth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect user to authorization URL
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code from the request parameters
    token_info = create_spotify_oauth().get_access_token(code)
    #save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('save_discover_weekly',_external= True))
                    
@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        # get the token info from the session
        token_info= get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not loggged in')
        return redirect("/")
    
    # spotipy instance with access token
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # get your palylists
    current_playlists = sp.current_user_playlists()['items']
    print(f'items as requested ')
    pprint.pprint(current_playlists)

    discover_weekly_playlist_id = None
    saved_weekly_playlist_id = None

    # find the Discover Weekly and Saved Weekly playlists
    count = 1
    print("printing playlists:")
    for playlist in current_playlists:
        if(playlist['name'] == 'Discover Weekly'):
            discover_weekly_playlist_id = playlist['id']
        if(playlist['name'] == 'Saved Weekly'):
            saved_weekly_playlist_id = playlist['id']
        print(f"{count}. {playlist['name']} ")
        count += 1

    # if the Discover Weekly playlist is not found, return an error message
    if not discover_weekly_playlist_id:
        return 'Discover Weekly not found.'

    # get the tracks from the Discover Weekly playlist
    discover_weekly_playlist = sp.playlist_items(discover_weekly_playlist_id)
    song_uris = []
    for song in discover_weekly_playlist['items']:
        song_uri= song['track']['uri']
        song_uris.append(song_uri)

    # add tracks to the saved Weekly playlist
    sp.user_playlist_add_tracks("YOUR_USER_ID", saved_weekly_playlist_id, song_uris, None)

    # return a success message
    return ('Discover Weekly songs added successfully')

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login',_external=False))

    # check if then token is expired and refresh itif necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotipy_oauth = create_spotify_oauth()
        token_info = spotipy_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

app.run(debug=False)


