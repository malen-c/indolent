import time
import copy
import re
from random import randint

#duration in seconds
def sleep(duration):
    start = time.perf_counter()
    while start + duration >= time.perf_counter():
        pass

#table of natural midi note numbers mod 12
note_numbers = {'C' : 0, 'D' : 2, 'E' : 4, 'F' : 5, 'G' : 7, 'A' : 9, 'B' : 11}
num_reg = re.compile('-?\d+')
def note_to_midi(note):
    #adds 1 if sharp, subtracts 1 if flat, or both if they included both hehe
    midi_num = note_numbers[note[0]] + ('#' in note) - ('b' in note)
    octave_nums = num_reg.search(note)
    if octave_nums == None:
        #defaults to 4th octave
        midi_num += 12 * (4+1)
    else:
        midi_num += 12 * (int(octave_nums[0])+1)
    return(midi_num)

class sequence:

    #initializing sequence, defining base pattern length
    def __init__(self, length = 16, tempo = 120):
        self._length = length
        self._pattern = [{} for i in range(length)]
        #tempo(bpm) and step length(sec)
        self._tempo = tempo
        self._step_length = 60/self._tempo*0.25

    def change_length(self, factor, with_copy = True):
        if type(with_copy) != bool:
            raise Exception("sequence.change_length(factor, with_copy = True) : 'with_copy' must be boolean, not " + str(type(with_copy)))
        if (self._length * factor) % 1 != 0:
            raise Exception("sequence.change_length(factor, with_copy = True) : new pattern length must be int")
        original_length = self._length
        self._length = self._length * factor
        if self._length < original_length:
            self._pattern = self._pattern[0:self._length - 1]
        else:
            if with_copy:
                self._pattern.extend([copy.deepcopy(self._pattern) for x in range(factor)])
            elif not with_copy:
                self._pattern.extend([{} for i in range(self._length - original_length)])

    def change_tempo(self, new_tempo):
        if tempo <= 0:
            raise Exception('sequence.change_tempo(new_tempo) : tempo must be positive int or float')
        else:
            self._tempo = new_tempo
            self._step_length = 60/self._tempo*0.25
    
    def add_note(self, step, pitch, velocity = 127):
        #user input steps range from 1 to 16 even though sequence is 0 to 15
        self._pattern[step-1][note_to_midi(pitch)] = velocity

    def play_note(self, pitch=60, velocity=127):
        print(('bop!', 'boop!', 'bum,',
               'tiss!', 'bap!', 'tskkk!',
               'WAP!')[randint(0, 6)], end = ' ')
        print(pitch, velocity)

    def play(self):
        playing = True
        #absolute step can exceed length of loop, e.g. you can be on step 18 of a 16 step loop if you're on the second repeat
        abs_step = 1
        end = self._length
        while playing:
            #seq step cannot exceed length of loop
            seq_step = (abs_step - 1) % self._length
            for note in self._pattern[seq_step]:
                #current step mod length of pattern so it repeats
                self.play_note(note, self._pattern[seq_step][note])
            sleep(self._step_length)
            if abs_step == end:
                playing = False
            abs_step += 1


x = sequence()
for i in range(1,16):
    x.add_note(i, 'C5')
