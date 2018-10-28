import os


def move_test(n: int):
    if not os.path.isdir("test"):
        os.mkdir("test")
    for i, file in enumerate([f for f in os.listdir() if os.path.isfile(f)]):
        if i % n == 0:
            os.rename(file, "test/" + file)


def move_train():
    if not os.path.isdir("train"):
        os.mkdir("train")
    for i, file in enumerate([f for f in os.listdir() if os.path.isfile(f)]):
        os.rename(file, "train/" + file)


def move_to_root():
    root = os.getcwd()
    for p, d, f in os.walk(root, topdown=False):
        if "!" in p:
            continue
        for n in f:
            os.rename(os.path.join(p, n), os.path.join(root, n))
        for n in d:
            try:
                os.rmdir(os.path.join(p, n))
            except:
                pass


def main():
    os.chdir("../Data/mozart/")
    move_to_root()
    move_test(4)
    move_train()


if __name__ == '__main__':
    main()