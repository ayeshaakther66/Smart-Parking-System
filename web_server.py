import time
from flask import Flask, render_template, request, redirect
import pymysql
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Dictionary of parking slot with name and element
gate = { 'state' : 0}
automate = { 'status' : 1}

slots = {
    1 : { 'name' : 'Parking Slot 1', 'state' : 1},
    2 : { 'name' : 'Parking Slot 2', 'state' : 0},
}

#MQTT
MQTT_SERVER = '172.20.10.3'

#local_client.on_message = on_message
#local_client.connect(MQTT_SERVER, 1883, 60)
#local_client.loop_start()
   
# Main function when accessing the website
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        maxTemp = request.form['content']
        updateMaxTemp(maxTemp)
        publish.single("/thermostat/threshold", str(maxTemp), hostname=MQTT_SERVER)
        return redirect('/')
    else:
        #This data wii be sent to index.html (pins dictionary)
        maxTemp = getMaxTemp()
        parkslot = getSlotsStatus()
        slots[1]['state'] = parkslot[0]
        slots[2]['state'] = parkslot[1]
        templateData = { 
                'automate' : automate,
                'gate' : gate,
                'slots' : slots,
                'maxTemp' : maxTemp,                            
                }
        
        # Pass the template data into the template index.html and return it
        return render_template('index.html', **templateData)

# Function with buttons that change depending on the status
@app.route("/<slot>/<state>")
def toggle_function(slot, state):
    # Convert the slot from the URL into an interger:
    slotName = slots[int(slot)]['name']

    parkslot = getSlotsStatus()
    slots[1]['state'] = parkslot[0]
    slots[2]['state'] = parkslot[1]

    #check if current slot is available
    if slots[int(slot)]['state'] != 0:
        #update the parking slot with new state
        slots[int(slot)]['state'] = int(state);
        publish.single("/slot/state", str(slot) + " " + str(state), hostname=MQTT_SERVER)
    #This data will be sent to index.html
    maxTemp = getMaxTemp()
    templateData = { 
        'automate' : automate,
        'gate' : gate,
        'slots' : slots,
        'maxTemp' : maxTemp,                            
         }
    
    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)

#Function to send simple commands
@app.route("/gate/<toggle>")
def action(toggle):
    gate['state'] = int(toggle);
    publish.single("/gate/order", toggle, hostname=MQTT_SERVER)
    #This data wii be sent to index.html (pins dictionary)
    maxTemp = getMaxTemp()
    parkslot = getSlotsStatus()
    slots[1]['state'] = parkslot[0]
    slots[2]['state'] = parkslot[1]

    templateData = { 
        'automate' : automate,
        'gate' : gate,
        'slots' : slots,
        'maxTemp' : maxTemp,                            
         }
    

    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)

#Change the automation of the website
@app.route("/automate/<toggle>")
def changeAutomate(toggle):

    automate['status'] = int(toggle);
    publish.single("/automate/toggle", toggle, hostname=MQTT_SERVER)

    maxTemp = getMaxTemp()
    parkslot = getSlotsStatus()
    slots[1]['state'] = parkslot[0]
    slots[2]['state'] = parkslot[1]

    templateData = { 
        'automate' : automate,
        'gate' : gate,
        'slots' : slots,
        'maxTemp' : maxTemp,                            
         }
    

    # Pass the template data into the template index.html and return it
    return render_template('index.html', **templateData)


def getMaxTemp():
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking')
        with dbConn:
            cursor = dbConn.cursor()
            sql = "SELECT `value` FROM `thresholds` WHERE `name`= %s"
            cursor.execute(sql, ('tempMax'))
            maxTemp = cursor.fetchone()[0]
            return maxTemp
    except Exception as e:
        print(e)
        return "N/a"

def getSlotsStatus():
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking')
        with dbConn:
            cursor = dbConn.cursor()
            sql = "SELECT `slot_1`, `slot_2` FROM `parkingSlot`"
            cursor.execute(sql)
            temp = cursor.fetchall()
            slots = temp[len(temp)-1]
            array = [0,0]
            if slots[0] == "AVAILABLE":
                array[0] = 1
            elif slots[0] == "BOOKED":
                array[0] = 2
            else:
                array[0] = 0

            if slots[1] == "AVAILABLE":
                array[1] = 1
            elif slots[1] == "BOOKED":
                array[1] = 2
            else:
                array[1] = 0
            print(array)
            return array
    except Exception as e:
        print(e)
        return "N/a"

def updateMaxTemp(maxT):
    try:
        dbConn = pymysql.connect(host = 'localhost', user='pi', password='', database='smart_parking')
        with dbConn:
            cursor = dbConn.cursor()
            sql = "UPDATE `thresholds` SET `value` = %s WHERE `name` = %s"
            cursor.execute(sql, (maxT, 'tempMax'))
            dbConn.commit()
            cursor.close()
    except Exception as e:
            print(e)

# Main function, set up serial bus, indicate port for the webserver,
# ans start the service.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 80, debug = True)
