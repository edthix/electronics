"""
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
"""

from time import sleep
import adafruit_dht
import board

# Initial the dht device, with data pin connected to:
dht_device = adafruit_dht.DHT22(board.D4) # GPIO4

for i in range(20):
    sleep(2)
    temp = dht_device.temperature
    print(temp)
