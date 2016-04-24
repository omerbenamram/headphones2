import simplejson as json

from headphones2.configuration import CONFIGURATION_PATH


def dump_configuration(configuration):
    with open(CONFIGURATION_PATH, str('wb')) as config_path:
        json.dump(configuration, config_path, indent=4)


def load_configuration_from_disk():
    try:
        with open(CONFIGURATION_PATH, str('rb')) as fp:
            current_configuration = json.load(fp)
    except IOError:
        current_configuration = {}

    return current_configuration
