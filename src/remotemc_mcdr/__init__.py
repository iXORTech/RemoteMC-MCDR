from mcdreforged.api.all import *

from remotemc_mcdr.flask import *
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = None

# Load Intergrated Flask Web Server
def load_flask():
    server.logger.info(i18n('loading_flask'))
    run_flask("127.0.0.1", 65362)

def on_load(plugin_server_interface: PluginServerInterface, prev):
    global server
    server = plugin_server_interface
    server.logger.info("==========================================================")
    server.logger.info("RemoteMC-MCDR Plugin Loaded")
    VERSION: str = server.get_self_metadata().version.__str__()
    server.logger.info(f"Version: {VERSION}")
    if "dev" in VERSION or "alpha" in VERSION or "beta" in VERSION:
        server.logger.info("THIS IS IN EXPERIMENTAL STAGE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    elif "rc" in VERSION:
        server.logger.info("THIS IS A RELEASE CANDIDATE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    server.logger.info("==========================================================")
    
def on_server_startup(plugin_server_interface: PluginServerInterface):
    load_flask()
