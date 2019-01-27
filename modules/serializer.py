import os
import music21
import numpy as np
import pandas as pd

from collections import deque
from joblib import Parallel, delayed
from tqdm import tqdm

filename = "data/chords.csv"


def pitches_tones(score):
    pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}
    for pitch in score.pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def pitches_semitones(score):
    pitchCount = [0] * 12
    for pitch in score.pitches:
        pitchCount[pitch.pitchClass] += 1
    values = np.array(list(pitchCount), dtype="float")
    values /= values.max()
    return values


def chords(score: music21.stream):
    values = deque()
    for note in score.flat.notes:
        noteinfo = []
        if note.isRest:
            noteinfo.append(-1)
        elif note.isChord:
            noteinfo.append(note.root().pitchClass+1)
            noteinfo.extend(note.primeForm)
        else:
            noteinfo.append(note.pitch.pitchClass+1)
        values.append(noteinfo)
    return list(values)


def durations(score):
    values = [note.duration.quarterLength for note in score.flat.notes]
    return values


def parse(path):
    score = music21.converter.parse(path)
    try:
        k = score.flat.keySignature.sharps
    except AttributeError:
        k = score.analyze('key').sharps
    return (score, k)


def extract(f: str, dir: str, composer: str, datasetType: str, funcs):
    path = os.path.join(dir, f)
    dat_path = path+".dat"
    dat_path_t = path+"_t.dat"
    if(os.path.exists(dat_path) and os.path.exists(dat_path_t)):  # exist already parsed dat file
        score = music21.converter.thaw(dat_path)
        score_t = music21.converter.thaw(dat_path_t)
    elif(os.path.getsize(path) > 1e5):
        return
    else:
        try:
            score, k = parse(path)
        except:
            return
        score_t = score.transpose((k*5) % 12)
        music21.converter.freeze(
            score, fmt="pickle", fp=path+".dat")
        music21.converter.freeze(
            score_t, fmt="pickle", fp=path+"_t.dat")
    data = [filename, composer, datasetType]
    data.append(chords(score_t))
    data.append(chords(score))
    data.append(durations(score))
    pd.DataFrame([data]).to_csv(
        filename, header=False, index=False, mode="a")
    # except:
    #     print(f"file {filename} file could not be parsed")


def main():
    root = "C:\\Users\\jiriv\\Disk Google\\ROP\\Data-preprocessed"
    composers = ["bach-js", "handel", "haydn"]
    datasetType = ["train", "test"]
    funcs = [chords, durations]
    ovt = None
    while True:
        key = input(f"Overwrite file {filename}? [Y/N]\n")
        if(key == "y" or key == "Y"):
            ovt = True
        elif(key == "n" or key == "n"):
            ovt = False
        if(ovt is not None):
            break

    if ovt:
        df = pd.DataFrame(columns=["filename", "composer", "data_type",
                                   "chords_t", "chords", "durations"])
        df = df.set_index("filename")
        df.to_csv(filename)
    for composer in composers:
        for data_type in datasetType:
            dir = os.path.join(root, composer, data_type)
            df = pd.read_csv(filename)
            done = df.iloc[:, 0].values
            paths = [f for f in os.listdir(
                dir) if f.endswith(".mxl") and f not in done and os.path.getsize(f) < 1e5]
            Parallel(
                n_jobs=1,
                backend="multiprocessing")(delayed(extract)(f, dir, composer, data_type, funcs)
                                           for f in tqdm(paths, desc=f"processing {composer}/{data_type}"))


if __name__ == '__main__':
    main()
