#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Wed Jul 13 17:21:01 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   <>
"""

import csv
import time

class procDataLog:
    
    def __init__(self):
        """Setup"""
        self.logRun = 0
    
    
    def write(self):
        """Write values to a log"""
        
        pass
    
    
    def startLog(self, name=None):
        """Create a new file and start logging
        
        :param Name: Optional File name. If 'None' sets as date/time
        :type Name: String        
        """
        if name == None:
            fileName = self.formatTime() + ".csv"
        else:
            fileName = str(name) +".csv"
        self.logFile = open(fileName, 'wb')
        self.csvLog = csv.writer(self.logFile,\
                                 delimiter=',',\
                                 quoting=csv.QUOTE_ALL)
        self.logRun = 1
    
    
    def stopLog(self):
        """Stop current log"""
        self.logFile.close()
        self.logRun = 0

    
    def formatTime(self):
        """Format the date and time appropriate for a filename"""
        
        timeNow = time.strftime('%H') + "." +\
                  time.strftime('%M') + "." +\
                  time.strftime('%S')
        
        date    = time.strftime('%d') + "." +\
                  time.strftime('%m') + "." +\
                  time.strftime('%Y')
        
        return (timeNow + " " + date)