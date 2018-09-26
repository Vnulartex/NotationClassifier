import pickle
import os

def Load(rep, composerNames):
    composers = []
    os.chdir("data")
    for dir in os.listdir():
        os.chdir(dir)
        with open (rep, "rb") as fp:
            data = pickle.load(fp)
        name = composerNames.index(dir)
        composers.append((name,data))
        os.chdir("..")
    return composers

print(Load("pitches",["bach","trecento"]))