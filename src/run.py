from core import AMQPExposerCore
import click

@click.command()
@click.option('--config', default='config.ini', help='general config file')
@click.option('--devices',default='devices.json', help='devices config file')
def run(config, devices):
    core = AMQPExposerCore(config, devices)


if __name__ == "__main__":
    run()