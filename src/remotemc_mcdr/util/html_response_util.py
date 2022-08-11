from flask import jsonify
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()


def get_200_response(message: str = "OK"):
    """
    :return: JSON object with status code 200 and message "OK"
    """
    server.logger.info(i18n("flask.sending_response", "200", message))
    return jsonify({"status_code": 200, "message": message})


def get_204_response():
    """
    :return: JSON object with status code 204 and message "NO_CONTENT"
    """
    server.logger.info(i18n("flask.sending_response", "204", "NO_CONTENT"))
    return jsonify({"status_code": 204, "message": "NO_CONTENT"})


def get_400_response():
    """
    :return: JSON object with status code 400 and message "BAD_REQUEST"
    """
    server.logger.error(i18n("flask.sending_response", "400", "BAD_REQUEST"))
    return jsonify({"status_code": 400, "message": "BAD_REQUEST"})


def get_401_response():
    """
    :return: JSON object with status code 401 and message "UNAUTHORIZED"
    """
    server.logger.error(i18n("flask.sending_response", "401", "UNAUTHORIZED"))
    return jsonify({"status_code": 401, "message": "UNAUTHORIZED"})
