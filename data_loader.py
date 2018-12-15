import os
import random
import numpy as np
import pandas as pd
import ast
from collections import Counter


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


def load(features_type, composer_names, train_count=None):
    if features_type == "chords":
        features_type = ["chords"]

    elif features_type == "chords_t":
        features_type = ["chords_t"]

    elif features_type == "durations":
        features_type = ["durations"]

    else:
        raise ValueError("Invalid data type")

    df = pd.read_csv("chords.csv")
    X_train, X_test, y_train, y_test = [], [], [], []
    for i, comp in enumerate(composer_names):
        for d_type in ("train", "test"):
            data = df.loc[(df["composer"] == comp) & (
                df["data_type"] == d_type), features_type].values

            data = [[feature[0] for feature in ast.literal_eval(
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
    load("chords_t", ["debussy", "mozart",
                      "beethoven", "tchaikovsky", "victoria"])
    # load("t", ["debussy", "haydn"])


if __name__ == '__main__':
    main()
