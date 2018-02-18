"""
Base class for objects implementing the observer pattern
"""
class Observer(object):
    def __init__(self):
        self._listeners = []
    
    def on_notify(self, event):
        raise NotImplementedError

    def notify(self, event):
        for l in self._listeners:
            l.on_notify(event)

    def add_listener(self, listener):
        self._listeners.append(listener)