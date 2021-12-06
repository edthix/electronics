#!/usr/bin/python

import requests
import json
import random
from time import sleep
import telegram

from requests.structures import CaseInsensitiveDict

api_url = "https://apiv2.favoriot.com/v2/streams"
device_developer_id = ""
api_key = ""

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["apiKey"] = api_key


bot_secret_key = ""
telegram_channel_id = ""
bot = telegram.Bot(token=bot_secret_key)


for i in range(20):
    sleep(5)
    temp = random.randrange(-2, 35)
    print(temp)

    payload = json.dumps({
    "device_developer_id": device_developer_id,
    "data": {
        "temperature": temp
    }
    })

    r = requests.post(api_url, headers=headers, data=payload)
    print(r)

    if temp > 37:
        bot.send_message(chat_id=telegram_channel_id, text="Notification IOT - check me I'm hot")
