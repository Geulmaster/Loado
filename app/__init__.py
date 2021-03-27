from configparser import ConfigParser
from pathlib import Path

def config_reader():
    config_file = Path(__file__).parent / 'configuration.ini'
    parser = ConfigParser()
    parser.read(config_file)
    return parser


def change_config_file(key, value):
    file_content = config_reader()
    file_content.set("Load Testing", key, value)
    with open("configuration.ini", "w") as config_file:
        file_content.write(config_file)
        