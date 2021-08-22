#!/usr/bin/python

"""
https://www.uugear.com/portfolio/using-light-sensor-module-with-raspberry-pi
https://gpiozero.readthedocs.io/en/stable/api_input.html?highlight=ldr#lightsensor-ldr
"""

from config.google_form import ldr_get_google_form_url
from datetime import datetime
import os
import requests
import time
from gpiozero import LightSensor

SLEEP_TIME = 6
DEVICE_ID = os.popen("cat /sys/firmware/devicetree/base/serial-number").read()
ldr = LightSensor(4) # GPIO4 / Pin 7


def save_to_google_form(reading):
    r = requests.get(ldr_get_google_form_url(str(datetime.now()), DEVICE_ID, reading))
    print(f"saved to google form - value : {reading}, status : {r.status_code}")

def main():
    while True:
        value = ldr.value
        save_to_google_form(value)
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
