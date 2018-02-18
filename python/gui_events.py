"""
Events related to the GUI
"""
class GUIBaseEvent(object):
    IDS = []
    def __init__(self, id, value):
        assert(id in self.IDS)
        self.id = id
        self.value = value


"""
We can set com_port, audio_device, or scaling
Value must be an integer or float.
"""
class GUIConfigEvent(GUIBaseEvent):
    IDS = ['com_port', 'audio_device', 'scaling']
    def __init__(self, id, value):
        super.__init__(id, value)
        assert(isinstance(value, (int, float)))


"""
We can set either r, g, or b.
Value must be a tuple or list of length 2
"""
class GraphConfigEvent(GUIBaseEvent):
    IDS = ['r', 'g', 'b']
    def __init__(self, id, value):
        super.__init__(id, value)
        assert(len(value)==2)