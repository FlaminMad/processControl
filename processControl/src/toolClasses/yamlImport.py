#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   03/06/2016
@rev:    1
@lang:   Python 2.7
@deps:   yaml
@desc:   acts as a quick way to import yaml files
"""

import yaml

class yamlImport():
    """Contains a function to import yaml files"""
    
    @staticmethod
    def importYAML(pathToFile):
        try:
            with open(pathToFile, "r") as f:
                config = yaml.load(f)
        except IOError:
            print("Failed to read " + pathToFile)
            raise SystemExit()
        return config