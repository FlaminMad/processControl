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

import time
from yamlImport import yamlImport

from pymodbus.client.sync import ModbusTcpClient, ModbusSerialClient
from pymodbus.exceptions  import ModbusIOException, ConnectionException
from pymodbus.payload     import BinaryPayloadBuilder, BinaryPayloadDecoder
from pymodbus.constants   import Endian

class modbusClient:
    """Class to carry out MODBUS read/write requests
    
    Usage:  Ensure all params are setup in the 'modbusSettings' file
            Call 'openConnection' to connect to the assigned server
            Use 'dataHandler' to read or write data to the server
            Call 'closeConnection' to safely close the connection
    """

    def __init__(self):
        """Load settings and connect to the designated slave"""
        
        self.modbusCfg = yamlImport.importYAML("./cfg/modbusSettings.yaml")
        if self.modbusCfg['logging'] == "enable":
            self.log = self.__logging()
        if self.__setupClient() == 0:
            return 0
        if self.openConnection() == 0:
            return 0
            
            
    def __logging(self):
        """Setup and enable logging on the client
        
        :return: enabled log instance
        """
        import logging
        logging.basicConfig()
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        return log
        
        
    def __setupClient(self):
        """Setup MODBUS client object"""
        if self.modbusCfg['method'] == "tcp":
            try:
                self.client = ModbusTcpClient(self.modbusCfg['ip'],\
                                              self.modbusCfg['tcpPort'])
            except:
                raise
                return 0
        elif self.modbusCfg['method'] == "rtu":
            try:
                self.client = ModbusSerialClient(self.modbusCfg['method'],\
                                                 self.modbusCfg['rtuPort'],\
                                                 self.modbusCfg['stopbits'],\
                                                 self.modbusCfg['bytesize'],\
                                                 self.modbusCfg['parity'],\
                                                 self.modbusCfg['baudrate'],\
                                                 self.modbusCfg['timeout'])
            except:
                raise
                return 0
            else:
                raise NameError("Unsupported method")
                return 0
            
            
    def openConnection(self):
        """Attempt connection with the MODBUS server"""
        for i in range(3):
            if self.client.connect() == True:
                return 1
            else:
                print "Attempt " + str(i) + " failed"
            if i == 2:
                raise IOError("Failed to connect to specified server")
                return 0
            time.sleep(0.5)
   

    def closeConnection(self):
        """Close connection with the MODBUS server"""
        try:
            self.client.close()
        except:
            print("Error - See log for details")
            return 0
        return 1
        
    
    def dataHandler(self, op, reg, addr, length=None, data=None, encoding=1):
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
        if op == 'r':
            for i in range(3):
                r = self.__readData(reg, addr, length, encoding)
                if (r == ConnectionException) or (r == ModbusIOException):
                    print("Read attempt " + str(i) + " failed")
                    if i == 2:
                        #TODO: remove sys exit and handle properly
                        raise SystemExit('Modbus Error: Failed 3 Attemps')
                elif r == ValueError:
                    #TODO: remove sys exit and handle properly
                    raise SystemExit('Invalid operation')
                else:
                    return r

        elif op == 'w':
            for i in range(3):           
                w = self.__writeData(reg, addr, data, encoding)
                if (w == ConnectionException) or (w == ModbusIOException):
                    print("Write attempt " + str(i) + " failed")
                    if i == 2:
                        #TODO: remove sys exit and handle properly
                        raise SystemExit('Modbus Error: Failed 3 Attemps')
                elif w == ValueError:
                    #TODO: remove sys exit and handle properly
                    raise SystemExit('Invalid operation')
                else:
                    return w
         
        else:
            return ValueError('Invalid Operation')
            
    
    def __readData(self, reg, addr, length, encoding):
        """Read data from the MODBUS Slave
        
        Called by 'dataHandler' in modbusClient.py
        
        Arguments:
        :param reg:      Modbus register to access (1-4)
        :param addr:     Address to start reading from
        :param length:   Quantity of registers to read
        :param encoding: States whether data should be decoded
        :type reg:       int
        :type addr:      int
        :type length:    int
        :type encoding: int
        
        :return:         List containing the requested data or failure exception.
        """
        data = []
        
        if 1 <= reg <= 2:
            try:
                if reg == 1:
                    co = self.client.read_coils(addr,length,unit=0x01)
                else:
                    co = self.client.read_discrete_inputs(addr,length,unit=0x01)
            except ConnectionException:
                return ConnectionException
            
            if co.function_code != reg:
                return ModbusIOException
                
            for i in range(length):
                data.append(co.getBit(i))
            return data
        
        
        elif 3 <= reg <= 4:
            try:
                if reg == 3:
                    hr = self.client.read_holding_registers(addr,length,unit=0x01)
                else:
                    hr = self.client.read_input_registers(addr,length,unit=0x01)
            except ConnectionException:
                return ConnectionException
            
            if hr.function_code != reg:
                return ModbusIOException
                
            for i in range(length):
                data.append(hr.getRegister(i))
            
            if encoding == 1:
                return self.__decodeData(data)
            return data
        
        else:
            return ValueError
            
    
    def __writeData(self, reg, addr, data, encoding):
        """Write data to the MODBUS slave
        
        Called by 'dataHandler' in modbusClient.py
        
        Arguments:
        :param reg:      Modbus register to access (15 or 16)
        :param addr:     Address to start writing to
        :param data:     List of data to write to the device
        :param encoding: States whether data should be encoded first
        :type reg:       int
        :type addr:      int
        :type length:    int
        :type encoding: int
        
        :return:         success or failure exception
        """
        if reg == 15:
            try:
                co = self.client.write_coils(addr,data,unit=0x01)
            except ConnectionException:
                return ConnectionException
            
            if co.function_code != reg:
                return ModbusIOException
        
        elif reg == 16:
            if encoding == 1:
                data = self.__encodeData(data)
            
            try:
                hr = self.client.write_registers(addr,data,unit=0x01)
            except ConnectionException:
                return ConnectionException
            
            if hr.function_code != reg:
                return ModbusIOException
            
        else:
            return ValueError
        
    
    def __encodeData(self, data):
        """Encode data to 32bit float
        
        Function encodes a list of data passed to it into a 32 bit float
        packet that can be written directly to the MODBUS server table.
        
        Arguments:
        :param data: Float to be encoded
        :type data: list
        """
        builder = BinaryPayloadBuilder(endian=Endian.Little)
        try:
            for i in range(0,len(data)):
                builder.add_32bit_float(data[i])
        except TypeError:
            builder.add_32bit_float(data)
        return builder.to_registers()

    def __decodeData(self, data):
        """Decode MODBUS data to float
        
        Function decodes a list of MODBUS 32bit float data passed to it
        into its respective list of floats.
        
        Arguments:
        :param data: Data to be decoded
        :type data: list
        """
        returnData = [0]*(len(data)/2)
        decoder = BinaryPayloadDecoder.fromRegisters(data, endian=Endian.Little)
        for i in range(0,len(data)/2):
            returnData[i] = round(decoder.decode_32bit_float(),2)
        return returnData