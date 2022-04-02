from mcdreforged.api.all import *

from remotemc_mcdr.flask import *
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.config_util import *

config: Configure
server: PluginServerInterface = None

# Load Intergrated Flask Web Server
def load_flask():
    server.logger.info(i18n('loading_flask'))
    run_flask("127.0.0.1", 65362)

def on_load(plugin_server_interface: PluginServerInterface, prev):
    global server, config
    server = plugin_server_interface
    config = load_config(server, server.get_plugin_command_source())
    server.logger.info("==========================================================")
    server.logger.info(i18n('plugin_loaded'))
    VERSION: str = server.get_self_metadata().version.__str__()
    server.logger.info(i18n('version', VERSION))
    if "dev" in VERSION or "alpha" in VERSION or "beta" in VERSION:
        server.logger.info(i18n('logger.warning.experimental'))
    elif "rc" in VERSION:
        server.logger.info(i18n('logger.warning.release_candidate'))
    server.logger.info("==========================================================")
    
def on_server_startup(plugin_server_interface: PluginServerInterface):
    load_flask()
