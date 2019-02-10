import pickle
import queue
import threading
import os
from time import sleep
from tkinter import END, Button, E, Entry, IntVar, Label, Tk, W, filedialog, DISABLED, NORMAL
from tkinter.ttk import Progressbar, Separator

import classifier
import modules.data_loader as loader
from modules.clfobj import Clfobj


class Gui:
    def __init__(self, root):
        self.master = root
        root.title("Midi classificator")

        self.clf = None
        self.clf_label = Label(root, text="Classifier:",
                               font=("DejaVu Sans", -14, "bold"))
        self.clf_label.grid(columnspan=2, pady=(10, 0))

        self.clf_value_label = Label(root, text="Choose some classifier")
        self.clf_value_label.grid(columnspan=2, padx=20)

        self.clf_label = Label(root, text="Classes:",
                               font=("DejaVu Sans", -14, "bold"))
        self.clf_label.grid(columnspan=2, pady=(10, 0))

        self.clf_class_label = Label(root, text="Choose some classifier")
        self.clf_class_label.grid(columnspan=2)

        self.clf_button = Button(
            root, text="Select classifier", command=self.get_classifier)
        self.clf_button.grid(columnspan=2, pady=10)

        Separator(root, orient="horizontal").grid(columnspan=2, sticky=W+E)

        self.filepaths = None
        self.files_label = Label(
            root, text="Files:", font=("DejaVu Sans", -14, "bold"))
        self.files_label.grid(column=0, pady=(10, 0), padx=20)

        self.y_label = Label(
            root, text="Classifier output:", font=("DejaVu Sans", -14, "bold"))
        self.y_label.grid(column=1, row=6, pady=(10, 0), padx=20)

        self.files_values_label = Label(root)
        self.files_values_label.grid(padx=20)

        self.files_y_label = Label(root)
        self.files_y_label.grid(column=1, row=7, padx=20)

        self.files_button = Button(
            root, text="Select midi files", command=self.get_files)
        self.files_button.grid(columnspan=2, pady=10)

        self.progressbar = Progressbar(
            root, orient="horizontal", mode="indeterminate")

        Separator(root, orient="horizontal").grid(columnspan=2, sticky=W+E)

        self.classify_button = Button(
            root, text="Classify", command=self.classify, state=DISABLED, height=2, width=10)
        self.classify_button.grid(columnspan=2, pady=10)

    def get_files(self):
        self.filepaths = filedialog.askopenfilenames(
            initialdir="./", title="Select music files", filetypes=[("Music files", "*.mid *.mxl")])
        if len(self.filepaths) == 0:
            self.filepaths = None
            self.files_values_label["text"] = ""
            self.files_y_label["text"] = ""
            self.set_button_state()
            return
        filenames = [os.path.basename(f) for f in self.filepaths]
        self.files_values_label["text"] = str.join("\n", filenames)
        self.files_y_label["text"] = ""
        self.set_button_state()

    def get_classifier(self):
        clf_path = filedialog.askopenfilename(
            initialdir="./", title="Select classifier file", filetypes=[("Binary files", "*.dat")])
        if clf_path == "":
            self.clf = None
            self.clf_value_label["text"] = ""
            self.clf_class_label["text"] = ""
            self.set_button_state()
            return
        with open(clf_path, "rb") as f:
            self.clf = pickle.load(f)
        self.clf_value_label["text"] = self.clf.clf
        self.clf_class_label["text"] = str.join(", ", self.clf.composers)
        self.set_button_state()

    def set_button_state(self):
        if self.filepaths is not None and self.clf is not None:
            self.classify_button["state"] = NORMAL
        else:
            self.classify_button["state"] = DISABLED

    def classify(self):
        self.classify_button["state"] = DISABLED
        self.progressbar.grid(columnspan=2)
        self.progressbar.start()
        self.queue = queue.Queue()
        ThreadedTask(self.queue, self.clf, self.filepaths).start()
        self.master.after(100, self.process_queue)

    def process_queue(self):
        try:
            y = self.queue.get(0)
            result = [self.clf.composers[i] for i in y]
            self.files_y_label["text"] = str.join("\n", result)
            self.classify_button["state"] = NORMAL
            self.progressbar.stop()
            self.progressbar.grid_forget()
        except queue.Empty:
            self.master.after(100, self.process_queue)


class ThreadedTask(threading.Thread):
    def __init__(self, queue, clf, filenames):
        threading.Thread.__init__(self)
        self.queue = queue
        self.clf = clf
        self.filenames = filenames

    def run(self):
        data = []
        for path in self.filenames:
            score = loader.load_file(path, self.clf.ser_func)
            data.append(score)
        y = classifier.classify(data, self.clf)
        self.queue.put(y)


root = Tk()
gui = Gui(root)
root.mainloop()
