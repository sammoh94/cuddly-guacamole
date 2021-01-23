#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 03:26:53 2020

@author: alec
"""

import json
import face_recognition
import cv2
import numpy as np
from time import time
from spotify_playback import playbackSong as ps
from build_database import updateFavoriteTrack as ut

def runFacialRecognition(cid, secret, timeOut = 5, faceLocations = [], faceEncodings = [], mappedNames = [], songIDs = [], processFrame = True):
    '''
    Summary
    -------
    

    Parameters
    ----------
    cid : TYPE
        DESCRIPTION.
    secret : TYPE
        DESCRIPTION.
    timeOut : TYPE, optional
        DESCRIPTION. The default is 5.
    faceLocations : TYPE, optional
        DESCRIPTION. The default is [].
    faceEncodings : TYPE, optional
        DESCRIPTION. The default is [].
    mappedNames : TYPE, optional
        DESCRIPTION. The default is [].
    songIDs : TYPE, optional
        DESCRIPTION. The default is [].
    processFrame : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    None.

    '''
    #store json object as dict that maps names to encodings and songs
    with open('encodings.json', 'r') as enc:
        identityMap = json.loads(enc.read())
        
    knownFaceNames, knownFaceEncodings, nameMusicMap = [], [], {}
    for identity in identityMap:
        knownFaceNames.append(identity)
        knownFaceEncodings.append(np.array(identityMap[identity][0]))
        nameMusicMap[identity] = identityMap[identity][1]
    
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    
    timeoutStart = time()
    
    while time() < timeoutStart + timeOut:
        # Grab a single frame of video
        ret, frame = video_capture.read()
    
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
    
        # Only process every other frame of video to save time
        if processFrame:
            # Find all the faces and face encodings in the current frame of video
            faceLocations = face_recognition.face_locations(rgb_small_frame)
            faceEncodings = face_recognition.face_encodings(rgb_small_frame, faceLocations)
    
            faceNames = []
            for faceEncoding in faceEncodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(knownFaceEncodings, faceEncoding)
    
                # Use the known face with the smallest distance to the new face
                faceDistances = face_recognition.face_distance(knownFaceEncodings, faceEncoding)
                bestMatchIndex = np.argmin(faceDistances)
                if matches[bestMatchIndex]:
                    name = knownFaceNames[bestMatchIndex]
                    faceNames.append(name)
                
            for name in faceNames:
                if name not in mappedNames:
                    mappedNames.append(name)
                    songIDs.append(nameMusicMap[name])
    
        processFrame = not processFrame
        
        # displays the video taken from webcam. Not actually necessary to run
        # cv2.imshow('Video', frame)
    
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
    # Run script that plays Spotify based on matched faces
    if songIDs:
        ps(songIDs, cid, secret) 

def main():
    #acquire Spotify keys from hidden file
    with open('keys.txt', 'r') as keys:
        cid, secret = keys.read().split('\n')
    
    #ask if user wants to update favorite track information
    if input('Update favorite track information? [Y/N] ').lower() == 'y':
        names = input('Enter names you wish to update favorite track for (separate each by commas): ').split(', ')
        ut(names, cid, secret)
        
    runFacialRecognition(cid, secret)
    

if __name__ == '__main__':
    main()



