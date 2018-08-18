import json
import importlib


class DeviceManager:
    def __init__(self, devices_config, config):
        self.devices_config = devices_config
        self.config = config
        self.devices = []
        self.initDevices()

    def initDevices(self):
        for device in self.devices_config:
            if device["output"] is not None:

                device['io_type'] = 'output'
            else:
                device['io_type'] = 'input'

            dev = self.dynImp(device)
            if dev is not None:
                self.devices.append(dev(device, self.config))


    def dynImp(self, config):
        try:
            module = importlib.import_module('devices.outputs')

        except ImportError:
            print("could not import outputs module")
            return

        try:
            klazz = getattr(module, config['type'].capitalize())
            return klazz

        except Exception as e:
            print(" [?] Device type '{}' is unknown".format(config['type']))


if __name__ == "__main__":
    import configparser
    import asyncio
    config = configparser.ConfigParser()
    config.read('../config.ini')
    with open('../devices.json') as f:
        data = json.load(f)
        devices = DeviceManager(data['devices'], config)
        loop = asyncio.get_event_loop()
        loop.run_forever()