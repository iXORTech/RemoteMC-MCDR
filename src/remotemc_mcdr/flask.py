from flask import Flask, request
from waitress import serve

from mcdreforged.api.all import *

from remotemc_mcdr.util.html_response_util import *
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.json_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

# Flask Server App and its configuration
flask_app = Flask(__name__)
flask_app.config['JSON_AS_ASCII'] = False
flask_app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
flask_app.config['DEBUG'] = True

auth_key: str = None

@flask_app.route('/ping', methods=["GET"])
def ping():
    return HtmlResponseUtil.get_200_response("PONG!")

@flask_app.route('/api/v1/mcserver/execute_command', methods=["POST"])
def execute_command():
    if not request.is_json:
        return HtmlResponseUtil.get_400_response()
    
    content = request.get_json()
    if not is_key_in_json(content, 'auth_key', 'command'):
        return HtmlResponseUtil.get_400_response()
    
    if not auth_key == content['auth_key']:
        return HtmlResponseUtil.get_401_response()
    
    command: str = content['command']
    
    is_rcon_running = server.is_rcon_running()
    if is_rcon_running:
        rcon_info = server.rcon_query(command)
        if rcon_info:
            return HtmlResponseUtil.get_200_response(rcon_info)
        else:
            return HtmlResponseUtil.get_200_response()
    else:
        server.execute_command(command)
        return HtmlResponseUtil.get_200_response(i18n('enable_rcon'))

@new_thread('Flask@RemoteMC-MCDR')
def run_flask(host: str, port: int, auth_key: str):
    # Start the Flask Server
    server.logger.info(i18n('starting_flask', host, port))
    globals()['auth_key'] = auth_key
    serve(flask_app, host=host, port=port)
