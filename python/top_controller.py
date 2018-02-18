# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 22:06:33 2017

@author: Wesley

Top controller holds instances of the LED Controller, Audio Processor,
and GUI. All of the events are hooked up in this file; it mediates communication
between the modules.
"""

from led_controller import LEDController
from audio_processor import AudioProcessor
from band_detector import BandDetector
from audio_events import DoneProcEvent
from gui_events import GUIConfigEvent, GraphConfigEvent
from utilities import get_stereo_mix
from led_tk_gui import LedTkGui
from observer import Observer


COM_PORT = 'COM15'

"""
Top Controller
Initializes with empty LEDController, AudioProcessor, and BandDetector instances
"""
class TopController(Observer):
    def __init__(self):
        super(TopController, self).__init__()
        self._led_controller = None
        self._audio_proc = None
        self._band_detector = None
        self._gui = LedTkGui()
        
    def set_led_controller(self, com_port):
        self._led_controller = LEDController(com_port)

    def set_audio_proc(self, audio_device):
        self.audio_proc = AudioProcessor(audio_device)
        self.audio_proc.add_listener(self)
        self.audio_proc.add_listener(self._gui)
        self._band_detector = BandDetector()

    def set_audio_scaling(self, value):
        if self._audio_proc:
            self._audio_proc.set_scale(value)

    def update_band_detector(self, event):
        if self._band_detector:
            self._band_detector.set_band(event.id, event.value)

    def on_notify(self, event):
        if type(event) == GUIConfigEvent:
            if event.id == 'com_port':
                self.set_led_controller(event.value)
            if event.id == 'audio_device':
                self.set_audio_proc(event.value)
            if event.id == 'scaling':
                self.set_audio_scaling(event.value)
        
        if type(event) == DoneProcEvent:
            if self._led_controller:
                self._led_controller.send_rgb_data(event.r, event.g, event.b)

        if type(event) == GraphConfigEvent:
            self.update_band_detector(event)

    def start(self):
        self._gui._root.mainloop()


def main():
    audio_device = get_stereo_mix()
    if audio_device < 0:
        raise("Stereo Mix device not found")

    controller = TopController()
    controller.set_audio_proc(audio_device)
    controller.start()
    return

if __name__ == '__main__':
    main()