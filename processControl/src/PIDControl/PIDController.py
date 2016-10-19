#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Mon Jul 25 23:55:32 2016
@rev:    1
@lang:   Python 2.7
@deps:   <>
@desc:   Contains PID controller algorithm for import
"""

import numpy as np
from ..toolClasses.yamlImport import yamlImport


class PIDController:
    """Help Text"""
    def __init__(self):
        """Read the config fle and set initial control mode"""        
        self.__readConfig()
        self.prevCtrlMode = "Startup"
        
    
    def runCtrl(self,PV,OP):
        """Call to run the PID control algorithm as per the cfg file
        
        :param PV:  Process variable at current time      
        :param OP:  Valve operating point
        :type PV:   float
        :type OP:   float
        
        :return: New value for OP
        """
        self.__readConfig()
        if self.prevCtrlMode != self.cfg['controlMode']:
            self.spErr = self.__reduceTransEffect(PV,OP)
            self.prevCtrlMode = self.cfg['controlMode']
        if self.cfg['controlMode'] == "acuto":
            return round(self.__autoControl(PV,OP),2)
        if self.cfg['controlMode'] == "manual":
            return self.cfg['setPoint']
        return ValueError("Invalid Control Mode")


    def __autoControl(self,PV,OP):
        """Handler for the PID control algorithm (auto mode)
        
        :param PV:  Process variable at current time      
        :param OP:  Valve operating point
        :type PV:   float
        :type OP:   float
        
        :return: New value for OP
        """
        ERR = self.cfg['setPoint'] - PV
        return self.__vlvLims(self.__pidAlgorithm(PV,ERR),ERR)
    

    def __pidAlgorithm(self,PV,ERR):
        """Runs the PID algorithm
        
        :param PV: Process Variable
        :param ERR: Setpoint Error
        :type PV: float
        :type ERR: float
        """
        if self.cfg['ctrlType'] == "P":
            return self.cfg['Kg'] * ERR
        elif self.cfg['ctrlType'] == "PI":
            return self.cfg["Kg"] * (ERR + self.__integral())
        elif self.cfg['ctrlType']  == "PID":
            return self.cfg["Kg"] * (ERR + self.__integral() + self.__derivitive(PV))
        else:
            return ValueError('Invalid Control Type - Options are P, PI & PID')
    
    
    def __integral(self):
        """Returns the integral term evaluation"""        
        return ((self.spErr *self.cfg['interval'])/self.cfg['Ki'])
        
    
    def __derivitive(self,PV):
        """Returns the derivative term evaluation
        
        Note that the derivitive evaluation avoids setpoint change spikes by 
        using the PV instead of error.
        
        :param PV: Process variable at current time
        :type PV: float        
        :return: Derivative evaluation
        """
        d = (((self.deriv - PV) * self.cfg['Kd'])/self.cfg['interval'])
        self.deriv = PV
        return d

    
    def __vlvLims(self,OP,ERR):
         """Enforce Valve Limitations and antiwindup
         
         :param OP:  Valve operating point
         :param ERR: Set point error
         :type OP:   float
         :type ERR:  float
         """
         if self.cfg["limitsActive"] == True:
             if OP > self.cfg["vlvHighLimit"]:
                 self.spErr += (self.cfg["antiWindUp"] * ERR)
                 return self.cfg["vlvHighLimit"]
             if OP < self.cfg["vlvLowLimit"]:
                 self.spErr += (self.cfg["antiWindUp"] * ERR)
                 return self.cfg["vlvLowLimit"]
         self.spErr += ERR
         return OP
    
    
    def __reduceTransEffect(self,PV,OP):
        """Calculate the value for spErr (set point error) to ensure seamless
        bump during controller changover. Note that deriv and prevErr are also
        set.

        :param PV:  Process variable at current time      
        :param OP:  Valve operating point
        :param ERR: Set point error
        :type PV:   float
        :type OP:   float
        :type ERR:  float
        
        :return: Value for spErr
        """
        self.deriv = PV
        self.prevErr = self.cfg['setPoint'] - PV
        
        if self.cfg["ctrlType"] == "P":
            return 0
        elif self.cfg["ctrlType"] == "PI" or self.cfg["ctrlType"] == "PID":
            return np.around(((self.cfg['Ki']/self.cfg['interval'])*((OP/self.cfg['Kg'])-(self.cfg['setPoint'] - PV))),0)   
        else:
            return ValueError('Invalid Control Type - Options are P, PI & PID')

    def __readConfig(self):
        """Read the PID control config file"""
        self.cfg = yamlImport.importYAML("./cfg/controllerSettings/PIDControl.yaml")