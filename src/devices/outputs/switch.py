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
        self.io = OutputDevice(self.device_config['output'][0])

    def exec(self, context):
        print("raw value: ".format(context['value']))
        if int(context['value']) == 0:
            self.io.on()
            print("powerState of {} is OFF".format(self.name))
        else:
            self.io.off()
            print("powerState of {} is ON".format(self.name))