#!/mnt/data/projects/plug-charger/.venv/bin/python
# A script which constantly watches for laptop battery. Logs it to file after 1 min and plays a sound using vlc when your laptop
# battery is less than 15% and also send a msg to your android using ntfy.sh pub / sub free service.
#
# Original Authors:
#   * https://github.com/iamtalhaasghar
#
# 2024-02-24

import os
import logging
from dotenv import load_dotenv
import time
import requests
from datetime import datetime 
import psutil
import vlc


logging.basicConfig(filename='/var/log/plug-charger/log.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)


def ntfy(url, msg):
    # send a post request to a url
    try:
        requests.post(url, data=msg, headers={'Priority': 'high'})
    except Exception as e:
        logging.exception(e)
        pass


if __name__ == '__main__':
    load_dotenv()
    url = os.getenv('NTFY_URL')
    alert_sound = os.getenv('ALERT_FILE')
    battery = psutil.sensors_battery()
    while True:
        logging.info(f"Battery Level: {battery.percent}%")
        if not battery.power_plugged and battery.percent < 15:
            ntfy(url, f'Battery! {battery.percent}')
            p = vlc.MediaPlayer(alert_sound)
            p.play()
        time.sleep(60)

