from flask import jsonify, Response
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()


def get_200_response(content=None):
    """
    :return: JSON object with status code 200 and message "OK"
    """
    if content is None:
        content = {"message": "OK"}
    server.logger.info(i18n("flask.sending_response", "200", content))
    return content, 200


def get_204_response():
    """
    :return: JSON object with status code 204 and message "NO_CONTENT"
    """
    server.logger.info(i18n("flask.sending_response", "204", "NO_CONTENT"))
    return "NO_CONTENT", 204


def get_400_response():
    """
    :return: JSON object with status code 400 and message "BAD_REQUEST"
    """
    server.logger.error(i18n("flask.sending_response", "400", "BAD_REQUEST"))
    return "BAD_REQUEST", 400


def get_401_response():
    """
    :return: JSON object with status code 401 and message "UNAUTHORIZED"
    """
    server.logger.error(i18n("flask.sending_response", "401", "UNAUTHORIZED"))
    return "UNAUTHORIZED", 401
