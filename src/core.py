import json
from env_config import get_envvar_configuration

from DeviceManager import DeviceManager
from heartbeat import Heartbeat
import asyncio
from dotenv import load_dotenv

class AMQPExposerCore:
    def __init__(self):
        load_dotenv()
        self.config = get_envvar_configuration('AMQP')
        self.heartbeat = Heartbeat(self.config)
        self.devices = DeviceManager(self.config['DEVICES']['devices'], self.config)
        loop = asyncio.get_event_loop()
        loop.run_forever()

if __name__ == "__main__":
    core = AMQPExposerCore()