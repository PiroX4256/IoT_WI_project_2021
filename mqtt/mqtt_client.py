import yaml
from paho.mqtt import client as mqtt_client
from parse import *

with open('secrets.yaml', 'r') as s_file:
    constants = yaml.safe_load(s_file)

print(f'Server address: {constants["server_addr"]}')

broker = constants["server_addr"]
port = 1883
topic = "#"
client_id = "vechus_pirox_mqtt"
output_file_name = "dataset.dat"


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        result = parse("{}" + "|{}" * 6, msg.payload.decode())
        if result is not None:
            coords = result[0]
            payload = '|'.join(result[i] for i in range(1, 7))
            print("Write this into dataset...")
            line = msg.topic + '\t' + coords + '\t' + payload + '\n'
            with open(output_file_name, 'a+') as f:
                if not any(line == x.rstrip('\r\n') for x in f):
                    f.write(line)
                else:
                    print("Already there....")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
