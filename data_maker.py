import os
import music21
import numpy as np
import pandas as pd

from joblib import Parallel, delayed


def __pitches_tones__(score):
    pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}
    for pitch in score.pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def __pitches_semitones__(score):
    pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}
    for pitch in score.pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def __get_disk_data__(composerNames, scoreSource, numScores=None):
    paths = []
    for composer in composerNames:
        files = [
            file for file in os.listdir(f"{scoreSource}/{composer}")
            if file.endswith(".mid")
        ]
        if numScores is not None:
            files = files[:numScores]
        paths.append([f"{scoreSource}/{composer}/{file}" for file in files])
    return paths


def __save__(composers, composer_names, target_file_name):
    os.chdir("data")
    for composer in composers:
        label = composer_names[composer[0]]
        os.chdir(label)
        with open(target_file_name, "wb+") as f:
            pickle.dump(composer[1], f)
        os.chdir("..")
    os.chdir("..")


def __make_data__(score_paths, feature_extraction_func, use_corpus=True):
    composers = []
    for j, composer in enumerate(score_paths):
        scoreFeatures = []
        print(f"composer {j+1}/{len(score_paths)}")
        for i, score in enumerate(composer):
            print(f"score {i+1}/{len(composer)}")
            if (use_corpus):
                score = music21.corpus.parse(score)
            else:
                score = music21.converter.parse(score)
            key = score.analyze("key")
            i = music21.interval.Interval(key.tonic,
                                          music21.note.Note('C').pitch)
            score = score.transpose(i)
            scoreFeatures.append(feature_extraction_func(score))
        composers.append((j, scoreFeatures))
    return composers


def main(composer_names,
         feature_extraction_func,
         target_file_name,
         numScores=None,
         scoreSource=None):
    scorePaths = __get_disk_data__(composer_names, scoreSource, numScores)
    composers = __make_data__(
        scorePaths, feature_extraction_func, use_corpus=False)
    __save__(composers, composer_names, target_file_name)


if __name__ == '__main__':
    main(
        composer_names=["schubert"],
        feature_extraction_func=__pitches_tones__,
        target_file_name="pitches.dat",
        scoreSource="../Data",
        numScores=210)
    print("done")
