import configparser
import json

from DeviceManager import DeviceManager
from heartbeat import Heartbeat
import asyncio


class AMQPExposerCore:
    def __init__(self, config_ini, devices_json):
        self.config = configparser.ConfigParser()
        self.config.read(config_ini)
        self.heartbeat = Heartbeat(self.config)
        with open(devices_json) as f:
            data = json.load(f)
            self.devices = DeviceManager(data['devices'], self.config)
            loop = asyncio.get_event_loop()
            loop.run_forever()

if __name__ == "__main__":
    core = AMQPExposerCore('../config.ini', '../devices.json')