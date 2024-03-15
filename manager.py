import paho.mqtt.client as mqtt
import json
import sqlite3
from mqtt_init import broker_ip, broker_port, username, password, sub_topic

# SQLite Database initialization
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS temperature_data
             (table_number INTEGER PRIMARY KEY, temperature REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS occupancy_data
             (table_number INTEGER PRIMARY KEY, is_occupied BOOLEAN)''')
c.execute('''CREATE TABLE IF NOT EXISTS light_data
             (table_number INTEGER PRIMARY KEY, is_on BOOLEAN)''')
c.execute('''CREATE TABLE IF NOT EXISTS ac_data
             (table_number INTEGER PRIMARY KEY, is_on BOOLEAN)''')
conn.commit()

# MQTT Client setup
client = mqtt.Client("SmartRestaurantManager")

# Callback function for MQTT message reception
def on_message(client, userdata, message):
    print("Received message:", message.payload.decode())
    topic = message.topic
    try:
        payload = json.loads(message.payload.decode())
    except:
        payload = ""

    if "tmp" in topic:
        handle_temperature(payload)
    if "occupied" in topic:
        handle_occupancy(payload)
    if "light" in topic:
        handle_light(payload)
    if "air_conditioner" in topic:
        handle_ac(payload)

# Function to handle temperature data
def handle_temperature(data):
    table_number = data["table_number"]
    temperature = float(data["temperature"])  # Convert to float
    ac_topic = "tables/air_conditioner"
    warning_topic = "tables/warning"
    threshold_temperature = 40  # Threshold temperature for warning

    print(f"Received temperature data for table {table_number}: {temperature}")

    # Update or insert into database
    c.execute("INSERT OR REPLACE INTO temperature_data VALUES (?, ?)", (table_number, temperature))
    conn.commit()

    # Check temperature threshold and control AC
    if temperature > threshold_temperature:
        print(f"Temperature for table {table_number} is above threshold, turning on AC.")
        message = f'{{"table_number": {table_number}, "is_on": {str(True).lower()}}}'
        client.publish(ac_topic, message)
        print("AC control message sent.")

        # Send warning message
        warning_message = f'Temperature for table {table_number} is above 40°C!'
        client.publish(warning_topic, warning_message)
        print("Warning message sent.")
    else:
        print(f"Temperature for table {table_number} is below threshold, turning off AC.")
        message = f'{{"table_number": {table_number}, "is_on": {str(False).lower()}}}'
        client.publish(ac_topic, message)
        print("AC control message sent.")

# Function to handle occupancy data
def handle_occupancy(data):
    table_number = data["table_number"]
    is_occupied = data["is_occupied"]
    occupancy_topic_send = "tables/light"
    if is_occupied:
        print(f"Table {table_number} is occupied, turning on light.")
        message = f'{{"table_number": {table_number}, "is_on": {str(True).lower()}}}'
        client.publish(occupancy_topic_send, message)
        print("Light control message sent.")
    else:
        print(f"Table {table_number} is unoccupied, turning off light.")
        message = f'{{"table_number": {table_number}, "is_on": {str(False).lower()}}}'
        client.publish(occupancy_topic_send, message)
        print("Light control message sent.")

    print(f"Received occupancy data for table {table_number}: {is_occupied}")
    # Update or insert into database
    c.execute("INSERT OR REPLACE INTO occupancy_data VALUES (?, ?)", (table_number, is_occupied))
    conn.commit()

# Function to handle light data
def handle_light(data):
    table_number = data["table_number"]
    is_on = data["is_on"]

    print(f"Received light data for table {table_number}: {is_on}")

    # Update or insert into database
    c.execute("INSERT OR REPLACE INTO light_data VALUES (?, ?)", (table_number, is_on))
    conn.commit()

# Function to handle air conditioner data
def handle_ac(data):
    table_number = data["table_number"]
    is_on = data["is_on"]

    print(f"Received AC data for table {table_number}: {is_on}")

    # Update or insert into database
    c.execute("INSERT OR REPLACE INTO ac_data VALUES (?, ?)", (table_number, is_on))
    conn.commit()

# Setup MQTT client callbacks
client.on_message = on_message

# Connect to MQTT broker
client.username_pw_set(username, password)
client.connect(broker_ip, int(broker_port))

# Subscribe to MQTT topics
client.subscribe(sub_topic)

# Start the MQTT loop
client.loop_forever()
