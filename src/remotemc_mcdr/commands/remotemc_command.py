from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.remotemc_core_check_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
config: Configure = load_config(server)


def status_command(source: CommandSource):
    remotemc_core_host = config.remotemc_core["host"]
    remotemc_core_port = int(config.remotemc_core["port"])
    remotemc_core_ssl = True if config.remotemc_core["ssl"].lower() == "true" else False
    remotemc_core_check_status = remotemc_core_check(remotemc_core_host, remotemc_core_port, remotemc_core_ssl)

    compatible_status = None
    if remotemc_core_check_status == RemoteMCCoreStatus.IS_COMPATIBLE:
        compatible_status = "Compatible"
    elif remotemc_core_check_status == RemoteMCCoreStatus.INCOMPATIBLE:
        compatible_status = "Incompatible"
    elif remotemc_core_check_status == RemoteMCCoreStatus.UNKNOWN_ERROR:
        compatible_status = "Unknown Error"
    elif remotemc_core_check_status == RemoteMCCoreStatus.NOT_CONNECTED:
        compatible_status = "Not Connected"

    connection = "Connected" if remotemc_core_check_status != RemoteMCCoreStatus.NOT_CONNECTED else "Disconnected"

    status_msg_lines = ["\n",
                        i18n("in_game.status_message.line1") + "\n",
                        i18n("in_game.status_message.line2") + "\n",
                        (
                            i18n("in_game.status_message.line3.disconnected",
                                 "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                            if remotemc_core_check_status == RemoteMCCoreStatus.NOT_CONNECTED
                            else
                            i18n("in_game.status_message.line3.compatible",
                                 "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                            if
                            remotemc_core_check_status == RemoteMCCoreStatus.IS_COMPATIBLE
                            else i18n("in_game.status_message.line3.incompatible",
                                      "RemoteMC-Core", remotemc_core_host, remotemc_core_port, connection)
                        ) + "\n"
                        ]

    status_msg_rtext = RTextList()
    for line in status_msg_lines:
        result = re.search(r"(?<=§7)!![\w ]*(?=§)", line)
        if result is not None:
            status_msg_rtext.append(
                RText(line).c(RAction.suggest_command, result.group()).h(
                    i18n("in_game.click_to_use_command", result.group())))
        else:
            status_msg_rtext.append(line)
    source.reply(status_msg_rtext)


def about_command(source: CommandSource):
    source.reply("ABOUT_COMMAND_REPLY")
