from consts import spotify_object as sp, device_ID as dev_ID
from time import sleep


def playback_song(song_ID, spotify_object = sp, device_ID = dev_ID):
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
    sp.start_playback(device_id = dev_ID, uris = song_ID)
    
    
def playback_other(ID, spotify_object = sp, device_ID = dev_ID):
    '''
    Summary
    -------
    Finds the id of the device from which you want to playback music (default
    is the first device in your active devices) and starts playback of
    a specific artist, album, or playlist through Spotify's API.
    
    Parameters
    ----------
    ID : string, required
        String taken in from a dictionary that maps faces to Spotify
        context URIs.
    spotify_object : Spotify Object
        Imported constant that allows access to Spotify information and music
        playback functionality.

    Returns
    -------
    None.

    '''
    sp.start_playback(device_id = dev_ID, context_uri = ID)

def main():
    id_map = {'track': 'spotify:track:1tuTH35fXW1zlg4thEAWQh',
              'playlist': 'spotify:playlist:5H2r8aEdGIl3jpfXQr741H',
              'artist': 'spotify:artist:1Uff91EOsvd99rtAupatMP',
              'album': 'spotify:album:3uHMSQ1cC1fFAi4WMnelQP'}
    for name, ID in id_map.items():
        print(f'Testing {name} playback...')
        if name == 'track':
            playback_song([ID])
            sleep(10)
        else:
            playback_other(ID)
            sleep(10)
            sp.next_track(dev_ID)
            sleep(10)
    sp.pause_playback(dev_ID)
    
if __name__ == '__main__':
    main()