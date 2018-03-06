#!/usr/bin/env python3

import os
import sys
import shutil
import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

app_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(app_dir, 'config.json'), 'r') as f:
    config = json.load(f)

# change this if your path differs
if sys.platform == 'win32':
    default_path = 'C:\Program Files (x86)\Steam\steamapps\common\devildaggers\dd'
elif sys.platform == 'darwin':
    default_path = os.path.expanduser('~/Library/Application Support/Steam/steamapps/common/devildaggers/Devil Daggers.app/Contents/Resources/dd')

spawnset_dir = os.path.join(app_dir, "spawnsets")
spawnsets = os.listdir(spawnset_dir)
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
    shutil.copy(os.path.join(spawnset_dir, combobox.get()), os.path.join(default_path, 'survival'))


button = Button(root, text='switch!', command=switchset)
button.place(x=310, y=10)

root.mainloop()
