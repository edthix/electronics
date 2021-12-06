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


# ********************************************************************************
# Configurations change here
# ********************************************************************************
api_url = "https://apiv2.favoriot.com/v2/streams"
device_developer_id = "GET FROM FAVORIOT"
api_key = "GET FROM FAVORIOT"

bot_secret_key = "GET FROM TELEGRAM"
telegram_channel_id = "GET FROM TELEGRAM"
telegram_text = "PANAS!!!"

max_temp = 24 # change accordingly

sleep_time = 2 # number of seconds to sleep before processing
# ********************************************************************************
# End of configurations
# ********************************************************************************


# initiate our telegram bot
bot = telegram.Bot(token=bot_secret_key)

# initiate our dht22 sensor
dht22 = adafruit_dht.DHT22(board.D4) # D4 = GPIO4

# Setup request headers
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["apiKey"] = api_key

def main():
    """
    Main function
    """
    while True:
        time.sleep(sleep_time)
        temp_c = dht22.temperature # in celcius
        print("Temperature is", temp_c)

        favoriot_payload = json.dumps({
            "device_developer_id": device_developer_id,
            "data": {
                "temperature": temp_c
            }
        })

        res = requests.post(api_url, headers=headers, data=payload)
        print(res)

        if temp > max_temp:
            bot.send_message(chat_id=telegram_channel_id, text=telegram_text)

        print("--------------------------------------------------------------------------------")


if __name__ == "__main__":
    main()
