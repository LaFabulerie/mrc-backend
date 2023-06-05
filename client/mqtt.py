from django.conf import settings

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    client.subscribe("mrc")

def on_message(client, userdata, msg):
    print(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print(f"Connecting to mqtt broker at {settings.MQTT_BROKER}")
client.connect(settings.MQTT_BROKER, 1883, 60)