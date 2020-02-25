# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import rtmidi

# import local files
from util import *

# terminal input arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--channel", required=False, default=1,
	help="output midi channel")
ap.add_argument("-s", "--scale", default='none', required=False,
	help="target scale to quantize the midi signals to.")
args = vars(ap.parse_args())

# set up values based on terminal input args
if args['channel'] == 1:
	channel = 0x90

if args['scale']=='none':
	pass
elif 'M' in args['scale']:
	scale_type = 1 #major
elif 'm' in args['scale']:
	scale_type = 2 #minor

if not args['scale']=='none':
	scale_name = args['scale'].lower().rsplit('m',1)[0]
	notes = compute_scale_notes(scale_name, scale_type)
	if notes == False:
		print("Not a valid scale")
		exit()
	

# set up the cv to read the webcam
vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)
vs.set(cv2.CAP_PROP_FPS, 25)

# set up rtmidi library and ports
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
if available_ports:
    midiout.open_port(0)
else:
    midiout.open_virtual_port("Virtual output")


# loop over frames from the webcam stream
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
	value= (int)(colorsum/unit_size + (max_midi-1))

	# add info text to the frame
	text='Dominant color is: bgr({})'.format(centers[0].astype(np.int32))
	cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)
	text2='MIDI value is: {}'.format(value)
	cv2.putText(frame, text2, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)
	text3='Target scale is: {}'.format(args['scale'])
	cv2.putText(frame, text3, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)

	# send the midi signal out
	with midiout:
		note_on = [0x90, value, 112] # channel 1, middle C, velocity 112
		# note_off = [0x80, 60, 0]
		midiout.send_message(note_on)
		# time.sleep(0.5)
		# midiout.send_message(note_off)
		# time.sleep(0.1)

	# display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# clean up before quiting
del midiout
vs.release()
cv2.destroyAllWindows()
