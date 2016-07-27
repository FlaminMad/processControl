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
import copy
import time
from yamlImport import yamlImport


class procDataLog:
    """Used to log data from the process upon controller runtime
    
    Usage: Create an instance of the class to initialise the required params
           Call 'startlog()' to begin logging
           Add to log using 'write(data)' where data contains a list of values
           When finished, call 'stoplog()'
           
    It should be noted that a config file is avaliable in the 'cfg' directory
    to allow the addition of headers to the file. Futhermore, a new config file
    is created at midnight each day to avoid problems with large files.
    """
    
    def __init__(self):
        """Setup"""
        self.logRun = 0
        self.dateNow = time.strftime('%d')
        self.headerCfg = yamlImport.importYAML("./cfg/logHeaders.yaml")
        self.headerCfg["log_headers"].insert(0,"Time")
    
    
    def write(self, procData):
        """Write given values to a log
        
        :param logData: list of data to log to the csv file
        :type logData: list
        """
        logData = copy.deepcopy(procData)
        if self.logRun == 1:
            if time.strftime('%d') != self.dateNow:
                self.stopLog()
                self.startLog()
                self.dateNow = time.strftime('%d')
                
            if type(logData) != list:
                logData = [self.formatTime(), logData]
            else:
                logData.insert(0, self.formatTime())
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
            fileName = "./log/" + self.__formatTimeDate() + ".csv"
        else:
            fileName = "./log/" + str(name) +".csv"
        self.logFile = open(fileName, 'wb')
        self.csvLog = csv.writer(self.logFile,\
                                 delimiter=',',\
                                 quoting=csv.QUOTE_ALL)
        self.csvLog.writerow(self.headerCfg["log_headers"])
        self.logFile.flush()
        self.logRun = 1
    
    
    def stopLog(self):
        """Stop current log"""
        self.logFile.close()
        self.logRun = 0


    def formatTime(self):
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