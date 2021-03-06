# Signifies our desired python version
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
.PHONY = help setup test-playback build run open-spotify

FILES = encodings.json keys.txt

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "-----------------------HELP------------------------"
	@echo "To setup the project's directories type make setup"
	@echo "To test music playback type make test-playback"
	@echo "To build your database of faces type make build"
	@echo "To run real-time recognition/playback type make run"
	@echo "---------------------------------------------------"

setup:
	@echo "Generating project files and directories..."
	@echo ""
	@[ -d known_people ] || (echo "known_people directory not found, generating..." && mkdir known_people)
	@for FILE in ${FILES}; do \
		[ -f $${FILE} ] || (echo "\nNo $${FILE} file found, generating..." && touch $${FILE}); \
	done
	@echo "Finished"

test-playback:
	@echo "Testing connection to Spotify's web API..."
	@${PYTHON} spotify_playback.py
	@echo "Success"

build:
	@echo "Building database to map face encodings from images in known_people directory to song choices..."
	@${PYTHON} build_database.py
	@echo "Mapping complete"

run:
	@echo "Running live facial recognition and Spotify playback..."
	@${PYTHON} facial_recognition.py

open-spotify:
	@echo "Opening Spotify web player in default browser..."
	@open https://open.spotify.com/?_ga=2.137983541.461928168.1612716830-1561551782.1610510379
	@sleep 10