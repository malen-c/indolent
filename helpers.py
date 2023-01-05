import time
import re

# table of natural midi note numbers mod 12
note_numbers = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
midi_notes = {v: k for k, v in note_numbers.items()}
num_reg = re.compile('-?\\d+')


# duration in seconds
def sleep(duration):
    start = time.perf_counter()
    while start + duration >= time.perf_counter():
        pass


def transpose_note(note, steps):
    if not isinstance(steps, int):
        raise TypeError('Steps to transpose by must be int')
    return midi_to_note(note_to_midi(note) + steps)


def note_to_midi(note):
    # adds 1 if sharp, subtracts 1 if flat, or both if they included both hehe
    midi_num = note_numbers[note[0]] + ('#' in note) - ('b' in note)
    octave_nums = num_reg.search(note)
    if octave_nums is None:
        # defaults to 4th octave
        midi_num += 12 * (4+1)
    else:
        midi_num += 12 * (int(octave_nums[0])+1)
    return midi_num


def midi_to_note(midi_num):
    # Never gives flats, sorry
    if not isinstance(midi_num, int):
        raise TypeError('MIDI number must be int')
    letter = midi_notes.get(midi_num % 12)
    sharp = ''
    if letter is None:
        letter = midi_notes[(midi_num-1) % 12]
        sharp = '#'
    octave = str(midi_num // 12 - 1)
    return letter+sharp+octave
