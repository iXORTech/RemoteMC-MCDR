from flask import Flask
from waitress import serve

from mcdreforged.api.all import *

from remotemc_mcdr.util.html_response_util import *
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

# Flask Server App and its configuration
flask_app = Flask(__name__)
flask_app.config['JSON_AS_ASCII'] = False
flask_app.config['JSONIFY_MIMETYPE'] = "application/json; charset=utf-8"
flask_app.config['DEBUG'] = True

@flask_app.route('/ping', methods=["GET"])
def ping():
    return HtmlResponseUtil.get_200_response("PONG!")

@new_thread('Flask@RemoteMC-MCDR')
def run_flask(host: str, port: int):
    # Start the Flask Server
    server.logger.info(i18n('starting_flask', host, port))
    serve(flask_app, host=host, port=port)
