
from observer import Observer
from audio_events import DoneFFTEvent
from Tkinter import Tk, Button, Canvas
import numpy as np
import time

NUM_BARS = 64
CANVAS_WIDTH = 256
CANVAS_HEIGHT = 200
BAR_WIDTH = CANVAS_WIDTH/NUM_BARS

class SpectrumGraph(object):
    def __init__(self, root):
        # create bar graph
        self._canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg='black')
        self._canvas.pack()

        self._bars = []
        for pos in range(0, CANVAS_WIDTH, BAR_WIDTH):
            r = self._canvas.create_rectangle(pos, CANVAS_HEIGHT, pos+BAR_WIDTH, 100, fill='white')
            self._bars.append(r)


    """
    Function set_bar_data(self, data)
    Takes a 1d signal of 2^N length, and averages it over the bars, then sets the data to the graph
    eg: an array a[1023:0:] -> a[63:0]
    """
    def set_bar_data(self, data):
        assert(len(data)%NUM_BARS == 0)
        stride = len(data)/NUM_BARS
        bars = np.mean(data.reshape(-1, stride), axis=1) # computes average for bars
        self._set_bars(bars)

    """
    Given a numpy array of length equal to the number of bars, we set each bar to that particular height
    """
    def _set_bars(self, bars):
        for i, pos in enumerate(range(0, CANVAS_WIDTH, BAR_WIDTH)):
            bar_height = min(CANVAS_HEIGHT, CANVAS_HEIGHT*bars[i])
            self._canvas.coords(self._bars[i], pos, CANVAS_HEIGHT, pos + BAR_WIDTH, CANVAS_HEIGHT-bar_height)


class LedTkGui(Observer):
    def __init__(self):
        super(LedTkGui, self).__init__()
        self._root = Tk()
        self._graph = SpectrumGraph(self._root)
        self._graph.set_bar_data(np.zeros(1024))

    def on_notify(self, event):
        if type(event) == DoneFFTEvent:
            self._graph.set_bar_data(event.data)
        else:
            raise("Unknown Event %s" % event)

    def update(self):
        self._root.update_idletasks()
        self._root.update()


def animation(root, graph):
    frame_rate = 60
    ramp = np.array(range(64))/64.0
    r=0
    while(1):
        r+=1
        frame_i = r%64
        data = np.zeros(64)
        data[frame_i] = ramp[frame_i]
        graph._set_bar_data(data)
        time.sleep(1./frame_rate)