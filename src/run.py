from core import AMQPExposerCore
import click

@click.command()
def run(config, devices):
    core = AMQPExposerCore()


if __name__ == "__main__":
    run()