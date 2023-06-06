#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Utility functions and common global variables
# ==============================================================

import os
import re
import sys

import tkinter as tk
from tkinter import *
from tkinter.messagebox import *

# ==============================================================

# Return codes for Calc_YiuResult()
PREV_REST_VAL           = 0x0100
SAME_TARGET_DIFF_NOTE   = 0x0001
DIFF_TARGET_SAME_NOTE   = 0x0002
IN_YIU_RANGE            = 0x0004
OUT_YIU_RANGE           = 0x0008  

# Pointer to log file
fLog = None

# Global variables related to song
# global PrevWord, PrevTone, PrevMelody, PrevRest
PrevWord   = ''
PrevTone   = 0          # tone of previous non-rest word (0-6)
PrevMelody = ''         # melody of the previous non-rest word (str); '' if it is the 1st word of the song
PrevRest   = False      # previous item is a rest

# Information from GUI/Calling program
Song_NoteFormat  = ''
Song_BeatsPerBar = 0

# Parsed information of song
SongInfo_List = list()

# Remarks for (partial-)mismatches
RemarkCount = 0
RemarkList  = list()

# List of errors
ErrList = list()

# ==============================================================

def OpenLog ( logFile ) :
    """ Write 'logStr' to the logfile

    Inputs:
        logFile : path to the log file
    Output:
        (none)
    """
    global      fLog

    fLog = open(logFile, 'w', encoding='utf-8')
# end def OpenLog()

def WriteLog ( logStr ) :
    """ Write 'logStr' to the logfile

    Inputs:
        logStr : string to write to the log file
    Output:
        (none)
    """
    global      fLog

    fLog.write(logStr + '\n')
    fLog.flush()
# end def WriteLog()

def WriteLog1 ( logStr ) :
    """ Write 'logStr' to the logfile and print to console

    Inputs:
        logStr : string to write to the log file
    Output:
        (none)
    """
    global      fLog

    print(logStr + '\n')
    fLog.write(logStr + '\n')
    fLog.flush()
# end def WriteLog1()
#
def WriteLog2 ( logStr ) :
    """ Write 'logStr' to the logfile and print to console and prompt user to press ENTER

    Inputs:
        logStr : string to write to the log file
    Output:
        (none)
    """
    global      fLog

    input(logStr + '\n  Press ENTER to continue ')
    fLog.write(logStr + '\n')
    fLog.flush()
# end def WriteLog2()

def CloseLog () :
    fLog.flush()
    fLog.close()
# end def CloseLog()

