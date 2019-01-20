import os
import pickle
import data_loader as loader
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def load_clf():
    clfs = [os.path.join("models/", clf)
            for clf in os.listdir("models/") if clf.endswith(".dat")]
    objs = []
    for path in clfs:
        with open(path, "rb") as f:
            objs.append(pickle.load(f))
        print("loaded classifier:", path)
    return objs


def vectorize(x, n):
    ngram_vectorizer = CountVectorizer(token_pattern="\d+", ngram_range=(1, n))
    return ngram_vectorizer.fit_transform(x)


def main():
    print("Loading classifiers...")
    clfs = load_clf()
    print("loading data...")
    data, filenames = loader.load_folder("input", "chords_t")
    data = loader.get_root(data)
    for clfobj in clfs:
        clf = clfobj.clf
        composers = clfobj.composers
        vectorizer = clfobj.vectorizer
        ser_func = clfobj.ser_func
        des_func = clfobj.des_func
        data = vectorizer.transform(data)
        print(clf)
        y = clf.predict(data)
        for file, x in zip(filenames, y):
            print(file, composers[x])

        # for x, file in zip(data, filenames):
        #     print(file, ":", clf.predict(np.reshape(x, (1, -1))))


if __name__ == "__main__":
    main()
