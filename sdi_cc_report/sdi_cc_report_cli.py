import os

from sdi_cc_report import config
from sdi_cc_report.app_cli.application import ApplicationCli


def run():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(ROOT_DIR, config.__config_file__)

    app = ApplicationCli(config_file=CONFIG_FILE)
    app.run()


if __name__ == "__main__":
    run()
