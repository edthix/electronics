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
device_developer_id = "GET FROM FAVORIOT"
api_key = "GET FROM FAVORIOT"

bot_secret_key = "GET FROM TELEGRAM"
telegram_channel_id = "GET FROM TELEGRAM"
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


def soil_moisture_callback(channel):
    """
    Callback for soil_moisture sensor
    """
    soil_moisture_reading = 0

    if GPIO.input(channel):
        print("No water detected")
        soil_moisture_reading = 0
    else:
        print("Water detected")
        soil_moisture_reading = 1

    payload = json.dumps(
        {
            "device_developer_id": device_developer_id,
            "data": {"soil_moisture": soil_moisture_reading},
        }
    )
    request.post(api_url, headers=headers, data=payload)


GPIO.add_event_detect(
    soil_moisture_channel, GPIO.BOTH, bouncetime=1000
)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(
    soil_moisture_channel, soil_moisture_callback
)  # assign function to GPIO PIN, Run function on change


def main():
    """
    Main function
    """
    while True:
        time.sleep(
            sleep_time
        )  # we want to sleep for few seconds to let the sensors capture data

        temp_c = dht22.temperature  # in celcius
        print("Temperature is", temp_c)

        # What we want to send to favoriot
        payload = json.dumps(
            {
                "device_developer_id": device_developer_id,
                "data": {"temperature": temp_c},
            }
        )

        res = requests.post(api_url, headers=headers, data=payload)
        print(res)

        if temp_c > max_temp:
            bot.send_message(chat_id=telegram_channel_id, text=telegram_text)

        print(
            "--------------------------------------------------------------------------------"
        )


if __name__ == "__main__":
    main()
