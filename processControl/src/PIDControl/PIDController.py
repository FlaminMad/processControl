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

from ..toolClasses.yamlImport import yamlImport


class PIDController:
    """Help Text"""
    def __init__(self):
        self.__readConfig()
        
    
    def runCtrl(self,PV,OP):
        if self.cfg['controlMode'] == "auto":
            return self.__autoControl(PV,OP)
        if self.cfg['controlMode'] == "manual":
            return self.cfg['setPoint']
        return ValueError("Invalid Control Mode")


    def __autoControl(self,PV,OP):
        ERR = self.cfg['setPoint'] - PV
        return self.__vlvLims(self.__algorithm(PV,ERR),ERR)
    

    def __algorithm(self,PV,ERR):
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
        elif self.settings['ctrlType']  == "PID":
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
    
    
    def __transition(self,pv,u,error):
        pass
        
        
    def __tools(self,pv,sp,op,error):
        pass
    
    def __readConfig(self):
        self.cfg = yamlImport.yamlImport("./cfg/controllerSettings/PIDControl.yaml")