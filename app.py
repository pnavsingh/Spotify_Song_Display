from flask import Flask, request , render_template
from main import get_token,playlist_display
import spotipy
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


load_dotenv()
client_id= os.getenv("Client_id")
client_secret= os.getenv("Client_secret")
Base_url=os.getenv("Base_url")
Redirect_uri = f"{Base_url}/callback"

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    return 'Callback received. You can close this page.'

@app.route('/')
def index():
    # Get the access token


    # Pass the access token and the list of tracks to the HTML template, along with the device ID
    token = get_token()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=Redirect_uri, scope="playlist-read-private, user-read-playback-state, app-remote-control"))

    # Get the list of playlists
    playlist_dic = {}
    playlist_display(sp, playlist_dic)

    # Get the playlist that the user selected
    playlist_selector = int(input("Select the playlist you want to access by choosing a number: "))
    selected = playlist_dic[playlist_selector]
    
    # Get the list of tracks in the playlist
    tracks = sp.playlist_tracks(selected['id'], token)['items']
    
    # Prepare a dictionary where keys are track numbers and values are track information
    tracks_dict = {num: track for num, track in enumerate(tracks, start=1)}
    

    # Pass the access token and the list of tracks to the HTML template
    return render_template('Webplayer_sdk.html', token=token, tracks=tracks_dict)

if __name__ == '__main__':
    app.run(debug=True)
