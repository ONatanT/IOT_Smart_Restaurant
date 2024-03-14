import time
import paho.mqtt.client as mqtt
import random
from mqtt_init import *

class MqttEmulator:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.start_emulation()
        else:
            print("Failed to connect to broker")

    def start_emulation(self):
        while True:
            self.send_temperature_message()
            self.send_light_message()
            self.send_ac_message()
            self.send_presence_message()
            self.send_call_waiter_message()
            time.sleep(5)  # Adjust the interval as needed

    def send_temperature_message(self):
        table_number = random.randint(1, 9999)
        temperature = random.randint(10, 40)  # Random temperature between 10 to 40 degrees
        topic = "tables/tmp"
        message = f'{{"table_number": {table_number}, "temperature": {temperature}}}'
        print("Sending Temperature Message:", message)
        self.client.publish(topic, message)

    def send_light_message(self):
        table_number = random.randint(1, 9999)
        is_on = random.choice([True, False])  # Randomly choose between True or False
        topic = "tables/light"
        message = f'{{"table_number": {table_number}, "is_on": {str(is_on).lower()}}}'
        print("Sending Light Message:", message)
        self.client.publish(topic, message)

    def send_ac_message(self):
        table_number = random.randint(1, 9999)
        is_on = random.choice([True, False])  # Randomly choose between True or False
        topic = "tables/air_conditioner"
        message = f'{{"table_number": {table_number}, "is_on": {str(is_on).lower()}}}'
        print("Sending Air Conditioner Message:", message)
        self.client.publish(topic, message)

    def send_presence_message(self):
        table_number = random.randint(1, 9999)
        is_occupied = random.choice([True, False])  # Randomly choose between True or False
        topic = "tables/occupied"
        message = f'{{"table_number": {table_number}, "is_occupied": {str(is_occupied).lower()}}}'
        print("Sending Presence Message:", message)
        self.client.publish(topic, message)

    def send_call_waiter_message(self):
        table_number = random.randint(1, 9999)
        topic = "tables/waiter_call"
        message = f'{{"table_number": {table_number}, "request": "call_waiter"}}'
        print("Sending Call Waiter Message:", message)
        self.client.publish(topic, message)

if __name__ == "__main__":
    mqtt_emulator = MqttEmulator()
    while True:
        time.sleep(1)  # Keep the main thread running
