import os
import re
import csv
import datetime
import time
import requests

from sdi_cc_report import config
from sdi_cc_report.libs.yaml import Yaml
from sdi_cc_report.libs.report import Report


# TODO: à mettre dans une librairie partagée (helpers)
def merge_dicts(d1, d2, path=None):
    "merges d2 into d1"
    if path is None: path = []
    for key in d2:
        if key in d1:
            if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                merge_dicts(d1[key], d2[key], path + [str(key)])
            elif d1[key] == d2[key]:
                pass # same leaf value
            else:
                pass # same key with différent values
        else:
            d1[key] = d2[key]
    return d1


class Application():

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_file = config.__config_file__
    config_default = config.__config_default__
    locales_file = None
    translate = None
    config = None
    logs = []
    verbose = False


    def __init__(self, config_file=None, app=None):
        self.app = app
        self.load_config(config_file)

        self.create_directories()

        self.add_logs(message='=' * 80)
        self.add_logs(message=self.translate['init_message'].format(app=self.app))
        self.add_logs(message='Config file "{config_file}" loaded.'.format(config_file=self.config_file))
        self.add_logs(message='Locales file "{locales_file}" loaded (language "{lang}")'.format(locales_file=self.locales_file, lang=self.translate['lang']))



    def load_config(self, config_file=None):
        if config_file is not None and os.path.isfile(config_file):
            self.config_file = config_file
            self.config = Yaml(file=self.config_file).data
            self.config = merge_dicts(self.config, self.config_default)
            self.locales_file = os.path.abspath(os.path.join(self.root_dir, self.config['locales']['directory'], self.config['locales']['lang'] + '.yaml'))
            self.log_file = os.path.abspath(os.path.join(self.root_dir, self.config['log']['log_file']))
            self.dashboard_templates_directory = os.path.abspath(os.path.join(self.root_dir, self.config['dashboard']['templates_directory']))
            self.translate = Yaml(file=self.locales_file).data

        else:
            print('ERROR: config file "{file}" cannot be loading.'.format(file=config_file))
            self.on_exit_app()


    def set_logs(self, message='', level='INFO'):
        
        if self.log_file is None:
            log_message = '{now} - {level}: Log file is not define in config.yaml'.format(now=now, level='ERROR')
            self.logs.append(log_message)
            print(message)
            exit()
        
        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w') as log_file:
                pass 
        
        now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        log_message = '{now} - {level}: {message}'.format(now=now, level=level, message=message)
        self.logs.append(log_message)
        
        with open(self.log_file, 'a') as log_file:
            log_file.write(log_message + '\n')
            
        return log_message

    
    def get_logs(self, search=None, limit=10):
        where = [s.strip() for s in '+'.join(search).split('+')] if search and search is not None else None
        
        # Logs file always exists at this point beacause it is load during application initialization
        with open(self.log_file, 'r') as log_file:
            if where and where is not None:
                logs = []
                for log in log_file:
                    nb_true = 0
                    for w in where:
                        if w.strip().lower() in log.lower():
                            nb_true += 1
                    if nb_true == len(where):
                        logs.append(log.strip())
            else:
                logs = [log.strip() for log in log_file.readlines()]
        
        logs.reverse()
        logs = logs[:limit] if limit else logs
        return logs


    def create_directories(self):
        path = os.path.dirname(self.log_file)
        if not os.path.exists(path):
            os.makedirs(path)
        return True


    def undefined(self):
        print('Undefined function')
        pass


    def echo(self, text=''):
        print(text)


    def on_exit_app(self):
        self.echo('Goodby!')
        sys.exit()

  
    def get_errors(self, report=None, filter=None, workspace=None, name=None, id=None):
        if report is None:
            return False
        
        r = Report(url=report['url'], title=report['name'], type=report['type'], ssl_verify=self.config['requests']['ssl_verify'])
        data = r.get_errors(filter=filter, workspace=workspace, name=name, id=id)
            
        return {
            'nb_errors': r.nb_errors,
            'errors': data.errors
        }

    
    def get_layers(self, report=None, filter=None, workspace=None, name=None, id=None):
        if report is None:
            return False
        
        r = Report(url=report['url'], title=report['name'], type=report['type'], ssl_verify=self.config['requests']['ssl_verify'])
        data = r.get_layers(filter=filter, workspace=workspace, name=name, id=id)
        
        return {
            'nb_layers': r.nb_layers,
            'layers': data.layers
        }

 
    def get_workspaces(self, report=None, filter=None):
        if report is None:
            return False
        
        r = Report(url=report['url'], title=report['name'], type=report['type'], ssl_verify=self.config['requests']['ssl_verify'])
        data = r.get_workspaces(filter=filter)
            
        return {
            'nb_workspaces': r.nb_workspaces,
            'workspaces': data.workspaces
        }
        
    
    def save_data_to_csv(self, file='data.csv', data=[{}]):
        keys = data[0].keys()
        with open(file, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    
    def get_report_summary(self, report=None):
        if report is None:
            return False
        
        r = Report(url=report['url'], title=report['name'], type=report['type'], ssl_verify=self.config['requests']['ssl_verify'])
        
        return {
            'nb_errors': r.nb_errors,
            'nb_layers': r.nb_layers,
            'nb_layers_ok': r.nb_layers_ok,
            'nb_layers_error': r.nb_layers_error,
            'nb_workspaces': r.nb_workspaces,
        }
        
    def generate_dashboard(self, report, destination=None, workspace=None, template=None):
        if report is None:
            return ['ERROR: report not define']
        
        result = []
        
        # Get files name
        if workspace and workspace is not None:
            template_file = report['type'] + '_ws'
            html_file = report['type'] + '_' + workspace
            csv_files = {
                'csv_report': report['type'] + '_' + workspace + '_report.csv'  ,
                'csv_errors': report['type'] + '_' + workspace + '_errors.csv'  ,
                'csv_layers': report['type'] + '_' + workspace + '_layers.csv'  ,
                'csv_ws': report['type'] + '_' + workspace + '_ws.csv'  ,
            }
        else:
            template_file = report['type']
            html_file = report['type']
            csv_files = {
                'csv_report': report['type'] + '_report.csv'  ,
                'csv_errors': report['type'] + '_errors.csv'  ,
                'csv_layers': report['type'] + '_layers.csv'  ,
                'csv_ws': report['type'] + '_ws.csv'  ,
            }
            
        # Get default destination path
        if not destination or destination is None:
            destination = self.config['dashboard']['destination_directory']
        
        # If destination is HTML file get name and change destination path
        if destination.endswith('.html'):
            html_file = os.path.basename(destination) + '.html'
            destination = os.dirname(destination)
        else:
            html_file = html_file + '.html'
        destination_file = os.path.join(destination, html_file)
        template_file = template if template and template is not None else os.path.join(self.dashboard_templates_directory, template_file + '.html')

        # Create destination path if necessary
        if not os.path.exists(destination):
            os.makedirs(destination) 
            result.append('')
            result.append('INFO: "--destination" {destination} path not exists and has been created.'.format(destination=destination))
            result.append('')
        
        # Generate HTML dashboard file from template
        with open(template_file, 'r') as tpl:
            template_content = tpl.read()
            template_content = template_content.replace('{title}', report['name'])
            template_content = template_content.replace('{type}', report['type'])
            template_content = template_content.replace('{url}', report['url'])
            template_content = template_content.replace('{workspace}', workspace)
            for csv_file in csv_files:
                template_content = template_content.replace('{'+ csv_file +'}', os.path.join('./', csv_files[csv_file]))
        
        # Save the generated HTML dashboard file
        with open(destination_file, 'w') as dst:
            dst.write(template_content)
        result.append('INFO: HTML dashboard has been generated')

        # Generate report CSV
        csv_file = os.path.join(destination, csv_files['csv_report'])
        data_reports = self.get_report_summary(report=report)
        self.save_data_to_csv(csv_file, [data_reports])
        result.append('INFO: {csv_report} file saved'.format(csv_report=csv_files['csv_report']))
        
        # Generate errors CSV
        csv_file = os.path.join(destination, csv_files['csv_errors'])
        data_errors = self.get_errors(report=report, workspace=workspace)
        self.save_data_to_csv(csv_file, data_errors['errors'])
        result.append('INFO: {csv_errors} file saved'.format(csv_errors=csv_files['csv_errors']))
        
        # Generate layers CSV
        csv_file = os.path.join(destination, csv_files['csv_layers'])
        data_layers = self.get_layers(report=report, workspace=workspace)
        self.save_data_to_csv(csv_file, data_layers['layers'])
        result.append('INFO: {csv_layers} file saved'.format(csv_layers=csv_files['csv_layers']))
        
        # Generate workspace CSV
        if report['type'].lower() in ['wms', 'wfs']:
            csv_file = os.path.join(destination, csv_files['csv_ws'])
            data_workspaces = self.get_workspaces(report=report, filter=workspace)
            self.save_data_to_csv(csv_file, data_workspaces['workspaces'])
            result.append('INFO: {csv_ws} file saved'.format(csv_ws=csv_files['csv_ws']))

        result.append('INFO: dashboard production complete')
        
        return result

