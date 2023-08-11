from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy 



from spotipy.oauth2 import SpotifyOAuth


load_dotenv()  #Gets the id's

client_id= os.getenv("Client_id")
client_secret= os.getenv("Client_secret")
Base_url=os.getenv("Base_url")
Redirect_uri = f"{Base_url}/callback"

def get_token():  #Gets the access code
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": "Basic "+ auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1" #Limit because we only want the first result

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("NO ARTIST EXISTS")
        return None
    return json_result[0]

def get_songs_by_artist(token,artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def playlist_display(sp,playlist_dic):
    playlists = sp.current_user_playlists()
    for num, playlist in enumerate(playlists["items"], start=1):
        playlist_dic[num] = playlist  # Store the entire playlist dictionary
        print(f"{num}. Playlist: {playlist['name']}")

"""
def play_song_on_webplayer(sp, playlist_id, track_num):
    # Get the URI of the track that the user wants to play
    tracks = sp.playlist_tracks(playlist_id)
    track = tracks["items"][track_num]["track"]
    uri = track["uri"]

    # Play the track on the user's webplayer4
    device_id = "9691fbe4b9829484c5fa84840de5a972a9260abe"
    #sp.start_playback(uris=[uri], device_id = device_id )
    #session.playTrack(uri, device_id)
"""
#input=input("Give an artist: ")
token= get_token()
#result = search_for_artist(token, input)
#artist_id = result["id"]
#songs = get_songs_by_artist(token, artist_id)
#for num,song in enumerate(songs):
    #print(f"{num+1}. {song['name']}")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=Redirect_uri,scope="playlist-read-private, user-read-playback-state, app-remote-control"))
# Get the user's playlists
devices = sp.devices()


# Access the "devices" key which should be a list
print(devices)
devices_list = devices['devices']

# Iterate through each device entry in the list
for device_info in devices_list:
    # Access the 'type' of the device
    device_type = device_info['name']
    device_id = device_info['id']
    print(f"Device Type: {device_type}")
    print(f"Device Type: {device_id}")


playlist_dic = {}


#playlists = sp.current_user_playlists()
playlist_display(sp,playlist_dic)
"""
playlist_selector=int(input("Select the playlist you want to access by choosing a number: "))
selected=playlist_dic[playlist_selector]
tracks = sp.playlist_tracks(selected['id'])
for num, track in enumerate(tracks['items'], start=1):
    print(f"{num}. {track['track']['name']} - {track['track']['artists'][0]['name']}")

track_num=int(input("Select the song you want to play by choosing a number: "))
"""
#play_song_on_webplayer(sp, selected['id'], track_num)









