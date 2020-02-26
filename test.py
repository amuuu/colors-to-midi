# import the necessary packages
import argparse
import os
import time
import cv2
import imutils
import numpy as np
import rtmidi


# set up rtmidi library and ports
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(2)
else:
    midiout.open_virtual_port("Virtual output")

while True:
	# send the midi signal out
	with midiout:
		note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
		note_off = [0x80, 60, 0]
		midiout.send_message(note_on)
		time.sleep(0.5)
		midiout.send_message(note_off)
		time.sleep(0.1)

# clean up before quiting
del midiout
