import os
import music21
import numpy as np
import pandas as pd

from collections import deque
from joblib import Parallel, delayed
from tqdm import tqdm


# timeout function that lets move on beyond too big files.
# by Thomas Ahle: http://stackoverflow.com/a/22348885
import signal


# class timeout:
#     def __init__(self, seconds=1, error_message='Timeout'):
#         self.seconds = seconds
#         self.error_message = error_message

#     def handle_timeout(self, signum, frame):
#         raise TimeoutError(self.error_message)

#     def __enter__(self):
#         signal.signal(signal.SIGALRM, self.handle_timeout)
#         signal.alarm(self.seconds)

#     def __exit__(self, type, value, traceback):
#         signal.alarm(0)


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
            noteinfo.extend(note.primeForm)
            noteinfo.append(note.root().pitchClass)
        else:
            noteinfo.append(note.pitch.pitchClass)
        values.append(noteinfo)
    return list(values)


def durations(score):
    values = [note.duration.quarterLength for note in score.flat.notes]
    return values


def extract(filename: str, dir: str, composer: str, datasetType: str, funcs):
    path = os.path.join(dir, filename)
    dat_path = path+".dat"
    dat_path_t = path+"_t.dat"
    if(os.path.exists(dat_path) and os.path.exists(dat_path_t)): #exist already parsed dat file
        score = music21.converter.thaw(dat_path)
        score_t = music21.converter.thaw(dat_path_t)
    elif(os.path.getsize(path) < 10000):
        return
        # with timeout(seconds=600):
        # try:
    else:
        score = music21.converter.parse(path)
        try:
            k = score.flat.keySignature.sharps
        except AttributeError:
            k = score.analyze('key').sharps
        except:
            print(f"{path} key could not be analyzed")
            return
        score_t = score.transpose((k*5) % 12)
        basename = filename.replace(".mid", "").replace(".mxl", "")
        music21.converter.freeze(
            score, fmt="pickle", fp=path+".dat")
        music21.converter.freeze(
            score_t, fmt="pickle", fp=path+"_t.dat")
    data = [filename, composer, datasetType]
    data.append(chords(score_t))
    data.append(chords(score))
    data.append(durations(score))
    pd.DataFrame([data]).to_csv(
        "chords.csv", header=False, index=False, mode="a")
    # except:
    #     print(f"file {filename} file could not be parsed")


def main():
    root = "C:\\Users\\jiriv\\Disk Google\\ROP\\Data-preprocessed"
    composers = ["debussy", "mozart", "beethoven", "victoria", "scarlatti"]
    datasetType = ["train", "test"]
    funcs = [chords, durations]

    # delete after first file
    df = pd.DataFrame(columns=["filename", "composer", "data_type",
                               "chords_t", "chords", "durations"])
    df = df.set_index("filename")
    df.to_csv("chords.csv")
    for composer in composers:
        for data_type in datasetType:
            dir = os.path.join(root, composer, data_type)
            df = pd.read_csv("chords.csv")
            done = df.iloc[:, 0].values
            paths = [f for f in os.listdir(
                dir) if f.endswith(".mxl") and f not in done]
            # paths = ["ar2.mid"]
            Parallel(
                n_jobs=-1,
                backend="multiprocessing")(delayed(extract)(f, dir, composer, data_type, funcs)
                                           for f in tqdm(paths, desc=f"processing {composer}/{data_type}"))


if __name__ == '__main__':
    main()
