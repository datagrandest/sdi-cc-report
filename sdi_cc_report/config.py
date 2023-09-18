__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2022, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@grandest.fr"
__status__ = "Developement"

__config_file__ = "config.yaml"

__config_default__ = {
  "app": {
    "name": "SDI CC Report",
    "title": "SDI CC Report",
    "width": 500,
    "height": 800,
    "theme": "breeze",
    "device": "desktop"
  },
  "locales": {
    "directory": "./sdi_cc_report/locales/",
    "lang": "fr"
  },
  "history": {
    "file": "./sdi_cc_report/data/.history",
    "clear_on_exit": False
  },
  "cli": {
    "prompt": ">"
  },
  "log": {
    "log_file": "./sdi_cc_report/data/log.txt"
  }
}

__app_name__ = "SDI CC Report"
__package_name__ = "sdi_cc_report"
