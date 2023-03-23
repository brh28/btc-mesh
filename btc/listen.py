import time
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import sys
import pprint
import json

args = sys.argv

def onReceive(packet, interface): # called when a packet arrives
    # if 'decoded' in packet and 'payload' in packet['decoded']:
    if 'decoded' in packet and 'portnum' in packet['decoded'] and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
        print(f"Received: {packet['decoded']['payload'].decode('utf-8')}")
    # print(packet['portnum'])
    # print(packet['decoded']['payload']) 
    # print(f"Received: {repr(packet)}")
    # if (packet['decode']):
    #     print(f"Received: {packet}")

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    interface.sendText(f"Connected to device: {args[1]}") # defaults to broadcast, specify a destination ID if you wish


pub.subscribe(onReceive, "meshtastic.receive") # could use meshtastic.receive.data.portnum to listen for specific events
# pub.subscribe(onConnection, "meshtastic.connection.established")

# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface(devPath=str(args[1]))

while True:
    time.sleep(1000)
