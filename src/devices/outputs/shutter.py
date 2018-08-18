from devices.outputs.output import Output
from gpiozero import OutputDevice
import asyncio

class Shutter(Output):
    controllable_properties = [
        'moveForTime'
    ]
    up = None
    down = None
    # 0 = DECREASING; 1 = INCREASING; 2 = STOPPED;
    positionState = 2

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
            if self.positionState == 2:
                loop = asyncio.get_event_loop()
                loop.create_task(self.moveForTime(context['value']))
            else:
                print("{} is busy".format(self.name))

    async def moveForTime(self, value):
        time = abs(int(value))
        if int(value) > 0:
            self.positionState = 1
            io = self.up
            print("Driving {} up for {} seconds".format(self.name, time))
        else:
            self.positionState = 0
            io = self.down
            print("Driving {} down for {} seconds".format(self.name, time))
        # for value seconds then on
        io.off()
        await asyncio.sleep(time)
        io.on()
        self.positionState = 2