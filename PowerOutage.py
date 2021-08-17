#!/usr/bin/python3
import os
import platform
import ntplib
import time
import telegram
import pytz
from datetime import datetime

tz_iran = pytz.timezone('Iran')
count = 0
triger = False

def notify_ending(message):
    token = 'Telegram_token'
    chat_id = 'Telegram_chat_id'
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=message)

def check_ping(hostname):
    os_name = platform.system()
    # os cheks...
    try:
        if (os_name == "Windows"):
            response = os.system("ping -n 1 " + hostname)
        elif (os_name == "Linux"):
            response = os.system("ping -c 1 " + hostname)
        else:
            print("Unknown system")
            return 5
        # and then check the response...
        if response == 0:
            print("Network Active")
            return 0
    except OSError:
        print("Network Error")
        return 2

def main(alarm_triger):
    hostname = "192.168.1.20"

    now = datetime.now(tz_iran)
    current_time_hours = now.strftime("%H")
    current_time_min = now.strftime("%M")
    current_time = now.strftime("%p")

    print(f"\n\n................{current_time_hours}:{current_time_min}....................")

    if (check_ping(hostname) == 0):
        print("ITS UP")
        return 0

    elif (check_ping(hostname) != 0):
        if (int(current_time_hours) <= 12 and current_time == "AM"):
            print("EXPECTED DOWN TIME")
            return 0
        elif (int(current_time_hours) >= 10 and int(current_time_hours) < 12 and current_time == "PM"):
            print("EXPECTED DOWN TIME")
            return 0
        else:
            if (alarm_triger == False):
                notify_ending("UNEXPECTED DOWN TIME Triger Alarm")
                return 2
            elif (alarm_triger == True):
                print("UNEXPECTED DOWN TIME")
                return 3


while (True):
    r = main(triger)
    if(r == 2):
        triger = True

    if (triger == True):
        count += 1
        time.sleep(60)
        if (count == 360):
            count = 0
            triger = False

    else:
        time.sleep(60)