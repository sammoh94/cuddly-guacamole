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
from spotify_playback import spotify_playback as sp
from build_database import build_database as bd

#acquire Spotify keys from hidden file
with open('keys.txt', 'r') as keys:
    cid, secret = keys.read().split('\n')

#update the database of known faces
bd(cid, secret)

#store json object as dict that maps names to encodings and songs
with open('encodings.json', 'r') as encodings:
    identityMap = json.loads(encodings.read())
    
known_face_names, known_face_encodings, name_music_map = [], [], {}
for identity in identityMap:
    known_face_names.append(identity)
    known_face_encodings.append(np.array(identityMap[identity][0]))
    name_music_map[identity] = identityMap[identity][1]
    
# =============================================================================
# # Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("./known_people/Barack Obama.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
# 
# # Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("./known_people/Joe Biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
# 
# # Load a photo of myself and learn how to recognize it
# alec_image = face_recognition.load_image_file("./known_people/Alec Echevarria.jpg")
# alec_face_encoding = face_recognition.face_encodings(alec_image)[0]
# 
# # Load a photo of Emily and learn how to recognize it
# emily_image = face_recognition.load_image_file("./known_people/Emily Echevarria.jpg")
# emily_face_encoding = face_recognition.face_encodings(emily_image)[0]
# 
# # Load a photo of Michelle and learn how to recognize it
# michelle_image = face_recognition.load_image_file("./known_people/Michelle Echevarria.jpg")
# michelle_face_encoding = face_recognition.face_encodings(michelle_image)[0]
# 
# # Load a photo of Savannah and learn how to recognize it
# savannah_image = face_recognition.load_image_file("./known_people/Savannah Arnold.jpg")
# savannah_face_encoding = face_recognition.face_encodings(savannah_image)[0]
# 
# # Load a photo of Sophia and learn how to recognize it
# sophia_image = face_recognition.load_image_file("./known_people/Sophia Arnold.jpg")
# sophia_face_encoding = face_recognition.face_encodings(sophia_image)[0]
# 
# # Create arrays of known face encodings and their names
# known_face_encodings = [
#     obama_face_encoding,
#     biden_face_encoding,
#     alec_face_encoding,
#     emily_face_encoding,
#     michelle_face_encoding,
#     savannah_face_encoding,
#     sophia_face_encoding
#     ]
# 
# known_face_names = [
#     "Barack Obama",
#     "Joe Biden",
#     "Alec Echevarria",
#     "Emily Echevarria",
#     "Michelle Echevarria",
#     "Savannah Arnold",
#     "Sophia Arnold"
#     ]
# 
# name_music_map = {
#     "Barack Obama": "spotify:track:7sxKAThQGyvNPtIA2bPBVp",
#     "Joe Biden": "spotify:track:1PUh1GENlvlgu0dW28I6tY",
#     "Alec Echevarria": "spotify:track:2Fxmhks0bxGSBdJ92vM42m",
#     "Emily Echevarria": "spotify:track:1fLhGF1JfGQYj6EZLndD86",
#     "Michelle Echevarria": "spotify:track:7vVIj8Tm1wCawjvwVZdeLD",
#     "Savannah Arnold": "spotify:track:0Y1MWB026LYxGvhq4EcMiC",
#     "Sophia Arnold": "spotify:track:0GONea6G2XdnHWjNZd6zt3"
#     }
# 
# =============================================================================




#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
mapped_names = []
songIDs = []
process_this_frame = True

# timeout variable can be omitted, if you use specific value in the while condition
timeout = 5  # [seconds]
timeout_start = time()

while time() < timeout_start + timeout:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            face_names.append(name)
            
        for name in face_names:
            if name not in mapped_names:
                mapped_names.append(name)
                songIDs.append(name_music_map[name])

    process_this_frame = not process_this_frame
    
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
    print(songIDs)
    sp(songIDs, cid, secret)



