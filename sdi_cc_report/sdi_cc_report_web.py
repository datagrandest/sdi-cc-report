import os

from sdi_cc_report import config
from sdi_cc_report.app_web.application import ApplicationWeb


def run(mode='dev'):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(ROOT_DIR, config.__config_file__)

    app = ApplicationWeb(config_file=CONFIG_FILE, mode=mode)
    
    if mode == 'wsgi':
        return app.run()
    
    app.run()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    run(mode)