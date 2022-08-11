import uuid
from remotemc_mcdr.util.i18n_util import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()

sender_id: str


def generate_sender_id():
    global sender_id
    server.logger.info(i18n("sender_id.generating"))
    sender_id = uuid.uuid4().hex.upper()
    server.logger.info(i18n("sender_id.generated", sender_id))
    return sender_id


def get_sender_id():
    return sender_id


def is_the_same_sender_id(received_sender_id: str):
    return received_sender_id == sender_id
