from typing import Dict
from mcdreforged.api.all import Serializable, ServerInterface

PLUGIN_ID = 'mcdreforged_remote'
plugin_server_interface = ServerInterface.get_instance().as_plugin_server_interface()


class Configure(Serializable):
    """
    config object class
    """

    # Default values
    remote_core: Dict[str, str] = {
        # Connection settings to MCDRemoteCore
        'host': "127.0.0.1",
        'port': "6536",
        'auth_key': "you_should_change_this_key_to_your_own_key",
    }
    