# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 22:06:33 2017

@author: Wesley
"""
from led_controller import LEDController
import time
import sys

port = 'COM12'

def main():
    controller = LEDController(port)
    time.sleep(1)
    
    delay = 0.016
    
    for r in range(0, 255, 10):
        for g in range(0, 255, 10):
            for b in range(0, 255, 10):
                controller.send_rgb_data(r=r, g=g, b=b)
                time.sleep(delay)
   
    
if __name__ == '__main__':
    main()