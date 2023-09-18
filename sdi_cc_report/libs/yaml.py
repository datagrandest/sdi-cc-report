#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import yaml


class Yaml(object):
    """
    Manage YAML file 
    Example as config file.
    """

    file = None
    content = None
    data = None

    def __init__(self, file=None):
        if file is not None and os.path.isfile(file):
            self.file = file
            self.get()

    def get(self, file=None):
        '''Get YAML file'''
        if file is not None and os.path.isfile(file):
            self.file = file
        with open(self.file, 'r') as f:
            self.content = f.read()
            self.data = yaml.load(self.content, Loader=yaml.FullLoader)
        return self

    def set(self, data=None, file=None, save=False, sort_keys=False):
        '''Set YAML file'''
        if file is not None:
            self.file = file
        if data is not None:
            self.data = data
        if save:
            self.save()

    def save(self, data=None, file=None, sort_keys=False):
        '''Set YAML file'''
        if file is not None:
            self.file = file
        if data is not None:
            self.data = data
        with open(self.file, 'w') as f:
            yaml.dump(self.data, f, sort_keys=sort_keys, indent=4)
        self


if __name__ == '__main__':
    file = './test.json'
    data = dict_file = [{'sports': ['soccer', 'football', 'basketball', 'cricket', 'hockey', 'table tennis']},
                        {'countries': ['Pakistan', 'USA', 'India', 'China', 'Germany', 'France', 'Spain']}]
    print(Yaml.set(data, file, True))
    print(Yaml.set(file))
