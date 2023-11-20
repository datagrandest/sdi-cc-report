#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
import click_repl

from sdi_cc_report.app_cli import display


def on_clear():
    """
    Clear screen
    > report clear
    """
    click.clear()


def on_exit(app):
    """
    Exit
    > report exit
    """
    if app.config["history"]["clear_on_exit"]:
        if os.path.isfile(app.config["history"]["file"]):
            os.remove(app.config["history"]["file"])

    app.echo("Goodby!")
    click_repl.exit()


def on_test(app):
    """
    Function for test
    > report connect LOGIN PASSWORD
    """
    app.echo("test")


def on_clear_history(app):
    """
    clear history file
    > report clear_history
    """
    if os.path.isfile(app.config["history"]["file"]):
        os.remove(app.config["history"]["file"])


def on_reports(app, files, csv, export):
    """
    Display files report list
    > report reports [FILES]
    """
    result = []
    reports = app.config["reports"]
    files = (
        [int(i.strip()) for i in ",".join(files).split(",")]
        if files and files is not None and len(files) > 0
        else files
    )

    if files and files is not None:
        for file in files:
            if file < len(reports):
                data = app.get_report_summary(report=reports[file])
                result.extend(display.print_report_summary(app, report=reports[file], data=data))
            else:
                result.append("")
                result.append("ERROR: file indice {file} doesn" "t exist".format(file=file))
    else:
        result.extend(display.print_reports_list(app, reports, files, title="Liste des fichiers"))

    if csv:
        app.save_data_to_csv(csv, [data])

    if export:
        with open(export, "w") as f:
            result_text = "\n".join(result)
            f.write(result_text)

    result_text = "\n".join(result)
    app.echo(result_text)


def on_errors(app, file, csv, search, workspace, name, id, limit, export):
    """
    > errors [FILE] [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des erreurs du rapport [FILE]
    """
    if not file or file is None or len(file) == 0:
        app.echo("")
        app.echo("ERROR: [FILE] argument is missing.")
        display.print_reports_list(
            app,
            app.config["reports"],
            title="Thanks to indicate a [FILE] id.",
            echo=True,
        )
        sys.exit()

    result = []
    file = [int(i.strip()) for i in ",".join(file).split(",")][0]
    report = app.config["reports"][file]

    data = app.get_errors(report=report, filter=search, workspace=workspace, name=name, id=id)
    result.extend(
        display.print_errors(
            app,
            report,
            data,
            limit,
            search=search,
            workspace=workspace,
            name=name,
            id=id,
        )
    )

    if csv:
        app.save_data_to_csv(csv, data["errors"])

    if export:
        with open(export, "w") as f:
            result_text = "\n".join(result)
            f.write(result_text)

    result_text = "\n".join(result)
    app.echo(result_text)


def on_layers(app, file, csv, search, workspace, name, id, limit, export):
    """
    > layers [FILE] [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des layers du rapport [FILE]
    """
    if not file or file is None or len(file) == 0:
        app.echo("")
        app.echo("ERROR: [FILE] argument is missing.")
        display.print_reports_list(
            app,
            app.config["reports"],
            title="Thanks to indicate a [FILE] id.",
            echo=True,
        )
        sys.exit()

    result = []
    file = [int(i.strip()) for i in ",".join(file).split(",")][0]
    report = app.config["reports"][file]

    if id:
        data = app.get_layers(report=report, id=id)
        data_errors = data["layers"][0]["errors"]
        result.extend(display.print_layers(app, report, data, id=id))
        result.extend(display.print_layer_errors(app, report, data_errors or []))

    else:
        data = app.get_layers(report=report, filter=search, workspace=workspace, name=name)
        result.extend(
            display.print_layers(
                app, report, data, limit, search=search, workspace=workspace, name=name
            )
        )

    if csv:
        app.save_data_to_csv(csv, data["layers"])

    if export:
        with open(export, "w") as f:
            result_text = "\n".join(result)
            f.write(result_text)

    result_text = "\n".join(result)
    app.echo(result_text)


def on_workspaces(app, file, csv, search, limit, export):
    """
    > ws [FILE] [--csv CSV] [--search SEARCH] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des workspaces du rapport [FILE]
    """

    if not file or file is None or len(file) == 0:
        app.echo()
        app.echo("ERROR: [FILE] argument is missing.")
        display.print_reports_list(
            app,
            app.config["reports"],
            title="Thanks to indicate a [FILE] id.",
            echo=True,
        )
        sys.exit()

    file = [int(i.strip()) for i in ",".join(file).split(",")][0]
    report = app.config["reports"][file]

    if report["type"].lower() not in ["wms", "wfs"]:
        app.echo()
        app.echo('ERROR: "ws" command works only on WMS and WFS report type.')
        app.echo()
        sys.exit()

    result = []
    data = app.get_workspaces(report=report, filter=search)
    result.extend(display.print_workspaces(app, report, data, limit, search))

    if csv:
        app.save_data_to_csv(csv, data["workspaces"])

    if export:
        with open(export, "w") as f:
            result_text = "\n".join(result)
            f.write(result_text)

    result_text = "\n".join(result)
    app.echo(result_text)


def on_dashboard(app, file, workspace, destination, template):
    """

    Générer un tableau de bord pour le rapport selectionné
    """

    if not file or file is None or len(file) == 0:
        app.echo()
        app.echo("ERROR: [FILE] argument is missing.")
        display.print_reports_list(
            app,
            app.config["reports"],
            title="Thanks to indicate a [FILE] id.",
            echo=True,
        )
        sys.exit()

    file = [int(i.strip()) for i in ",".join(file).split(",")][0]
    report = app.config["reports"][file]

    if workspace and workspace is not None and report["type"].lower() not in ["wms", "wfs"]:
        app.echo()
        app.echo('ERROR: "--workspace" option works only on WMS and WFS report type.')
        app.echo()
        sys.exit()

    result = app.generate_dashboard(
        report=report, workspace=workspace, destination=destination, template=template
    )

    result_text = "\n".join(result)
    app.echo(result_text)
