import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "<YOUR IOTHUB CONNECTION STRING>"
MSG_TXT = '{{"unknown_face": {unknown_face}}}'



def iothub_client_init():

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def sendAlert(numberOfPersons):
    client = iothub_client_init()
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )


    msg_txt_formatted = MSG_TXT.format(unknown_face = numberOfPersons)
    message = Message(msg_txt_formatted)
    message.custom_properties["unknownPersonDetected"] = "true"


    time.sleep(1)
    # Send the message.
    print( "Sending message: {}".format(message) )
    client.send_message(message)
    print ( "Message successfully sent" )
    time.sleep(5)
