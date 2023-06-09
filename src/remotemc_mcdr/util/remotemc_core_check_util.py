from enum import Enum

import requests

from remotemc_mcdr.util.version_util import get_version_property


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


def get_compatible_status(config) -> str:
    remotemc_core_host = config.remotemc_core["host"]
    remotemc_core_port = int(config.remotemc_core["port"])
    remotemc_core_ssl = True if config.remotemc_core["ssl"].lower() == "true" else False
    remotemc_core_check_status = remotemc_core_check(remotemc_core_host, remotemc_core_port, remotemc_core_ssl)

    compatible_status = None
    if remotemc_core_check_status == RemoteMCCoreStatus.IS_COMPATIBLE:
        compatible_status = "Compatible"
    elif remotemc_core_check_status == RemoteMCCoreStatus.INCOMPATIBLE:
        compatible_status = "Incompatible"
    elif remotemc_core_check_status == RemoteMCCoreStatus.UNKNOWN_ERROR:
        compatible_status = "Unknown Error"
    elif remotemc_core_check_status == RemoteMCCoreStatus.NOT_CONNECTED:
        compatible_status = "Not Connected"
    return compatible_status
