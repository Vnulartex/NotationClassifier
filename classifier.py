import os
import pickle
import modules.data_loader as loader
import numpy as np
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer


def main(files, clfpath):
    data = []
    with open(clfpath, "rb") as f:
        clfobj = pickle.load(f)
    clf = clfobj.clf
    composers = clfobj.composers
    vectorizer = clfobj.vectorizer
    ser_func = clfobj.ser_func
    des_func = clfobj.des_func
    for path in tqdm(files, desc="Parsing files"):
        score = loader.load_file(path, ser_func)
        data.append(score)
    data = des_func(data)
    data = vectorizer.transform(data)
    print(clf)
    y = clf.predict(data)
    for f, x in zip(files, y):
        print(f, "classified as:", composers[x])


if __name__ == "__main__":
    files = [f for f in os.listdir("input") if f.endswith(
        ".mxl") or f.endswith(".mid")]
    clf = [f for f in os.listdir("classifiers") if f.endswith(
        ".dat")][0]
    main(files, clf)
