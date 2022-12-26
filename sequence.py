import copy
import mido
from random import randint
from helpers import *


class Sequence:
    # initializing sequence, defining base pattern length
    def __init__(self, length: int = 16, tempo: float = 120, out=None):
        self._length = length
        self._pattern = [{} for i in range(length)]
        # tempo(bpm) and step length(sec)
        self._tempo = tempo
        # assumes 4/4 bpm for step length
        self._step_length = 60/self._tempo*0.25
        self.out = out

    def set_length(self, factor: int, with_copy: bool = True):
        if (self._length * factor) % 1 != 0:
            raise Exception("sequence.set_length(factor, with_copy = True) : new pattern length must be int")
        original_length = self._length
        self._length = self._length * factor
        if self._length < original_length:
            self._pattern = self._pattern[0:self._length - 1]
        else:
            if with_copy:
                for x in range(factor):
                    self._pattern.extend(copy.deepcopy(self._pattern))
            elif not with_copy:
                for x in range(self._length - original_length):
                    self._pattern.extend({})

    def set_tempo(self, new_tempo: float):
        if new_tempo <= 0:
            raise Exception('sequence.set_tempo(new_tempo) : tempo must be positive int or float')
        else:
            self._tempo = new_tempo
            self._step_length = 60/self._tempo*0.25

    def add_note(self, step, pitch, velocity=127):
        # user input steps range from 1 to 16 even though sequence is 0 to 15
        self._pattern[step-1][note_to_midi(pitch)] = velocity

    def play_note(self, pitch=60, velocity=127):
        self.out.send(mido.Message('note_on', note=pitch, velocity=velocity))
        print(('bop!', 'boop!', 'bum,',
               'tiss!', 'bap!', 'tskkk!',
               'WAP!')[randint(0, 6)], end=' ')
        print(pitch, velocity)

    def play(self):
        playing = True
        # absolute step can exceed length of loop, e.g. you can be on
        # step 18 of a 16-step loop if you're on the second repeat
        abs_step = 1
        end = self._length
        while playing:
            # seq step cannot exceed length of loop
            seq_step = (abs_step - 1) % self._length
            for note, velocity in self._pattern[seq_step].items():
                # current step mod length of pattern so it repeats
                self.play_note(note, velocity)
            sleep(self._step_length)
            if abs_step == end:
                playing = False
            abs_step += 1
