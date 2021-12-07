#!/usr/bin/python

"""
ref1 : https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

1. Get DHT on GPIO4
2. Send to favoriot
3. If temperature > MAX_TEMP send to telegram
"""

from requests.structures import CaseInsensitiveDict
import adafruit_dht
import board
import json
import random
import requests
import telegram
import time
import RPi.GPIO as GPIO

# ********************************************************************************
# Configurations change here
# ********************************************************************************
api_url = "https://apiv2.favoriot.com/v2/streams"
device_developer_id = "deviceDefault@ruzainah"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJ1emFpbmFoIiwicmVhZF93cml0ZSI6dHJ1ZSwiaWF0IjoxNjM3OTEzNzk4fQ.5X1wPDtf663_QEFh13gPeITquaJmK0xioi5eTX2Jtw0"

bot_secret_key = "2105205678:AAEsYZm13kP9asseyAZBT4CgqjCjXXVW8ZI"
telegram_channel_id = "-1001722314638"
telegram_text = "PANAS!!!"

max_temp = 24  # change accordingly to send to telegram

sleep_time = 2  # number of seconds to sleep before processing
# ********************************************************************************
# End of configurations
# ********************************************************************************


# initiate our telegram bot
bot = telegram.Bot(token=bot_secret_key)

# initiate our dht22 sensor
dht22 = adafruit_dht.DHT22(board.D4)  # D4 = GPIO4

# initiate our soil moisture sensor
soil_moisture_channel = 21  # GPIO21
GPIO.setmode(GPIO.BCM)
GPIO.setup(soil_moisture_channel, GPIO.IN)


# Setup request headers for Favoriot
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["apiKey"] = api_key


def send_to_favoriot(device_developer_id, data):
    """
    Generate favoriot payload and send to favoriot
    """
    payload = json.dumps(
        {
            "device_developer_id": device_developer_id,
            "data": data,
        }
    )

    r = requests.post(api_url, headers=headers, data=payload)
    print("sent to favoriot", r)


def soil_moisture_callback(channel):
    """
    Callback for soil_moisture sensor
    """
    soil_moisture_reading = 0

    if GPIO.input(channel):
        soil_moisture_reading = 0
    else:
        soil_moisture_reading = 1

    print("Soil Moisture", soil_moisture_reading)
    send_to_favoriot(device_developer_id, {"soil_moisture": soil_moisture_reading})


GPIO.add_event_detect(
    soil_moisture_channel, GPIO.BOTH, bouncetime=5000
)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(
    soil_moisture_channel, soil_moisture_callback
)  # assign function to GPIO PIN, Run function on change


def main():
    """
    Main function
    """

    print(
        "--------------------------------------------------------------------------------"
    )
    print("START READING DATA")

    while True:
        time.sleep(
            sleep_time
        )  # we want to sleep for few seconds to let the sensors capture data

        try:
            temp_c = dht22.temperature  # in celcius
            print("Temperature (C)", temp_c)

            send_to_favoriot(device_developer_id, {"temperature": temp_c})

            if temp_c > max_temp:
                bot.send_message(chat_id=telegram_channel_id, text=telegram_text)

        except:
            print(
                "error detected during reading of DHT22 sensor - do nothing and wait for next reading"
            )

        print(
            "--------------------------------------------------------------------------------"
        )


if __name__ == "__main__":
    main()
