import paho.mqtt.client as mqtt
import json
import sqlite3
from mqtt_init import broker_ip, broker_port, username, password, sub_topic

# SQLite Database initialization
conn = sqlite3.connect('restaurant.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS temperature_data
             (table_number INTEGER, temperature REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS occupancy_data
             (table_number INTEGER, is_occupied BOOLEAN)''')
conn.commit()

# MQTT Client setup
client = mqtt.Client("SmartRestaurantManager")

# Callback function for MQTT message reception
def on_message(client, userdata, message):
    print("Received message:", message.payload.decode())
    topic = message.topic
    payload = json.loads(message.payload.decode())

    if "tmp" in topic:
        handle_temperature(payload)
    if "occupied" in topic:
        handle_occupancy(payload)


# Function to handle temperature data
def handle_temperature(data):
    table_number = data["table_number"]
    temperature = data["temperature"]
    ac_topic = "tables/air_conditioner"

    print(f"Received temperature data for table {table_number}: {temperature}")

    # Update database
    c.execute("INSERT INTO temperature_data VALUES (?, ?)", (table_number, temperature))
    conn.commit()

    # Check temperature threshold and control AC
    if temperature > threshold_temperature:
        print(f"Temperature for table {table_number} is above threshold, turning on AC.")
        message = f'{{"table_number": {table_number}, "is_on": {str(True).lower()}}}'
        client.publish(ac_topic, message)
        print("AC control message sent.")
    else:
        print(f"Temperature for table {table_number} is below threshold, turning off AC.")
        message = f'{{"table_number": {table_number}, "is_on": {str(False).lower()}}}'
        client.publish(ac_topic, message)
        print("AC control message sent.")


# Function to handle occupancy data
def handle_occupancy(data):
    print(f"{data=}")
    table_number = data["table_number"]
    is_occupied = data["is_occupied"]
    occupancy_topic_send = "tables/light"


    print(f"Received occupancy data for table {table_number}: {is_occupied}")

    # Update database
    c.execute("INSERT INTO occupancy_data VALUES (?, ?)", (table_number, is_occupied))
    conn.commit()

    # Control light based on occupancy
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


# Setup MQTT client callbacks
client.on_message = on_message

# Connect to MQTT broker
client.username_pw_set(username, password)
client.connect(broker_ip, int(broker_port))

# Subscribe to MQTT topics
client.subscribe(sub_topic)

# Set temperature threshold
threshold_temperature = 25  # Example threshold temperature

# Start the MQTT loop
client.loop_forever()
