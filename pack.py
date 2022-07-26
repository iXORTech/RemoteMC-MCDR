import os
import json

version = "0.0.1"
stage = "dev"
revision = "0000000"
with os.popen("git rev-parse --short=7 HEAD") as f:
    revision = f.readline().strip()

version_properties = {
    "version": version,
    "stage": stage,
    "revision": revision
}

version_properties_obj = json.dumps(version_properties)
version_properties_file = "src/remotemc_mcdr/version.json"

with open(version_properties_file, "w") as f:
    f.write(version_properties_obj)
    f.close()

os.chdir(f"{os.getcwd()}/src")
os.system("python3 -m mcdreforged pack")
