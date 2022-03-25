from mcdreforged.api.all import *

def on_load(server: PluginServerInterface, prev):
    server.logger.info("==========================================================")
    server.logger.info("RemoteMC-MCDR Plugin Loaded")
    VERSION: str = server.get_self_metadata().version.__str__()
    server.logger.info(f"Version: {VERSION}")
    if "dev" in VERSION or "alpha" in VERSION or "beta" in VERSION:
        server.logger.info("THIS IS IN EXPERIMENTAL STAGE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    elif "rc" in VERSION:
        server.logger.info("THIS IS A RELEASE CANDIDATE, DO NOT USE IN PRODUCTION ENVIRONMENT!")
    server.logger.info("==========================================================")
