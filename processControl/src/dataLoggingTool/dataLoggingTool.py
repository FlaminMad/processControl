#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sun Jul 24 20:46:03 2016
@rev:    1
@lang:   Python 2.7
@deps:   <None>
@desc:   Tool to log and plot data from a MODBUS connection. Acts as an ideal
         tool for logging and monitoring step tests as they progress.
"""
import time

from ..toolClasses.modbusClient   import modbusClient
from ..toolClasses.osTools        import osTools
from ..toolClasses.plotDataPoints import plotDataPoints
from ..toolClasses.procDataLog    import procDataLog
from ..toolClasses.yamlImport     import yamlImport

class dataLoggingTool:
    """Tool to log and plot data from a MODBUS connection
    
    Usage:  Ensure all params are setup in the 'controllerSettings' file
            Create an instance of the class to initialise the required params
            Call 'startStop(1)' to begin logging and connection to server
            Call 'run()' to enter main loop
            Call 'startStop(0)' to close log and connection
    """
    
    def __init__(self):
        """Create all required objects and import settings"""
        self.coms = modbusClient()
        self.ext = osTools()
        self.gph = plotDataPoints()
        self.log = procDataLog()
        self.cfg = yamlImport.importYAML("./cfg/controllerSettings/dataLoggingTool.yaml")
        self.count = 0

    
    def startStop(self,run):
        """Use to open/close connections before/after running main loop
        
        :param run: set to 1 or 0 to start or stop the outgoing connections
        :type run: int
        """
        if run == 1:
            self.coms.openConnection()  
            self.log.startLog()
        elif run == 0:
            self.log.stopLog()            
            self.coms.closeConnection()
            self.gph.closeBlock()               #Keep data plot open until exit
        else:
            raise ValueError 
        
    
    def run(self):
        """Main run loop for the data logging tool
        Ensure that the startStop method is called before and after this function
        """
        startTime = time.time()                 #For time reference
        while(True):
            loopTime = time.time()              #Itteration start time
            runTime = round(time.time() - startTime)
            data = self.IOHandler()
            self.log.write(data)
            self.gph.dataUpdate(runTime, data)
            if self.ext.kbdExit():              #Detect exit condition
                break
            print self.count                    #Heartbeat
            self.count += 1                     #Heartbeat
            time.sleep(self.cfg['interval'] -\
                      (time.time() - loopTime)) #Loop Interval
    
    def IOHandler(self):
        """Used to read data from the MODBUS connection and append to one list
        Add data by including additional lines of ioData.extend or modifying the
        current read address lengths
        """
        ioData = self.coms.dataHandler('r',4,0,length=2)
        ioData.extend(self.coms.dataHandler('r',3,0,length=2))
        return ioData
        
    
def main():
    ctrl = dataLoggingTool()                      #Initialise the data logging tool class
    ctrl.startStop(1)                             #Start logs and open connection
    ctrl.run()                                    #Run main method
    ctrl.startStop(0)                             #Start logs and open connection  

if __name__ == '__main__':main()