from tabulate import tabulate


def print_reports_list(app, reports, files=None, title=None, echo=False):
    nb_total_reports = len(reports)
    nb_display_reports = nb_total_reports

    # Add id value for each file report line
    for id, report in enumerate(reports):
        reports[id]["id"] = id

    headers = ["ID", "NAME", "TYPE", "URL"]

    # Get table data according file parameter
    if files and files is not None:
        data = [
            [
                reports[i]["id"],
                reports[i]["name"],
                reports[i]["type"],
                reports[i]["url"],
            ]
            for i in files
            if i < nb_total_reports
        ]
        nb_display_reports = len(data)
    else:
        data = [
            [
                reports[i]["id"],
                reports[i]["name"],
                reports[i]["type"],
                reports[i]["url"],
            ]
            for i in range(0, nb_total_reports)
        ]

    table = tabulate(data, headers, tablefmt="pretty")

    # Display data table
    result = []
    result.append("")
    if title and title is not None:
        result.append(title)
    result.append(
        "Nb. reports: {nb_display_reports}/{nb_total_reports}".format(
            nb_display_reports=nb_display_reports, nb_total_reports=nb_total_reports
        )
    )
    if nb_display_reports > 0:
        result.append(table)
    else:
        result.append(
            "Aucun fichier à afficher. Merci de vérifier les paramètres indiqués."
        )
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result


def print_report_summary(app, report, data, title=None, echo=False):
    # Get table data
    data = [[key, value] for key, value in data.items()]
    table = tabulate(
        data, tablefmt="pretty", colalign=("left", "right"), maxcolwidths=[30, 8]
    )

    # Display data table
    result = []
    result.append("")
    if title and title is not None:
        result.append(title)
        result.append("")
    result.append("Report name: {report_name}".format(report_name=report["name"]))
    result.append("Report type: {report_type}".format(report_type=report["type"]))
    result.append("Report URL: {report_url}".format(report_url=report["url"]))
    result.append("")
    result.append("Summary:")
    result.append(table)
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result


def print_errors(
    app,
    report,
    data,
    limit=None,
    search=None,
    workspace=None,
    name=None,
    id=None,
    echo=False,
):
    # Get headers, columns and data
    if report["type"].lower() in ["wms", "wfs"]:
        headers = ["ID", "WORKSPACE", "NAME", "STATUS", "ERROR CODE", "MESSAGE"]
        colalign = ("right", "left", "left", "center", "left", "left")
        maxcolwidths = [5, 20, 20, 8, 15, 60]
        data_errors = [
            [
                d["id"],
                d["workspace"],
                d["name"],
                "OK" if d["error"] == 0 else "ERROR",
                d["error_code"],
                d["message"],
            ]
            for d in data["errors"]
        ]
    else:
        headers = ["ID", "NAME", "STATUS", "ERROR CODE", "MESSAGE"]
        colalign = ("right", "left", "center", "left", "left")
        maxcolwidths = [5, 20, 8, 15, 60]
        data_errors = [
            [
                d["id"],
                d["name"],
                "OK" if d["error"] == 0 else "ERROR",
                d["error_code"],
                d["message"],
            ]
            for d in data["errors"]
        ]

    nb_total_errors = data["nb_errors"]
    nb_display_errors = len(data_errors)

    # Display data table
    result = []
    result.append("")
    result.append("Report name: {report_name}".format(report_name=report["name"]))
    result.append("Report type: {report_type}".format(report_type=report["type"]))
    result.append("Report URL: {report_url}".format(report_url=report["url"]))
    result.append("")
    result.append(
        "Nb. errors: {nb_display_errors}/{nb_total_errors}".format(
            nb_display_errors=nb_display_errors, nb_total_errors=nb_total_errors
        )
    )
    if search and search is not None:
        result.append("Search parameter: {search}".format(search=search))
    if workspace and workspace is not None:
        result.append("Workspace parameter: {workspace}".format(workspace=workspace))
    if name and name is not None:
        result.append("Name parameter: {name}".format(name=name))
    if id and id is not None:
        result.append("Id parameter: {id}".format(id=id))
    if limit and limit is not None:
        data_errors = data_errors[0 : int(limit)]
        result.append("Limit parameter: {limit}".format(limit=limit))
    if nb_display_errors > 0:
        result.append("Errors:")
        table = tabulate(
            data_errors,
            headers,
            tablefmt="grid",
            colalign=colalign,
            maxcolwidths=maxcolwidths,
        )
        result.append(table)
    else:
        result.append("")
        result.append("No layer to display")
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result


def print_layers(
    app,
    report,
    data,
    limit=None,
    search=None,
    workspace=None,
    name=None,
    id=None,
    echo=False,
):
    # Get headers, columns and data
    if report["type"].lower() in ["wms", "wfs"]:
        headers = ["ID", "WORKSPACE", "NAME", "STATUS", "NB ERRORS"]
        colalign = ("right", "left", "left", "center", "right")
        data_layers = [
            [
                d["id"],
                d["workspace"],
                d["name"],
                "OK" if d["nb_errors"] == 0 else "ERROR",
                d["nb_errors"],
            ]
            for d in data["layers"]
        ]
    else:
        headers = ["ID", "NAME", "STATUS", "NB ERRORS"]
        colalign = ("right", "left", "center", "right")
        data_layers = [
            [
                d["id"],
                d["name"],
                "OK" if d["nb_errors"] == 0 else "ERROR",
                d["nb_errors"],
            ]
            for d in data["layers"]
        ]

    nb_total_layers = data["nb_layers"]
    nb_display_layers = len(data["layers"])

    # Display data table
    result = []
    result.append("")
    result.append("Report name: {report_name}".format(report_name=report["name"]))
    result.append("Report type: {report_type}".format(report_type=report["type"]))
    result.append("Report URL: {report_url}".format(report_url=report["url"]))
    result.append("")
    result.append(
        "Nb. layers: {nb_display_layers}/{nb_total_layers}".format(
            nb_display_layers=nb_display_layers, nb_total_layers=nb_total_layers
        )
    )
    if search and search is not None:
        result.append("Search parameter: {search}".format(search=search))
    if workspace and workspace is not None:
        result.append("Workspace parameter: {workspace}".format(workspace=workspace))
    if name and name is not None:
        result.append("Name parameter: {name}".format(name=name))
    if id and id is not None:
        result.append("Id parameter: {id}".format(id=id))
    if limit and limit is not None:
        data_layers = data_layers[0 : int(limit)]
        result.append("Limit parameter: {limit}".format(limit=limit))
    if nb_display_layers > 0:
        result.append("Layers:")
        table = tabulate(data_layers, headers, tablefmt="pretty", colalign=colalign)
        result.append(table)
    else:
        result.append("")
        result.append("No layer to display")
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result


def print_layer_errors(app, report, data, echo=False):
    # Get headers, columns and data
    headers = ["ID", "CODE", "MESSAGE"]
    colalign = ("right", "left", "left")
    maxcolwidths = [5, 20, 80]
    data_errors = [[d["error_id"], d["error_code"], d["error_message"]] for d in data]

    # Display data table
    result = []
    if len(data_errors) > 0:
        table = tabulate(
            data_errors,
            headers,
            tablefmt="grid",
            colalign=colalign,
            maxcolwidths=maxcolwidths,
        )
        result.append("Errors:")
        result.append(table)
    else:
        result.append("No error to display")
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result


def print_workspaces(app, report, data, limit=None, search=None, echo=False):
    # Get headers, columns and data
    headers = [
        "ID",
        "WORKSPACE",
        "STATUS",
        "NB ERRORS",
        "NB LAYERS",
        "NB LAYERS OK",
        "NB LAYERS ERROR",
    ]
    colalign = ("right", "left", "center", "right", "right", "right", "right")
    data_ws = [
        [
            d["id"],
            d["workspace"],
            "OK" if d["nb_errors"] == 0 else "ERROR",
            d["nb_errors"],
            d["nb_layers"],
            d["nb_layers_ok"],
            d["nb_layers_error"],
        ]
        for d in data["workspaces"]
    ]

    nb_total_ws = data["nb_workspaces"]
    nb_display_ws = len(data_ws)

    # Display data table
    result = []
    result.append("")
    result.append("Report name: {report_name}".format(report_name=report["name"]))
    result.append("Report type: {report_type}".format(report_type=report["type"]))
    result.append("Report URL: {report_url}".format(report_url=report["url"]))
    result.append("")
    result.append(
        "Nb. workspaces: {nb_display_ws}/{nb_total_ws}".format(
            nb_display_ws=nb_display_ws, nb_total_ws=nb_total_ws
        )
    )
    if search and search is not None:
        result.append("Search parameter: {search}".format(search=search))
    if limit and limit is not None:
        data_ws = data_ws[0 : int(limit)]
        result.append("Limit parameter: {limit}".format(limit=limit))
    if nb_display_ws > 0:
        result.append("Workspaces:")
        table = tabulate(data_ws, headers, tablefmt="pretty", colalign=colalign)
        result.append(table)
    else:
        result.append("")
        result.append("No workspace to display")
    result.append("")

    if echo:
        result_text = "\n".join(result)
        app.echo(result_text)

    return result
