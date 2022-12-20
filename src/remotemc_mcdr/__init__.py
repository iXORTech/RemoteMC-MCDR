from remotemc_mcdr.flask import *
from remotemc_mcdr.commands.help_command import *
from remotemc_mcdr.commands.msg_command import *
from remotemc_mcdr.commands.broadcast_command import *
from remotemc_mcdr.constants import *
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.version_util import *
from remotemc_mcdr.util.sender_id_util import generate_sender_id

config: Configure
server: PluginServerInterface = None


def register_commands(server: PluginServerInterface):
    def register_help_message(command, *params):
        command_string = f"!!{command}"
        for param in params:
            command_string += f" {param}"
        help_message_string = f"{i18n(f'command.help_message.{command}')}"
        server.logger.info(i18n("command.registering_help_message", command_string, help_message_string))
        server.register_help_message(command_string, help_message_string)

    def get_literal_node(literal):
        server.logger.info(i18n("command.getting_literal_node", literal))
        lvl = config.permission.get(literal, 0)
        server.logger.info(i18n("command.permission_level", literal, lvl))
        return Literal(f"!!{literal}").requires(lambda src: src.has_permission(lvl),
                                                lambda: i18n("command.permission_denied"))

    server.register_command(
        get_literal_node(CONTROL_COMMAND_PREFIX).runs(show_help)
    )
    register_help_message(f"{CONTROL_COMMAND_PREFIX}")
    server.logger.info(i18n("command.registered", CONTROL_COMMAND_PREFIX))

    server.register_command(
        get_literal_node(MESSAGE_COMMAND_PREFIX).then(
            GreedyText("message").runs(send_message)
        )
    )
    register_help_message(f"{MESSAGE_COMMAND_PREFIX}", "<Message>")
    server.logger.info(i18n("command.registered", MESSAGE_COMMAND_PREFIX))

    server.register_command(
        get_literal_node(BROADCAST_COMMAND_PREFIX).then(
            GreedyText("message").runs(broadcast)
        )
    )
    register_help_message(f"{BROADCAST_COMMAND_PREFIX}", "<Message>")
    server.logger.info(i18n("command.registered", BROADCAST_COMMAND_PREFIX))


# Load Intergrated Flask Web Server
def load_flask():
    server.logger.info(i18n("loading_flask"))
    run_flask(config)


def on_load(plugin_server_interface: PluginServerInterface, prev):
    global server, config
    server = plugin_server_interface
    load_version_properties()
    config = load_config(server, server.get_plugin_command_source())
    register_commands(server)
    server.logger.info("==========================================================")
    server.logger.info(i18n("plugin_loaded"))
    plugin_version = get_version()
    server.logger.info(i18n("version", plugin_version))
    if "DEV" in plugin_version or "Alpha" in plugin_version or "Beta" in plugin_version:
        server.logger.info(i18n("logger.warning.experimental"))
    elif "Release Candidate" in plugin_version:
        server.logger.info(i18n("logger.warning.release_candidate"))
    server.logger.info("==========================================================")
    server.logger.info(i18n("message_and_broadcast.sender_id_generated", generate_sender_id()))


def on_server_startup(plugin_server_interface: PluginServerInterface):
    load_flask()
