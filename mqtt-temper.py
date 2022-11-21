import os
import time
import sys
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import random

import serial

device = '/dev/ttyS0'

arduino = serial.Serial(device,9600)

MQTT_SERVER = '172.20.10.3'
THINGSBOARD_HOST = '172.20.10.2'
ACCESS_TOKEN = 'rNOlDFDG45l07N286hCY'

sensor_data = {'temperature': 0}

client = mqtt.Client()

client.username_pw_set(ACCESS_TOKEN)
#connect using default mqtt port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)

client.loop_start()
try:
    while True:
        temperature = arduino.readline()
        print("Temperature: " + str(temperature) )
        sensor_data['temperature'] = temperature

        #send data to thingsboard
        client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        #send data to local MQTT
        publish.single("/thermostat/temperature", temperature, hostname=MQTT_SERVER)

except KeyboardInterrupt:
    pass
client.loop_stop()
client.disconnect()
