import configparser

import os
from pathlib import Path


class ConfigManager:

    FRAMEWORK_CONFIG_FILE = "..\\..\\resources\\framework.ini"

    def __init__(self):
        config = configparser.ConfigParser()
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ConfigManager.FRAMEWORK_CONFIG_FILE)
        config.read(path)
        self.config = config

