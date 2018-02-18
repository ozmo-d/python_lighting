# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 13:46:46 2017

@author: Wesley

Audio processor.
Opens the pyaudio stream and emits events when there is new data
"""
from audio_events import DoneProcEvent
from observer import Observer
import numpy as np


class BandDetector(Observer):
    def __init__(self, band_settings=None):
        super(BandDetector, self).__init__()
        self.bands = {'r' : [0, 100],
                      'g' : [100, 200],
                      'b' : [200, 300] }
    
    def process(self, FFT):
        # Create rgb tuple
        rgb = ()
        for _, bounds in self.bands.iteritems():
            val = np.mean(FFT[bounds[0]:bounds[1]])
            val = min(255*val, 255)
            rgb += (val,)

        return rgb

    def set_band(self, id, band):
        assert(id in self.bands.keys())
        assert(len(band)==2)
        self.bands[id] = band

    def on_notify(self, event):
        rgb = self.process(event.data)
        self.notify(DoneProcEvent(*rgb))
