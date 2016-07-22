#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Wed Jul 13 17:21:01 2016
@rev:    1
@lang:   Python 2.7
@deps:   csv, time
@desc:   class to log process data to a csv file
"""

import csv
import time
from yamlImport import yamlImport

#@todo: write logs to their own designted folder

class procDataLog:
    
    def __init__(self):
        """Setup"""
        self.logRun = 0
        self.headerCfg = yamlImport.importYAML("../../cfg/logHeaders.yaml")
    
    
    def write(self, logData):
        """Write values to a log
        
        :param logData: list of data to log to the csv file
        :type logData: list
        """
        if self.logRun == 1:
            if type(logData) != list:
                logData = [self.__formatTime(), logData]
            else:
                logData.insert(0, self.__formatTime())
            self.csvLog.writerow(logData)
            self.logFile.flush()
        else:
            print("No log currently active")
    
    
    def startLog(self, name=None):
        """Create a new file and start logging
        
        :param Name: Optional File name. If 'None' sets as date/time
        :type Name: String        
        """
        if self.logRun == 1:
            print("A log is already running. Please stop that first")
            return
        if name == None:
            fileName = self.__formatTimeDate() + ".csv"
        else:
            fileName = str(name) +".csv"
        self.logFile = open(fileName, 'wb')
        self.csvLog = csv.writer(self.logFile,\
                                 delimiter=',',\
                                 quoting=csv.QUOTE_ALL)
        self.headerCfg["log_headers"].insert(0,"Time")
        self.csvLog.writerow(self.headerCfg["log_headers"])
        self.logFile.flush()
        self.logRun = 1
    
    
    def stopLog(self):
        """Stop current log"""
        self.logFile.close()
        self.logRun = 0


    def __formatTime(self):
        """Format the time appropriate for logging"""
        return time.strftime('%H') + ":" +\
               time.strftime('%M') + ":" +\
               time.strftime('%S')


    def __formatTimeDate(self):
        """Format the date and time appropriate for a filename"""
        timeNow = time.strftime('%H') + "." +\
                  time.strftime('%M') + "." +\
                  time.strftime('%S')
        date    = time.strftime('%d') + "." +\
                  time.strftime('%m') + "." +\
                  time.strftime('%Y')
        return (timeNow + " " + date)