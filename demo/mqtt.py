from paho.mqtt import client as mqtt_client


broker = '192.168.0.137'
port = 1883
topic = "/foo"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


client = mqtt_client.Client()
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()