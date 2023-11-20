#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module docstring
SDI CC REPORT 2023 WEB
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2023, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@grandest.fr"
__status__ = "Developement"


import json
import os
import platform
import sys
import threading
import time
import webbrowser

import bottle

try:
    import webview
except ImportError:
    print("Module 'webview' doesn't install or can't be load. Only 'wsgi' mode enabled.")

from sdi_cc_report.app.application import Application


class ApplicationWeb(Application):
    """App class."""

    mode = None
    config_file = None
    config = {}
    title = None

    _width = 400
    _height = 800

    _server_host = None
    _server_port = None
    _server_url = None
    _ui_host = None
    _ui_port = None
    _ui_url = None

    _cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "X-Token, Authorization, Origin, Accept, Content-Type, X-Requested-With",
        # 'Access-Control-Expose-Headers': 'X-My-Custom-Header, ...',
        # 'Access-Control-Max-Age': '86400',
        # 'Access-Control-Allow-Credentials': 'true',
    }

    def __init__(
        self,
        config_file=None,
        mode="dev",
        server_host=None,
        server_port=None,
        ui_host=None,
        ui_port=None,
        debug=False,
    ):
        super().__init__(config_file, "web")

        self.mode = mode
        self._server_host = server_host or self.config["web"]["server_host"]
        self._server_port = server_port or self.config["web"]["server_port"]
        self._server_url = "http://{host}:{port}".format(
            host=self._server_host, port=self._server_port
        )
        self._ui_host = ui_host or self.config["web"]["ui_host"]
        self._ui_port = ui_port or self.config["web"]["ui_port"]
        self._ui_url = "http://{host}:{port}".format(host=self._ui_host, port=self._ui_port)
        self._debug = debug
        self._width = self.config["web"]["width"]
        self._height = self.config["web"]["height"]

        self._app = bottle.Bottle()

        self._route()
        self._hook()

        # Initialize application parameters
        self._title = self.config["app"]["title"] or "APP NAME"

    def add_logs(self, message="", level="INFO"):
        log_message = self.set_logs(message=message, level=level)
        print("{level} - {message}".format(level=level, message=message))

    def on_exit_app(self):
        self.echo("Goodby!")
        sys.exit()

    def echo(self, text=""):
        print(text)

    # TODO: still used ?
    def on_close(self, mode=None):
        print("close")
        pass

    def _open_browser(self, url=None):
        url = url or self._server_url or self._ui_url
        webbrowser.open_new(url)

    def _hook(self):
        self._app.add_hook("before_request", self._hook_handle_options)
        self._app.add_hook("after_request", self._hook_enable_cors)

    def _route(self):
        self._app.route("/", method="GET", callback=self._route_index)
        self._app.route("/reports", method="GET", callback=self._route_reports)
        self._app.route("/reports/", method="GET", callback=self._route_reports)
        self._app.route("/reports/<report:int>", method="GET", callback=self._route_reports)
        self._app.route("/errors", method="GET", callback=self._route_errors)
        self._app.route("/errors/", method="GET", callback=self._route_errors)
        self._app.route("/errors/<report:int>", method="GET", callback=self._route_errors)
        self._app.route("/layers", method="GET", callback=self._route_layers)
        self._app.route("/layers/", method="GET", callback=self._route_layers)
        self._app.route("/layers/<report:int>", method="GET", callback=self._route_layers)
        self._app.route("/workspaces", method="GET", callback=self._route_ws)
        self._app.route("/workspaces/", method="GET", callback=self._route_ws)
        self._app.route("/workspaces/<report:int>", method="GET", callback=self._route_ws)

        self._app.route("/hello", callback=self._route_hello)
        self._app.route("/hello/", callback=self._route_hello)
        self._app.route("/hello/<name>", callback=self._route_hello)

        self._app.route("/<filename:path>", method="GET", callback=self._route_static)

    def _hook_handle_options(self):
        if bottle.request.method == "OPTIONS":
            # Bypass request routing and immediately return a response
            raise bottle.HTTPResponse(headers=self._cors_headers)

    def _hook_enable_cors(self):
        """Add headers to enable CORS"""
        for key, value in self._cors_headers.items():
            bottle.response.set_header(key, value)

    def _send_response(self, code=200, content="", format="json"):
        formats = {
            "json": "application/json",
            "text": "text/plain",
            "html": "text/html",
            "xml": "text/xml",
        }

        bottle.response.status = code
        bottle.response.headers["Content-Type"] = formats[format]

        if format == "json":
            return json.dumps(content)

        return content

    def _route_index(self):
        # TODO: chemin à mettre dans un fichier de config... web_ui_path ou directory
        file = os.path.join(os.getcwd(), "sdi_cc_report", "app_web", "ui", "dist", "index.html")
        return bottle.template(file)

    def _route_hello(self, name="Guest"):
        return "Hello {name}, how are you?".format(name=name)

    def _route_static(self, filename="index.html"):
        return bottle.static_file(
            filename,
            root=os.path.join(os.getcwd(), "sdi_cc_report", "app_web", "ui", "dist"),
        )

    def _route_reports(self, report=None):
        """
        Get list of items
        """
        reports = self.config["reports"]

        if report is not None:
            report = reports[report]
            data = self.get_report_summary(report=report)
            data["report_name"] = report["name"]
            data["report_type"] = report["type"]
            data["report_url"] = report["url"]
            return self._send_response(code=200, content=[data], format="json")

        else:
            # Add id value for each file report line
            for id, report in enumerate(reports):
                reports[id]["id"] = id
            return self._send_response(code=200, content=reports, format="json")

        return []

    def _route_errors(self, report=0):
        """ """
        params = bottle.request.params
        search = params["search"] if "search" in params else None
        workspace = params["ws"] if "ws" in params else None
        name = params["name"] if "name" in params else None
        id = params["id"] if "id" in params else None
        limit = params["limit"] if "limit" in params else None
        offset = params["offset"] if "offset" in params else None
        details = params["details"] if "details" in params else None

        report = self.config["reports"][report]
        data = self.get_errors(report=report, filter=search, workspace=workspace, name=name, id=id)

        if offset is not None or limit and limit is not None:
            offset = 0 if offset is None else offset
            limit = 10000 if limit is None else limit
            data["errors"] = data["errors"][int(offset) : int(limit)]

        if details and details is not None:
            data["report"] = report
            data["search"] = search
            data["workspace"] = workspace
            data["name"] = name
            data["id"] = id
            data["limit"] = limit
            data["offset"] = offset
            data["nb_errors_return"] = len(data["errors"])
            return data

        else:
            return self._send_response(code=200, content=data["errors"], format="json")

    def _route_layers(self, report=0):
        """ """
        params = bottle.request.params
        search = params["search"] if "search" in params else None
        workspace = params["ws"] if "ws" in params else None
        name = params["name"] if "name" in params else None
        id = params["id"] if "id" in params else None
        limit = params["limit"] if "limit" in params else None
        offset = params["offset"] if "offset" in params else None
        details = params["details"] if "details" in params else None

        report = self.config["reports"][report]
        data = self.get_layers(report=report, filter=search, workspace=workspace, name=name, id=id)

        if offset is not None or limit and limit is not None:
            offset = 0 if offset is None else offset
            limit = 10000 if limit is None else limit
            data["layers"] = data["layers"][int(offset) : int(limit)]

        if details and details is not None:
            data["report"] = report
            data["search"] = search
            data["workspace"] = workspace
            data["name"] = name
            data["id"] = id
            data["limit"] = limit
            data["offset"] = offset
            data["nb_layers_return"] = len(data["layers"])
            return data

        else:
            return self._send_response(code=200, content=data["layers"], format="json")

    def _route_ws(self, report=0):
        """ """

        report = self.config["reports"][report]
        if report["type"].lower() not in ["wms", "wfs"]:
            response = {"message": "/wokspaces enable only for WMS and WFS report type."}
            self._send_response(code=404, content=response, format="json")

        params = bottle.request.params
        search = params["search"] if "search" in params else None
        limit = params["limit"] if "limit" in params else None
        offset = params["offset"] if "offset" in params else None
        details = params["details"] if "details" in params else None

        data = self.get_workspaces(report=report, filter=search)

        if offset is not None or limit and limit is not None:
            offset = 0 if offset is None else offset
            limit = 10000 if limit is None else limit
            data["workspaces"] = data["workspaces"][int(offset) : int(limit)]

        if details and details is not None:
            data["report"] = report
            data["search"] = search
            data["limit"] = limit
            data["offset"] = offset
            data["nb_workspaces_return"] = len(data["workspaces"])
            return data

        else:
            return self._send_response(code=200, content=data["workspaces"], format="json")

    def start_bottle_server(self):
        self._app.run(host=self._server_host, port=self._server_port, debug=self._debug)

    def run(self, mode=None):
        self.mode = mode or self.mode

        if self.mode == "wsgi":  # deploy as wsgi application
            return self._app

        elif self.mode == "browser":  # open in browser
            self._debug = True
            # TODO: faire en sorte que l'on puisse arréter le serveur qui démarre dans un Thead...
            serverthread = threading.Thread(target=self._open_browser, args=[self._ui_url])
            serverthread.start()
            self.start_bottle_server()

        elif self.mode == "dev":  # open in webview
            self._debug = True
            serverthread = threading.Thread(target=self.start_bottle_server)
            serverthread.daemon = True
            serverthread.start()
            webview.create_window(
                self._title, url=self._ui_url, width=self._width, height=self._height
            )
            webview.start(debug=self._debug, server=self._app)
            sys.exit()

        else:  # prod
            serverthread = threading.Thread(target=self.start_bottle_server)
            serverthread.daemon = True
            serverthread.start()
            webview.create_window(
                self._title,
                url=self._server_url,
                width=self._width,
                height=self._height,
            )
            webview.start(
                debug=self._debug,
                server=self._app,
                server_args={"host": self._server_host, "port": self._server_port},
            )
            sys.exit()
