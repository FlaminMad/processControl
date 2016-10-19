#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Sat Jul 23 14:13:53 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   <>
"""

import warnings
import numpy as np
import matplotlib.pyplot as plt
from yamlImport import yamlImport

class plotDataPoints:
    """Plots a graph of the data passed to it
    
    Usage:  Ensure all params are setup in the 'plotPenConfig' file 
            Create an instance of the class to initialise the required params
            Call 'dataUpdate' to add data to the plot
            Use 'closeBlock' upon program end to keep plot window open
    """
    
    def __init__(self):
        """Import config and call the necessary setup functions"""
        self.plotCfg = yamlImport.importYAML("./cfg/plotPenConfig.yaml")
        self.__setupPlots()
        self.__setupArrays()
        self.__setupPens()
        self.__startFlag = 1


    def __setupPlots(self):
        """Setup matplotlib figure and configure each of the respective plots"""
        self.fig = plt.subplots()
        self.__createSubPlots()
        self.__configureSubPlots()
        plt.ion()
        plt.show()
    
    
    def __setupArrays(self):
        """Initalise the arrays for data plotting"""
        self.xData = np.array([[]])
        self.yData = np.array([[]]).reshape((self.plotCfg.__len__()-1),0)
        
    
    def __createSubPlots(self):
        """Using the config file create all required subplots"""
        plotNo = []
        for i in range(1,(self.plotCfg.__len__())):
            plotNo.append(self.plotCfg["pen_" + str(i)]['plot'])
        
        self.ax = {}        
        for i in range(1,max(plotNo)+1):
            self.ax[i] = plt.subplot(max(plotNo),1,i)
        
        
    def __configureSubPlots(self):
        """Add axis lables and set range"""
        for i in range(1, self.ax.__len__()+1):
            self.ax[i].set_xlabel(self.plotCfg['plot_cfg']['x_axis_label'])
            self.ax[i].set_ylabel(self.plotCfg['plot_cfg']['y_axis_label'])            
            self.ax[i].set_ylim(self.plotCfg['plot_cfg']['y_axis_min'],\
                                self.plotCfg['plot_cfg']['y_axis_max'])


    def __configureLegends(self):
        """Enable legends on each of the subplots"""
        for i in range(1, self.ax.__len__()+1):
            self.ax[i].legend()
    
    
    def __setupPens(self):
        """Setup pens ready for graphical plotting"""
        self.penDict = {}
        for i in range(1,len(self.ax)+1):
            axPens  = []
            for j in range(1,(self.plotCfg.__len__())):
                if self.plotCfg["pen_" + str(j)]['plot'] == i:
                    axPens.append("pen_" + str(j))
            self.penDict[i] = axPens
    
    def __plot(self):
        """Plots the x and y data from the 'dataUpdate' method"""
        for i in range(1, self.penDict.__len__()+1):
            for j in range(self.penDict[i].__len__()):
                self.ax[i].plot(self.xData,\
                np.transpose(self.yData[int(self.penDict[i][j][-1])-1,:]),\
                self.plotCfg[self.penDict[i][j]]["colour"],\
                label=self.plotCfg[self.penDict[i][j]]["name"] )
        if self.__startFlag == 1:
            self.__configureLegends()
            self.__startFlag = 0
        plt.draw()                              # Draws the graph to your screen
        warnings.simplefilter("ignore")         # Hide depreciation warnings
        plt.pause(0.001)                        # Workaround to avoid the freezing problem
    
    def __graphScroll(self):
        """Removes all lines on the graph ready for updated data"""
        for i in range(1, self.penDict.__len__()+1):
            self.ax[i].lines = []
            self.ax[i].set_xlim(self.xData[0],self.xData[-1])
    
    
    def dataUpdate(self, x, *y):
        """Add data to the graph"""
        self.xData = np.append(self.xData,x)
        #todo: Need to add try catch on this line as will fail if config is wrong
        self.yData = np.append(self.yData,np.transpose(np.matrix(y)),1)
        if len(self.xData) > self.plotCfg['plot_cfg']['x_axis_length']:
            self.xData = np.delete(self.xData,0)
            self.yData = np.delete(self.yData,0,1)
        self.__graphScroll()
        self.__plot()
      
    
    def closeBlock(self):
        """Use to block the graph closing upon exit"""
        print("Close plot window to finish...")
        plt.show(block=True)