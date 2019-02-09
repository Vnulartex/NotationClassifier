import os
import pickle
import modules.data_loader as loader
import modules.clfobj
import numpy as np
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer


def classify(data, clfobj):
    data = clfobj.des_func(data)
    data = clfobj.vectorizer.transform(data)
    y = clfobj.clf.predict(data)
    return y


if __name__ == "__main__":
    clf_folder = "classifiers"
    input_folder = "input"
    files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(
        ".mxl") or f.endswith(".mid")][:1]
    clfpath = [os.path.join(clf_folder, f) for f in os.listdir(clf_folder) if f.endswith(
        ".dat")][0]
    with open(clfpath, "rb") as f:
        clfobj = pickle.load(f)
    data = []
    for path in tqdm(files, desc="Parsing files"):
        score = loader.load_file(path, clfobj.ser_func)
        data.append(score)
    print(clfobj.clf)
    y = classify(data, clfobj)
    for f, x in zip(files, y):
        print(f, "classified as:", clfobj.composers[x])
