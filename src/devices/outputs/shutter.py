from devices.outputs.output import Output
from gpiozero import OutputDevice
import asyncio

class Shutter(Output):
    controllable_properties = [
        'moveForTime'
    ]
    up = None
    down = None

    def __init__(self, device_config, config):
        self.type = "shutter"
        super().__init__(device_config, config)
        self.initIO()
        print(' [x] Shutter has been initalized.')

    def initIO(self):
        """"""
        self.up = OutputDevice(self.device_config['output'][0])
        self.down = OutputDevice(self.device_config['output'][1])

    def exec(self, context):
        if context['property'] == 'moveForTime':
            loop = asyncio.get_event_loop()
            loop.create_task(self.moveForTime(context['value']))

    async def moveForTime(self, value):
        io = None
        if int(value) > 0:
            io = self.up
            print("Driving {} up for {} seconds".format(self.name, abs(value)))
        else:
            io = self.down
            print("Driving {} down for {} seconds".format(self.name, abs(value)))
        # for value seconds then on
        io.off()
        await asyncio.sleep(abs(value))
        io.on()