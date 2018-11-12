import os
import music21
import numpy as np
import pandas as pd

from joblib import Parallel, delayed
from tqdm import tqdm


# timeout function that lets move on beyond too big files.
# by Thomas Ahle: http://stackoverflow.com/a/22348885
import signal


class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        signal.alarm(0)


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


def extract(filename: str, dir: str, composer: str, datasetType: str, funcs):
    path = os.path.join(dir, filename)
    if(os.path.getsize(path) > 10000):
        with timeout(seconds=600):
            try:
                score = music21.converter.parse(path)
                try:
                    k = score.flat.keySignature.sharps
                except AttributeError:
                    k = score.analyze('key').sharps
                except:
                    print(f"{path} key could not be analyzed")
                    return
                score_t = score.transpose((k*5) % 12)
                score.freeze
                data = [filename, composer, datasetType]
                for func in funcs:
                    data.extend(func(score))
                pd.DataFrame(np.array([data])
                             ).to_csv("data.csv", header=False, index=False, mode="a")


def main():
    root = "../Data"
    composer = "brahms"
    datasetType = "test"
    funcs = [pitches_tones, pitches_semitones]

    # # delete after first file
    # pd.DataFrame(columns=["filename", "composer", "data_type", "st0", "st1",
    #                       "st2", "st3", "st4", "st5", "st6", "t0", "t1", "t2",
    #                       "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10", "t11"]).to_csv("data.csv", index=False)

    dir = os.path.join(root, composer, datasetType)
    paths = [f for f in os.listdir(dir) if f.endswith(".mid")]
    Parallel(
        n_jobs=-1,
        backend="multiprocessing")(delayed(extract)(f, dir, composer, datasetType, funcs) for f in tqdm(paths, ascii=True))


if __name__ == '__main__':
    main()
