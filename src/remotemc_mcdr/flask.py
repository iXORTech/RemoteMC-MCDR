from flask import Flask, request
from waitress import serve
from mcstatus import JavaServer

from remotemc_mcdr.util.html_response_util import *
from remotemc_mcdr.util.config_util import *
from remotemc_mcdr.util.sender_id_util import is_the_same_sender_id

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

# Flask Server App and its configuration
flask_app = Flask(__name__)
flask_app.config["JSON_AS_ASCII"] = False
flask_app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"
flask_app.config["DEBUG"] = True

config: Configure

auth_key: str = None


@flask_app.route("/ping", methods=["GET"])
def ping():
    server.logger.info(i18n("flask.received_get", "/ping"))
    return get_200_response("PONG!")


@flask_app.route("/api/v1/mcserver/status", methods=["GET"])
def status():
    server.logger.info(i18n("flask.received_get", "/api/v1/mcserver/status"))
    minecraft_server_address = f"{config.minecraft_server['host']}:{config.minecraft_server['port']}"
    minecraft_server = JavaServer.lookup(minecraft_server_address)
    server.logger.info(i18n("flask.status.looking_up_server", minecraft_server_address))
    query = minecraft_server.query()
    message = "{0}\n{1}{2}\n{3}[{4}/{5}]".format(
        i18n("status.server_running"),  # {0}
        i18n("status.game_version"),  # {1}
        query.software.version,  # {2}
        i18n("status.player_online"),  # {3}
        query.players.online,  # {4}
        query.players.max)  # {5}
    for player in query.players.names:
        message = message + "\n> {0}".format(player)
    server.logger.info(i18n("flask.status.server_status", message))
    return get_200_response(message)


@flask_app.route("/api/v1/mcserver/execute_command", methods=["POST"])
def execute_command():
    server.logger.info(i18n("flask.received_post", "/api/v1/mcserver/execute_command"))

    if not request.is_json:
        server.logger.error(i18n("flask.request_is_not_json"))
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, "auth_key", "command"):
        server.logger.error(i18n("flask.request_missing_keys_in_json"))
        return get_400_response()

    if not auth_key == content["auth_key"]:
        server.logger.error(i18n("flask.auth_key_not_match"))
        return get_401_response()

    command: str = content["command"]
    server.logger.info(i18n("flask.execute_command.executing_command", command))

    is_rcon_running = server.is_rcon_running()
    if is_rcon_running:
        server.logger.info(i18n("flask.execute_command.rcon_is_running"))
        rcon_info = server.rcon_query(command)
        server.logger.info(i18n("flask.execute_command.command_executed"))
        if rcon_info:
            return get_200_response(rcon_info)
        else:
            return get_200_response()
    else:
        server.logger.info(i18n("flask.execute_command.rcon_is_not_running"))
        server.execute_command(command)
        server.logger.info(i18n("flask.execute_command.command_executed"))
        return get_200_response(i18n("enable_rcon"))


@flask_app.route("/api/v1/mcserver/send_message", methods=["POST"])
def say():
    server.logger.info(i18n("flask.received_post", "/api/v1/mcserver/send_message"))

    if not request.is_json:
        server.logger.error(i18n("flask.request_is_not_json"))
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, "auth_key", "sender_id", "source", "sender", "message"):
        server.logger.error(i18n("flask.request_missing_keys_in_json"))
        return get_400_response()

    if not auth_key == content["auth_key"]:
        server.logger.error(i18n("flask.auth_key_not_match"))
        return get_401_response()

    sender_id = content["sender_id"]
    server.logger.info(i18n("flask.say.sender_id", sender_id))

    if is_the_same_sender_id(sender_id):
        server.logger.info(i18n("message_and_broadcast.received_message_from_self"))
        return get_200_response()

    source = content["source"]
    server.logger.info(i18n("flask.say.source", source))
    sender = content["sender"]
    server.logger.info(i18n("flask.say.sender", sender))
    message = content["message"]
    server.logger.info(i18n("flask.say.message", message))

    server.say(f"[{source}] {sender}: {message}")
    return get_200_response()


@flask_app.route("/api/v1/mcserver/broadcast", methods=["POST"])
def broadcast():
    server.logger.info(i18n("flask.received_post", "/api/v1/mcserver/broadcast"))

    if not request.is_json:
        server.logger.error(i18n("flask.request_is_not_json"))
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, "auth_key", "message"):
        server.logger.error(i18n("flask.request_missing_keys_in_json"))
        return get_400_response()

    if not auth_key == content["auth_key"]:
        server.logger.error(i18n("flask.auth_key_not_match"))
        return get_401_response()

    message = content["message"]
    server.logger.info(i18n("flask.say.message", message))

    server.say(f"[{i18n('broadcast')}] {message}")
    return get_200_response()


@new_thread("Flask@RemoteMC-MCDR")
def run_flask(configure: Configure):
    global config, auth_key
    config = configure
    # Start the Flask Server
    host = config.remotemc_mcdr_flask["host"]
    port = int(config.remotemc_mcdr_flask["port"])
    auth_key = config.remotemc["auth_key"]
    server.logger.info(i18n("starting_flask", host, port))
    serve(flask_app, host=host, port=port)
