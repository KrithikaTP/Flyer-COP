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
import iothub
import cv2
import numpy as np
import random

KEY = "<YOUR KEY>"

# This endpoint will be used in all examples in this quickstart.
ENDPOINT = "<YOUR ENDPOINT>"

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
# Used in the Person Group Operations and Delete Person Group examples.
# You can call list_person_groups to print a list of preexisting PersonGroups.
# SOURCE_PERSON_GROUP_ID should be all lowercase and alphanumeric. For example, 'mygroupname' (dashes are OK).
PERSON_GROUP_ID = str('campus') # assign a random ID (or name it anything)

# Used for the Delete Person Group example.
TARGET_PERSON_GROUP_ID = str('campus') # assign a random ID (or name it anything)



# Create empty Person Group. Person Group ID must be lower case, alphanumeric, and/or with '-', '_'.
print('Person group:', PERSON_GROUP_ID)
def createPersonGroup(user_images):
    face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)

    # Define woman friend
    user1 = face_client.person_group_person.create(PERSON_GROUP_ID, "user1")
    # Find all jpeg images of friends in working directory
    # user_images = ['test1.jpg','test2.jpg','test3.jpg']


    # Add to a woman person
    for image in user_images:
        w = open(image, 'r+b')
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, user1.person_id, w)
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
def testForIdentification(inputImageFrame):
    # Group image for testing against
    test_image_array = glob.glob(inputImageFrame)
    image = cv2.imread(inputImageFrame) # to show bounding box input
    image = open(test_image_array[0], 'r+b')

    print('Pausing for 60 seconds to avoid triggering rate limit on free account...')
    # time.sleep (60)

    # Detect faces
    face_ids = []
    # We use detection model 2 because we are not retrieving attributes.
    faces = face_client.face.detect_with_stream(image, detectionModel='detection_02')
    for face in faces:
        face_ids.append(face.face_id)
    # Identify faces

    if(len(face_ids) > 0):
        results = face_client.face.identify(face_ids, PERSON_GROUP_ID)
        print('Identifying faces in {}'.format(os.path.basename(image.name)))
        if not results:
            print('No person identified in the person group for faces from {}.'.format(os.path.basename(image.name)))
        for person in range(len(results)):
            # put a bounding box for each person's face
            rect = faces[person].face_rectangle
            left = rect.left
            top = rect.top
            right = left + rect.width
            bottom = top + rect.height
            if len(results[person].candidates) > 0:
                cv2.rectangle(image, (left, top), (right, bottom),
                    (0, 255, 0), 2) # green bounding box for known people
                # known person identified, so do nothing
                continue
            else:
                cv2.rectangle(image, (left, top), (right, bottom),
                    (0, 0, 255), 2) # red bounding box for unknown people
                # unknown person detected so immediatedly send notification
                iothub.sendAlert(len(face_ids))
                break
            cv2.imshow("Output", image)
            cv2.waitKey(0)
    else:
        print('No faces detected')
