import os
import pickle
import random
import numpy as np
import pandas as pd
import ast


def get_data_counts(composers):
    df = pd.read_csv("data.csv")
    counts = []
    for composer in composers:
        comp = df.loc[(df["composer"] == composer)]
        train_count = len(comp.loc[(comp["data_type"] == "train")])
        counts.append(train_count)
    return counts


def shuffle_data(X_train, X_test, y_train, y_test):
    c = list(zip(X_train, y_train))
    random.shuffle(c)
    X_train, y_train = zip(*c)

    c = list(zip(X_test, y_test))
    random.shuffle(c)
    X_test, y_test = zip(*c)

    return (X_train, X_test, y_train, y_test)


def pad_data(X_train, X_test, pad_length):
    for a in X_train:
        a.extend([0] * (pad_length - len(a)))
    for a in X_test:
        a.extend([0] * (pad_length - len(a)))
    return (X_train, X_test)


def load_chords(dataset_type, composer_names, train_count=None):
    if dataset_type == "chords":
        dataType = ["chords"]

    elif dataset_type == "chords_t":
        dataType = ["chords_t"]

    elif dataset_type == "durations":
        dataType = ["durations"]

    else:
        raise ValueError("Invalid data type")

    df = pd.read_csv("chords.csv")
    maxlen = 0
    X_train, X_test, y_train, y_test = [], [], [], []
    for i, comp in enumerate(composer_names):
        comp_train = df.loc[(df["composer"] == comp) & (
            df["data_type"] == "train"), dataType].values

        comp_train = [[feature[0] for feature in ast.literal_eval(
            piece[0])] for piece in comp_train]

        if(train_count is not None):
            comp_train = comp_train[:train_count]

        maxlen2 = max((len(a) for a in comp_train))
        if(maxlen2 > maxlen):
            maxlen = maxlen2

        comp_test = df.loc[(df["composer"] == comp) & (
            df["data_type"] == "test"), dataType].values

        comp_test = [[feature[0]
                      for feature in ast.literal_eval(a[0])] for a in comp_test]

        maxlen2 = max((len(a) for a in comp_test))
        if(maxlen2 > maxlen):
            maxlen = maxlen2

        X_train.extend(comp_train)
        X_test.extend(comp_test)
        y_train.extend([i]*len(comp_train))
        y_test.extend([i]*len(comp_test))

    X_train, X_test = pad_data(X_train, X_test, maxlen)
    return shuffle_data(X_train, X_test, y_train, y_test)


def load(dataset_type, composer_names, train_count=None):
    """load specified dataset from data folder

    params:
    dataset_type: string - string representation of dataset type
                            (ie. "pitches")
    composer_names : list[string] - names of composers

    returns touple (x_train,  x_test,y_train, y_test)"""

    if dataset_type == "t":
        dataType = ["t0", "t1", "t2", "t3", "t4", "t5"]

    elif dataset_type == "st":
        dataType = ["st0", "st1", "st2", "st3", "st4", "st5",
                    "st6", "st7", "st8", "st9", "st10", "st11"]

    else:
        raise ValueError("Invalid data type")

    df = pd.read_csv("data.csv")

    X_train, X_test, y_train, y_test = [], [], [], []
    for i, comp in enumerate(composer_names):
        comp_train = df.loc[(df["composer"] == comp) & (
            df["data_type"] == "train"), dataType].values

        if(train_count is not None):
            comp_train = comp_train[:train_count]

        comp_test = df.loc[(df["composer"] == comp) & (
            df["data_type"] == "test"), dataType].values

        X_train.extend(comp_train)
        X_test.extend(comp_test)
        y_train.extend([i]*len(comp_train))
        y_test.extend([i]*len(comp_test))

    return shuffle_data(X_train, X_test, y_train, y_test)


def main():
    print(load_chords("chords_t", ["debussy"])[0][0])
    # load("t", ["debussy", "haydn"])


if __name__ == '__main__':
    main()
