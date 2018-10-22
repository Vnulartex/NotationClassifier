import os
import pickle
import random
import numpy as np


def Load(dataset_type, composer_names):
    """Load specified dataset from data folder

    params:
    dataset_type: string - string representation of dataset type
                            (ie. "pitches")
    composer_names : list[string] - names of composers
    train_ratio: double - percentage of data reserved for training data
    all: bool - if all exaples from each composer should be loaded
    num_data: int - number of examples to load from each directory,
    ignored if all = True

    returns touple (x_train, y_train, x_test, y_test)"""
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
    return (data)
