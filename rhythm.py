from sequence import Sequence
import random


class Rhythm:
    def __init__(self, length=None, pattern=None):
        # Fill out pattern with rests
        if pattern is None:
            pattern = []
        if length is None:
            length = len(pattern)
        self.pattern = pattern + [0] * (length - len(pattern))
        self.length = length

    # Todo: add different ways to arpeggiate
    def make_sequence(self, pitches):
        if isinstance(pitches, str):
            pitches = [pitches]
        x = Sequence(length=self.length)
        for i in range(self.length):
            if self.pattern[i]:
                x.add_note(i+1, pitch=pitches[i % len(pitches)])
        return x

    def shift(self, steps):
        new_pattern = self.pattern[steps:] + self.pattern[:steps]
        return self.__class__(length=self.length, pattern=new_pattern)

    def __add__(self, other):
        return self.__class__(length=self.length + other.length, pattern=self.pattern + other.pattern)

    def __repr__(self):
        return f"<Rhythm ({self.length}): {''.join(['x'*i + '.'*(1-i) for i in self.pattern])}>"


def r_euclidean(n, k):
    if k > n:
        raise ValueError("k cannot be greater than n")
    pattern = ['1']*k + ['0']*(n-k)

    r = k
    to_move = min(r, n - r)
    while to_move > 1:
        for i, x in enumerate(pattern[-to_move:]):
            pattern[i] += x
        pattern = pattern[:-to_move]
        r = sum([x == min(pattern) for x in pattern])
        to_move = min(r, len(pattern) - r)
    return Rhythm(pattern=[int(i) for i in ''.join(pattern)])


def r_random(n, k):
    pattern = ['1']*k + ['0']*(n-k)
    random.shuffle(pattern)
    return Rhythm(pattern=[int(i) for i in ''.join(pattern)])


def r_fromstring(pattern):
    pattern = pattern.replace('x', '1')
    pattern = pattern.replace('.', '0')
    return Rhythm(pattern=[int(i) for i in pattern])
