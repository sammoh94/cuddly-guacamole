from consts import spotify_object as sp


def playback_song(song_ID, spotify_object = sp):
    '''
    Summary
    -------
    Finds the id of the device from which you want to playback music (default
    is the first device in your active devices) and starts playback of
    the song(s) in song_ID through Spotify's API.
    
    Parameters
    ----------
    song_ID : list, required
        List of strings taken in from a dictionary that maps faces to Spotify
        track URIs.
    spotify_object : Spotify Object
        Imported constant that allows access to Spotify information and music
        playback functionality.

    Returns
    -------
    None.

    '''
    # uncomment to see all active devices
    # print(sp.devices())
    dev_ID = sp.devices()['devices'][0]['id']
    
    sp.start_playback(device_id = dev_ID, uris = song_ID)

def main():
    playback_song(['spotify:track:1tuTH35fXW1zlg4thEAWQh'])
    
if __name__ == '__main__':
    main()