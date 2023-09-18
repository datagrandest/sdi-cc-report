import os
import re
import datetime
import time
import requests

from sdi_cc_report import config
from sdi_cc_report.libs.yaml import Yaml


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

        self.add_logs(message='=' * 80)
        self.add_logs(message=self.translate['init_message'].format(app=self.app))
        self.add_logs(message='Config file "{config_file}" loaded.'.format(config_file=self.config_file))
        self.add_logs(message='Locales file "{locales_file}" loaded (language "{lang}")'.format(locales_file=self.locales_file, lang=self.translate['lang']))

        self.create_directories()


    def load_config(self, config_file=None):
        if config_file is not None and os.path.isfile(config_file):
            self.config_file = config_file
            self.config = Yaml(file=self.config_file).data
            self.config = merge_dicts(self.config, self.config_default)
            self.locales_file = os.path.join(self.config['locales']['directory'], self.config['locales']['lang'] + '.yaml')
            self.translate = Yaml(file=self.locales_file).data

        else:
            print('ERROR: config file "{file}" cannot be loading.'.format(file=config_file))
            self.on_exit_app()


    def set_logs(self, message='', level='INFO'):
        
        if self.config['log']['log_file'] is None:
            log_message = '{now} - {level}: Log file is not define in config.yaml'.format(now=now, level='ERROR')
            self.logs.append(log_message)
            print(message)
            exit()
        
        if not os.path.isfile(self.config['log']['log_file']):
            with open(self.config['log']['log_file'], 'w') as log_file:
                pass 
        
        now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        log_message = '{now} - {level}: {message}'.format(now=now, level=level, message=message)
        self.logs.append(log_message)
        
        with open(self.config['log']['log_file'], 'a') as log_file:
            log_file.write(log_message + '\n')
            
        return log_message

    
    def get_logs(self, search=None, limit=10):
        where = [s.strip() for s in '+'.join(search).split('+')] if search and search is not None else None
        
        # Logs file always exists at this point beacause it is load during application initialization
        with open(self.config['log']['log_file'], 'r') as log_file:
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
        return True


    def undefined(self):
        print('Undefined function')
        pass


    def echo(self, text=''):
        print(text)


    def on_exit_app(self):
        self.echo('Goodby!')
        sys.exit()
   
    
    def get_report_data(self, url):
        requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
        wms_report = requests.get(url, verify=self.config['requests']['ssl_verify'])
        
        layers = [layer for layer in wms_report.text.split('\n\n') if layer.startswith('#')]

        layers_dict = []
        for layer in layers:
            layer = layer.split('\n')
            layer_dict = {
                'id':    layer[0].lstrip()[1:],
                'layer': layer[1].lstrip()[7:],
                'error': 0,
                'error_code': 'NONE',
                'message': 'OK'
            }

            if len(layer) == 2:
                layer_dict['layer'] = layer_dict['layer'][0:-3]
                
            if len(layer) == 3:
                layer_dict['error'] = 1
                layer_dict['message'] = layer[2].lstrip()[7:]
                
                if layer_dict['message'].lower().startswith('metadata'):
                    layer_dict['error_code'] = 'ERROR_MD_LINK'
                if layer_dict['message'].lower().startswith('no metadata'):
                    layer_dict['error_code'] = 'ERROR_NO_MD'
                if layer_dict['message'].lower().startswith('the requested style'):
                    layer_dict['error_code'] = 'ERROR_STYLE'
                if layer_dict['message'].lower().startswith('rendering process failed'):
                    layer_dict['error_code'] = 'ERROR_RENDERING'

            layers_dict.append(layer_dict)

        return layers_dict

    
    def save_data_to_csv(self, file='data.csv', data=[{}]):
        keys = data[0].keys()
        with open(file, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)

    
    def get_report_summary(self, data=[{}], type='dict'):
        layers_id = set([l['id'] for l in data])
        
        nb_layers = len(layers_id)
        nb_layers_ok = len([layer for layer in data if layer['error'] == 0])
        nb_layers_errors = nb_layers - nb_layers_ok
        nb_total_errors = len([layer for layer in data if layer['error'] == 1])

        if type == 'dict':
            return {
                'nb_layers': nb_layers,
                'nb_layers_ok': nb_layers_ok,
                'nb_layers_errors': nb_layers_errors,
                'nb_total_errors': nb_total_errors
            }

        if type == 'list':
            return [
                ["nb_layers", nb_layers],
                ["nb_layers_ok", nb_layers_ok], 
                ["nb_layers_errors", nb_layers_errors], 
                ["nb_total_errors", nb_total_errors]
            ]