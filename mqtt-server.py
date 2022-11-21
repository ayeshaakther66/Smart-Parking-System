import paho.mqtt.client as mqtt
import threading
import time
import pymysql

MQTT_SERVER = '172.20.10.3'

def updateGateState(state):
    print("update gate state with state: " + state)
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking') or die("Could not connect")
        with dbConn:
            cursor = dbConn.cursor()
            sql = "INSERT INTO `gateState` (`state`) VALUE (%s)"
            cursor.execute(sql, (state))
            dbConn.commit
            cursor.close()
    except Exception as e:
        print(e)

def updateTemperature(value):
    print("update temperature with value: " + str(value))
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking') or die("Could not connect")
        with dbConn:
            cursor = dbConn.cursor()
            sql = "INSERT INTO `temperature` (`temperature`) VALUE (%s)"
            cursor.execute(sql, (value))
            dbConn.commit
            cursor.close()
    except Exception as e:
        print(e)

def updateParkingSlot(slot1, slot2):
    print("update parking slot 1: " + slot1 + " slot 2: " + slot2)
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking') or die("Could not connect")
        with dbConn:
            cursor = dbConn.cursor()
            sql = "INSERT INTO `parkingSlot` (`slot_1`, `slot_2`) VALUE (%s, %s)"
            cursor.execute(sql, (slot1, slot2))
            dbConn.commit
            cursor.close()
    except Exception as e:
        print(e)


def on_connect1(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("/gate/state")
    client.subscribe("/thermostat/temperature")
    client.subscribe("/parking/slot")
    client.subscribe("thermostat/threshold")

def on_message1(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    topic = msg.topic.split('/')
    target = topic[1]
    subtarget = topic[2]
    if target == "gate":
        value = str(msg.payload)
        UpdateGate = threading.Thread(target = updateGateState, args=(value,))
        UpdateGate.start()
    elif target == "thermostat":
        value = int(msg.payload)
        if subtarget == "temperature":
            UpdateTemp = threading.Thread(target = updateTemperature, args=(value,))
            UpdateTemp.start()
    elif target == "parking":
        slots = msg.payload.split()
        value1 = slots[0]
        value2 = slots[1]
        if subtarget == "slot":
            UpdateSlot = threading.Thread(target = updateParkingSlot, args=(value1, value2,))
            UpdateSlot.start()

try:
    client1 = mqtt.Client()
    client1.on_connect = on_connect1
    client1.on_message = on_message1

    client1.connect(MQTT_SERVER, 1883, 60)

    client1.loop_start()

    while True:
        print("do smth")
        time.sleep(2)
except Exception as e:
    print(e)
client1.disconnect()
client1.loop_stop()
