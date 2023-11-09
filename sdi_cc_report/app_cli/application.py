#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module docstring
SDI CC Report v1 CLI
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2020, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@grandest.fr"
__status__ = "Developement"


import os
import sys
import time

import click
import click_repl
import prompt_toolkit

from sdi_cc_report.app.application import Application
from sdi_cc_report.app_cli.cli import cli


class ApplicationCli(Application):
    """App class."""

    config_file = None
    config = {}
    title = None
    prompt = ">"
    rprompt = ""
    bindings = None
    history_file = None

    def __init__(self, config_file=None):
        super().__init__(config_file, "cli")

        # Initialize application parameters
        self.title = self.config["app"]["title"] or "APP NAME"
        self.prompt = self.config["cli"]["prompt"] or ">"
        self.rprompt = "Disconnected"

        history_file = self.config["history"]["file"] or "./sdi_cc_report/data/.history"
        self.history_file = os.path.abspath(os.path.join(self.root_dir, history_file))
        if not os.path.isfile(self.history_file):
            with open(self.history_file, "w") as history_file:
                pass

    def get_bottom_toolbar(self):
        now = time.strftime("%d-%m-%Y %H:%M:%S")
        return prompt_toolkit.formatted_text.HTML(
            " {app_title} - time: {datetime}".format(app_title=self.title, datetime=now)
        )

    def get_prompt_text(self):
        return "{prompt} ".format(prompt=self.prompt)

    def get_rprompt_text(self):
        return "{rprompt}".format(rprompt=self.rprompt)

    def cli(self, ctx):
        if ctx.invoked_subcommand is None:
            ctx.invoke(self.cli_repl)

    def cli_repl(self):
        prompt_toolkit.shortcuts.clear()

        style = prompt_toolkit.styles.Style.from_dict(
            {
                "completion-menu.completion": "bg:#008888 #ffffff",
                "completion-menu.completion.current": "bg:#00aaaa #000000",
                "scrollbar.background": "bg:#88aaaa",
                "scrollbar.button": "bg:#222222",
                "prompt": "#339933",
                "prompt.arg.text": "#00aaaa",
                "rprompt": "bg:#ffffff #333333",
                # "bottom-toolbar": "#ffffff bg:#ffffff",
                # "bottom-toolbar.text": "#ffffff bg:#333333",
            }
        )

        prompt_kwargs = {
            "key_bindings": self.bindings,
            "style": style,
            "message": self.get_prompt_text,
            "rprompt": self.get_rprompt_text,
            "bottom_toolbar": self.get_bottom_toolbar,
            "refresh_interval": 0.5,
            "history": prompt_toolkit.history.FileHistory(self.history_file),
            "color_depth": prompt_toolkit.output.color_depth.ColorDepth.DEPTH_24_BIT,
        }
        click_repl.repl(click.get_current_context(), prompt_kwargs=prompt_kwargs)

    def add_logs(self, message="", level="INFO"):
        log_message = self.set_logs(message=message, level=level)
        print("{level} - {message}".format(level=level, message=message))

    def on_exit_app(self):
        self.echo("Goodby!")
        # click_repl.exit()
        sys.exit()

    def echo(self, text=""):
        click.echo(text)

    def input_prompt(self, input_name, input_value, label, is_password):
        if not input_name:
            input_value = prompt_toolkit.prompt(label, is_password=is_password)
        else:
            if input_value is None:
                if not getattr(self, input_name):
                    input_value = prompt_toolkit.prompt(label, is_password=is_password)
                else:
                    input_value = getattr(self, input_name)
            setattr(self, input_name, input_value)
        return input_value

    def run(self):
        cli(obj=self)
