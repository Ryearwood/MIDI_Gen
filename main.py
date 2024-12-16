from midiutil import MIDIFile
from mingus.core import chords
import os

OUTPUT_DIR = "Generated_MIDI"
OUTPUT_FILENAME = "pure-edm-fire-arpeggio"
SUFFIX = ".mid"

NOTES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

chord_progression = ["Cmaj7", "Cmaj7", "Fmaj7", "Gdom7"]

errors = {"notes": "Bad input, please refer to this spec-\n"}


def swap_accidentals(note: str) -> str:
    """Function to replace note values based on existing nuance in music theory.
    For example: The note Bb is physically the same note as A# but in different contexts
    its referred to by a different names. This function helps simplify this nuance.

    Args:
        note (str): The key note in question

    Returns:
        str: Corrected key note
    """
    if note == "Db":
        return "C#"
    if note == "D#":
        return "Eb"
    if note == "E#":
        return "F"
    if note == "Gb":
        return "F#"
    if note == "G#":
        return "Ab"
    if note == "A#":
        return "Bb"
    if note == "B#":
        return "C"
    return note


def note_to_number(note: str, octave: int) -> int:
    """Function to map a given note within an Octave into its corresponding numerical
    value as understood by the MIDIUtil tooling library. "MidiUtil" does not understand
    notes as strings, but does understand them numerically (ex. 'C' vs 60).

    Args:
        note (str): string representation of musical note
        octave (int): Octave range

    Returns:
        int: numerical representation of the original provided note.
    """
    note = swap_accidentals(note)
    assert note in NOTES, errors["notes"]
    assert octave in OCTAVES, errors["notes"]

    note = NOTES.index(note)
    note += NOTES_IN_OCTAVE * octave

    assert 0 <= note <= 127, errors["notes"]
    return note


array_of_notes = []
for chord in chord_progression:
    array_of_notes.extend(chords.from_shorthand(chord))

array_of_note_numbers = []
for note in array_of_notes:
    OCTAVE = 4
    array_of_note_numbers.append(note_to_number(note, OCTAVE))

# Configuration for MIDI Generation
track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 120  # In BPM
volume = 100  # 0-127, as per the MIDI standard

# One track, defaults to format 1 (tempo track is created automatically)
MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(array_of_note_numbers):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME, SUFFIX), "wb") as output_file:
    MyMIDI.writeFile(output_file)
