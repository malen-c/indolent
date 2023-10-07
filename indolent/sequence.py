import os

import mido
from .helpers import *


class Sequence:
    def __init__(self, length=16, tempo=120, out=None):
        # initializing sequence, defining base pattern length
        self.length = length
        self.pattern = [{} for i in range(length)]
        # tempo(bpm) and quarter note beat length(sec)
        self.tempo = tempo
        self.beat_length = 60 / self.tempo * 0.25

        # MIDI controller
        self.out = out

    def shift(self, steps):
        new = self.__class__(length=self.length, tempo=self.tempo, out=self.out)
        new.pattern = self.pattern[steps:] + self.pattern[:steps]
        return new

    def set_accent(self, subdivision, pitch, value):
        if self.length % subdivision != 0:
            raise(ValueError('Sequence length must be divisible by subdivision'))
        if abs(value) > 1:
            raise(ValueError('Accent value must be between -1 and 1'))

        for step in range(1, self.length, self.length // subdivision * 4):
            self.change_velocity(step, pitch, value, factor=True)
            value = -value

    def set_length(self, factor, with_copy=True):
        if (self.length * factor) % 1 != 0:
            raise TypeError("New pattern length must be int")

        new = self.__class__(length=self.length*factor, tempo=self.tempo, out=self.out)
        if new.length < self.length:
            new.pattern = self.pattern[0:new.length - 1]
            return new

        if with_copy:
            new.pattern = [{} for i in range(new.length)]
            for i in range(self.length):
                for note, velocity in self.pattern[i].items():
                    for x in range(factor):
                        # Place note in its spot in each new measure
                        new.pattern[i + (x * self.length)][note] = velocity
        else:
            new.pattern = self.pattern + [{} for i in range(new.length - self.length)]
        return new

    def set_tempo(self, new_tempo):
        if new_tempo <= 0:
            raise ValueError('Tempo must be positive int or float')
        else:
            self.tempo = new_tempo
            self.beat_length = 60 / self.tempo * 0.25

    def transpose(self, steps):
        if not isinstance(steps, int):
            raise TypeError('Steps to transpose by must be int')
        new = self.__class__(length=self.length, tempo=self.tempo, out=self.out)
        new.pattern = [{note+steps: velocity for note, velocity in self.pattern[i].items()} for i in range(self.length)]
        return new

    def add_note(self, step, pitch, velocity=60):
        # user input steps range from 1 to 16 even though sequence is 0 to 15 e.g.
        self.pattern[step - 1][note_to_midi(pitch)] = velocity

    def change_velocity(self, step, pitch, velocity, factor=False):
        if self.pattern[step - 1].get(note_to_midi(pitch)):
            if factor:
                self.pattern[step - 1][note_to_midi(pitch)] = round(self.pattern[step - 1][note_to_midi(pitch)] * velocity)
            else:
                self.pattern[step - 1][note_to_midi(pitch)] = velocity
        else:
            raise(ValueError("Can't change velocity on note that has not been added to sequence"))

    def play_note(self, pitch=60, velocity=127):
        # print(velocity)
        self.out.send(mido.Message('note_on', note=pitch, velocity=velocity))
        # print(('bop!', 'boop!', 'bum,',
        #        'tiss!', 'bap!', 'tskkk!',
        #        'WAP!')[randint(0, 6)], end=' ')
        # print(pitch, velocity)
        self.stop_note(pitch)

    def stop_note(self, pitch):
        self.out.send(mido.Message('note_off', note=pitch))

    def play(self, repeats=1):
        playing = True
        # absolute step can exceed length of loop, e.g. you can be on
        # step 18 of a 16-step loop if you're on the second repeat
        abs_step = 1
        end = self.length * repeats
        while playing:
            # seq step cannot exceed length of loop
            seq_step = (abs_step - 1) % self.length
            for note, velocity in self.pattern[seq_step].items():
                self.play_note(note, velocity)
            sleep(self.beat_length)
            if abs_step == end:
                for x in self.pattern[-1]:
                    self.stop_note(x)
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
        step_length = mido.second2tick(self.beat_length / 4, mid.ticks_per_beat, mido.bpm2tempo(self.tempo))

        delta = 0
        next_delta = delta + step_length
        for i in range(self.length):
            for note, velocity in self.pattern[i].items():
                track.append(mido.Message('note_on', note=note, velocity=velocity, time=int(delta)))
                track.append(mido.Message('note_off', note=note, time=int(next_delta)))
            delta += step_length
            next_delta += step_length
        mid.save(os.path.abspath(outdir + '/' + name))

    def concatenate(self, other, inplace=True):
        if inplace:
            self.pattern += other.pattern
            self.length += other.length
        else:
            new = self.__class__(length=self.length+other.length, tempo=self.tempo, out=self.out)
            new.pattern = self.pattern + other.pattern
            return new

    def __add__(self, other):
        # Adding two sequences yields their superimposed combination, like hitting play on each simultaneously
        shorter, longer = sorted([self, other], key=lambda x: x.length)

        new = self.__class__(length=longer.length, tempo=self.tempo, out=self.out)
        new.pattern = longer.pattern

        for i in range(shorter.length):
            for note, velocity in shorter.pattern[i].items():
                new.pattern[i][note] = velocity
        return new
