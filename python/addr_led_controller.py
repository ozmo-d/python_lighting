# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 21:14:18 2017

@author: Wesley

This LED controller passed the values to individual addresses in
this format
[CMD, ADDR, R, G, B]

This used too much bandwidth to be practical

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
        self._send_cmd(self.START)
        self.send_rgb_data()
        self._send_cmd(self.STOP)
        
    def _send_cmd(self, cmd):
        cmd_bytes = cmd + 4*chr(0)
        self._write(cmd_bytes)
        
    def send_rgb_data(self, r=0, g=0, b=0):
        cmds = []
        for addr in range(self.ADDR_WIDTH):
            cmd_array = (self.DATA, chr(addr), chr(r), chr(g), chr(b))
            cmd_bytes = b''.join(cmd_array)
            assert len(cmd_bytes)==5, "bad command %s" % cmd_bytes
            cmds.append(cmd_bytes)
   
        self._send_cmd(self.START)
        for cmd in cmds:
            self._write(cmd)
        self._send_cmd(self.STOP)
        
    def _write(self, packet):
        print packet.__repr__()
        print self._serial.write(packet)