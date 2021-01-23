# Entrance Music
Connects to a camera and runs facial recognition software to play specific songs/artists/playlists on Spotify

# Getting Started
## Pre-Requisites
1. face-recognition: `1.3.0`
    - Python 3.3+ or Python 2.7
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

[face-recognition download](https://pypi.org/project/face-recognition/)
[face-recognition documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)

Run the following in your terminal/command prompt:

`pip install face-recognition`
or
`python3 -m pip install face-recognition`


[spotipy download](https://pypi.org/project/spotipy/)
[spotipy documentation](https://spotipy.readthedocs.io/en/2.16.1/)


Run the following in your terminal/command prompt:

`pip install spotipy`
or
`python3 -m pip install spotipy`

# How to Use
navigate to the local repository

`cd cuddly_guacamole/`

and run build_database.py from the terminal

`python3 build_database.py`

or from your favorite IDE to create required files and directories (see docstring for build_database.py for more information) and add them to your .gitignore file

**Note** - first run creates the 'known_people' directory in which you will store your images.

You will then have to manually add images of people you want to store in your database to this directory. Files should be named with the form 'firstName lastName.jpg' (e.g. Alec Echevarria.jpg).

Once you've added your images, you can rerun build_database.py to build your database mapping names to faces and music.

There's more I'll add later

# Contributors

[Alec Echevarria](https://github.com/aleceche)
[Samarth Mohan](https://github.com/sammoh94)


# License
This project is licensed under the MIT License - see the LICENSE file for details