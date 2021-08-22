#!/usr/bin/python

"""
https://www.raspberry-pi-geek.com/Archive/2017/22/The-BH1750-Digital-Light-Sensor
http://www.pibits.net/code/raspberry-pi-bh1750-light-sensor.php
"""

from config.google_form import bh1750_get_google_form_url
from datetime import datetime
import os
import smbus
import time

DEVICE = 0x23  # default I2C state
POWER_DOWN = 0x00  # no active state
POWER_UP = 0x01  # power on
RESET = 0x07  # reset data register value
ONE_TIME_HIGH_RES_MODE = 0x20

SLEEP_TIME = 10
DEVICE_ID = os.system("cat /sys/firmware/devicetree/base/serial-number")

bus = smbus.SMBus(1)


def save_to_google_form(reading):
    bh1750_get_google_form_url(str(datetime.now()), DEVICE_ID, value)
    print(f"saved to google form - value : {reading}")


def main():
    while True:
        data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGH_RES_MODE)
        value = (data[1] + (256 * data[0])) / 1.2
        save_to_google_form(value)
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
