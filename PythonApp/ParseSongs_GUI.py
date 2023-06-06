#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
#
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import *
#
sys.path.append('./ParseSongs_Util')
from ParseSongs_Util import *
#
sys.path.append('./ParseSongs_ProcessReq')
from ParseSongs_ProcessReq import *

# ======

FilePath    = ''        # full path of file
BrowserPath = '''C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'''
BrowserPath = '''C:/Program Files/Google/Chrome/Application/chrome.exe'''
#
QUARTER_BEAT  = chr(0xBC)
ONETHIRD_BEAT = chr(0x2153) 
HALF_BEAT     = chr(0xBD)
#
VERSION_STRING = "Version 20230605"

# ==============================================================

# Ref:
# Tkinter file dialogs : https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog

def SelectFile():
    """ callback when the Start button is clicked

    Inputs:
        (none)
    Outputs:
        (none)
    """
    global      FilePath
    
    filetypes1 = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    FilePath = fd.askopenfilename(filetypes=filetypes1)
    # FilePath = fd.askopenfilename(title='Select file for song')
    #
    if (FilePath != '') :
        fileNameLastIdx = FilePath.rindex('/')
        fileNameLast    = FilePath[(fileNameLastIdx+1):]
        FileNameLabel['text']        = fileNameLast
        FileNameLabel['borderwidth'] = 1
    # end if
# end def SelectFile()


def SelectEditFile():
    """ Select file to edit

    Inputs:
        (none)
    Outputs:
        (none)
    """
    pass
# def SelectEditFile()


def SelectBrowserPath():
    """ callback when the Config->BrowserPath button is clicked

    Inputs:
        (none)
    Outputs:
        (none)
    """
    global      BrowserPath

    fileTypes2 = ( ('exe files', '*.exe'), ('All files', '*.*') )
    BrowserPath0 = fd.askopenfilename(title='Select path for browser', filetypes=fileTypes2)
    if (BrowserPath0 != '') :
        BrowserPath = BrowserPath0
    # end if
    showinfo(title = 'Information', message=('Browser path set to ' + BrowserPath))
# end def SelectBrowserPath()


def ShowVersion():
    """ callback when the Config->BrowserPath button is clicked

    Inputs:
        (none)
    Outputs:
        (none)
    """
    global      VERSION_STRING

    showinfo(title = 'Information', message=VERSION_STRING)
# end def ShowVersion()


def StartClicked():
    """ callback when the Start button is clicked

    Inputs:
        (none)
    Outputs:
        (none)
    """
    global      FilePath
    
    songNameVal    = SongName.get()
    beatsPerBarVal = BeatsPerBar.get()
    noteFormatVal  = NoteFormatEntry.get()

    if ((FilePath == '') or (songNameVal == '') or (noteFormatVal == '') or (beatsPerBarVal == '')) :
        showinfo(title = 'Info', message='Please fill in the top 3 fields and provide file name')
        return
    # end if

    if (noteFormatVal == '1,2,3') :
        noteFormat = 'N'
    elif (noteFormatVal == 'C,D,E') :
        noteFormat = 'A'
    else :
        showinfo(title = 'Info', message='noteFormat is not recognized')
        return
    # end if

    (code, errStr) = ProcessRequest(FilePath, songNameVal, int(beatsPerBarVal), noteFormat, BrowserPath)
    if (code == 0) :
        # showinfo(title = 'Info', message='Success')
        StatusText['text'] = 'Success'
    else :
        # showinfo(title = 'Info', message=errStr)
        StatusText['text'] = errStr
    # end if
# end def StartClicked()


# ==============================================================

# Root
root = tk.Tk()
root.title('Parse Songs')
root.geometry('300x300')
root.resizable(False, False)
root.configure(background='#b3ffb3')

# Styles
style = ttk.Style(root)

# Define InfoFrame for user information
InfoFrame = ttk.Frame(root, style='InfoFrame.TFrame')
style.configure('InfoFrame.TFrame', background='#b3ffb3')
InfoFrame.pack(padx=10, pady=10, fill='x', expand=True)

# Configure grid layout for InfoFrame 
InfoFrame.columnconfigure(0, weight=1)
InfoFrame.columnconfigure(1, weight=2)

if (1) :
    # DEBUG - use preset value
    SongName    = tk.StringVar(value='迷路找朋友')
    BeatsPerBar = tk.StringVar(value='4')
    NoteFormat  = tk.StringVar(value='1,2,3')
else :
    SongName    = tk.StringVar()
    BeatsPerBar = tk.StringVar()
    NoteFormat  = tk.StringVar()
# end if

# Song name
SongNameLabel = ttk.Label(InfoFrame, text="Name of Song")
SongNameLabel.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
SongNameEntry = ttk.Entry(InfoFrame, textvariable=SongName)
SongNameEntry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

# Units per bar
BeatsPerBarLabel = ttk.Label(InfoFrame, text="Beats per bar")
BeatsPerBarLabel.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
BeatsPerBarEntry = ttk.Entry(InfoFrame, textvariable=BeatsPerBar)
BeatsPerBarEntry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

# Note format
NoteFormatVals  = ('1,2,3', 'C,D,E')
NoteFormatLabel = ttk.Label(InfoFrame, text="Note format")
NoteFormatLabel.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
NoteFormatEntry = ttk.Combobox(InfoFrame, textvariable = NoteFormat)
NoteFormatEntry['values'] = NoteFormatVals
NoteFormatEntry['state']  = 'readonly'
NoteFormatEntry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)

# Open name dialogue
FileButton = ttk.Button(InfoFrame, text='Open input file', command=SelectFile)
FileButton.grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
FileNameLabel = ttk.Label(InfoFrame, text="")
FileNameLabel.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

# File name dialogue
EditFileButton = ttk.Button(InfoFrame, text='Edit input file', command=SelectEditFile)
EditFileButton.grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
EditFileNameLabel = ttk.Label(InfoFrame, text="")
EditFileNameLabel.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

# Start button
StartButton = ttk.Button(InfoFrame, text="Start", command=StartClicked)
StartButton.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

# Separator
Separator = ttk.Separator(InfoFrame, orient='horizontal')
Separator.grid(row=7, column=0, columnspan=2, pady=5, sticky='EW')

# Status
StatusLabel = ttk.Label(InfoFrame, text="Status")
StatusLabel.grid(row=8, column=0, sticky=tk.E, padx=5, pady=5)
StatusText = ttk.Label(InfoFrame, text="unknown", foreground="blue")
StatusText.grid(row=8, column=1, sticky=tk.EW, padx=5, pady=5)

# Menu bar
MenuBar = Menu(root)
root.config(menu=MenuBar)
#
ConfigMenu = Menu(MenuBar, tearoff=False)
ConfigMenu.add_command(label="BrowserPath", command=SelectBrowserPath)
ConfigMenu.add_command(label="Version", command=ShowVersion)
#
MenuBar.add_cascade(label="Config", menu=ConfigMenu)

# keep the window displaying
root.mainloop()
