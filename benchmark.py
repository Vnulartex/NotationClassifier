import music21
import os
import numpy as np
from joblib import Parallel, delayed


def __pitchCounts__(score):
    pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}
    for pitch in score.pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def parse():
    score = music21.converter.parse("debussy_nocturnes_1_(c)siu.mid")
    key = score.analyze("key")
    i = music21.interval.Interval(key.tonic, music21.note.Note('C').pitch)
    score = score.transpose(i)
    return __pitchCounts__(score)


def main():
    os.chdir("../Data/debussy/test")
    a = Parallel(
        n_jobs=-1,
        backend="multiprocessing")(delayed(parse)() for i in range(10))


if __name__ == '__main__':
    main()
