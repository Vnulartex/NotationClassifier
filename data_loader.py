import os
import pickle
import random
import numpy as np


def Load(dataset_type, composer_names, train_ratio=0.8, all=True, num_data=50):
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
        if (all):
            composers.append((y, data))
        else:
            composers.append((y, data[:num_data]))
        os.chdir("..")

    os.chdir("..")
    split = int(len(composers[0][1]) * train_ratio)
    training_data = []
    test_data = []
    for composer in composers:
        y = composer[0]
        training_data.extend([[x, y] for x in composer[1][:split]])
        test_data.extend([[x, y] for x in composer[1][split:]])
    random.shuffle(training_data)
    random.shuffle(test_data)

    x_train = [a[0] for a in training_data]
    y_train = [a[1] for a in training_data]
    x_test = [a[0] for a in test_data]
    y_test = [a[1] for a in test_data]

    return (np.array(x_train), np.array(y_train), np.array(x_test),
            np.array(y_test))
