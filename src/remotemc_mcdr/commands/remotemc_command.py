from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.version_util import *
from remotemc_mcdr.util.remotemc_core_check_util import *
from remotemc_mcdr.util.reply_util import reply_to_source

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
config: Configure = load_config(server)


def status_command(source: CommandSource):
    remotemc_core_host = config.remotemc_core["host"]
    remotemc_core_port = int(config.remotemc_core["port"])
    compatible_status = get_compatible_status(config)

    connection = "Connected" if compatible_status != "Not Connected" else "Disconnected"

    status_msg_lines = ["\n",
                        i18n("in_game.status_message.line1") + "\n",
                        i18n("in_game.status_message.line2") + "\n",
                        (
                            i18n("in_game.status_message.line3.disconnected",
                                 "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                            if compatible_status == "Not Connected"
                            else
                            i18n("in_game.status_message.line3.compatible",
                                 "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                            if
                            compatible_status == "Compatible"
                            else i18n("in_game.status_message.line3.incompatible",
                                      "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                        ) + "\n"
                        ]

    reply_to_source(source, status_msg_lines)


def about_command(source: CommandSource):
    about_msg_lines = ["\n",
                       i18n("in_game.about_message.line1") + "\n",
                       i18n("in_game.about_message.line2") + "\n",
                       i18n("in_game.about_message.line3", get_version(), get_build_date()) + "\n",
                       i18n("in_game.about_message.line4") + "\n"
                       ]
    reply_to_source(source, about_msg_lines)
