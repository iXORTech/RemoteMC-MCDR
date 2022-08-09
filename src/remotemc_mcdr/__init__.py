from remotemc_mcdr.flask import *
from remotemc_mcdr.commands.help_command import *
from remotemc_mcdr.commands.msg_command import *
from remotemc_mcdr.constants import *
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.version_util import *
from remotemc_mcdr.util.sender_id_util import generate_sender_id

config: Configure
server: PluginServerInterface = None


def register_commands(server: PluginServerInterface):
    server.register_command(
        Literal(CONTROL_COMMAND_PREFIX).runs(show_help)
    )
    server.register_command(
        Literal(MESSAGE_COMMAND_PREFIX).then(
            GreedyText('message').runs(send_message)
        )
    )


# Load Intergrated Flask Web Server
def load_flask():
    server.logger.info(i18n('loading_flask'))
    run_flask(config)


def on_load(plugin_server_interface: PluginServerInterface, prev):
    global server, config
    server = plugin_server_interface
    load_version_properties()
    config = load_config(server, server.get_plugin_command_source())
    register_commands(server)
    server.logger.info("==========================================================")
    server.logger.info(i18n('plugin_loaded'))
    server.logger.info(i18n('version', get_version()))
    stage = get_version_property("stage")
    if "dev" in stage or "alpha" in stage or "beta" in stage:
        server.logger.info(i18n('logger.warning.experimental'))
    elif "rc" in stage:
        server.logger.info(i18n('logger.warning.release_candidate'))
    server.logger.info("==========================================================")
    server.logger.info(i18n('message_and_broadcast.sender_id_generated', generate_sender_id()))


def on_server_startup(plugin_server_interface: PluginServerInterface):
    load_flask()
