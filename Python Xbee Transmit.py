# Xbee Python Continuous Transmit

import time

# Define Xbee Device
from digi.xbee.devices import XBeeDevice
device = XBeeDevice("COM12", 115200) # Running at a faster baud rate
device.open() # Open serial coms

# Infinite loop
while True:
    # Get local time
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)

    # Send predetermined packet
    device.send_data_broadcast("Hello EEL4599!")
    
    # Print time sent
    print("Packet sent at:", result)
    
    # Wait 5 seconds
    time.sleep(5)

device.close()