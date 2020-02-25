# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import rtmidi

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--midi-channel", required=False, default=1,
	help="output midi channel")
ap.add_argument("-s", "--scale", default='CM', required=False,
	help="target scale to quantize the midi signals to")
args = vars(ap.parse_args())

if args['midi-channel'] == 1:
	channel = 0x90


vs = cv2.VideoCapture(0)
vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)
vs.set(cv2.CAP_PROP_FPS, 25)

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

	data = np.reshape(frame, (-1,3))
	data = np.float32(data)

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	flags = cv2.KMEANS_RANDOM_CENTERS
	compactness,labels,centers = cv2.kmeans(data,1,None,criteria,10,flags)

	color_list=centers[0].astype(np.int32).tolist()
	colorsum=color_list[0]+color_list[1]+color_list[2]
	min_midi = 36 #c2
	max_midi = 88 #c8
	unit_size=400/(float)(max_midi-min_midi)
	value= (int)(colorsum/unit_size + (max_midi-1))

	text='Dominant color is: bgr({})'.format(centers[0].astype(np.int32))
	cv2.putText(frame, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)

	text2='MIDI value is: {}'.format(value)
	cv2.putText(frame, text2, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 10 , 2)

	with midiout:
		note_on = [0x90, value, 112] # channel 1, middle C, velocity 112
		# note_off = [0x80, 60, 0]
		midiout.send_message(note_on)
		# time.sleep(0.5)
		# midiout.send_message(note_off)
		# time.sleep(0.1)

	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

del midiout
vs.release()
cv2.destroyAllWindows()
