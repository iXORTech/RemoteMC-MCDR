from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
config: Configure = load_config(server)


def status_command(source: CommandSource):
    source.reply("STATUS_COMMAND_REPLY")


def about_command(source: CommandSource):
    source.reply("ABOUT_COMMAND_REPLY")
