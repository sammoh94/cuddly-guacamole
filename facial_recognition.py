import face_recognition
import cv2
import numpy as np
from time import time
from spotify_playback import playback_song as ps
from build_database import update_favorite_track as ut
import helper
from consts import cid, secret

def run_facial_recognition(cid = cid, secret = secret, time_out = 5, face_locations = [], face_encodings = [], mapped_names = [], song_IDs = [], process_frame = True):
    '''
    Summary
    -------
    Imports the mapping from your encodings file and runs openCV and the facial
    recognition API to check if the faces found by the connected camera match
    any in your known_people directory. Plays the corresponding music for each
    recognized face.

    Parameters
    ----------
    cid : string, required
        Represents the Spotify app's client_id. You will get this by creating an
        authorized Spotify Developer App.
    secret : string, required
        Represents the Spotify app's secret id. You will get this by creating an
        authorized Spotify Developer App (DO NOT SHARE WITH OTHERS).
    time_out : int, optional
        Represents the number of seconds that the camera will remain on when running
        the script. The default value is 5 seconds.
    face_locations : list
        Creates a list that will be updated with face location coordinates as the
        program runs. The list defaults to empty.
    face_encodings : list
        Creates a list that will be updated with face encodings for all faces
        found by the camera. The list defaults to empty.
    mapped_names : list
        Creates a list that will be updated with the names of any faces that
        the camera recognizes and that match someone in oyur known_people directory.
        The list defaults to empty.
    song_IDs : list
        Creates a list that will be updated with the track URIs of all the
        people that are added to the mapped_names list. The list defaults to empty.
    process_frame : bool
        a bool that determines whether or not a frame will be processed in a given
        passthrough of the while loop. This allows the facial recognition API
        to run more efficiently. The default is True.

    Returns
    -------
    None.

    '''
    #store json object as dict that maps names to encodings and songs
    identity_map = helper.open_encoding_file_read()
        
    known_face_names, known_face_encodings, name_music_map = [], [], {}
    for identity in identity_map:
        known_face_names.append(identity)
        known_face_encodings.append(np.array(identity_map[identity][0]))
        name_music_map[identity] = identity_map[identity][1]
    
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    
    time_out_start = time()
    
    while time() < time_out_start + time_out:
        # Grab a single frame of video
        ret, frame = video_capture.read()
    
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
    
        # Only process every other frame of video to save time
        if process_frame:
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
                    song_IDs.append(name_music_map[name])
    
        process_frame = not process_frame
        
        # displays the video taken from webcam. Not actually necessary to run
        # cv2.imshow('Video', frame)
    
        # Hit 'q' on the keyboard to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    
    # Run script that plays Spotify based on matched faces
    if song_IDs:
        ps(song_IDs) 

def main(key_file = 'keys.txt'):
    #ask if user wants to update favorite track information
    if input('Update favorite track information? [Y/N] ').lower() == 'y':
        names = input('Enter names for which you wish to update favorite track (separate each by comma and space): ').split(', ')
        ut(names, cid, secret)
        
    run_facial_recognition()
    

if __name__ == '__main__':
    main()



