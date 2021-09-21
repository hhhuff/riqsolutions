from os import path
from configparser import ConfigParser
from .configure import CONFIGFILE_DEFAULT_NAME

def configure_api(api_instance, context='DEFAULT', configpath=None):
    if context is None:
        context = 'DEFAULT'
    if not configpath:
        configpath = path.join(path.expanduser('~'), CONFIGFILE_DEFAULT_NAME)
    config = ConfigParser()
    config.read(configpath)
    api_instance.configure(config[context]['api_token'], config[context]['api_key'],config[context]['proxy'],config[context]['context'])
    return api_instance

def check_context(context='DEFAULT', configpath=None):
    if context is None:
        context = 'DEFAULT'
    if not configpath:
        configpath = path.join(path.expanduser('~'), CONFIGFILE_DEFAULT_NAME)
    config = ConfigParser()
    config.read(configpath)
    try:
        config[context]
        return True
    except Exception as e:
        return False