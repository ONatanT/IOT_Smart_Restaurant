# mqtt_sender.py
import sys
import paho.mqtt.client as mqtt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QSpinBox, QHBoxLayout, QDockWidget
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

        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        layout.addWidget(QLabel("Table Number:"))
        layout.addWidget(self.table_number_input)

        self.temperature_input = QSpinBox()
        self.temperature_input.setMinimum(1)
        self.temperature_input.setMaximum(9999)
        self.temperature_input.setValue(25)
        layout.addWidget(QLabel("Temperature:"))
        layout.addWidget(self.temperature_input)

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

        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        layout.addWidget(QLabel("Table Number:"))
        layout.addWidget(self.table_number_input)

        self.send_on_button = QPushButton("Send Light ON")
        self.send_on_button.clicked.connect(lambda: self.send_light_message(True))
        layout.addWidget(self.send_on_button)

        self.send_off_button = QPushButton("Send Light OFF")
        self.send_off_button.clicked.connect(lambda: self.send_light_message(False))
        layout.addWidget(self.send_off_button)

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

        self.table_number_input = QSpinBox()
        self.table_number_input.setMinimum(1)
        self.table_number_input.setMaximum(9999)
        layout.addWidget(QLabel("Table Number:"))
        layout.addWidget(self.table_number_input)

        self.send_on_button = QPushButton("Send AC ON")
        self.send_on_button.clicked.connect(lambda: self.send_ac_message(True))
        layout.addWidget(self.send_on_button)

        self.send_off_button = QPushButton("Send AC OFF")
        self.send_off_button.clicked.connect(lambda: self.send_ac_message(False))
        layout.addWidget(self.send_off_button)

        widget.setLayout(layout)
        self.setWidget(widget)

    def send_ac_message(self, is_on):
        table_number = self.table_number_input.value()
        topic = "tables/air_conditioner"
        message = f'{{"table_number": {table_number}, "is_on": {str(is_on).lower()}}}'
        print("Sending Air Conditioner Message:", message)
        mqtt_sender.client.publish(topic, message)


class MqttSender(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MQTT Message Sender")
        self.setGeometry(300, 300, 300, 200)

        # Central Widget
        central_layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Create instances of dock widgets
        self.temperature_dock = TemperatureDock()
        self.light_dock = LightDock()
        self.ac_dock = AirConditionerDock()

        # Add dock widgets to the layout
        central_layout.addWidget(self.temperature_dock)
        central_layout.addWidget(self.light_dock)
        central_layout.addWidget(self.ac_dock)

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
