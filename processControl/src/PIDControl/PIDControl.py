#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Mon Jul 25 23:19:51 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   Simple PID controller algorithm
"""

import time

from ..toolClasses.modbusClient   import modbusClient
from ..toolClasses.osTools        import osTools
from ..toolClasses.plotDataPoints import plotDataPoints
from ..toolClasses.procDataLog    import procDataLog
from ..toolClasses.yamlImport     import yamlImport
from .PIDController               import PIDController

class PIDControl:
    """A PID algorithm for use with a wide range control applications
    
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
        self.PID = PIDController()
        self.cfg = yamlImport.importYAML("./cfg/controllerSettings/PIDControl.yaml")
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
        """Main run loop for the PID controller
        Ensure that the startStop method is called before and after this function
        """
        startTime = time.time()                             #For time reference
        while(True):
            loopTime = time.time()                          #Itteration start time
            runTime = round(time.time() - startTime)        #Graph plot x axis
            data = self.IOHandler()                         #Read device
            data[1] = self.PID.runCtrl(data[0],data[1])     #Calculate OP           
            self.coms.dataHandler('w',16,0,data=data[1])    #Write new OP to device
            data.append(self.PID.cfg["setPoint"])           #Append setpoint to array
            self.log.write(data)                            #Write data array to csv
            self.gph.dataUpdate(runTime, data)              #Plot data array to graph
            if self.ext.kbdExit():                          #Check for exit condition
                break
            print self.count                                #Heartbeat
            self.count += 1                                 #Heartbeat
            time.sleep(self.cfg['interval'] - (time.time() - loopTime))
    
    def IOHandler(self):
        """Used to read data from the MODBUS connection and append to one list
        Add data by including additional lines of ioData.extend or modifying the
        current read address lengths
        """
        ioData = self.coms.dataHandler('r',4,0,length=2)        #PV
        ioData.extend(self.coms.dataHandler('r',3,0,length=2))  #OP
        return ioData
        
    
def main():
    ctrl = PIDControl()                      #Initialise a PID instance
    ctrl.startStop(1)                        #Start logs and opens a connection
    ctrl.run()                               #Run main method
    ctrl.startStop(0)                        #Stops logs and closes the connection 

if __name__ == '__main__':main()