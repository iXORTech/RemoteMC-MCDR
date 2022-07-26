from mcdreforged.api.all import PluginServerInterface, ServerInterface

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

CONTROL_COMMAND_PREFIX = "!!remotemc"
MESSAGE_COMMAND_PREFIX = "!!msg"
BROADCAST_COMMAND_PREFIX = "!!broadcast"
