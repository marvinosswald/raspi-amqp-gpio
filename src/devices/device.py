class Device:
    def __init__(self, config):
        self.device_config = config
        if config["name"] is None:
            raise Exception("name not set")
        self.name = config["name"]