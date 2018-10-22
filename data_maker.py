import os
import pickle
import random

import music21
import numpy as np


def _pitchCounts(score):
    pitchCount = {"C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "A": 0, "B": 0}
    for pitch in score.pitches:
        pitchCount[pitch.step] += 1
    values = np.array(list(pitchCount.values()), dtype="float")
    values /= values.max()
    return values


def _getCorpusPaths(composerNames, numScores):
    if (numScores is not None):
        scorePaths = [
            random.sample(music21.corpus.getComposer(composer), numScores)
            for composer in composerNames
        ]
    else:
        scorePaths = [
            music21.corpus.getComposer(composer) for composer in composerNames
        ]
    return scorePaths


def _getDiskData(composerNames, scoreSource, numScores=None):
    paths = []
    for composer in composerNames:
        files = [
            file for file in os.listdir(f"{scoreSource}/{composer}")
            if file.endswith(".mxl")
        ]
        if numScores is not None:
            files = files[:numScores]
        paths.append([f"{scoreSource}/{composer}/{file}" for file in files])
    return paths


def _save(composers, composer_names, target_file_name):
    os.chdir("data")
    for composer in composers:
        label = composer_names[composer[0]]
        os.chdir(label)
        with open(target_file_name, "wb+") as f:
            pickle.dump(composer[1], f)
        os.chdir("..")
    os.chdir("..")


def _makeData(score_paths, feature_extraction_func, use_corpus=True):
    composers = []
    for j, composer in enumerate(score_paths):
        scoreFeatures = []
        for score in composer:
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
    if (scoreSource is None):
        scorePaths = _getCorpusPaths(composer_names, numScores)
        composers = _makeData(
            scorePaths, feature_extraction_func, use_corpus=True)
    else:
        scorePaths = _getDiskData(composer_names, scoreSource, numScores)
        composers = _makeData(
            scorePaths, feature_extraction_func, use_corpus=False)
    _save(composers, composer_names, target_file_name)


if __name__ == '__main__':
    main(
        composer_names=["debussy"],
        feature_extraction_func=_pitchCounts,
        target_file_name="pitches.dat",
        scoreSource="../Data")
    print("done")
