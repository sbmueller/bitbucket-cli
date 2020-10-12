import json
import os


class Config:
    def __init__(self, path):
        """
        C'tor of Config, represents a configuration database stored in a JSON file.

        :param: path Path to the configuration file
        """
        if not os.path.exists(path):
            raise FileNotFoundError("Could not find config file at " + path)
        self.path = path

    def get_config_value(self, key):
        """
        Reads the value for key from the config file.

        :param: key Key in JSON file
        """
        with open(self.path) as config:
            data = json.load(config)
        return data[key]
