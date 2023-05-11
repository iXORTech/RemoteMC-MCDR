from remotemc_mcdr.flask import *
from remotemc_mcdr.commands.broadcast_command import *
from remotemc_mcdr.commands.help_command import *
from remotemc_mcdr.commands.msg_command import *
from remotemc_mcdr.commands.remotemc_command import *
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
        server.register_help_message(command_string.replace('.', ' '), help_message_string)

    def get_literal_node(literal):
        server.logger.info(i18n("command.getting_literal_node", literal))
        lvl = config.permission.get(literal, 0)
        server.logger.info(i18n("command.permission_level", literal, lvl))
        return Literal(literal).requires(lambda src: src.has_permission(lvl))\
            .on_error(RequirementNotMet, lambda src: src.reply(i18n('command.permission_denied')), handled=True)

    server.register_command(
        Literal(f"!!{CONTROL_COMMAND_PREFIX}").
        runs(show_help).
        then(
            get_literal_node("help")
            .runs(show_help)
        ).
        then(
            get_literal_node("status")
            .runs(status_command)
        ).
        then(
            get_literal_node("about")
            .runs(about_command)
        )
    )
    register_help_message(f"{CONTROL_COMMAND_PREFIX}")
    server.logger.info(i18n("command.registered", CONTROL_COMMAND_PREFIX))
    register_help_message(f"{CONTROL_COMMAND_PREFIX}.help")
    register_help_message(f"{CONTROL_COMMAND_PREFIX}.status")
    register_help_message(f"{CONTROL_COMMAND_PREFIX}.about")

    server.register_command(
        get_literal_node(f"!!{MESSAGE_COMMAND_PREFIX}").then(
            GreedyText("message").runs(send_message)
        )
    )
    register_help_message(f"{MESSAGE_COMMAND_PREFIX}", "<Message>")
    server.logger.info(i18n("command.registered", MESSAGE_COMMAND_PREFIX))

    server.register_command(
        get_literal_node(f"!!{BROADCAST_COMMAND_PREFIX}").then(
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
    generate_sender_id()

    remotemc_core_host = config.remotemc_core["host"]
    remotemc_core_port = int(config.remotemc_core["port"])
    remotemc_core_ssl = True if config.remotemc_core["ssl"].lower() == "true" else False
    remotemc_core_check_status = remotemc_core_check(remotemc_core_host, remotemc_core_port, remotemc_core_ssl)
    if remotemc_core_check_status == RemoteMCCoreStatus.INCOMPATIBLE:
        server.logger.warning(i18n("logger.warning.core_incompatible"))
    elif remotemc_core_check_status == RemoteMCCoreStatus.UNKNOWN_ERROR:
        server.logger.error(i18n("logger.warning.core_unknown_error"))
    elif remotemc_core_check_status == RemoteMCCoreStatus.NOT_CONNECTED:
        server.logger.warning(i18n("logger.warning.core_not_connected"))


def on_server_startup(plugin_server_interface: PluginServerInterface):
    load_flask()
