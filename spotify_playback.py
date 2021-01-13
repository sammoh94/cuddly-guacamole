#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 3 20:41:09 2021

@author: alec
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def spotify_playback(songID, cid, secret, redURI = 'https://www.google.com', scope = 'streaming, user-read-playback-state, user-modify-playback-state'):
    '''

    Parameters
    ----------
    songID : list of strings, required
        This value is taken in from a dictionary that maps faces to Spotify
        track URIs.
    cid : string, required ()
        Represents the Spotify app's client_id. You will get this by creating an
        authorized Spotify Developer App
    secret : string, required
        Represents the Spotify app's secret id. You will get this by creating an
        authorized Spotify Developer App (DO NOT SHARE WITH OTHERS)
    redURI : string, optional
        Redirect URI. You must confirm that you are redirected to the correct
        URI on first run of script. The default value is https://www.google.com;
        however, this will vary based on the credentials of your own app. You will
        have to make sure that whatever URI you use here is also added to your
        app in the Spotify Developer Dashboard.
    scope : string, optional
        The scopes represent what functionalities we can access.
        The scopes 'streaming, user-read-playback-state, user-modify-playback-state'
        allow us to playback music and acquire the device id from which we want
        to do that playback. Can add additional scopes for additional functionality

    Returns
    -------
    None.

    '''
    
    #create an instance of a Spotify object using our credentials
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cid, client_secret=secret, redirect_uri=redURI, scope=scope))
    
    #find the id of the device from which you want to playback music
    #default is the first device in your active devices
    #print(sp.devices())
    did = sp.devices()['devices'][0]['id']
    
    #once you know the device_id of the device you want to use you can set it
    #manually to avoid accidentally changing your active playback device
    #note: device_id changes when you close and reopen Spotify web player
    # did = ''
    
    #start playback of song that corresponds to the input song id
    sp.start_playback(device_id = did, uris=songID)
    