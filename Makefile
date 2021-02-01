# Signifies our desired python version
PYTHON = python3

# .PHONY defines parts of the makefile that are not dependant on any specific file
.PHONY = help setup test-playback build run clean

FILES = .gitignore encodings.json keys.txt

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
		[ -d $${FILE} ] || (echo "\nNo $${FILE} file found, generating..." && touch $${FILE}); \
		[ $${FILE} == .gitignore ] || (echo "Adding $${FILE} to .gitignore...") \
	done
	@echo "Finished"

.gitignore:
	# I have no idea how I'm supposed to write to my gitignore file
	$(file <$@)

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