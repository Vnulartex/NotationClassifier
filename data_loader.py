import os
import pickle
import random
import numpy as np
import pandas as pd


def get_data_counts(composers):
    df = pd.read_csv("data.csv")
    counts = []
    for composer in composers:
        comp = df.loc[(df["composer"] == composer)]
        train_count = len(comp.loc[(comp["data_type"] == "train")])
        counts.append(train_count)
    return (counts)


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

    elif dataset_type == "chords":
        dataType = ["chords"]

    elif dataset_type == "chords_t":
        dataType = ["chords_t"]

    elif dataset_type == "durations":
        dataType = ["durations"]

    df = pd.read_csv("chords.csv")

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

    c = list(zip(X_train, y_train))
    random.shuffle(c)
    X_train, y_train = zip(*c)

    c = list(zip(X_test, y_test))
    random.shuffle(c)
    X_test, y_test = zip(*c)

    print(X_train, y_train)
    print(X_test, y_test)
    return (X_train, X_test, y_train, y_test)


def main():
    print(get_data_count(["mozart", "tchaikovsky", "haydn"]))
    # load("t", ["debussy", "haydn"])


if __name__ == '__main__':
    main()
