from mcdreforged.api.all import PluginServerInterface, ServerInterface

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

VERSION = server.get_self_metadata().version.__str__()

CONTROL_COMMAND_PREFIX = "!!remotemc"
MESSAGE_COMMAND_PREFIX = "!!msg"
BROADCAST_COMMAND_PREFIX = "!!broadcast"
