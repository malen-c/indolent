from indolent.melody import Note


class Chord:
    """A collection of musical notes that sound simultaneously

    Attributes
    ----------
        notes : set(Note)
            The collection of Notes that make up the chord
    """
    def __init__(self, notes):
        self.notes = set(notes)

    def add_note(self, note):
        self.notes.add(Note(pitch=note))


def create_chord(root, minor=False, seven=None, extensions=None):
    chord = Chord()