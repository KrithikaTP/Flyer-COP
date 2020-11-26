# Flyer-Cop 

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [About the Project](#about-the-project)
* [Built With](#built-with)
* [Set Up the Azure Backend](#set-up-the-azure-backend)
* [Connecting the sensors with Raspberry Pi](#connecting-the-sensors-with-raspberry-Pi)
* [How to Run Bin Part Using Raspberry Pi](#how-to-run-bin-part-using-raspberry-pi)

<!-- ABOUT THE PROJECT -->
## About The Project
Traffic Police have a greater responsibility in order to maintain the public traffic control, medical emergency as well as security. 

It's a hectic task for the police to manage all these together as the current system is based on one-size-fits-all approach.

No automation involved to assist the police.

Medical emergency vehicles are not given prior attention for signal management. 

No traffic analysis is made for traffic management.

### Solution
Flyer Cop – AI / IOT enabled Drone to assist traffic police. There are several features incorporated to benefit the cop, as well as the public.

The drone is connected with Raspberry Pi B+ along with a 8MP camera. The drone was tested within a certain limted height, so as to ensure internet connectivity (connected to Mobile Hotsopt).

The drone performs real time object detection (Azure Object Detection) on roads to detect and manipulate the vehicles, people, signals and a lot more.

The detected data is then transfered to PowerBi Dashboard for analysis. Different ways of graph interpretation is done for visualizing and managing the traffic.

Also, social distance violators are detected and regions of high crowding are notified to police to handle social distancing.

Drones  have the capability to fly far off the roads and can detect any emergency vehicles (Ambulance detection on Custom Vision) are heading. This information is notified immediately to the cop for immediate signal management. Hence, the roads of the ambulances get cleared very quickly. 

In some situations such as natural calamities or any disasters, people get caught in some risky regions such as low lying hilly areas, deeply dug bore wells, etc. 

Hence, the drone works 70-80% accurate for human detection under low light, foggy areas, sandy regions where humans cannot travel easily. This ensures that the drone can also handle rescue operations.

Flyer-Cop also detects if any unknown person(Face recognition) has entered any restricted areas such as government buildings, research or scientific campus, etc.

If any unknown person is detected, then immediately a notification is sent to take immediate actions. 