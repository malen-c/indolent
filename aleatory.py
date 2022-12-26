from sequence import Sequence
import numpy as np


def euclidean_rhythm(n, k, pitch):
    if k > n:
        raise ValueError("k cannot be greater than n")
    x = n
    q = k
    r = x % q

    mat = np.zeros((n//2, n), dtype=int)
    mat[0, 0:k] = 1
    step = 1
    end_col = n
    while r > 0:
        mat[step:2*step, :q] = mat[:step, end_col-q:end_col]
        end_col -= q
        x = q
        q = r
        r = x % q
        step += 1
    pattern = mat[:step+1, :end_col].flatten('F')[:n]

    sequence = Sequence(length=n)
    for i, x in enumerate(pattern):
        if x:
            sequence.add_note(i, pitch=pitch)

    return sequence
