import identifyFace
from picamera import PiCamera
import time

camera = PiCamera()

while True:
    camera.start_preview() # display the video on screen
    camera.capture('inputImageFrame.jpg') # capturing the video framewise
    time.sleep(1) #to avoid unusual traffic buffer
    identifyFace.testForIdentification('inputImageFrame.jpg') # frame wise input sent to the api call
    
