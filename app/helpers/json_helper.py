import json
from os import environ

def get_config_file(path):
    with open(path, "r", encoding="utf-8") as file:
        config_file = json.load(file)
        return config_file