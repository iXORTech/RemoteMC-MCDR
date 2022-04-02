__credits__ = ["KevinZonda", "alex3236"]

import json
from threading import Lock
from traceback import print_exc

import requests
from mcdreforged.api.all import *

from remotemc_mcdr.util.i18n_util import *

json_cache = {}
json_cache_lock = Lock()


def is_key_in_json(json, *keys):
    """
    Check if a key exists in a JSON object.
    :param json: JSON object
    :param keys: keys to check
    :return: True if all keys exist, False otherwise
    """
    key_iter = iter(keys)
    for key in key_iter:
        if not key in json:
            return False
    return True


def parse_json(psi: PluginServerInterface, addr, path):
    try:
        req = requests.get(addr, timeout=5).text
    except requests.exceptions:
        print_exc()
        return i18n('json_failed')
    try:
        req_json = json.loads(req)
        for i in path.strip().split('/'):
            req_json = req_json.get(i, dict())
        return req_json
    except ValueError:
        psi.plugin_server_interface.logger.error(i18n('json_parsing_error'))
        print_exc()
        return req


@new_thread('RemoteMC-MCDR')
def update_json_cache(psi: PluginServerInterface, json_list):
    global json_cache_lock, json_cache
    acquired = json_cache_lock.acquire(blocking=False)
    if not acquired:
        return
    for i in json_list:
        _ = json_list[i]
        json_cache[i] = RTextList(_['prefix'], ' ', parse_json(psi, _['addr'], _['path']))
    json_cache_lock.release()
    