import spotipyfrom spotipy.oauth2 import SpotifyOAuthfrom helper import open_keys_file_read as keysred_URI = 'https://www.google.com'scopes = 'streaming, user-read-playback-state, user-modify-playback-state'cid, secret = keys()spotify_object = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = cid, client_secret = secret, redirect_uri = red_URI, scope = scopes))device_ID = spotify_object.devices()['devices'][0]['id']