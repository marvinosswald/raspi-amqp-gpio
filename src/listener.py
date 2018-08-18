import asyncio
from aio_pika import connect, IncomingMessage


class Listener:
    def __init__(self, config):
        self.config = config
        loop = asyncio.get_event_loop()
        loop.create_task(self.main(loop))
        loop.run_forever()

    async def on_message(self, message: IncomingMessage):
        """
        on_message doesn't necessarily have to be defined as async.
        Here it is to show that it's possible.
        """
        print(" [x] Received message %r" % message)
        print("Message body is: %r" % message.body)
        print("Before sleep!")
        await asyncio.sleep(5) # Represents async I/O operations
        print("After sleep!")

    async def main(self, loop):
        # Perform connection
        connection = await connect(
            self.config['RABBITMQ']['HOST'], loop=loop
        )

        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(self.config['COMMAND']['QUEUE'])

        # Start listening the queue with name 'hello'
        await queue.consume(self.on_message, no_ack=True)


if __name__ == "__main__":
    import configparser

    config = configparser.ConfigParser()
    config.read('../config.ini')
    print(" [*] Waiting for messages. To exit press CTRL+C")
    l = Listener(config)

    # we enter a never-ending loop that waits for data and runs callbacks whenever necessary.
