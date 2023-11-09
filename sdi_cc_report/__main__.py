import sys
from master import app_cli  # , app_gui

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "gui":
        # app_gui.run()
        pass
    else:
        app_cli.run()
