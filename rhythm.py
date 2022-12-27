from sequence import Sequence
import numpy as np


class Rhythm:
    def __init__(self, length=None, pattern=None):
        # Fill out pattern with rests
        if pattern is None:
            pattern = []
        if length is None:
            length = len(pattern)
        self.pattern = pattern + ['.'] * (length - len(pattern))
        self.length = length

    # Todo: add different ways to arpeggiate
    def make_sequence(self, pitches):
        x = Sequence(length=self.length)
        for i in range(1, self.length+1):
            if self.pattern[i] == 'x':
                x.add_note(i, pitch=pitches[(i-1) % len(pitches)])
        return x

    def __add__(self, other):
        return self.__class__(length=self.length + other.length, pattern=self.pattern + other.pattern)

    def __repr__(self):
        return f"<Rhythm ({self.length}): {''.join(self.pattern)}>"


def euclidean_rhythm(n, k):
    if k > n:
        raise ValueError("k cannot be greater than n")

    mat = np.array(['.'] * (n ** 2)).reshape((n, n))
    mat[0, 0:k] = 'x'
    step = 1

    t = k
    end_col = n

    while t >= 2:
        mat[step:2 * step, :t] = mat[:step, end_col-t:end_col]
        end_col -= t
        t = end_col % t
        step += 1
    pattern = mat[:step+1, :end_col+1].flatten('F')[:n]

    return Rhythm(pattern=pattern.tolist())
