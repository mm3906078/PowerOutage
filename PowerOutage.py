#!/usr/bin/python3
import os
import platform
import ntplib
import time
import telegram
import pytz
import smtplib
from datetime import datetime

# change telegram token & chat_id in notify_tel
# change send_mail & rciver_mail & pass in send_mail
# change hostname in main

tz_iran = pytz.timezone('Iran')
count = 0
triger = False

def notify_tel(message):
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

def send_mail(body):
    send_mail = "sender_mail"
    recive_mail = "rciver_mail"
    passwd = "mail_pass"
    server = smtplib.SMTP('smtp.gmail.com',587)
    # stable connection
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(send_mail , passwd)
    subject = 'PowerOutage'
    msg = f"Subject : {subject} \n\n {body}"
    server.sendmail(
        send_mail,
        recive_mail,
        msg
    )
    print("EMAIL SENT!!")
    server.quit()

def main(alarm_triger):
    hostname = "192.168.1.20"

    now = datetime.now(tz_iran)
    current_time_hours = now.strftime("%H")
    current_time_min = now.strftime("%M")
    current_time = now.strftime("%p")

    print(f"\n\n................{current_time_hours}:{current_time_min}....................")

    if (check_ping(hostname) != 0):
        print("ITS UP")
        return 0

    elif (check_ping(hostname) == 0):
        if (int(current_time_hours) <= 12 and current_time == "AM"):
            print("EXPECTED DOWN TIME")
            return 0
        elif (int(current_time_hours) >= 10 and int(current_time_hours) < 12 and current_time == "PM"):
            print("EXPECTED DOWN TIME")
            return 0
        else:
            if (alarm_triger == False):
                notify_tel("UNEXPECTED DOWN TIME Triger Alarm")
                # send_mail("UNEXPECTED DOWN TIME Triger Alarm")
                return 2
            elif (alarm_triger == True):
                print("UNEXPECTED DOWN TIME")
                return 3
                
while (True):
    r = main(triger)
    if(r == 2):
        triger = True
    else:
        triger = False
        count  = 0
    if (triger == True):
        count += 1
        if (count == 10):
            send_mail("UNEXPECTED DOWN TIME Triger Alarm")
            count = 0
            triger = False
        time.sleep(60)
    else:
        time.sleep(60)