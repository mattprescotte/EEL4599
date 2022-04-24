# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
import threading
import requests

# The serial port where the local module is connected to.
PORT = "COM12"
# The baud rate of the local module.
BAUD_RATE = 115200
# Name of remote XBee.
REMOTE_NODE_ID = "XBEE_B"

# Analog inputs
AD2 = IOLine.DIO2_AD2 # IEFSR w/ 10k Pull-down
AD3 = IOLine.DIO3_AD3 # TMP36 Temperature Sensor

# Analog voltage reference (here, VDD)
VREF = 3300


def main():
    print(" +--------------------------------------------+")
    print(" | XBee Python Library Read Remote ADC Sample |")
    print(" +--------------------------------------------+\n")

    stop = False
    th = None

    # Instantiate local XBee
    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        local_device.open()

        # Obtain the remote XBee device from the XBee network.
        xbee_network = local_device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)
            
        # Obtain remote device address
        remote_addr = remote_device.get_64bit_addr()         
            
        # Set AD2 & AD3 as ADC inputs
        remote_device.set_io_configuration(AD2, IOMode.ADC)
        remote_device.set_io_configuration(AD3, IOMode.ADC)

        def read_task():
            while not stop:
                # Read the analog value from the remote input lines.
                ad2_counts = remote_device.get_adc_value(AD2)
                ad3_counts = remote_device.get_adc_value(AD3)
                
                # Convert ADC3 counts to temperature
                ad3_volts = ad3_counts * (VREF / 1024.0)
                temperature = (ad3_volts - 500) / 10
                
                # Convert ADC2 counts to weight
                ad2_volts = ad2_counts * (VREF / 1024.0)
                weight = (ad2_volts) * 10
                
                # Get RSSI of devices
                #rssi_raw = local_device.ddo_get_param(None, 'DB')
                #rssi_val = struct.unpack('=B', rssi_raw)
                
                # Print values
                roundedTemp = float('%.5g' % temperature)
	            roundedPres = float('%.5g' % weight)
                print(str(roundedTemp) + " C, " + str(roundedPres) + " g")
                #print("%0.2f C, %0.2f g, %d dBm" % (temperature, weight, rssi_val))
                
                #Input request to thingspeak
                requestLink = "http://api.thingspeak.com/update?api_key=8O0PFDFMUYX0ARAN&field1=" + str(roundedTemp) + "&field2=" + str(roundedPres)
                requests.get(requestLink)
                
                time.sleep(1)

        th = threading.Thread(target = read_task)

        time.sleep(0.5)
        th.start()

        input()

    finally:
        stop = True
        if th is not None and th.isAlive():
            th.join()
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == '__main__':
    main()
