# mqtt_data_collector.py
# Skrypt do pobierania danych z MQTT i zapisywania ich do pliku CSV
# MQTT data collector script saving data to CSV file

import paho.mqtt.client as mqtt
import csv
from datetime import datetime

#  MQTT connection details / Dane dostepowe do serwera MQTT
BROKER = "your_broker_address"       # e.g. "mqtt.example.com" or IP address
PORT = 1883                          # usually 1883 for unencrypted connection
USERNAME = "your_username"            # your MQTT username
PASSWORD = "your_password"            # your MQTT password
TOPIC = "if0754/#"                   # topic pattern to subscribe, e.g. "if0754/#"

#  Output CSV file name / Nazwa pliku CSV do zapisu
CSV_FILE = "mqtt_data_new.csv"

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with code: " + str(rc))
    client.subscribe(TOPIC)

# Callback when a message is received
def on_message(client, userdata, msg):
    timestamp = datetime.now().isoformat()
    topic = msg.topic
    value = msg.payload.decode(errors="ignore")

    print(f"{timestamp} | {topic}  {value}")

    # Append message to CSV file
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, topic, value])

# Create MQTT client and configure callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker and start listening
client.connect(BROKER, PORT, 60)
client.loop_start()

# Now the script will run in background and save incoming MQTT messages to CSV
# You can also manually send commands, for example:
# client.publish("if0754/fca/cmd", "out3=1")

