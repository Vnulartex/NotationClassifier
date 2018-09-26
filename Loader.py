import pickle
import os

def Load(rep, composerNames):
    composers = []
    os.chdir("data")
    for dir in composerNames:
        os.chdir(dir)
        with open (rep, "rb") as fp:
            data = pickle.load(fp)
        name = composerNames.index(dir)
        composers.append((name,data))
        os.chdir("..")
    os.chdir("..")
    return composers
