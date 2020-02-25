max_midi_note = 88 #C8
min_midi_note = 36 #C2

base_notes_values = {"c": 24, "c#": 25, "d": 26, "d#": 27,
					 "e": 28, "f": 29, "f#": 30, "g": 31,
					 "g#": 32, "a": 33, "a#": 34, "b":35}

def compute_scale_notes():
    if scale_name not in base_notes_values:
        return False
	
    base_note = base_notes_values.get(scale_name)
    if scale_type == 1: # major
        notes = [base_note, base_note+2, base_note+4, base_note+5, base_note+7, base_note+9, base_note+11]

