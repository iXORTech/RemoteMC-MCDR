__credits__ = ["alex3236"]

import os

from remotemc_mcdr.default_config import *
from remotemc_mcdr.util.json_util import *


def load_config(psi: PluginServerInterface, source=None):
    """
    Load the config from JSON file.
    :return: config object
    """

    config = psi.load_config_simple(target_class=Configure, in_data_folder=True, echo_in_console=False)

    with open(os.path.join(psi.get_data_folder(), 'config.json'), 'r', encoding='utf8') as f:
        json_list = json.load(f)
    if source:
        source.reply(i18n('reloaded'))
    update_json_cache(psi, json_list)

    return config
