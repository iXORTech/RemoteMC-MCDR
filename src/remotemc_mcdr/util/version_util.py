import json
import re

from remotemc_mcdr import Configure
from remotemc_mcdr.util.i18n_util import *
from remotemc_mcdr.util.remotemc_core_check_util import RemoteMCCoreStatus, remotemc_core_check

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
version_properties = None


def load_version_properties():
    global version_properties
    with server.open_bundled_file(f"remotemc_mcdr/version.json") as f:
        version_properties = json.load(f)
    server.logger.info(i18n("version_util.file_loaded"))


def get_version_property(value: str) -> str:
    server.logger.info(i18n("version_util.getting_version_property",
                            value, version_properties[value]))
    return version_properties[value]


def get_version() -> str:
    server.logger.info(i18n("version_util.getting_version"))
    version_property = get_version_property("version")
    revision_property = get_version_property("revision")
    revision_property = revision_property.upper()
    stage_property = get_version_property("stage")
    if stage_property == "stable":
        version_property = f"{version_property} ({revision_property})"
        return version_property
    stage_property = re.sub(r"dev", "DEV", stage_property)
    stage_property = re.sub(r"alpha\.", "Alpha ", stage_property)
    stage_property = re.sub(r"alpha", "Alpha", stage_property)
    stage_property = re.sub(r"beta\.", "Beta ", stage_property)
    stage_property = re.sub(r"beta", "Beta", stage_property)
    stage_property = re.sub(r"rc\.", "Release Candidate ", stage_property)
    stage_property = re.sub(r"rc", "Release Candidate", stage_property)
    version_property = f"{version_property} {stage_property} ({revision_property})"
    return version_property


def get_build_date() -> str:
    return get_version_property("build_date")


def get_compatible_status(config: Configure) -> str:
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
