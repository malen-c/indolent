from indolent.helpers import *


class Note:
    """A single musical note

    Attributes
    ----------
        pitch : int
            The pitch of the note in MIDI code
        pitch_name : str
            The pitch of the note in name
        velocity : int
            The MIDI velocity of the note
        length : (int, int)
            The length of the note in (number of beats, reciprocal of value of beat) i.e. (1, 4) = one quarter note
    """
    def __init__(self, pitch, velocity=60, length=(1, 4)):
        if isinstance(pitch, str):
            self.pitch_name = pitch
            self.pitch = note_to_midi(pitch)
        else:
            self.pitch_name = midi_to_note(pitch)
            self.pitch = pitch
        self.velocity = velocity
        self.length = length

    def __hash__(self):
        return hash(self.pitch)

    def __eq__(self, other):
        return self.pitch == other.pitch

    def __repr__(self):
        return f'<Note> \nPitch: {self.pitch_name}, Velocity: {self.velocity}, Length: {self.length[0]}/{self.length[1]}\n'

    def __lt__(self, other):
        return self.pitch < other.pitch
