# import the necessary packages
import argparse
import os
import time
import cv2
import imutils
import numpy as np
import rtmidi
import threading
import multiprocessing 

from util import *
from signalthread import *

count = 0

# terminal input arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--channel", required=False, default=1,
	help="output midi channel")
ap.add_argument("-p", "--port", required=False, default=2,
	help="midi port inside the channel")
ap.add_argument("-s", "--scale", default='none', required=False,
	help="target scale to quantize the midi signals to.")
args = vars(ap.parse_args())

# set up values based on terminal input args
if args['channel'] == 1:
	channel = 0x90

if args['scale']=='none':
	scale_type = 0 # none
elif 'M' in args['scale']:
	scale_type = 1 # major
elif 'm' in args['scale']:
	scale_type = 2 # minor

if not args['scale']=='none':
	scale_name = args['scale'].lower().rsplit('m',1)[0]
	notes = compute_scale_notes(scale_name, scale_type)
	if len(notes)==0:
		print("Not a valid scale")
		exit()
	

# set up the cv to read the webcam
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)
vs.set(cv2.CAP_PROP_FPS, 25)

# set up rtmidi library and ports
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)
if available_ports:
    midiout.open_port(args['port'])
else:
    midiout.open_virtual_port("Virtual output")


# loop over frames from the webcam stream
with midiout:
	while True:
		
		# grab a frame from webcam
		(grabbed, frame) = vs.read()
		if not grabbed:
			break

		# find the most dominant color in the frame
		data = np.reshape(frame, (-1,3))
		data = np.float32(data)
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
		flags = cv2.KMEANS_RANDOM_CENTERS
		compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

		# add the rgb values of the color together
		color_list=centers[0].astype(np.int32).tolist()
		colorsum=color_list[0]+color_list[1]+color_list[2]
		
		# calculate the midi value
		unit_size=400/(float)(max_midi_note-min_midi_note)
		value=(int)(colorsum/unit_size) + (max_midi_note-1)
		
		if scale_type != 0:
			idx = (np.abs(notes-value)).argmin()
			value = notes[idx]

		# add info text to the frame
		text='Dominant color is: bgr({})'.format(centers[0].astype(np.int32))
		cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)
		text2='MIDI value is: {}'.format(value)
		cv2.putText(frame, text2, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)
		text3='Target scale is: {}'.format(args['scale'])
		cv2.putText(frame, text3, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)

		if count%10==0: # don't make a new sound on each frame
			play_thread = midi_signal_thread(midiout, value)
			play_thread.start()

		# display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
		# add counter (to control the times where new signal threads are made)
		count += 1

# clean up before quiting
midiout.close_port()
del midiout
vs.release()
cv2.destroyAllWindows()
