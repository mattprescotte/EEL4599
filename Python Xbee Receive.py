# Xbee Python Continuous Receive

import time

# Define Xbee device
from digi.xbee.devices import XBeeDevice
device = XBeeDevice("COM13", 115200) # Running at a faster baud rate
device.open() # Open serial coms

# Define callback for message interrupts (no polling required)
def my_data_received_callback(xbee_message):
    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")
    print("Received data from %s: %s" % (address, data))

# Add callback
device.add_data_received_callback(my_data_received_callback)

# Infinite loop
while True:
    time.sleep(0.1)

device.close()