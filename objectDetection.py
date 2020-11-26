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
import powerBi
COLORS = np.random.uniform(0, 255, size=(20, 3))
subscription_key = "<YOUR SUBSCRIPTION KEY>"
endpoint = "<YOUR ENDPOINT>"

def detectObjectsOnRoad(inputImageFrame):
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    image = cv2.imread(inputImageFrame)
    print("===== Detect Objects - local =====")
    inputImageFrame = open(inputImageFrame, "rb")

    minDistance = 65 # setting a basic threshold
    social_distance_violators = 0
    signal_count = 0
    vehicleCentroids = []
    peopleCentroids = []
    vehicle_distance_array = []
    objects_on_road = []
    two_wheeler_count = 0
    four_wheeler_count = 0

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
            # to find the centroid of an object
            centroid = ((obj.rectangle.x +(obj.rectangle.x + obj.rectangle.w))//2, (obj.rectangle.y +(obj.rectangle.y + obj.rectangle.h))//2)
            objects_on_road.append(obj.object_property)

            if(obj.object_property == 'person'):
                peopleCentroids.append(centroid)
            elif(obj.object_property == 'traffic light'):
                signal_count +=1
            else:
                vehicleCentroids.append(centroid)

    # people
    # to check atleast if two people are there
    if(len(peopleCentroids) >=2):
        for i in range(0,len(peopleCentroids)-1):
            for j in range(1,len(peopleCentroids)):
                d = distance.euclidean(peopleCentroids[i], peopleCentroids[j])
                if(d < minDistance):
                    social_distance_violators +=1
    # minimum distance between vehicles to check the traffic crowd
    if(len(vehicleCentroids) >=2):
        for i in range(0,len(vehicleCentroids)-1):
            for j in range(1,len(vehicleCentroids)):
                d = distance.euclidean(vehicleCentroids[i], vehicleCentroids[j])
                vehicle_distance_array.append(d)

    objects = (Counter(objects_on_road))
    for object in objects:
        if(object == 'car' or object =='truck' or object == 'shuttle bus'):
            four_wheeler_count += objects[object]
        elif(object == 'motorbike' or object == 'bicycle'):
            two_wheeler_count += objects[object]
    # send data for analysing
    powerBi.sendDataToPowerBi(len(personCentroids),min(vehicle_distance_array),signal_count,social_distance_violators,two_wheeler_count,four_wheeler_count,objects)
    cv2.imshow("Output", image)
    cv2.waitKey(0)
