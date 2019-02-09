class Clfobj:
    def __init__(self, clf, composers, vectorizer, ser_func, des_func):
        self.clf = clf
        self.composers = composers
        self.vectorizer = vectorizer
        self.ser_func = ser_func
        self.des_func = des_func
