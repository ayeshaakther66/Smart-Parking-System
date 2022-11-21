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
ACCESS_TOKEN_1 = '0boFAe72kOFDtJiGkGa4'
ACCESS_TOKEN_2 = 'XMPt6XpnaMF85BA5Crzm'
ACCESS_TOKEN_3 = 'sSkj4iRRTXzWnrc5oQVU'
ACCESS_TOKEN_4 = 'icBC6hmdxVFjWockpbOY'

sensor_data_1 = {'status': 'Empty'}
sensor_data_2 = {'status': 'Empty'}
actuator_data_1 = {'state': 'Green'}
actuator_data_2 = {'state': 'Green'}

client_1 = mqtt.Client()
client_2 = mqtt.Client()
client_3 = mqtt.Client()
client_4 = mqtt.Client()
local_client = mqtt.Client()

client_1.username_pw_set(ACCESS_TOKEN_1)
client_2.username_pw_set(ACCESS_TOKEN_2)
client_3.username_pw_set(ACCESS_TOKEN_3)
client_4.username_pw_set(ACCESS_TOKEN_4)

def book1():
    arduino.write(b"0")    
def cancel1():
    arduino.write(b"1")
def book2():
    arduino.write(b"2")
def cancel2():
    arduino.write(b"3")

#setup subscriber
def on_message(client, userdata, msg):
    print('Topic' + msg.topic + '\nMessage: ' + str(msg.payload))
    topic = msg.topic.split('/')
    target = topic[1]
    value = msg.payload.split()
    slot = int(value[0])
    status = int(value[1])
    if target == "slot":
        if slot == 1:
            if status == 1:
                cancel1()
            elif status == 2:
                book1()
        elif slot == 2:
            if status == 1:
                cancel2()
            elif status == 2:
                book2()

def on_connect(client, userdata, flags, rc):
    print("connect to local mqtt server: result " + str(rc))
    client.subscribe("/parking/automate")
    client.subscribe("/slot/state")

local_client.on_connect = on_connect
local_client.on_message = on_message

#connect using default mqtt port and 60 seconds keepalive interval
client_1.connect(THINGSBOARD_HOST, 1883, 60)
client_2.connect(THINGSBOARD_HOST, 1883, 60)
client_3.connect(THINGSBOARD_HOST, 1883, 60)
client_4.connect(THINGSBOARD_HOST, 1883, 60)
local_client.connect(MQTT_SERVER, 1883, 60)

client_1.loop_start()
client_2.loop_start()
client_3.loop_start()
client_4.loop_start()
local_client.loop_start()
try:
    while True:
        #this is fake data you can change to arduino data
        line = arduino.readline()
        array = line.split()
        status_1 = array[0]
        status_2 = array[1]
        if status_1 == "DETECTED":
            state1 = "TAKEN"
        else:
            state1= "AVAILABLE"
            
        if status_2 == "DETECTED":
            state2 = "TAKEN"
        else:
            state2= "AVAILABLE"
        
        
        print("Parking spot 1: " + status_1 + " " + "Light state: " + state1 + "\n" + "Parking spot 2: " + status_2 + " "+ "Light state: " + state2 + "\n"  )
        sensor_data_1['status'] = status_1
        sensor_data_2['status'] = status_2
        actuator_data_1['state'] = state1
        actuator_data_2['state'] = state2

        #send data to thingsboard
        client_1.publish('v1/devices/me/telemetry', json.dumps(sensor_data_1), 1)
        client_2.publish('v1/devices/me/telemetry', json.dumps(sensor_data_2), 1)
        client_3.publish('v1/devices/me/telemetry', json.dumps(actuator_data_1), 1)
        client_4.publish('v1/devices/me/telemetry', json.dumps(actuator_data_2), 1)
        #send data to local server
        publish.single("/parking/slot", str(state1) + " " + str(state2), hostname=MQTT_SERVER)
    
except Exception as e:
    print(e)
client_1.loop_stop()
client_2.loop_stop()
client_3.loop_stop()
client_4.loop_stop()
local_client.loop_stop()
client_1.disconnect()
client_2.disconnect()
client_3.disconnect()
client_4.disconnect()
local_client.disconnect()
