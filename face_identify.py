# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 19:14:29 2020

@author: Alec
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 21:53:35 2020
@author: alec
"""

import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


KEY = "f93c38a4fde34ad5913b81302b4133ea"
ENDPOINT = "https://facial-recognition-music.cognitiveservices.azure.com/"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))


# <snippet_persongroupvars>
# Used in Person Group Operations and Delete Person Group.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)

# Used for Delete Person Group.
TARGET_PERSON_GROUP_ID = str(uuid.uuid4()) # assign a random ID (or name it anything)
# </snippet_persongroupvars>



print('-----------------------------')
print()
print('PERSON GROUP OPERATIONS')
print()

# <snippet_persongroup_create>
'''
Create the PersonGroup
'''
# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

# Define alec
alec = face_client.person_group_person.create(PERSON_GROUP_ID, "Alec")
# Define man friend
elvy = face_client.person_group_person.create(PERSON_GROUP_ID, "Elvy")
# </snippet_persongroup_create>

# <snippet_persongroup_assign>
'''
Detect faces and register to correct person
'''
# Find all jpeg images of friends in working directory
alec_images = [file for file in glob.glob('*.jpg') if file.startswith("alec")]
elvy_images = [file for file in glob.glob('*.jpg') if file.startswith("elvy")]

# Add to a alec person
for image in alec_images:
    al = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, alec.person_id, al)

# Add to a man person
for image in elvy_images:
    el = open(image, 'r+b')
    face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, elvy.person_id, el)

# </snippet_persongroup_assign>

# <snippet_persongroup_train>
'''
Train PersonGroup
'''
print()
print('Training the person group...')
# Train the person group
face_client.person_group.train(PERSON_GROUP_ID)

while (True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status: {}.".format(training_status.status))
    print()
    if (training_status.status is TrainingStatusType.succeeded):
        break
    elif (training_status.status is TrainingStatusType.failed):
        sys.exit('Training the person group has failed.')
    time.sleep(5)
# </snippet_persongroup_train>

# <snippet_identify_testimage>
'''
Identify a face against a defined PersonGroup
'''
# Group image for testing against
test_image_array = glob.glob('test-alec-elvy.jpg')
image = open(test_image_array[0], 'r+b')

print('Pausing for 60 seconds to avoid triggering rate limit on free account...')
time.sleep (60)

# Detect faces
face_ids = []
# We use detection model 2 because we are not retrieving attributes.
faces = face_client.face.detect_with_stream(image, detectionModel='detection_02')
for face in faces:
    face_ids.append(face.face_id)
# </snippet_identify_testimage>

# <snippet_identify>
# Identify faces
results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
print('Identifying faces in {}'.format(os.path.basename(image.name)))
if not results:
    print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
for person in results:
	if len(person.candidates) > 0:
		print('Person for face ID {} is identified in {} with a confidence of {}.'.format(person.face_id, os.path.basename(image.name), person.candidates[0].confidence)) # Get topmost confidence score
	else:
		print('No person identified for face ID {} in {}.'.format(person.face_id, os.path.basename(image.name)))
# </snippet_identify>
print()


print('-----------------------------')
print()
print('DELETE PERSON GROUP')
print()
# <snippet_deletegroup>
# Delete the main person group.
face_client.person_group.delete(person_group_id=PERSON_GROUP_ID)
print("Deleted the person group {} from the source location.".format(PERSON_GROUP_ID))
print()
# </snippet_deletegroup>
