import requests
import os
import json

# Step 1: Your API key (replace with your actual key)
api_key = '94b5899701940c5c05f41760c0722084'

# Step 2: The hardcoded URL of the song     for song in  example, a YouTube video URL)
# song_url = input("PASTE SONG MIX URL LINK HERE:").strip()
mo_bamba = 'https://www.youtube.com/results?search_query=mo+bamba'
sampha_tinydesk = 'https://www.youtube.com/watch?v=fnIu25lXXY8'
red_button = 'https://www.youtube.com/watch?v=leWap1vgE8U&list=PLqEwRgo0ltuUNr4RAUiIgFsqF9FW_RJZB'
song_url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

# Step 3: Set up the API endpoint and parameters
api_endpoint = 'https://enterprise.audd.io/'
api_single_song = 'https://api.audd.io/'


def single_song():
# Step 6: Handle the response (you can access various details like artist name, song title, etc.)
    if song_data['status'] == 'success':
        print(f"Song: {1}")
        print(f"Song Title: {song_data['result']['title']}")
        print(f"Artist: {song_data['result']['artist']}")
        print(f"Album: {song_data['result']['album']}")
        if 'spotify' in song_data['result']:
            print(f"SPOTIFY LINK: {song_data['result']['spotify']['external_urls']['spotify']}")
            print(f"URI: {song_data['result']['spotify']['uri']}")
        print("________________________________________________")
        # Additional data can be accessed similarly
    else:
        print("Song not recognized")

def append_song_data():
    if song_data['status'] == 'success' and "spotify" not in song_data['result']:
        songsforSpotify.append({"Song Title": song_data['result']['title'], 
                                "Artist": song_data['result']['title'], 
                                "Album": song_data['result']['album'],
                                "spotify_link": "spotify data unavailable",
                                "spotify_uri": "spotify data unavailable"}
                                )
    else:
        songsforSpotify.append({"song Title": song_data['result']['title'], 
                                "artist": song_data['result']['title'], 
                                "album": song_data['result']['album'],
                                "spotify_link": song_data['result']['spotify']['external_urls']['spotify'],
                                "spotify_uri": song_data['result']['spotify']['uri']}
                                )


def getSonglocations():
    # Define the path to your music folder
    music_folder = r'C:\Users\cash\Music'

    # Traverse the directory and its subdirectories
    song_paths =[]
    supported_song_formats = [
        ".mp3",
        ".wav",
        ".flac",
        ".ogg",
        ".aac",
        ".m4a",
        ".wma",
        ".aiff",
        ".alac"
    ]
    song_paths =[]
    for root, dirs, files in os.walk(music_folder):
        for file_name in files:
            # Full path to the file by joining song name with root folder
            file_path = os.path.join(root, file_name)
            # If you need to check the file's name or extension
            file_base_name, file_extension = os.path.splitext(file_name)
            if file_extension.lower() in supported_song_formats:
                song_paths.append(file_path)
                
    return song_paths 

songs = getSonglocations()
print(songs)

songsforSpotify = []

with open('song_data.json', 'w') as json_file:
    pass
for song_path in songs:
    audio_path = r'C:\Users\cash\Downloads\utomp3.com - Lonely feat Lorine Chia.mp3'

    params = {
        'api_token': api_key,
        'return': 'spotify'  # This can include 'apple_music', 'spotify', 'deezer', etc.
    }

    with open(song_path, 'rb') as audio_file:
        files = {'file': audio_file}

    # Step 4: Make the request to the Audd.io API
        response = requests.post(api_single_song, data=params, files=files)

    # Step 5: Check the response and parse the result
    if response.status_code == 200:
        song_data = response.json()


        with open('song_data.json', 'a') as json_file:
            json.dump(song_data, json_file, indent=4)
        
        print(song_data)
        single_song()
        append_song_data()
    else:
        print(f"Error: {response.status_code}")


print (songsforSpotify)

def multi_song():
    # Step 6: Handle the response (you can access various details like artist name, song title, etc.)
    if song_data['status'] == 'success':
        # iterating thru results
        for songs_list in song_data['result']:
            # iterate thru songs map
            for song_map in songs_list:
                print(f"Song Title: {song_map['title']}")
                print(f"Artist: {song_map['artist']}")
                print(f"Album: {song_map['album']}")
                # print(f"uri: {song_map['album']}")
                # print(f"Spotify Link: {song_map['album']}")
                # Additional data can be accessed similarly
    else:
        print("Song not recognized")

