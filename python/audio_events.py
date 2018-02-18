# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 13:46:46 2017

@author: Wesley

Events related to audio processing
"""

class AudioEvent(object):
    pass


class DoneFFTEvent(AudioEvent):
    def __init__(self, fft_data):
        self.data = fft_data


class DoneProcEvent(AudioEvent):
    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b


class AudioAvailable(AudioEvent):
    pass