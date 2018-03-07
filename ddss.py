#!/usr/bin/env python3

import os
import sys
import shutil
import json
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

app_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(app_dir, 'config.json'), 'r') as f:
    config = json.load(f)

# change this if your path differs
if sys.platform == 'win32':
    default_path = 'C:\Program Files (x86)\Steam\steamapps\common\devildaggers\dd'
elif sys.platform == 'darwin':
    default_path = os.path.expanduser('~/Library/Application Support/Steam/steamapps/common/devildaggers/Devil Daggers.app/Contents/Resources/dd')

if not config['dd_location']:
    config['dd_location'] = default_path
    with open(os.path.join(app_dir, 'config.json'), 'w') as f:
         json.dump(config, f)

spawnset_dir = os.path.join(app_dir, "spawnsets")
spawnsets = os.listdir(spawnset_dir)
spawnsets = sorted(spawnsets)


root = Tk()
root.title('Devil Daggers Spawnset Selector')
root.minsize(275, 90)
root.geometry('275x90')

spawnset = StringVar()
combobox = ttk.Combobox(root, textvariable=spawnset, width=27)
combobox.set(spawnsets[0])
combobox.grid(columnspan=2, padx=5)
combobox.config(state="readonly", values=spawnsets)

def switchset():
    os.remove(os.path.join(default_path, 'survival'))
    shutil.copy(os.path.join(spawnset_dir, combobox.get()), os.path.join(default_path, 'survival'))
    messagebox.showinfo("Success!", "'" + combobox.get() + "' spawnset selected.")

def set_default():
    os.remove(os.path.join(default_path, 'survival'))
    shutil.copy(os.path.join(spawnset_dir, 'default'), os.path.join(default_path, 'survival'))
    messagebox.showinfo("Success!", "'default' spawnset selected.")

def set_dd_location():
    dirname = filedialog.askdirectory(parent=root, initialdir="/", title='Please select a directory')
    if dirname:
        config['dd_location'] = dirname
        with open(os.path.join(app_dir, 'config.json'), 'w') as f:
             json.dump(config, f)
        messagebox.showinfo("Success!", "dd location set to " + dirname)

btn_switch = Button(root, text='switch!', command=switchset)
btn_switch.grid(row=1, padx=5)

btn_default = Button(root, text='default', command=set_default)
btn_default.grid(row=1, column=1, padx=5)

btn_set_dd = Button(root, text='change dd location', command=set_dd_location)
btn_set_dd.grid(row=2, columnspan=2, padx=5)

root.iconbitmap('ddss.ico')
root.mainloop()
