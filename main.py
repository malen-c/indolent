import time
import copy
from random import randint

#duration in seconds
def sleep(duration):
    start = time.perf_counter()
    while start + duration >= time.perf_counter():
        pass

class note:
    pitch = 'C'
    velocity = 0

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
            self.tempo = new_tempo
            self._step_length = 60/self._tempo*0.25

    def play_note(self, pitch='C', velocity=127):
        print(('bop!', 'boop!', 'bum,',
               'tiss!', 'bap!', 'tskkk!',
               'WAP!')[randint(0, 6)], end = ' ')

    def play(self):
        playing = True
        current_step = 1
        end = self._length * 4
        while playing:
            for note in self._pattern[current_step - 1]:
                self.play_note(self._pattern[current_step - 1][note].pitch,
                               self._pattern[current_step - 1][note].velocity)
            sleep(self._step_length)
            if current_step == end:
                playing = False
            current_step += 1
            
                
            
            


x = sequence()
