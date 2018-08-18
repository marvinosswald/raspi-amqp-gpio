from devices.outputs.output import Output
from gpiozero import OutputDevice


class Switch(Output):
    controllable_properties = [
        'powerState'
    ]
    io = None

    def __init__(self, device_config, config):
        self.type = "switch"
        super().__init__(device_config, config)
        self.initIO()
        print(' [x] Switch has been initalized.')

    def initIO(self):
        """"""
        self.io = OutputDevice(self.config['output'][0])

    def exec(self, context):
        if context['value'] == 0:
            print('OFF')
        else:
            print('ON')