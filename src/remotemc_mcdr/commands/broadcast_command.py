import requests.exceptions

from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
config: Configure = load_config(server)


def broadcast(source: CommandSource, context: dict):
    message = context["message"]

    server.logger.info(i18n("message_and_broadcast.broadcasting", message))

    remotemc_core_url = config.remotemc_core["host"] + ":" + config.remotemc_core["port"]
    if config.remotemc_core["ssl"] == "true":
        remotemc_core_url = "https://" + remotemc_core_url
    else:
        remotemc_core_url = "http://" + remotemc_core_url
    remotemc_core_url += "/broadcast"

    server.logger.info(i18n("message_and_broadcast.core_url", remotemc_core_url))

    try:
        remotemc_core_response = requests.post(remotemc_core_url, json={
            "authKey": config.remotemc["auth_key"],
            "message": message
        })
    except requests.exceptions.ConnectionError as error:
        server.logger.error(i18n("message_and_broadcast.core_connection_error", error))
        server.say(i18n("message_and_broadcast.core_connection_error", error))
        return

    if remotemc_core_response.status_code == 200:
        server.logger.info(i18n("message_and_broadcast.sucessful_execution_response_received",
                                i18n("broadcast"),
                                remotemc_core_response.status_code,
                                remotemc_core_response.text))
    else:
        server.logger.warning(i18n("unsucessful_execution_response_received",
                                   i18n("broadcast"),
                                   remotemc_core_response.status_code,
                                   remotemc_core_response.text))
        server.say(i18n("unsucessful_execution_response_received",
                        i18n("broadcast"),
                        remotemc_core_response.status_code,
                        remotemc_core_response.text))
