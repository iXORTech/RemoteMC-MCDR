from enum import Enum

import requests

from remotemc_mcdr.util.version_util import *


class RemoteMCCoreStatus(Enum):
    IS_COMPATIBLE = 0
    INCOMPATIBLE = 1
    UNKNOWN_ERROR = 2
    NOT_CONNECTED = 3


def remotemc_core_check(host: str, port: int, ssl: bool) -> RemoteMCCoreStatus:
    try:
        response = requests.get(f"http{'s' if ssl else ''}://{host}:{port}/ping",
                                json={'module': 'remotemc_mcdr',
                                      'version': get_version_property("version"),
                                      'stage': get_version_property("stage"),
                                      'revision': get_version_property("revision")})
        if response.status_code == 200:
            return RemoteMCCoreStatus.IS_COMPATIBLE
        elif response.status_code == 426:
            return RemoteMCCoreStatus.INCOMPATIBLE
        else:
            return RemoteMCCoreStatus.UNKNOWN_ERROR
    except requests.exceptions.ConnectionError:
        return RemoteMCCoreStatus.NOT_CONNECTED
