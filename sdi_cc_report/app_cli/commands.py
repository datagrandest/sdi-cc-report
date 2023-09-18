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
    if app.config['history']['clear_on_exit']:
        if os.path.isfile(app.config['history']['file']):
            os.remove(app.config['history']['file'])

    app.echo('Goodby!')
    click_repl.exit()


def on_test(app):
    """
    Function for test
    > report connect LOGIN PASSWORD
    """
    app.echo('test')


def on_clear_history(app):
    """
    clear history file
    > report clear_history
    """
    if os.path.isfile(app.config['history']['file']):
        os.remove(app.config['history']['file'])


def on_reports(app, files=None):
    """
    Display files report list
    > report reports [FILES]  
    """
    result = []
    files = [int(i.strip()) for i in ','.join(files).split(',')] if files and files is not None and len(files) > 0 else files

    if files and files is not None:
        for file in files:
            if file < len(app.config['reports']):
                report = app.config['reports'][file]
                layers = app.get_report_data(report['url'])
                report_summary = app.get_report_summary(layers, 'list')
                result.extend(display.print_report_table(app, report=report, data=report_summary))
            else:
                result.append('')
                result.append('ERROR: file indice {file} doesn''t exist'.format(file=file))
    else:
        result.extend(display.print_reports_list(app, app.config['reports'], files, title="Liste des fichiers"))
        
    result_text = '\n'.join(result)
    app.echo(result_text)


def on_layers(app, file, csv, search, workspace, id, limit, export):
    """
    > layers [FILE] [--csv CSV] [--search SEARCH] [--workspace WS] [--id ID] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des layers du rapport [FILE]
    """
    result = []

    if not file or file is None or len(file) == 0:
        result.append('ERROR: [FILE] argument is missing.')
        result.extend(display.print_reports_list(app, app.config['reports'], title="Thanks to indicate a [FILE] id."))

    else: 

        file = [int(i.strip()) for i in ','.join(file).split(',')][0]
        report = app.config['reports'][file]

        layers = app.get_report_data(report['url'])
        report['nb_total_layers'] = len(set([l['id'] for l in layers]))

        if id:
            layer_errors = []
            error_id = 0;
            for line in layers:
                if line['id'] == id:
                    layer_name = line['layer']
                    layer_ws = ''
                    if report['type'].lower() in ['wms', 'wfs']:
                        layer_ws = line['layer'].split(':')[0]
                        layer_name = line['layer'].split(':')[1]
                    
                    if line['error'] == 1:
                        layer_errors.append({
                            'error_id': error_id,
                            'error_code':    line['error_code'],
                            'error_message': line['message']   
                        })
                        error_id += 1

            data = [{
                'id': id,
                'workspace': layer_ws,
                'name': layer_name,
                'nb_errors': len(layer_errors), 
                'errors': layer_errors
            }]

            result.extend(display.print_layers(app, report, data))
            result.extend(display.print_layer_errors(app, report, layer_errors or []))

        elif search or workspace or limit:
            data = {}
            data_id = []
            for line in layers:
                if line['id'] not in data_id:
                    layer_name = line['layer']
                    layer_ws = ''
                    if report['type'].lower() in ['wms', 'wfs']:
                        layer_ws = line['layer'].split(':')[0]
                        layer_name = line['layer'].split(':')[1]
                    
                    data[line['id']] = {
                        'id': line['id'],
                        'workspace': layer_ws,
                        'name': layer_name,
                        'nb_errors': 0, 
                        'errors': [],
                        'search': ' | '.join([line['id'], line['layer']])
                    }
                    data_id.append(line['id'])
                    
                if line['error'] == 1:
                    data[line['id']]['nb_errors'] += 1
                    data[line['id']]['search'] += ' | ' + line['error_code'] + ' | ' + line['message']

            if search:
                data = [data[d] for d in data if search in data[d]['search']]
            else:
                data = [data[d] for d in data]
                
            if workspace:
                if report['type'].lower() in ['wms', 'wfs']:
                    data = [d for d in data if workspace in d['workspace']]
                else:
                    result.append('')
                    result.append('INFO: Check report type: --workspace parameter ignored.')

            result.extend(display.print_layers(app, report, data, limit, search))

        else:
            report_summary = app.get_report_summary(layers, 'list')
            result.extend(display.print_report_table(app, report=report, data=report_summary))

        if csv:
            app.save_data_to_csv(csv, layers)
            
        if export:
            with open(export, 'w') as f:
                result_text = '\n'.join(result)
                f.write(result_text)
                
    result_text = '\n'.join(result)
    app.echo(result_text)


def on_workspaces(app, file, search, limit, export):
    """
    > ws [FILE] [--search SEARCH] [--limit LIMIT] [--export EXPORT]
    Affiche la liste des workspaces du rapport [FILE]
    """

    if not file or file is None or len(file) == 0:
        app.echo()
        app.echo('ERROR: [FILE] argument is missing.')
        display.print_reports_list(app, app.config['reports'], title="Thanks to indicate a [FILE] id.", echo=True)
        sys.exit()
    
    file = [int(i.strip()) for i in ','.join(file).split(',')][0]
    report = app.config['reports'][file]
    
    if report['type'].lower() not in ['wms', 'wfs']:
        app.echo()
        app.echo('ERROR: "ws" command works only on WMS and WFS report type.')
        app.echo()
        sys.exit()
    
    result = []

    layers = app.get_report_data(report['url'])

    data_id = []
    data = []
    for line in layers:
        if line['id'] not in data_id:
            layer_ws = line['layer'].split(':')[0]
            if layer_ws not in data:
                data.append(layer_ws)
            data_id.append(line['id'])

    report['nb_total_ws'] = len(data)
    if search:
        data = [d for d in data if search in d]
    
    result.extend(display.print_ws(app, report, data, limit, search))
        
    if export:
        with open(export, 'w') as f:
            result_text = '\n'.join(result)
            f.write(result_text)
                
    result_text = '\n'.join(result)
    app.echo(result_text)


