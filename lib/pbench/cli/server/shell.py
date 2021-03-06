#!/bin/env python3

import subprocess
import sys

from configparser import NoSectionError, NoOptionError

from pbench.common.exceptions import BadConfig, ConfigFileNotSpecified
from pbench.server.api import create_app, get_server_config


def app():
    try:
        server_config = get_server_config()
    except (ConfigFileNotSpecified, BadConfig) as e:
        print(e)
        sys.exit(1)
    return create_app(server_config)


def main():
    try:
        server_config = get_server_config()
    except (ConfigFileNotSpecified, BadConfig) as e:
        print(e)
        sys.exit(1)
    try:
        port = str(server_config.get("pbench-server", "rest_port"))
        host = str(server_config.get("pbench-server", "bind_host"))
        workers = str(server_config.get("pbench-server", "workers"))
    except (NoOptionError, NoSectionError) as e:
        print(f"{__name__}: ERROR: {e.__traceback__}")
        sys.exit(1)

    subprocess.run(
        [
            "gunicorn",
            "--workers",
            workers,
            "--pid",
            "/run/pbench-server/gunicorn.pid",
            "--bind",
            f"{host}:{port}",
            "pbench.cli.server.shell:app()",
        ]
    )
