from typing import Dict
from mcdreforged.api.all import Serializable, ServerInterface

PLUGIN_ID = 'mcdreforged_remote'
plugin_server_interface = ServerInterface.get_instance().as_plugin_server_interface()


class Configure(Serializable):
    """
    config object class
    """

    # Default values
    
    remotemc_mcdr: Dict[str, str] = {
        "auth_key": "you_should_change_this",
    }
    
    remotemc_mcdr_flask: Dict[str, str] = {
        # Flask Server Config
        'host': "127.0.0.1",
        'port': "65362",
    }
    
    remotemc_core: Dict[str, str] = {
        'host': "127.0.0.1",
        'port': "65360",
        'ssl': "false",
    }
    