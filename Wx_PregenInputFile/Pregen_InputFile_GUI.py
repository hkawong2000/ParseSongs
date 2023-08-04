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
sys.path.append('./Pregen_InputFile')
from Pregen_InputFile import *

# ======

FilePath = ''           # Field on form
InFile   = ''           # full path of input file

# Expert mode parameters
AllowExpert   = 0       # expert mode allowed
SelectFrameOn = 0       # whether select frame is on

# Return values for select
selectJP = ''           # the selected Jyutping
newEntry = list()       # the reordered entry list

# Version string
VERSION_STRING = "Version 20230707"

# ==============================================================

# Ref:
# Tkinter file dialogs : https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog

def UserChoiceG ( curLine, oneChar, wordNum, entryList ) :
    """ Let user choose Jyutping from list of characters, to be run in non-GUI mode
    
    Inputs:
        curLine   : current text line
        oneChar   : the Chinese character
        wordNum   : word number within line (for message)
        entryList : list containing the possible pronunciations
    Output:
        (none)
    """
    # not yet supported
    input('Graphical support for user choice in expert mode not yet supported.  Press ENTER to continue ')
    return('', [])
# end def UserChoiceG()


def SelectJyutPing() :
    """ Allow user to select Jyutping

    Inputs:
        (tbd)
    Outputs:
        (tbd)
    """
    print('SelectJyutPing() called')
# end if


def SelectFile():
    """ callback when the Start button is clicked

    Inputs:
        (none)
    Outputs:
        (none)
    """
    global      FilePath
    global      InFile
    
    filetypes1 = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    FilePath = fd.askopenfilename(filetypes=filetypes1)
    print('FilePath = ' + FilePath)    
    #
    if (FilePath != '') :
        fileNameLastIdx = FilePath.rindex('/')
        fileNameLast    = FilePath[(fileNameLastIdx+1):]
        FileNameLabel['text']        = fileNameLast
        FileNameLabel['borderwidth'] = 3
        InFile = fileNameLast
        print('InFile   = ' + InFile)
    # end if
# end def SelectFile()


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
    global      InFile
    global      SelectFrameOn

##    if (1) :
##        print('Testing')
##        if (SelectFrameOn) :
##            SelectFrame.pack_forget()
##            SelectFrameOn = 0
##        else :
##            SelectFrame.pack()
##            SelectFrameOn = 1
##        # end if
##        return
##    # end if

    # expertVal
    if (AllowExpert == 1) :
        expertVal = ExpertMode.get()
        #x showinfo(title = 'Info', message=('expertVal = ' + str(expertVal)))
    else :
        expertVal = 0
    # end if

    # filePath
    if (FilePath == '') :
        showinfo(title = 'Info', message='請選擇文字檔案')
        return
    # end if

    guiParam = [selectJP, newEntry, UserChoiceG]
    (code, errStr) = ProcessFile(InFile, expertVal, graphicsMode=1, guiParam=guiParam)

    if (code == 0) :
        # showinfo(title = 'Info', message='Success')
        outFile     = re.sub('.txt', '_input.txt', InFile)
        noteFile    = re.sub('.txt', '_Notes.txt', InFile)
        successText = '成功 !\n結果在 : ' + outFile + '\n附注在 : ' + noteFile
        # StatusText['text'] = '成功'
        StatusText['text']    = successText
        FileNameLabel['text'] = ''
    else :
        # showinfo(title = 'Info', message=errStr)
        StatusText['text'] = errStr
    # end if
# end def StartClicked()

# ==============================================================
        
# Root
root = tk.Tk()
root.title('粵拼查找程式')
root.resizable(False, False)
root.configure(background='#E0FFFF')
if (AllowExpert == 1) :
    root.geometry('300x300')
else :
    root.geometry('300x200')
# end if

# Styles
style = ttk.Style(root)

# Define InfoFrame for user information
InfoFrame = ttk.Frame(root, style='InfoFrame.TFrame')
style.configure('InfoFrame.TFrame', background='#E0FFFF')
InfoFrame.pack(padx=10, pady=10, fill='x', expand=True)

# Configure grid layout for InfoFrame 
InfoFrame.columnconfigure(0, weight=1)
InfoFrame.columnconfigure(1, weight=2)

# Open name dialogue
FileButton = ttk.Button(InfoFrame, text='選擇檔案', command=SelectFile)
FileButton.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
FileNameLabel = ttk.Label(InfoFrame, text="")
FileNameLabel.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

if (AllowExpert == 1) :
    # Expert mode
    ExpertMode = tk.IntVar()
    ExpertLabel = ttk.Label(InfoFrame, text="Expert mode")
    ExpertLabel.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
    ExpertEntry = tk.Checkbutton(InfoFrame, variable=ExpertMode, onvalue=1, offvalue=0)
    ExpertEntry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
# end if

# Start button
StartButton = ttk.Button(InfoFrame, text="開始", command=StartClicked)
StartButton.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

# Separator-1
Separator1 = ttk.Separator(InfoFrame, orient='horizontal')
Separator1.grid(row=3, column=0, columnspan=2, pady=5, sticky='EW')

# Status
StatusLabel = ttk.Label(InfoFrame, text="狀態")
StatusLabel.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
StatusText = ttk.Label(InfoFrame, text="(未知)", foreground="blue")
StatusText.grid(row=5, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)

if (AllowExpert == 1) :
    SelectFrame = ttk.Frame(root, style='SelectFrame.TFrame')
    #x style.configure('SelectFrame.TFrame', background='#E0FFFF')
    style.configure('SelectFrame.TFrame', background='#FFFFCC')
    SelectFrame.pack(padx=0, pady=0, fill='x', expand=True)

    # Separator-2
    Separator2 = ttk.Separator(SelectFrame, orient='horizontal')
    Separator2.grid(row=6, column=0, columnspan=2, pady=5, sticky='EW')

    # Line text for reference
    LineTextLabel = ttk.Label(SelectFrame, text="-")
    LineTextLabel.grid(row=7, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
    # LineTextLabel.configure(state='disable')
    LineTextLabel.lower()

    # Selection box
    SelectJp     = tk.StringVar()
    SelectJpVals = ('1', '2', '3', '4', '5', '6')
    SelectBox  = ttk.Combobox(SelectFrame, height=5, textvariable = SelectJp)
    SelectBox['values'] = SelectJpVals
    SelectBox.grid(row=8, column=0, sticky=tk.EW, padx=5, pady=5)
    # SelectBox.configure(state='disable')
    SelectBox.lower()

    SubmitButton = ttk.Button(SelectFrame, text='提交', command=SelectJyutPing)
    SubmitButton.grid(row=8, column=1, sticky=tk.E, padx=5, pady=5)
    # SubmitButton.configure(state='disable')
    SubmitButton.lower()

    # Make it invisible at the beginning
    SelectFrame.pack_forget()
# end if

# Menu bar
MenuBar = Menu(root)
root.config(menu=MenuBar)
#
ConfigMenu = Menu(MenuBar, tearoff=False)
ConfigMenu.add_command(label="版本", command=ShowVersion)
#
MenuBar.add_cascade(label="設定", menu=ConfigMenu)

# keep the window displaying
root.mainloop()

