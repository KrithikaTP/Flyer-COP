from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import sendSMS
import time
import cv2

# Replace with valid values
ENDPOINT = "<YOUR ENDPOINT>"
training_key = "<YOUR TRAINING KEY>"
prediction_key = "<YOUR PREDICTION KEY>"
prediction_resource_id = "<YOUR RESOURCE ID>"
project_id = '<YOUR PROJECT ID>'
publish_iteration_name = "<YOUR MODEL NAME>"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

# Now there is a trained endpoint that can be used to make a prediction
def detectAmbulance(inputImageFrame):
    # Open the sample image and get back the prediction results.
    image = cv2.imread(inputImageFrame)
    with open(inputImageFrame, mode="rb") as test_data:
        results = predictor.detect_image(project_id, publish_iteration_name, test_data)

    # Display the results.
    for prediction in results.predictions:
        if(prediction.tag_name == 'ambulance'):
            left = prediction.bounding_box.left
            top = prediction.bounding_box.top
            right = prediction.bounding_box.left + prediction.bounding_box.width
            bottom = prediction.bounding_box.top+ prediction.bounding_box.height
            cv2.rectangle(image, (left, top), (right, bottom),
                (0, 255, 0), 2)
            # sending sms notification to the traffic police to clear the traffic
            sendSMS.sendToTrafficPolice(200)
    cv2.imshow("Output", image)
    cv2.waitKey(0)
