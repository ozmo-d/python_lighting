# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 12:39:13 2017

@author: Wesley

Simple LED controller sends RGB data which is written uniformly to the LEDs
packet = [R, G, B]; where each is one byte.

"""

import serial
    
class LEDController(object):
    START= chr(1)
    STOP = chr(2)
    DATA = chr(0)
    ADDR_WIDTH = 50
    
    def __init__(self, port):
        """
        port : port compatible with serial, such as 'com1'
        """
        self._serial = serial.Serial(port=port, timeout=1, baudrate=9600)
        self.zero_leds()
        
    def zero_leds(self):
        self.send_rgb_data(r=0, g=0, b=0)
        
    def send_rgb_data(self, r, g, b):
        cmd_array = (chr(r), chr(g), chr(b))
        cmd_bytes = b''.join(cmd_array)
        self._write(cmd_bytes)
        
    def _write(self, packet):
        print packet.__repr__()
        print self._serial.write(packet)