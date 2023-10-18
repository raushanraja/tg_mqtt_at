import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, return_code):
    if return_code == 0:
        print("connected")
        client.publish("Test", "Hello World")
        while True:
            text = input("Enter a new text to send: ")
            if text:
                client.publish("Test", text)
    else:
        print("could not connect, return code:", return_code)


def on_message(client, userdata, message):
    try:
        print("Received message: " ,str(message.payload.decode("utf-8")))
    except:
        print("Error decoding received message")


broker_hostname ="localhost"
port = 1883 

client = mqtt.Client("Client1")
# client.username_pw_set(username="user_name", password="password") # uncomment if you use password auth
client.on_connect=on_connect
client.on_message=on_message

client.connect(broker_hostname, port) 
client.loop_start()

try:
    time.sleep(10)
finally:
    client.loop_forever()
