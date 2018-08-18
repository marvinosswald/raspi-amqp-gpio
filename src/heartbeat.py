import asyncio
from aio_pika import connect, Message
import socket


class Heartbeat:
    def __init__(self, config):
        self.config = config

        loop = asyncio.get_event_loop()
        loop.create_task(self.main(loop))

    async def main(self, loop):
        # Perform connection
        connection = await connect(
            self.config['RABBITMQ']['HOST'], loop=loop
        )

        # Creating a channel
        channel = await connection.channel()

        # Sending the message
        await channel.default_exchange.publish(
            Message(bytes('Client Alive: ' + self.config['DEFAULT']['CLIENTNAME'] + '('+self.get_ip()+')', 'utf-8')),
            routing_key=self.config['HEARTBEAT']['ROUTING_KEY'],
        )

        print(" [x] Sent heartbeat ❤️")

        await connection.close()

        await asyncio.sleep(30)
        await self.main(loop)

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP


if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read('../config.ini')
    heartbeat = Heartbeat(config)
    loop = asyncio.get_event_loop()
    loop.run_forever()