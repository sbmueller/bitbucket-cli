import json
import os
from typing import Union


class Config:
    """Represents a configuration database stored in a JSON file."""

    def __init__(self, path: str):
        """
        C'tor.

        :param str path: Path to the configuration file
        """
        if not os.path.exists(path):
            raise FileNotFoundError("Could not find config file at " + path)
        self.path = path

    def get_config_value(self, key: str) -> Union[str, int]:
        """
        Read the value for key from the config file.

        :param Union[str, int] key: Key in JSON file
        :return: Value in JSON file (str or int)
        """
        with open(self.path) as config:
            data = json.load(config)
        return data[key]
