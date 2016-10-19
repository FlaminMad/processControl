#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: Alexander David Leech
Date:   14/10/2015
Rev:    1
Lang:   Python 2.7
Deps:   <none>
Desc:   OS based tools for smooth trasitions between linux & windows
"""

import os
import sys

if os.name == 'nt':
    import msvcrt
else:
    import select


class osTools:
    """Set of functions useful in working between platforms"""

    def __init__(self):
        """Setup params when instance is initialised"""
        self.osType = self.__osDetect()
        print("Press c to exit")
        pass


    def __osDetect(self):
        """Returns the OS type where 0 represents Windows and 1 Linux"""
        if os.name == 'nt':
            return 0
        elif os.name == 'posix':
            return 1
        else:
            raise SystemExit("Unsupported OS Type")


    def kbdExit(self):
        """Handler for breaking a loop with a keyboard press"""
        if self.osType == 1:
            return self.__linuxExit()
        else:
            return self.__ntExit()

        
    def __linuxExit(self):
        """Checks for the c key being pressed (Linux specific)
        
        :return: boolean
        """
        i,o,e = select.select([sys.stdin],[],[],0.0001)
        for x in i:
            if x == sys.stdin:
                if sys.stdin.readline()  == 'c\n':
                    return True
        return False


    def __ntExit(self):
        """Checks for the c key being pressed (Windows specific)
        
        :return: boolean
        """
        x = msvcrt.kbhit()
        if x:
            if msvcrt.getch() == 'c':
                return True
        return False