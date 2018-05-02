import pandas as pd
import re
import os
import random
import music21
from music21 import *

# defines numerical values for notes
notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
note_to_num = dict([[n, i] for i, n in enumerate(notes)])
num_to_note = dict([[v, k] for k, v in note_to_num.items()])

same_note = {'A#':'Bb', 'C#':'Db', 'D#':'Eb', 'F#': 'Gb', 'G#':'Ab'}

def split_note(note):
    assert re.fullmatch('[A-G](#|b)?[0-7]', note) is not None, 'Note not formatted correctly.'
    return note[:-1], int(note[-1])


def name_to_num(name):
    note, octave = split_note(name)
    b = ""
    if note in same_note:
        b = note_to_num[same_note[note]]
    else:
        b = note_to_num[note]
    a = (octave + 1) * 12
    return a + b

print(name_to_num("C4"))

us = music21.environment.UserSettings()
us.getSettingsPath()

directory = os.fsencode("generated_solos/")


def produce_midi(filename, df):
    s1 = music21.stream.Stream()
    mm1 = tempo.MetronomeMark(number=120)
    s1.append(mm1)

    running_offset = 0
    for index, row in df.iterrows():
        note_type = '16th'
        if row[3] < 0.07 and row[3] > 0.0:
            note_type = '16th'
        elif row[3] < 0.15:
            note_type = 'eighth'
        elif row[3] < 0.30:
            note_type = 'quarter'
        elif row[3] < 0.6:
            note_type = 'half'
        elif row[3] < 1:
            note_type = 'whole'
        print(note_type)
        interval_range = random.choice([0, 0, 7, 9])
        i = interval.Interval(interval_range)


        x = music21.note.Note(name_to_num(row[1]), type=note_type)
        y = i.transposeNote(x)
        x.offset = row[2] * 4 + running_offset
        y.offset = x.offset
        s1.insert(x)
        s1.insert(y)

        #EXPERT MACHINE LEARNING
        decision = random.random()
        print(decision)
        if decision < 0.05:
            interval_range = 7
            i = interval.Interval(interval_range)
            i1 = interval.Interval(interval_range + 4)
            i3 = interval.Interval(interval_range -2)
            t1 = i.transposeNote(x)
            t2 = i1.transposeNote(x)
            t3 = i.transposeNote(x)
            t4 = i3.transposeNote(x)
            t1.offset = x.offset + 0.33
            t2.offset = t1.offset + 0.33
            t3.offset = t2.offset + 0.33
            t4.offset = t3.offset + 1
            s1.insert(t1)
            s1.insert(t2)
            s1.insert(t3)
            s1.insert(t4)
            running_offset += 2

        if decision > 0.1 and decision < 0.11:
            interval_range = 3
            i = interval.Interval(interval_range)
            i1 = interval.Interval(interval_range + 3)
            i3 = interval.Interval(interval_range -1)
            t1 = i.transposeNote(x)
            t2 = i1.transposeNote(x)
            t3 = i.transposeNote(x)
            t4 = i3.transposeNote(x)
            t1.offset = x.offset + 0.33
            t2.offset = t1.offset + 0.33
            t3.offset = t2.offset + 0.33
            t4.offset = t3.offset + 1
            s1.insert(t1)
            s1.insert(t2)
            s1.insert(t3)
            s1.insert(t4)
            running_offset += 2

    for note in s1:
        print(note)
        note.volume = random.randint(60, 120)
        if note.duration.quarterLength < 0.01:
            s1.remove(note)

    s1.write("midi", "generated_solos_midis_3/" + filename[:-4] + ".mid")

    s1.show()


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        # print(os.path.join(directory, filename))
        print(filename)
        df = pd.read_csv("generated_solos/" + filename)
        produce_midi(filename, df)
    else:
        continue
