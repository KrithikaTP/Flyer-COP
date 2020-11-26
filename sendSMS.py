from twilio.rest import Client


client = Client("<YOUR AUTHORIZATION ID>", "YOUR AUTH TOKEN")


def sendToTrafficPolice(ambulanceDistance):
    client.messages.create(to="+919840346724",
                           from_="+16573004187",
                           body="Manage the signal. An ambulance is heading !!. It's away from " + str(ambulanceDistance) + " meters. Clear the Traffic.")
