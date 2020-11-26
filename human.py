from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from scipy.spatial import distance
from collections import Counter
from array import array
import os
from PIL import Image
import sys
import time
import cv2
import numpy as np
import random
from twilio.rest import Client

COLORS = np.random.uniform(0, 255, size=(20, 3))
subscription_key = "<YOUR SUBSCRIPTION KEY>"
endpoint = "<YOUR ENDPOINT>"
client = Client("<YOUR AUTHORIZATION ID>", "YOUR AUTH TOKEN")

def detectHuman(inputImageFrame):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    image = cv2.imread(inputImageFrame)
    inputImageFrame = open(inputImageFrame, "rb")
    detect_objects_results_local = computervision_client.detect_objects_in_stream(inputImageFrame)

    # Print results of detection with bounding boxes
    print("Detecting objects in local image:")

    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        for obj in detect_objects_results_local.objects:
            #plotting the bounding box
            cv2.rectangle(image, (obj.rectangle.x, obj.rectangle.y), (obj.rectangle.x + obj.rectangle.w, obj.rectangle.y + obj.rectangle.h),
            	COLORS[random.randint(0, 10)], 2)
            y = obj.rectangle.y - 15 if obj.rectangle.y - 15 > 15 else obj.rectangle.y + 15
            cv2.putText(image, obj.object_property, (obj.rectangle.x, y),
            	cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[random.randint(0, 10)], 2)

            if(obj.object_property == 'person'):
                # sending alert when person found
                client.messages.create(to="+919840346724",
                                       from_="+16573004187",
                                       body="Person Detected. Rescue soon")
    cv2.imshow("Output", image)
    cv2.waitKey(0)
