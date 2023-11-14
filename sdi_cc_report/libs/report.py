#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Module docstring
"""

import json
import csv
import requests

# from .text import Text

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2023, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@grandest.fr"
__status__ = "Developement"


class Report(object):
    """Report object.

    Utilisation:

    ``` python
    # charger un rapport
    wfs_report = Report(url=wfs_url, type=wfs_type, title=wfs_name, ssl_verify=True)
    # ou
    wfs_report = Report().load(url=wfs_url, type=wfs_type, title=wfs_name, ssl_verify=True)
    ```

    Liste des propriétés
    ``` python
    wfs_report.ssl_verify             # indique si le certificat doit être vérifié lors de la récupération du rapport
    wfs_report.url                    # URL du rapport
    wfs_report.title                  # titre du rapport
    wfs_report.type                   # type de rapport ('wms, 'wfs', 'csw')
    wfs_report.text                   # text du fichier de rapport
    wfs_report.nb_errors              # nombre de ligne d'erreur dans le rapport
    wfs_report.nb_layers              # nombre de layers dans le rapport
    wfs_report.nb_layers_error        # nombre de layers en erreur dans le rapport
    wfs_report.nb_layers_ok           # nombre de layers sans erreur dans le rapport
    wfs_report.nb_workspaces          # nombre de workspaces dans le rapport
    wfs_report.errors                 # liste de errors du le rapport
    wfs_report.layers                 # liste des layers du rapport
    wfs_report.workspaces             # liste des workspaces du rapport (valable uniquement pour les rapports de type 'wms' et 'wfs')
    ```

    Liste des méthodes publiques
    ``` python
    # méthodes permettant de filtrer respectivement la liste des 'errors', 'layers' et 'workspaces': 'get_errors()', 'get_layers()' et 'get_workspaces()'
    # les filtres sont cumulatifs et ne fonctionnent que de façon descendante : 'errors' > 'layers' > 'workspaces'
    # ainsi, 'get_errors()' va avoir un impact sur les propriétés 'layers' et 'workspaces', mais 'get_workspaces()', n'a pas d'impact sur les propriétés 'layers' et 'errors'
    # les propriétés de compte: 'nb_errors', 'nb_layers', etc. ne sont pas mises à jour et renseignent toujours la valeur globale du rapport
    # Pour obtenir le nombre d'éléments filtrer, utiliser la fonction native 'len()'. Par exemple `ws = len(wfs_report.get_workspaces(filter='edit').workspaces)`
    wfs_report.get_errors(filter='', workspace='', layer='', id='').errors
    wfs_report.get_layers(filter='', workspace='', layer='', id='').layers
    wfs_report.get_workspaces(filter='').workspaces

    # méthodes permettant d'enregistrer respectivement la liste 'errors', 'layers' et 'workspace' sous forme d'un fichier CSV
    wfs_report.save_errors_to_csv(file='')
    wfs_report.save_layers_to_csv(file='')
    wfs_report.save_workspaces_to_csv(file='')
    ```
    """

    ssl_verify = True
    url = None
    title = None
    type = None
    text = None
    nb_errors = 0
    nb_layers = 0
    nb_layers_error = 0
    nb_layers_ok = 0
    nb_workspaces = 0
    errors = []
    layers = []
    workspaces = []

    def __init__(self, url=None, title=None, type=None, ssl_verify=True):
        """Initialize Report object."""
        self.load(url=url, title=title, type=type, ssl_verify=ssl_verify)

    def load(self, url=None, title=None, type=None, ssl_verify=True):
        if title is not None:
            self.title = title
        if type is not None:
            self.type = type.lower() if type is not None else None
        if ssl_verify is not None:
            self.ssl_verify = ssl_verify

        if url is not None:
            self.url = url
            self.errors = self._get_errors(self.url)
            self.layers = self._get_layers()
            self.workspaces = self._get_workspaces()
            self.nb_errors = self._get_nb_errors()
            self.nb_layers = self._get_nb_layers()
            self.nb_layers_error = self._get_nb_layers_error()
            self.nb_layers_ok = self._get_nb_layers_ok()
            self.nb_workspaces = self._get_nb_workspaces()

        return self

    def _get_report_text(self, url=None):
        if url is not None:
            self.url = url

        requests.packages.urllib3.disable_warnings(
            requests.packages.urllib3.exceptions.InsecureRequestWarning
        )
        r = requests.get(self.url, verify=self.ssl_verify)
        if r.status_code == 200:
            return r.text

        return ""

    def is_filter(self, value=None, search=None):
        if search is None or value is None:
            return False

        if search.startswith("*"):
            if search.endswith("*"):
                return search[1:-1] in value
            else:
                return value.endswith(search[1:])
        else:
            if search.endswith("*"):
                return value.startswith(search[:-1])
            else:
                return value == search

    def _get_errors(self, url=None, filter=None, workspace=None, name=None, id=None):
        if url is not None:
            self.url = url

        self.text = self._get_report_text(url=self.url)
        errors_text = [
            error for error in self.text.split("\n\n") if error.startswith("#")
        ]

        errors = []
        for error_text in errors_text:
            # todo: we could use regular expressions to parse text?
            error_lines = error_text.split("\n")
            e_id = int(error_lines[0].lstrip()[1:])
            e_ws = ""
            e_name = error_lines[1].lstrip()[7:]

            if len(error_lines) == 2:
                e_name = e_name[0:-3]

            if self.type in ["wms", "wfs"]:
                e_ws = e_name.split(":")[0]
                e_name = e_name.split(":")[1]

            error = {
                "id": e_id,
                "workspace": e_ws,
                "name": e_name,
                "error": 0,  # todo: what does this mean?
                "error_code": "",
                "message": "",
                "search": "",
            }

            if len(error_lines) > 2:
                error["error"] = 1
                error["message"] = "\n".join(error_lines[2:]).lstrip()[7:]
                message_lower = error["message"].lower()

                if message_lower.startswith("metadata"):
                    error["error_code"] = "ERROR_MD_LINK"
                    if "mismatched tag" in message_lower:
                        error["error_code"] = "ERROR_MD_LINK - mismatched tag"
                    elif "certificate verify failed" in message_lower:
                        error[
                            "error_code"
                        ] = "ERROR_MD_LINK - certificate verify failed"
                    elif "failed to resolve" in message_lower:
                        error["error_code"] = "ERROR_MD_LINK - failed to resolve"
                    elif "http 404" in message_lower:
                        error["error_code"] = "ERROR_MD_LINK - HTTP 404"
                    elif "not well-formed" in message_lower:
                        error["error_code"] = "ERROR_MD_LINK - not well-formed"
                    elif (
                        "Type 'xml.etree.elementtree.element' cannot be serialized"
                        in message_lower
                    ):
                        error[
                            "error_code"
                        ] = "ERROR_MD_LINK - XML element cannot be serialized"

                elif message_lower.startswith("no metadata"):
                    error["error_code"] = "ERROR_NO_MD"
                elif message_lower.startswith("the requested style"):
                    error["error_code"] = "ERROR_STYLE"
                elif (
                    "rendering process failed" in message_lower
                    or "error rendering" in message_lower
                ):
                    error["error_code"] = "ERROR_RENDERING"
                    if "unsupported geometry type" in error["message"]:
                        error[
                            "error_code"
                        ] = "ERROR_RENDERING - unsupported geometry type"

                elif message_lower.startswith("remote layers are not allowed"):
                    error["error_code"] = "REMOTE_LAYER"

            error["search"] = " | ".join(
                [
                    str(error["id"]),
                    error["workspace"],
                    error["name"],
                    error["error_code"],
                    error["message"],
                ]
            )

            errors.append(error)

        if filter and filter is not None:  # todo: second test seems useless
            errors = [error for error in errors if filter in error["search"]]

        if workspace and workspace is not None:
            errors = [
                error
                for error in errors
                if self.is_filter(error["workspace"], workspace)
            ]

        if name and name is not None:
            errors = [error for error in errors if self.is_filter(error["name"], name)]

        if id and id is not None:
            errors = [error for error in errors if error["id"] == id]

        return errors

    def _get_nb_errors(self):
        return len(self.errors)

    def _get_layers(
        self, url=None, errors=None, filter=None, workspace=None, name=None, id=None
    ):
        if url is not None:
            self.errors = self._get_errors(url=url)

        layers = {}
        layers_id = []
        for error in self.errors:
            if error["id"] not in layers_id:
                layers[error["id"]] = {
                    "id": error["id"],
                    "workspace": error["workspace"],
                    "name": error["name"],
                    "error": error["error"],
                    "nb_errors": 0,
                    "errors": [],
                    "search": " | ".join(
                        [str(error["id"]), error["workspace"], error["name"]]
                    ),
                }
                layers_id.append(error["id"])

            if error["error"] == 1:
                layers[error["id"]]["nb_errors"] += 1
                layers[error["id"]]["search"] += (
                    " | " + error["error_code"] + " | " + error["message"]
                )
                layers[error["id"]]["errors"].append(
                    {
                        "error_id": layers[error["id"]]["nb_errors"],
                        "error_code": error["error_code"],
                        "error_message": error["message"],
                    }
                )

        layers = [layers[l] for l in layers]

        if filter and filter is not None:
            layers = [layer for layer in layers if filter in layer["search"]]

        if workspace and workspace is not None:
            layers = [
                layer
                for layer in layers
                if self.is_filter(layer["workspace"], workspace)
            ]

        if name and name is not None:
            layers = [layer for layer in layers if self.is_filter(layer["name"], name)]

        if id and id is not None:
            layers = [layer for layer in layers if layer["id"] == id]

        return layers

    def _get_workspaces(self, workspace=None):
        workspaces = {}
        for layer in self.layers:
            if layer["workspace"] not in workspaces.keys():
                workspaces[layer["workspace"]] = {
                    "id": len(workspaces.keys()),
                    "workspace": layer["workspace"],
                    "nb_errors": 0,
                    "nb_layers": 0,
                    "nb_layers_ok": 0,
                    "nb_layers_error": 0,
                }

            if layer["error"] == 1:
                workspaces[layer["workspace"]]["nb_errors"] += layer["nb_errors"]
                workspaces[layer["workspace"]]["nb_layers_error"] += 1
            else:
                workspaces[layer["workspace"]]["nb_layers_ok"] += 1

            workspaces[layer["workspace"]]["nb_layers"] += 1

        workspaces = [workspaces[ws] for ws in workspaces]

        if workspace and workspace is not None:
            workspaces = [
                ws for ws in workspaces if self.is_filter(ws["workspace"], workspace)
            ]

        return workspaces

    def _get_nb_layers(self):
        return len(self.layers)

    def _get_nb_layers_ok(self):
        layers_ok = [layer for layer in self.layers if layer["error"] == 0]
        return len(layers_ok)

    def _get_nb_layers_error(self):
        layers_error = [layer for layer in self.layers if layer["error"] == 1]
        return len(layers_error)

    def _get_nb_workspaces(self):
        return len(self.workspaces)

    def _save_to_csv(self, file=None, data=None):
        if file is None or data is None or len(data) == 0:
            return False

        keys = data[0].keys()
        with open(file, "w", newline="") as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

        return file

    def get_errors(self, filter=None, workspace=None, name=None, id=None):
        self.errors = self._get_errors(
            filter=filter, workspace=workspace, name=name, id=id
        )
        self.layers = self._get_layers()
        self.workspaces = self._get_workspaces()
        return self

    def get_layers(self, filter=None, workspace=None, name=None, id=None):
        self.errors = self._get_errors()
        self.layers = self._get_layers(
            filter=filter, workspace=workspace, name=name, id=id
        )
        self.workspaces = self._get_workspaces()
        return self

    def get_workspaces(self, filter=None):
        self.errors = self._get_errors()
        self.layers = self._get_layers()
        self.workspaces = self._get_workspaces(workspace=filter)
        return self

    def save_errors_to_csv(self, file=None):
        if file is None or len(self.errors) == 0:
            return False

        return self._save_to_csv(file=file, data=self.errors)

    def save_layers_to_csv(self, file=None):
        if file is None or len(self.layers) == 0:
            return False

        layers = [
            {key: val for key, val in layer.items() if key not in ["errors"]}
            for layer in self.layers
        ]

        return self._save_to_csv(file=file, data=layers)

    def save_workspaces_to_csv(self, file=None):
        if file is None or len(self.workspaces) == 0:
            return False

        return self._save_to_csv(file=file, data=self.workspaces)

    # def dict(self):
    #     return vars(self)

    # def __repr__(self):
    #     return json.dumps(self.dict())

    # def __str__(self):
    #     return json.dumps(self.dict())


if __name__ == "__main__":
    wms_url = "https://www.datagrandest.fr/public/wms-report.log"
    wfs_name = "WFS DataGrandEst"
    wfs_type = "wfs"
    wfs_url = "https://www.datagrandest.fr/public/wfs-report.log"
    csw_name = "CSW DataGrandEst"
    csw_type = "csw"
    csw_url = "https://www.datagrandest.fr/public/csw-report.log"

    # wms_report = Report(url=wms_url, type='wms')
    # print(
    #     wms_report.errors,
    #     wms_report.layers,
    #     wms_report.workspaces,
    #     wms_report.nb_errors,
    #     wms_report.nb_layers,
    #     wms_report.nb_layers_error,
    #     wms_report.nb_layers_ok,
    #     wms_report.nb_workspaces,
    # )

    # csw_report = Report().load(url=csw_url, type=csw_type, title=csw_name)
    # print(
    #     csw_report.errors,
    #     csw_report.layers,
    #     csw_report.workspaces,
    #     csw_report.nb_errors,
    #     csw_report.nb_layers,
    #     csw_report.nb_layers_error,
    #     csw_report.nb_layers_ok,
    #     csw_report.nb_workspaces,
    # )

    wfs_report = Report(url=wfs_url, type=wfs_type, title=wfs_name)
    # print(
    #     wfs_report.errors,
    #     wfs_report.layers,
    #     wfs_report.workspaces,
    #     wfs_report.nb_errors,
    #     wfs_report.nb_layers,
    #     wfs_report.nb_layers_error,
    #     wfs_report.nb_layers_ok,
    #     wfs_report.nb_workspaces,
    # )
    # wfs_report.get_layers(filter='geograndest').save_layers_to_csv(file='wfs_report.csv')

    print(1, len(wfs_report.errors))
    print(2, len(wfs_report.layers))
    print(3, len(wfs_report.workspaces))
    print(4, len(wfs_report.get_errors(workspace="geograndest").layers))
    print(5, len(wfs_report.get_errors(workspace="araa").layers))
    print(6, len(wfs_report.get_layers(workspace="araa").layers))
    print(7, len(wfs_report.get_layers(filter="geograndest").errors))
    print(8, len(wfs_report.get_layers(filter="geograndest").layers))
    print(9, len(wfs_report.workspaces))
    print(10, wfs_report.nb_workspaces)
    print(11, len(wfs_report.get_workspaces(filter="edit").layers))
    print(12, len(wfs_report.workspaces))
    print(13, len(wfs_report.get_workspaces().workspaces))
