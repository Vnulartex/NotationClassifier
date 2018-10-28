from joblib import Parallel, delayed
import pandas as pd
import numpy as np


def increment(i):
    print(i)
    pd.DataFrame(np.array([[i, i**2]])).to_csv(
        "test.csv", header=False, index=False, mode="a")


pd.DataFrame(columns=['i', 'i^2']).to_csv("test.csv", index=False)
Parallel(n_jobs=-1)(delayed(increment)(i) for i in range(10))