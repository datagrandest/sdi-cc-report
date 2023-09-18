from tabulate import tabulate

def print_reports_list(app, reports, files=None, title=None, print=False):

    nb_total_reports = len(reports)
    nb_display_reports = nb_total_reports
    
    # Add id value for each file report line
    for id, report in enumerate(reports):
        reports[id]['id'] = id

    headers = ['ID', 'NAME', 'TYPE', 'URL']

    # Get table data according file parameter
    if files and files is not None:
        data = [[reports[i]['id'], reports[i]['name'], reports[i]['type'], reports[i]['url']] for i in files if i < nb_total_reports]
        nb_display_reports = len(data)
    else:
        data = [[reports[i]['id'], reports[i]['name'], reports[i]['type'], reports[i]['url']] for i in range(0, nb_total_reports)]
    
    table = tabulate(data, headers, tablefmt="pretty")

    # Display data table
    result = []
    result.append('')
    if title and title is not None:
        result.append(title)
    result.append('Nb. reports: {nb_display_reports}/{nb_total_reports}'.format(nb_display_reports=nb_display_reports, nb_total_reports=nb_total_reports))
    if nb_display_reports > 0:
        result.append(table)
    else:
        result.append('Aucun fichier à afficher. Merci de vérifier les paramètres indiqués.')
    result.append('')

    if print:
        result_text = '\n'.join(result)
        app.echo(result_text)
    
    return result
    

def print_report_table(app, report, data, title=None, print=False):
    #Get table data
    table = tabulate(data, tablefmt="pretty", colalign=('left', 'right'), maxcolwidths=[30, 8])

    # Display data table
    result = []
    result.append('')
    if title and title is not None:
        result.append(title)
        result.append('')   
    result.append('Report name: {report_name}'.format(report_name=report['name']))
    result.append('Report type: {report_type}'.format(report_type=report['type']))
    result.append('Report URL: {report_url}'.format(report_url=report['url']))
    result.append('')
    result.append('Summary:')
    result.append(table)
    result.append('')

    if print:
        result_text = '\n'.join(result)
        app.echo(result_text)
        
    return result


def print_layers(app, report, data, limit=None, search=None, print=False):
    # Get headers, columns and data
    headers = ['ID', 'NAME', 'STATUS', 'ERRORS']
    colalign = ('right', 'left', 'left', 'left')
    data = [[d['id'], d['name'], 'OK' if d['nb_errors'] == 0 else 'ERROR', d['nb_errors']] for d in data]

    # Display data table
    result = []
    result.append('')
    result.append('Report name: {report_name}'.format(report_name=report['name']))
    result.append('Report type: {report_type}'.format(report_type=report['type']))
    result.append('Report URL: {report_url}'.format(report_url=report['url']))
    result.append('')
    result.append('Nb. layers: {nb_display_layers}/{nb_total_layers}'.format(nb_display_layers=len(data), nb_total_layers=report['nb_total_layers']))
    if search and search is not None:
        result.append('Search parameter: {search}'.format(search=search))
    if limit and limit is not None:
        data = data[0:int(limit)]
        result.append('Limit parameter: {limit}'.format(limit=limit))
    if len(data) > 0:
        result.append('Layers:')
        table = tabulate(data, headers, tablefmt="pretty", colalign=colalign)
        result.append(table)
    else:
        result.append('')
        result.append('No layer to display')
    result.append('')

    if print:
        result_text = '\n'.join(result)
        app.echo(result_text)
        
    return result


def print_layer_errors(app, report, data, print=False):
    # Get headers, columns and data    
    headers = ['ID', 'CODE', 'MESSAGE']
    colalign = ('middle', 'left', 'left')
    maxcolwidths = [5, 20, 80]
    data = [[d['error_id'], d['error_code'], d['error_message']] for d in data]

    # Display data table
    result = []
    if len(data) > 0:
        table = tabulate(data, headers, tablefmt="grid", colalign=colalign, maxcolwidths=maxcolwidths)
        result.append('Errors:')
        result.append(table)
    else:
        result.append('No error to display')
    result.append('')

    
    if print:
        result_text = '\n'.join(result)
        app.echo(result_text)
        
    return result
