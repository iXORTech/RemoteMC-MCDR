import json
import re

from mcdreforged.api.all import *

server: PluginServerInterface = ServerInterface.get_instance().as_plugin_server_interface()
version_properties = None


def load_version_properties():
    global version_properties
    with server.open_bundled_file(f"remotemc_mcdr/version.json") as f:
        version_properties = json.load(f)


def get_version_property(value: str) -> str:
    return version_properties[value]


def get_version() -> str:
    version_property = get_version_property("version")
    stage_property = get_version_property("stage")
    stage_property = re.sub(r"dev", "DEV", stage_property)
    stage_property = re.sub(r"alpha\.", "Alpha ", stage_property)
    stage_property = re.sub(r"alpha", "Alpha", stage_property)
    stage_property = re.sub(r"beta\.", "Beta ", stage_property)
    stage_property = re.sub(r"beta", "Beta", stage_property)
    stage_property = re.sub(r"rc\.", "Release Candidate ", stage_property)
    stage_property = re.sub(r"rc", "Release Candidate", stage_property)
    revision_property = get_version_property("revision")
    revision_property = revision_property.upper()
    return f"{version_property} {stage_property} ({revision_property})"
