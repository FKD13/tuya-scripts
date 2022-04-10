import json
from signal import signal, SIGINT, SIGTERM

import psutil
import tinytuya

device: tinytuya.BulbDevice

with open('devices.json', 'r') as file:
    devices: list[dict] = json.load(file)
    device = tinytuya.BulbDevice(
        devices[0]['id'],
        '0.0.0.0',
        devices[0]['key']
    )

device.set_version(3.3)
device.turn_on()


def run():
    while True:
        v = psutil.cpu_percent(0.25)
        device.set_colour(max(round((v / 100) * 255), 5), 0, 0)


def handle_exit(_signal, _frame):
    device.turn_off()
    exit()


if __name__ == '__main__':
    signal(SIGINT, handle_exit)
    signal(SIGTERM, handle_exit)

    run()
