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


THINGSBOARD_HOST = '172.20.10.2'
MQTT_SERVER = '172.20.10.3'
ACCESS_TOKEN_1 = 'zezMTL9ZQh6Ran1XuWTk'
ACCESS_TOKEN_2 = 'xkOXh82O8Gqyq4xcN1X9'

sensor_data = {'status': 'Empty'}
actuator_data = {'state': 'Close'}

client_1 = mqtt.Client()
client_2 = mqtt.Client()
local_client = mqtt.Client()

client_1.username_pw_set(ACCESS_TOKEN_1)
client_2.username_pw_set(ACCESS_TOKEN_2)
#automation
def openGate():
    arduino.write(b"2")
def closeGate():
    arduino.write(b"1")
def autoOff():
    arduino.write(b"4")
def autoOn():
    arduino.write(b"5")

tocheck = "30"
#setup subscriber
def on_message(client, userdata, msg):
    print('Topic' + msg.topic + '\nMessage: ' + str(msg.payload))
    topic = msg.topic.split('/')
    target = topic[1]
    subtarget = topic[2]
    value = int(msg.payload)
    if target == "thermostat":
        if subtarget == "temperature":
            if value > int(tocheck):
                autoOff()
                openGate()
        elif target == "threshold":
            pass
    elif target == "automate":
        if value == 1:
            autoOn()
        elif value == 0:
            autoOff()

    elif target == "gate":
        if value == 1:
            openGate()
        elif value == 0:
            closeGate()

def on_connect(client, userdata, flags, rc):
    print("connect to local mqtt server: result " + str(rc))
    client.subscribe("/thermostat/temperature")
    client.subscribe("/thermostat/threshold")
    client.subscribe("/automate/toggle")
    client.subscribe("/gate/order")

local_client.on_connect = on_connect
local_client.on_message = on_message
#connect using default mqtt port and 60 seconds keepalive interval
client_1.connect(THINGSBOARD_HOST, 1883, 60)
client_2.connect(THINGSBOARD_HOST, 1883, 60)
local_client.connect(MQTT_SERVER, 1883, 60)

client_1.loop_start()
client_2.loop_start()
local_client.loop_start()
try:
    while True:
        line = arduino.readline()
        array = line.split()
        status = array[0]
        state = array[1]
        #state = "CLOSE"
        #status = "EMPTY"
        print("Front gate: " + state + " " + status )
        sensor_data['status'] = status
        actuator_data['state'] = state

        #send data to thingsboard
        client_1.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)
        client_2.publish('v1/devices/me/telemetry', json.dumps(actuator_data), 1)
        #send data to local server
        publish.single("/gate/state", state, hostname=MQTT_SERVER)
        #time.sleep(2)

except KeyboardInterrupt:
    pass
client_1.loop_stop()
client_2.loop_stop()
local_client.loop_stop()
client_1.disconnect()
client_2.disconnect()
local_client.disconnect()
