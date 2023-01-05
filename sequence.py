import mido
import os
from random import randint
from helpers import *


class Sequence:

    def __init__(self, length=16, tempo=120, out=None):
        # initializing sequence, defining base pattern length
        self.length = length
        self.pattern = [{} for i in range(length)]
        # tempo(bpm) and step length(sec)
        self.tempo = tempo
        # assumes 4/4 bpm for step length
        self.step_length = 60 / self.tempo * 0.25
        self.out = out

    def __mul__(self, other):
        # Multiplying two sequences yields their superimposed combination, essentially hitting play on each
        # simultaneously
        longer = max(self, other, key=lambda x: x.length)
        shorter = min(other, self, key=lambda x: x.length)

        new = self.__class__(length=longer.length, tempo=self.tempo, out=self.out)
        new.pattern = longer.pattern
        for i in range(shorter.length):
            for note, velocity in shorter.pattern[i].items():
                new.pattern[i][note] = velocity
        return new

    def set_length(self, factor, with_copy=True):
        if (self.length * factor) % 1 != 0:
            raise Exception("New pattern length must be int")
        original_length = self.length

        self.length = self.length * factor
        if self.length < original_length:
            self.pattern = self.pattern[0:self.length - 1]
        else:
            if with_copy:
                # Faster to recreate by accessing values directly rather than repeated copy.deepcopy uses
                original_pattern = self.pattern
                self.pattern = [{} for i in range(self.length)]
                for i in range(original_length):
                    for note, velocity in original_pattern[i].items():
                        for x in range(factor):
                            # Place note in its spot in each new measure
                            self.pattern[i + (x * original_length)][note] = velocity
            else:
                self.pattern = self.pattern + [{} for i in range(self.length - original_length)]

    def set_tempo(self, new_tempo):
        if new_tempo <= 0:
            raise ValueError('Tempo must be positive int or float')
        else:
            self.tempo = new_tempo
            self.step_length = 60 / self.tempo * 0.25

    def transpose(self, steps):
        if not isinstance(steps, int):
            raise TypeError('Steps to transpose by must be int')
        self.pattern = [{note+steps: velocity} for i in range(self.length)
                        for note, velocity in self.pattern[i].items()]

    def add_note(self, step, pitch, velocity=127):
        # user input steps range from 1 to 16 even though sequence is 0 to 15
        self.pattern[step - 1][note_to_midi(pitch)] = velocity

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
        end = self.length
        while playing:
            # seq step cannot exceed length of loop
            seq_step = (abs_step - 1) % self.length
            for note, velocity in self.pattern[seq_step].items():
                # current step mod length of pattern so it repeats
                self.play_note(note, velocity)
            sleep(self.step_length)
            if abs_step == end:
                playing = False
            abs_step += 1

    def save_to_mid(self, name, outdir=None):
        if name[-4:] != '.mid':
            name += '.mid'
        if outdir is None:
            outdir = os.getcwd()

        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)

        track.append(mido.Message('program_change', program=12, time=0))
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(self.tempo)))
        step_length = mido.second2tick(self.step_length/4, mid.ticks_per_beat, mido.bpm2tempo(self.tempo))

        delta = 0
        next_delta = delta + step_length
        for i in range(self.length):
            for note, velocity in self.pattern[i].items():
                track.append(mido.Message('note_on', note=note, velocity=velocity, time=int(delta)))
                track.append(mido.Message('note_off', note=note, time=int(next_delta)))
            delta += step_length
            next_delta += step_length
        mid.save(os.path.abspath(outdir + '/' + name))
