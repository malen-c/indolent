from indolent.melody import Note
from indolent.helpers import note_to_midi


class Chord:
    """A collection of musical notes that sound simultaneously

    Chords are (currently) velocity agnostic and are used more as organizational units than actual music to be played.
    This class is paired with the "chord" constructor function, which makes it easier to put together a particular
    chord.


    Attributes
    ----------
        notes : set(Note)
            The collection of Notes that make up the chord
    """
    def __init__(self, notes):
        if any([not isinstance(x, Note) for x in notes]):
            raise TypeError('Chord must be constructed with an iterable of Note objects')
        self.notes = set(notes)

    def add_note(self, note):
        self.notes.add(Note(pitch=note))

    def __repr__(self):
        return ' '.join([x.pitch_name for x in sorted(self.notes)])


def create_chord(root, minor=False, seven=None, diminished=False, extensions=[]):
    """Constructor method for Chord class

    Parameters
    ----------
        root : str or int
            The root note of the chord as a name (e.g. 'C5' or MIDI code)
        minor : bool, default False
            Whether the chord is minor or not
        seven : str, default None
            Either 'minor' or 'major' if seventh is to be added
        diminished : bool, default False
            Whether the chord is diminished or not
        extensions : list(str) or list(int), default []
            A list of the note names to be added as extensions
    Returns
    -------
        An instance of the Chord class with notes as specified
    """
    # Allow a single extension to be passed as a string
    if isinstance(extensions, str):
        extensions = [extensions]
    if isinstance(root, str):
        root = note_to_midi(root)

    # Add root
    notes = {Note(pitch=root)}

    # Add third
    if minor:
        notes.add(Note(pitch=root+3))
    else:
        notes.add(Note(pitch=root+4))

    # Add fifth
    if diminished:
        notes.add(Note(pitch=root+6))
    else:
        notes.add(Note(pitch=root+7))

    # Add seventh
    if seven is not None:
        if seven == 'minor':
            notes.add(Note(pitch=root+10))
        elif seven == 'major':
            notes.add(Note(pitch=root+11))
        else:
            raise ValueError('Seven must be one of "minor", "major", or None.')

    for pitch in extensions:
        notes.add(Note(pitch=pitch))

    return Chord(notes)
