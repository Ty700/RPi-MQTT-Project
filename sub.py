import paho.mqtt.client as mqtt
import random
import hashlib
import time

topics = [('system/plant/soilinfo', 0),
          ('system/pump/waterinfo', 0)]
clientID = f"rpi{random.randint(0,100)}"
broker = "broker.emqx.io"
port = 1883

def hash_password(input):
    return (hashlib.md5(input.encode()).hexdigest() == '051ebc83e3617c4304d6f5ba51d2cc75')

def login():
    user_input = input("Enter password: ")
    return hash_password(user_input)

def connect() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to {broker}")

    print("Creating new instance")
    client = mqtt.Client(clientID)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, message):
    print(f"Message received at {time.strftime('%Y-%m-%d %H:%M:%S')}:", str(message.payload.decode("utf-8")))
    print("Message topic =", message.topic)
    print("")

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to Topics: ", end="")
    for i in range(len(topics)):
        if i < len(topics) - 1:
            print(f'{topics[i][0]}, ', end="")
        else:
            print(f'{topics[i][0]}')

def subscribe(client: mqtt):
    client.subscribe(topics)
    client.on_subscribe = on_subscribe
    client.on_message = on_message

def main():
    if login():
        client = connect()
        subscribe(client)
        client.loop_forever()
    else:
        print('Wrong password')

if __name__ == '__main__':
    main()
