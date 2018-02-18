# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 13:46:46 2017

@author: Wesley

Audio processor.
Opens the pyaudio stream and emits events when there is new data
"""

import pyaudio
import numpy as np

from observer import Observer
from audio_events import DoneProcEvent, DoneFFTEvent
from band_detector import BandDetector
from utilities import get_stereo_mix


class AudioProcessor(Observer):
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 2048
    n = np.arange(0, BUFFER_SIZE, dtype=np.float)
    f = (n*SAMPLE_RATE)/BUFFER_SIZE
    A_WEIGHTS = (10**(.17/20))*(12200**2)*(f**3)/((f**2 + 20.6**2)*(f**2 + 12200**2)*np.sqrt(f**2+158.5**2))    
    SCALE_DEFAULT = 10000

    def __init__(self, audio_device):
        super(AudioProcessor, self).__init__()
        self._device = audio_device
        self._scale = self.SCALE_DEFAULT

        p = pyaudio.PyAudio()
        self._stream = p.open(format = pyaudio.paInt16,
            channels = 1,
            rate = 44100,
            input = True,
            input_device_index = self._device,
            stream_callback = self._new_data_callback,
            frames_per_buffer = self.BUFFER_SIZE
            )

    def set_scale(self, scale):
        self._scale = scale
        
    def _new_data_callback(self, in_data, n_frames, info, flags):
        signal = np.fromstring(in_data, 'Int16')

        # Calculate FFT
        fft = np.abs(np.fft.fft(signal))
        fft = fft*self.A_WEIGHTS
        self.notify(DoneFFTEvent(fft))

        return (None, pyaudio.paContinue)


class TestListener(object):
    def on_notify(self, event):
        print "test_notify"
        print event.r
        print event.g
        print event.b 
        print source

def main():
    ap = AudioProcessor(get_stereo_mix())
    listener = TestListener()
    ap.add_listener(listener)

if __name__ == "__main__":
    main()