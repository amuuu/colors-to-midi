# Colors to MIDI!
Convert the colors the webcam captures to midi (cv) signals using `cv2` and `python-rtmidi` library

## How to Run?
You will need a webcam to be captured by the program and a deviced connected via midi to your computer to be sent signals to. To run the program, enter the below command in terminal:

```
python color2midi.py -s C#m -c 1 -p 2
```

`-c` is for midi output channel, `-p` is for the port, and `-s` is for the target scale. It currently has only major and minor scales. Use "M" for major and "m" for minor.
