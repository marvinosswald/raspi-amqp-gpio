import asyncio

from aio_pika import IncomingMessage, connect

from devices.device import Device


class Output(Device):
    controllable_properties = None

    def __init__(self, device_config, config):
        self.type="no output type defined"
        self.config = config
        super().__init__(device_config)
        loop = asyncio.get_event_loop()
        loop.create_task(self.main(loop))

    async def on_message(self, message: IncomingMessage):
        print(message)
        if message.headers['target'] == self.name and self.ifPropertyAllowed(message.headers['property']) and self.runChecks(message.headers):
            self.exec(message.headers, message)
        else:
            message.nack()

    def ifPropertyAllowed(self, property):
        if property in self.controllable_properties:
            return True

    def runChecks(self, context):
        return True

    def exec(self, context,message: IncomingMessage):
        raise Exception("no handling for {} defined".format(self.type))

    async def main(self, loop):
        # Perform connection
        connection = await connect(
            self.config['HOST'], loop=loop
        )

        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(self.config['COMMANDS_QUEUE'])

        # Start listening the queue with name 'hello'
        await queue.consume(self.on_message)