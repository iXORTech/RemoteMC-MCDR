from flask import Flask, request
from waitress import serve
from mcstatus import JavaServer

from remotemc_mcdr.util.html_response_util import *
from remotemc_mcdr.util.config_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

# Flask Server App and its configuration
flask_app = Flask(__name__)
flask_app.config['JSON_AS_ASCII'] = False
flask_app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
flask_app.config['DEBUG'] = True

config: Configure

auth_key: str = None


@flask_app.route('/ping', methods=["GET"])
def ping():
    return get_200_response("PONG!")


@flask_app.route('/api/v1/mcserver/status', methods=["GET"])
def status():
    minecraft_server = JavaServer.lookup(f"{config.minecraft_server['host']}:{config.minecraft_server['port']}")
    query = minecraft_server.query()
    message = "{0}\n{1}{2}\n{3}[{4}/{5}]".format(
        i18n('status.server_running'),  # {0}
        i18n('status.game_version'),  # {1}
        query.software.version,  # {2}
        i18n('status.player_online'),  # {3}
        query.players.online,  # {4}
        query.players.max)  # {5}
    for player in query.players.names:
        message = message + "\n> {0}".format(player)
    return get_200_response(message)


@flask_app.route('/api/v1/mcserver/execute_command', methods=["POST"])
def execute_command():
    if not request.is_json:
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, 'auth_key', 'command'):
        return get_400_response()

    if not auth_key == content['auth_key']:
        return get_401_response()

    command: str = content['command']

    is_rcon_running = server.is_rcon_running()
    if is_rcon_running:
        rcon_info = server.rcon_query(command)
        if rcon_info:
            return get_200_response(rcon_info)
        else:
            return get_200_response()
    else:
        server.execute_command(command)
        return get_200_response(i18n('enable_rcon'))


@flask_app.route('/api/v1/mcserver/send_message', methods=["POST"])
def say():
    if not request.is_json:
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, 'auth_key', 'source', 'sender', 'message'):
        return get_400_response()

    if not auth_key == content['auth_key']:
        return get_401_response()

    source = content['source']
    sender = content['sender']
    message = content['message']

    server.say(f"[{source}] {sender}: {message}")
    return get_200_response()


@flask_app.route('/api/v1/mcserver/broadcast', methods=["POST"])
def broadcast():
    if not request.is_json:
        return get_400_response()

    content = request.get_json()
    if not is_key_in_json(content, 'auth_key', 'message'):
        return get_400_response()

    if not auth_key == content['auth_key']:
        return get_401_response()

    message = content['message']

    server.say(f"[{i18n('broadcast')}] {message}")
    return get_200_response()


@new_thread('Flask@RemoteMC-MCDR')
def run_flask(configure: Configure):
    global config, auth_key
    config = configure
    # Start the Flask Server
    host = config.remotemc_mcdr_flask['host']
    port = int(config.remotemc_mcdr_flask['port'])
    auth_key = config.remotemc['auth_key']
    server.logger.info(i18n('starting_flask', host, port))
    serve(flask_app, host=host, port=port)
