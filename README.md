# Entrance Music
Connects to a camera and runs facial recognition software to play specific songs/artists/playlists on Spotify

# Getting Started
## Pre-Requisites
1. face-recognition: `1.3.0`
    - Python 3.3+ or Python 2.7 (Note: This library works in Python 2.7, but the project runs Python 3+)
    - macOS or Linux (Windows not officially supported, but might work)
    - have [dlib](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf) installed
2. spotipy: `2.16.1`
3. Have a [Spotify Premium account](https://www.spotify.com/ca-en/premium/)
4. Sign up for a [Spotify developer account](https://developer.spotify.com)

## Setup
Clone this repository

`git clone git@github.com:sammoh94/cuddly-guacamole.git`

Create a new app in your Spotify developer account and take note of your client ID and secret key.
Make sure to also add a Redirect URI to your project by clicking the edit button on your app (the default used for this project is https://www.google.com, but any valid URL should work).

# API Reference

[face-recognition download](https://pypi.org/project/face-recognition/)\
[face-recognition documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)

Run the following in your terminal/command prompt:

`pip install face-recognition`\
or\
`python3 -m pip install face-recognition`


[spotipy download](https://pypi.org/project/spotipy/)\
[spotipy documentation](https://spotipy.readthedocs.io/en/2.16.1/)


Run the following in your terminal/command prompt:

`pip install spotipy`\
or\
`python3 -m pip install spotipy`

# How to Use
1. Navigate to the local repository:

`cd cuddly_guacamole/`

2. Run *make setup* from the terminal to create required files and directories if they do not already exist:

`make setup`

3. In your text editor, manually enter your client ID and secret ID into the *keys.txt* file (see *keys.txt.sample* file for proper formatting)

4. Manually add images of people you want to store in your database to the *known_people* directory that was just created. Files must be named with the form 'firstName lastName.jpg' (e.g. Alec Echevarria.jpg).

5. Run *make build* from the terminal to build your database that maps names to face encodings and music selections:

`make build`

**Note** The user will be prompted to input song and artist information for every .jpg file in the *known_people* directory. If the song is not found (spelled incorrectly or not on Spotify), the user will be prompted to try again.

6. Run *make test-playback* from the terminal to ensure that you can connect to the Spotify web API and playback music:

`make test-playback`

7. Run *make run* from the terminal to run the facial recognition program and playback music from Spotify for all recognized faces.

`make run`

**Note** The user will be asked if they want to update favorite track information for anyone in the *known_people* directory. If so, type *Y* and input the new information. Else, type *N*.

7. Whenever you add new photos to your *known_people* directory, be sure to update the database by running *make build* in the terminal:

`make build`

**Note** Type *make* or *make help* in the terminal to see what each rule in the Makefile does:

`make` or `make help`

# Contributors

[Alec Echevarria](https://github.com/aleceche)\
[Samarth Mohan](https://github.com/sammoh94)


# License
This project is licensed under the MIT License - see the LICENSE file for details