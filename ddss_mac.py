#!/usr/bin/env python3

import os
import shutil
from tkinter import *
from tkinter import ttk


default_path = os.path.expanduser('~/Library/Application Support/Steam/steamapps/common/devildaggers/Devil Daggers.app/Contents/Resources/dd')
current_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spawnsets")
spawnsets = os.listdir(current_path)
spawnsets = sorted(spawnsets)


root = Tk()
root.title('Devil Daggers Spawnset Selector')
root.minsize(400, 70)
root.geometry('400x70')

spawnset = StringVar()
combobox = ttk.Combobox(root, textvariable=spawnset, width=27)
combobox.set(spawnsets[0])
combobox.place(x=40, y=10)
combobox.config(state="readonly", values=spawnsets)


def switchset():
    os.remove(os.path.join(default_path, 'survival'))
    shutil.copy(os.path.join(current_path, combobox.get()), os.path.join(default_path, 'survival'))


button = Button(root, text='switch!', command=switchset)
button.place(x=310, y=10)

root.mainloop()
