#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sun Jul 24 20:46:03 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   <>
"""



class dataLoggingTool:
    
    def __init__(self):
        # Instances
        self.ext = osTools()
        self.log = procDataLog()
        self.gph = plotDataPoints()
        self.coms = modbusClient()
        pass
    
    def run(self):
        pass


def main():
    rp = dataLoggingTool()                      #Initialise the data logging tool class
    rp.run()                                    #Run main method
    rp.pg.end()                                 #Keep data plot open until exit

if __name__ == '__main__':main()