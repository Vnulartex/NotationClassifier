import random
import numpy as np
import pandas as pd
import ast
import os
import music21
import modules.serializer as maker
from tqdm import tqdm
from collections import Counter
from fractions import Fraction

filename = "C:\\Users\\jiriv\\Disk Google\\ROP\\chords.csv"


class Classifier:
    def __init__(self, clf, composers, vectorizer, ser_func, des_func):
        self.clf = clf
        self.composers = composers
        self.vectorizer = vectorizer
        self.ser_func = ser_func
        self.des_func = des_func


def get_data_counts(y, composer_names):
    counts = Counter(y)
    return {composer_names[key]: value for key, value in counts.items()}


def shuffle_data(x, y):
    c = list(zip(x, y))
    random.shuffle(c)
    return zip(*c)


def pad_or_truncate(a, n):
    for i, x in enumerate(a):
        if(len(x) < n):
            x.extend([0] * (n-len(x)))
        else:
            a[i] = x[:n]


def get_root(X):
    return [str([chord[0] for chord in example]) for example in X]


def load_file(path, dataset):
    if (dataset not in ["chords", "chords_t", "durations"]):
        raise ValueError("Invalid dataset type")
    score, k = maker.parse(path)
    if(dataset == "chords_t"):
        score_t = score.transpose((k*5) % 12)
        return maker.chords(score_t)
    elif(dataset == "chords"):
        return maker.chords(score)
    else:
        return maker.durations(score)


def load(features_type, composer_names, train_count=None, df=None):
    if features_type == "chords":
        features_type = ["chords"]

    elif features_type == "chords_t":
        features_type = ["chords_t"]

    elif features_type == "durations":
        features_type = ["durations"]

    else:
        raise ValueError("Invalid dataset type")

    if (df == None):
        df = pd.read_csv(filename)
    X_train, X_test, y_train, y_test = [], [], [], []
    for i, comp in enumerate(composer_names):
        for d_type in ("train", "test"):
            data = df.loc[(df["composer"] == comp) & (
                df["data_type"] == d_type), features_type].values

            data = [[feature for feature in eval(
                    piece[0])] for piece in data]

            if(train_count is not None):
                data = data[:train_count]

            if(d_type == "train"):
                X_train.extend(data)
                y_train.extend([i]*len(data))
            elif(d_type == "test"):
                X_test.extend(data)
                y_test.extend([i]*len(data))

    return (X_train, X_test, y_train, y_test)


def main():
    pass
    # print(load_folder("midis", "chords"))

    # y_train = load("chords_t", ["debussy", "mozart",
    #                             "beethoven", "tchaikovsky", "victoria"])[2]
    # print(get_data_counts(y_train, ["debussy", "mozart",
    #                                 "beethoven", "tchaikovsky", "victoria"]))
    # load("t", ["debussy", "haydn"])


if __name__ == '__main__':
    main()
