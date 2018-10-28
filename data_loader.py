import os
import pickle
import random
import numpy as np
from sklearn.model_selection import train_test_split


def load(dataset_type, composer_names):
    """load specified dataset from data folder

    params:
    dataset_type: string - string representation of dataset type
                            (ie. "pitches")
    composer_names : list[string] - names of composers

    returns touple (x_train,  x_test,y_train, y_test)"""
    composers = []
    os.chdir("data")
    for dir in composer_names:
        os.chdir(dir)
        with open(dataset_type + ".dat", "rb") as fp:
            data = pickle.load(fp)
        y = composer_names.index(dir)
        composers.append((y, data))
        os.chdir("..")
    os.chdir("..")
    data = []
    for composer in composers:
        y = composer[0]
        data.extend([[x, y] for x in composer[1]])
    x = [a[0] for a in data]
    y = [a[1] for a in data]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
    return (X_train, X_test, y_train, y_test)


def load_test():
    with open("test.dat", "rb") as fp:
        data = pickle.load(fp)
    return data
