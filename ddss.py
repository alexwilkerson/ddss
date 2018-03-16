#!/usr/bin/env python3

import os
import sys
import shutil
import json
from urllib.request import urlretrieve
from urllib import request
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

app_dir = os.path.dirname(os.path.abspath(__file__))

update_label_text = ""

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

spawnsets_from_net = []
with request.urlopen("http://devildaggers.info/Content/spawnsets.json") as url:
    data = json.loads(url.read())
    for item in data:
        spawnsets_from_net.append(item["DownloadLink"].split('/')[-1])
    spawnsets_from_net.append('default')


def need_update():
    global spawnsets_from_net
    for s in spawnsets_from_net:
        if s not in spawnsets:
            print(s)
            return True
    return False


def update_spawnsets():
    with request.urlopen("http://devildaggers.info/Content/spawnsets.json") as url:
        data = json.loads(url.read())
        for item in data:
            if item["DownloadLink"].split('/')[-1] not in spawnsets:
                urlretrieve(item["DownloadLink"], os.path.join(spawnset_dir, item["DownloadLink"].split('/')[-1]))
        lbl_update.config(text='Updated!')
        combobox.config(values=spawnsets)
        combobox.set(spawnsets[0])


root = Tk()
root.title('Devil Daggers Spawnset Selector')
root.minsize(275, 140)
root.geometry('275x140')

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

btn_update = Button(root, text='update', command=update_spawnsets)
btn_update.grid(row=3, columnspan=2, padx=5)

if need_update():
    update_label_text = "An update is available."

lbl_update = Label(root, text=update_label_text)
lbl_update.grid(row=4, columnspan=2, padx=5)

root.mainloop()
