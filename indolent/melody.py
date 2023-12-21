from indolent.helpers import *


class Note:
    """A single musical note

    Parameters
    ----------
        pitch : str or int
            The pitch of the note being created. If string, interpreted as a note name (e.g. C#). If int, interpreted
            as the MIDI value of
        velocity : int
            The MIDI velocity of the note
        length : (int, int)
            The length of the note in (number of beats, reciprocal of value of beat) i.e. (1, 4) = one quarter note
    """
    def __init__(self, pitch, velocity=60, length=(1, 4)):
        if isinstance(pitch, str):
            self.pitch = note_to_midi(pitch)
        else:
            self.pitch = pitch
        self.velocity = velocity
        self.length = length
