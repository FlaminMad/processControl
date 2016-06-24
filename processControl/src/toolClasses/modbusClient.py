#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Alexander David Leech
@date:   Wed Jun 15 20:16:53 2016
@rev:    1
@lang:   Python 2.7
@deps:   pymodbus
@desc:   Class to carry out MODBUS read/write requests
"""

from yamlImport import yamlImport

class modbusClient:
    """Class to carry out MODBUS read/write requests"""
    
    def __init__(self):
        """Load settings and connect to the designated slave"""
        
        self.modbusCfg = yamlImport.importYAML("../cfg/.yaml")
        if self.modbusCfg['logging'] == "enable":
            self.log = self.__logging()
        #Open connection
        
        pass
    
    def dataHandler(self, op, reg, addr, length=None, data=None):
        """Handle the MODBUS read/write requests and pass to the appropriate function
        
        Arguments:
        :param op: Operation to perform (R/W)
        :param reg: Modbus register to access (1-4)
        :param addr: Address to start operation at
        :type op:  string
        :type reg: int
        :type addr: int
        
        Keyword Arguments:
        :param length: Length of registers to read (default None)
        :param data: Data to write to the slave
        :type length: int
        :type data: list
        
        :return: List containing the requested data or confimation of send.
        """
        pass
    
    def __readData(self, reg, addr, length):
        """Read data from the MODBUS Slave
        
        Called by 'dataHandler' in modbusClient.py
        
        Arguments:
        :param reg: Modbus register to access (1-4)
        :param addr: Address to start reading from
        :param length: Quantity of registers to read
        :type reg: int
        :type addr: int
        :type length: int
        
        :return: List containing the requested data.
        """
        pass
    
    def __writeData(self, reg, addr, data):
        """Write data to the MODBUS slave
        
        Called by 'dataHandler' in modbusClient.py
        
        Arguments:
        :param reg: Modbus register to access (1-4)
        :param addr: Address to start reading from
        :param data: Data to write to the slave
        :type reg: int
        :type addr: int
        :type data: list
        
        :return: Success or failure
        """
        pass
    
    def __encodeData(self, data):
        """Encode data to 32bit float
        
        Function encodes a list of data passed to it into a 32 bit float
        packet that can be written directly to the MODBUS server table.
        
        Arguments:
        :param data: Float to be encoded
        :type data: list
        """
        pass

    def __decodeData(self, data):
        """Decode MODBUS data to float
        
        Function deodes a list of MODBUS 32bit float data passed to it
        into its respective list of floats.
        
        Arguments:
        :param data: Data to be decoded
        :type data: list
        """
        pass
    
    def __logging(self):
        """Setup and enable logging on the client        
        
        :return: enabled log instance
        """
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        return log