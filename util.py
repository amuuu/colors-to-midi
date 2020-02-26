import numpy as np

max_midi_note = 88 #C8
min_midi_note = 36 #C2

base_notes_values = {"c": 24, "c#": 25, "d": 26, "d#": 27,
					 "e": 28, "f": 29, "f#": 30, "g": 31,
					 "g#": 32, "a": 33, "a#": 34, "b":35}

def compute_scale_notes(scale_name, scale_type):
    if scale_name not in base_notes_values:
        return []
	
    base_note = base_notes_values.get(scale_name)
    notes = []
    
    if scale_type == 1: # major
        for i in range(1, 7): #from c2 to c7 (6 octaves)
            notes.extend([base_note, base_note+2, base_note+4, base_note+5, base_note+7, base_note+9, base_note+11])
            base_note += 12 # go one octave further
            print('in for')
    
    if scale_type == 2: # minor
        for i in range(1, 7): #from c2 to c7 (6 octaves)
            notes.extend([base_note, base_note+2, base_note+3, base_note+5, base_note+7, base_note+8, base_note+10])
            base_note += 12 # go one octave further

    print(notes)
    return np.asarray(notes)
