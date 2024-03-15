import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QSpinBox, QDockWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from mqtt_init import *

class TemperatureDock(QDockWidget):
    def __init__(self):
        super().__init__("Temperature")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        self.table_label = QLabel("Table Number:")
        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_number_input)
        layout.addLayout(table_layout)

        temp_layout = QHBoxLayout()
        self.temp_label = QLabel("Temperature:")
        self.temperature_input = QSpinBox()
        self.temperature_input.setMinimum(1)
        self.temperature_input.setMaximum(9999)
        self.temperature_input.setValue(25)
        temp_layout.addWidget(self.temp_label)
        temp_layout.addWidget(self.temperature_input)
        layout.addLayout(temp_layout)

        send_button = QPushButton("Send Temperature")
        send_button.clicked.connect(self.send_temperature_message)
        layout.addWidget(send_button)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_temperature_message(self):
        table_number = self.table_number_input.value()
        temperature = self.temperature_input.value()
        topic = "tables/tmp"
        message = f'{{"table_number": {table_number}, "temperature": {temperature}}}'
        print("Sending Temperature Message:", message)
        mqtt_sender.client.publish(topic, message)


class LightDock(QDockWidget):
    def __init__(self):
        super().__init__("Light")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        self.table_label = QLabel("Table Number:")
        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_number_input)
        layout.addLayout(table_layout)

        button_layout = QHBoxLayout()
        self.send_on_button = QPushButton("Send Light ON")
        self.send_on_button.clicked.connect(lambda: self.send_light_message(True))
        button_layout.addWidget(self.send_on_button)

        self.send_off_button = QPushButton("Send Light OFF")
        self.send_off_button.clicked.connect(lambda: self.send_light_message(False))
        button_layout.addWidget(self.send_off_button)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_light_message(self, is_on):
        table_number = self.table_number_input.value()
        topic = "tables/light"
        message = f'{{"table_number": {table_number}, "is_on": {str(is_on).lower()}}}'
        print("Sending Light Message:", message)
        mqtt_sender.client.publish(topic, message)


class AirConditionerDock(QDockWidget):
    def __init__(self):
        super().__init__("Air Conditioner")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        self.table_label = QLabel("Table Number:")
        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_number_input)
        layout.addLayout(table_layout)

        button_layout = QHBoxLayout()
        self.send_on_button = QPushButton("Send AC ON")
        self.send_on_button.clicked.connect(lambda: self.send_ac_message(True))
        button_layout.addWidget(self.send_on_button)

        self.send_off_button = QPushButton("Send AC OFF")
        self.send_off_button.clicked.connect(lambda: self.send_ac_message(False))
        button_layout.addWidget(self.send_off_button)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_ac_message(self, is_on):
        table_number = self.table_number_input.value()
        topic = "tables/air_conditioner"
        message = f'{{"table_number": {table_number}, "is_on": {str(is_on).lower()}}}'
        print("Sending Air Conditioner Message:", message)
        mqtt_sender.client.publish(topic, message)


class PresenceDock(QDockWidget):
    def __init__(self):
        super().__init__("Presence")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        self.table_label = QLabel("Table Number:")
        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_number_input)
        layout.addLayout(table_layout)

        button_layout = QHBoxLayout()
        self.send_occupied_button = QPushButton("Send Occupied")
        self.send_occupied_button.clicked.connect(lambda: self.send_presence_message(True))
        button_layout.addWidget(self.send_occupied_button)

        self.send_not_occupied_button = QPushButton("Send Not Occupied")
        self.send_not_occupied_button.clicked.connect(lambda: self.send_presence_message(False))
        button_layout.addWidget(self.send_not_occupied_button)
        layout.addLayout(button_layout)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_presence_message(self, is_occupied):
        table_number = self.table_number_input.value()
        topic = "tables/occupied"
        message = f'{{"table_number": {table_number}, "is_occupied": {str(is_occupied).lower()}}}'
        print("Sending Presence Message:", message)
        mqtt_sender.client.publish(topic, message)


class CallWaiterDock(QDockWidget):
    def __init__(self):
        super().__init__("Call Waiter")
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        table_layout = QHBoxLayout()
        self.table_label = QLabel("Table Number:")
        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        table_layout.addWidget(self.table_label)
        table_layout.addWidget(self.table_number_input)
        layout.addLayout(table_layout)

        self.call_waiter_button = QPushButton("Call a Waiter")
        self.call_waiter_button.clicked.connect(self.send_call_waiter_message)
        layout.addWidget(self.call_waiter_button)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_call_waiter_message(self):
        table_number = self.table_number_input.value()
        topic = "tables/waiter_call"
        message = f'{{"table_number": {table_number}, "request": "call_waiter"}}'
        print("Sending Call Waiter Message:", message)
        mqtt_sender.client.publish(topic, message)


class MqttSender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MQTT Message Sender")
        self.setGeometry(300, 300, 300, 200)

        # Create instances of dock widgets
        self.temperature_dock = TemperatureDock()
        self.light_dock = LightDock()
        self.ac_dock = AirConditionerDock()
        self.presence_dock = PresenceDock()
        self.call_waiter_dock = CallWaiterDock()

        # Add dock widgets to the main window
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.temperature_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.light_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.ac_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.presence_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.call_waiter_dock)

        # Connect to MQTT broker
        self.client = mqtt.Client()
        self.client.username_pw_set(username, password)
        self.client.on_connect = self.on_connect
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to broker")
        else:
            print("Failed to connect to broker")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mqtt_sender = MqttSender()
    mqtt_sender.show()
    sys.exit(app.exec_())
