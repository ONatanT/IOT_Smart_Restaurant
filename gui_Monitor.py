# gui_monitor.py
import sys
import random
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import socket
import json
import  bisect

# Import MQTT initialization parameters from mqtt_init.py
from mqtt_init import *

# Global variables
table_temperatures = {}
table_lights = {}
table_air_conditioners = {}
table_waiter_calls = {}
table_presence = {}

class Mqtt_client(QtCore.QObject):
    temperature_updated = QtCore.pyqtSignal(int, int)
    light_updated = QtCore.pyqtSignal(int, bool)
    air_conditioner_updated = QtCore.pyqtSignal(int, bool)
    waiter_call_received = QtCore.pyqtSignal(int)
    table_presence_updated = QtCore.pyqtSignal(int, bool)

    def __init__(self):
        super().__init__()

        # Creating unique client name
        r = random.randrange(1, 10000000)
        self.clientname = "IOT_client-Id-" + str(r)
        
        # Initializing MQTT parameters
        self.broker = broker_ip
        self.port = int(broker_port)
        self.username = username
        self.password = password
        self.temperature_topic = "tables/tmp"
        self.light_topic = "tables/light"
        self.air_conditioner_topic = "tables/air_conditioner"
        self.waiter_call_topic = "tables/waiter_call"
        self.table_presence_topic = "tables/occupied"

        # Creating MQTT client instance
        self.client = mqtt.Client(self.clientname, clean_session=True)
        self.client.username_pw_set(self.username, self.password)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        # Initialize sorted table numbers list
        self.sorted_table_numbers = []

        # Connect signals to slots
        self.temperature_updated.connect(self.update_temperature_slot)
        self.light_updated.connect(self.update_light_slot)
        self.air_conditioner_updated.connect(self.update_air_conditioner_slot)
        self.waiter_call_received.connect(self.receive_waiter_call_slot)
        self.table_presence_updated.connect(self.update_table_presence_slot)
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
            self.client.subscribe(sub_topic, 0)
        else:
            print("Bad connection. Returned code=", rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("Disconnected from broker. Result code: ", str(rc))
            
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = str(msg.payload.decode("utf-8", "ignore"))
        print("Message from:", topic, payload)
        try:
            data = json.loads(payload)
            if topic == self.temperature_topic:
                table_number = data["table_number"]
                temperature = data["temperature"]
                self.temperature_updated.emit(table_number, temperature)
            elif topic == self.light_topic:
                table_number = data["table_number"]
                is_on = data["is_on"]
                self.light_updated.emit(table_number, is_on)
            elif topic == self.air_conditioner_topic:
                table_number = data["table_number"]
                is_on = data["is_on"]
                self.air_conditioner_updated.emit(table_number, is_on)
            elif topic == self.waiter_call_topic:
                table_number = data["table_number"]
                self.waiter_call_received.emit(table_number)
            elif topic == self.table_presence_topic:
                table_number = data["table_number"]
                is_occupied = data["is_occupied"]
                self.table_presence_updated.emit(table_number, is_occupied)
        except json.JSONDecodeError:
            print("Invalid JSON format")
        except KeyError as e:
            print(f"Missing key: {str(e)}")

    def connect_to_broker(self):
        print("Connecting to broker ", self.broker)
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        
    def disconnect_from_broker(self):
        self.client.disconnect()
        self.client.loop_stop()

    @QtCore.pyqtSlot(int, int)
    def update_temperature_slot(self, table_number, temperature):
        if table_number in table_temperatures:
            table_temperatures[table_number].setText(f"Table: {table_number}, Temperature: {temperature} °C")
        else:
            print(f"Table {table_number} does not exist in GUI dock. Adding it now.")
            mainwin.TemperatureDock.add_table_to_dock(table_number, temperature)

    @QtCore.pyqtSlot(int, bool)
    def update_light_slot(self, table_number, is_on):
        if table_number in table_lights:
            label = table_lights[table_number]
            label.setText(f"Table: {table_number}, Light: {'On' if is_on else 'Off'}")
            if is_on:
                label.setStyleSheet("color: green;")
            else:
                label.setStyleSheet("color: red;")
        else:
            print(f"Table {table_number} does not exist in GUI dock. Adding it now.")
            mainwin.lightDock.add_table_to_dock(table_number, is_on)

    @QtCore.pyqtSlot(int, bool)
    def update_air_conditioner_slot(self, table_number, is_on):
        if table_number in table_air_conditioners:
            label = table_air_conditioners[table_number]
            label.setText(f"Table: {table_number}, AC: {'On' if is_on else 'Off'}")
            if is_on:
                label.setStyleSheet("color: green;")
            else:
                label.setStyleSheet("color: red;")
        else:
            print(f"Table {table_number} does not exist in GUI dock. Adding it now.")
            mainwin.airConditionerDock.add_table_to_dock(table_number, is_on)

    @QtCore.pyqtSlot(int)
    def receive_waiter_call_slot(self, table_number):
        print(f"Waiter call received from table {table_number}")
        if table_number in table_waiter_calls:
            # Remove the button only if it's present in the dock
            button = table_waiter_calls[table_number]
            button.deleteLater()
            del table_waiter_calls[table_number]
            mainwin.waiterCallDock.mc.sorted_table_numbers.remove(table_number)
        else:
            print(f"Table {table_number} does not exist in waiter call dock. Adding it now.")
            mainwin.waiterCallDock.add_table_to_dock(table_number)

    @QtCore.pyqtSlot(int, bool)
    def update_table_presence_slot(self, table_number, is_occupied):
        if is_occupied:
            if table_number not in table_presence:
                print(f"Table {table_number} is occupied.")
                mainwin.presenceDock.add_table_to_dock(table_number)
        else:
            if table_number in table_presence:
                print(f"Table {table_number} is vacant.")
                mainwin.presenceDock.remove_table_from_dock(table_number)

class TemperatureDock(QDockWidget):
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.connect_to_broker()
        
        self.setWindowTitle("Temperature Sensors")
        self.setStyleSheet("background-color: white")
        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.sorted_table_numbers = []

    def add_table_to_dock(self, table_number, temperature):
        widget = QWidget()
        label = QLabel(f"Table: {table_number}, Temperature: {temperature} °C")
        label.setAlignment(Qt.AlignCenter)
        widget_layout = QVBoxLayout(widget)
        widget_layout.addWidget(label)

        if table_number not in self.sorted_table_numbers:
            self.sorted_table_numbers.append(table_number)
            self.sorted_table_numbers.sort()

        index = self.sorted_table_numbers.index(table_number)
        self.layout.insertWidget(index, widget)

        table_temperatures[table_number] = label

class LightDock(QDockWidget):
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        
        self.setWindowTitle("Light Sensors")
        self.setStyleSheet("background-color: white")
        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.sorted_table_numbers = []

    def add_table_to_dock(self, table_number, is_on):
        widget = QWidget()
        label = QLabel(f"Table: {table_number}, Light: {'On' if is_on else 'Off'}")
        label.setAlignment(Qt.AlignCenter)
        widget_layout = QVBoxLayout(widget)
        widget_layout.addWidget(label)

        if is_on:
            label.setStyleSheet("color: green;")
        else:
            label.setStyleSheet("color: red;")
        
        if table_number not in self.sorted_table_numbers:
            self.sorted_table_numbers.append(table_number)
            self.sorted_table_numbers.sort()

        index = self.sorted_table_numbers.index(table_number)
        self.layout.insertWidget(index, widget)

        table_lights[table_number] = label

class AirConditionerDock(QDockWidget):
    def __init__(self, mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        
        self.setWindowTitle("Air Conditioner Sensors")
        # self.setStyleSheet("background-color: white")
        self.setStyleSheet("QDockWidget { background-color: #f0f0f0; border: 1px solid #ccc; }")

        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.sorted_table_numbers = []

    def add_table_to_dock(self, table_number, is_on):
        widget = QWidget()
        label = QLabel(f"Table: {table_number}, AC: {'On' if is_on else 'Off'}")
        label.setAlignment(Qt.AlignCenter)
        widget_layout = QVBoxLayout(widget)
        widget_layout.addWidget(label)

        if is_on:
            label.setStyleSheet("color: green;")
        else:
            label.setStyleSheet("color: red;")

        if table_number not in self.sorted_table_numbers:
            self.sorted_table_numbers.append(table_number)
            self.sorted_table_numbers.sort()

        index = self.sorted_table_numbers.index(table_number)
        self.layout.insertWidget(index, widget)

        table_air_conditioners[table_number] = label

class WaiterCallDock(QDockWidget):
    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc

        self.setWindowTitle("Waiter Calls")
        self.setStyleSheet("background-color: white")
        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.mc.waiter_call_received.connect(self.add_table_to_dock)


    def add_table_to_dock(self, table_number):
        print(f"Waiter call received from table {table_number}")
        if table_number in table_waiter_calls:
            print(f"Table {table_number} already exists in waiter call dock.")
        else:
            button = QPushButton(f"Table {table_number} - Call Dismissed")
            button.clicked.connect(lambda: self.dismiss_call(table_number))

            index = bisect.bisect_left(self.mc.sorted_table_numbers, table_number)
            self.layout.insertWidget(index, button)

            table_waiter_calls[table_number] = button
            self.mc.sorted_table_numbers.append(table_number)
            self.mc.sorted_table_numbers.sort()

    def dismiss_call(self, table_number):
        print(f"Dismissed waiter call from table {table_number}")
        if table_number in table_waiter_calls:
            button = table_waiter_calls[table_number]
            button.deleteLater()
            del table_waiter_calls[table_number]
            self.mc.sorted_table_numbers.remove(table_number)
        else:
            print(f"Table {table_number} does not exist in waiter call dock.")

class PresenceDock(QDockWidget):
    def __init__(self, mc):
        QDockWidget.__init__(self)

        self.mc = mc

        self.setWindowTitle("Table Presence")
        self.setStyleSheet("background-color: white")
        self.central_widget = QWidget()
        self.setWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

    def add_table_to_dock(self, table_number):
        label = QLabel(f"Table {table_number} - Occupied")

        index = bisect.bisect_left(self.mc.sorted_table_numbers, table_number)
        self.layout.insertWidget(index, label)

        table_presence[table_number] = label
        self.mc.sorted_table_numbers.append(table_number)
        self.mc.sorted_table_numbers.sort()

    def remove_table_from_dock(self, table_number):
        if table_number in table_presence:
            label = table_presence[table_number]
            label.deleteLater()
            del table_presence[table_number]
            self.mc.sorted_table_numbers.remove(table_number)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
                
        # Init of Mqtt_client class
        self.mc = Mqtt_client()
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # Set up main window
        self.setGeometry(700, 300, 450, 550)
        self.setWindowTitle('Restaurant Hub')

        # Init QDockWidget objects
        self.TemperatureDock = TemperatureDock(self.mc)
        self.lightDock = LightDock(self.mc)
        self.airConditionerDock = AirConditionerDock(self.mc)
        self.waiterCallDock = WaiterCallDock(self.mc)
        self.presenceDock = PresenceDock(self.mc)

        # Add docks to main window
        self.addDockWidget(Qt.LeftDockWidgetArea, self.TemperatureDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.lightDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.airConditionerDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.waiterCallDock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.presenceDock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()
    sys.exit(app.exec_())
