#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 3 20:41:09 2021

@author: alec
"""

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
        list of strings taken in from a dictionary that maps faces to Spotify
        track URIs.
    spotify_object : Spotify Object
        imported constant that allows access to Spotify information and music
        playback

    Returns
    -------
    None.

    '''
    
    # uncomment to see all active devices
    # print(sp.devices())
    dev_ID = sp.devices()['devices'][0]['id']
    
    sp.start_playback(device_id = dev_ID, uris = song_ID)

    