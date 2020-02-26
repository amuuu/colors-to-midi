import threading
import multiprocessing 
import time
import rtmidi

class midi_signal_thread(threading.Thread):
    def __init__(self, midiout, value):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.midiout = midiout
        self.value = value

    def run(self):
        try:
            note_on = [0x90, self.value, 112]
            note_off = [0x80, 60, 0]
            self.midiout.send_message(note_on)
            time.sleep(2)
            self.midiout.send_message(note_off)
            time.sleep(0.2)
        finally:
            self._stop_event.set()
    
    def get_id(self): 
        # returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id