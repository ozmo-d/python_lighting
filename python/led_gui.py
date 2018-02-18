# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 13:46:46 2017

@author: Wesley

Gui for controlling LEDs
"""

from kivy.app import App
from kivy.uix.button import Button

class LedGui(App):
    def build(self):
        return Button(text='Yo Mama')

LedGui().run()
