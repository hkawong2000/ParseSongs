#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Utility functions and common global variables
# ==============================================================

import os
import re
import sys

# import tkinter as tk
# from tkinter import *
# from tkinter.messagebox import *

# ==============================================================

# Return codes for Calc_YiuResult()
PREV_REST_VAL           = 0x0100
SAME_TARGET_DIFF_NOTE   = 0x0001
DIFF_TARGET_SAME_NOTE   = 0x0002
IN_YIU_RANGE            = 0x0004
OUT_YIU_RANGE           = 0x0008  

# Pointer to log file
fLog = None

# List of errors
ErrList = list()

# Directives
DirectiveDict = {
#   "DX" : "3",         # debug (flag 1 to print debug message to console, flag 2 to write to log file) 
    "DA" : "0",         # debug msg grp A 
    "DB" : "0",         # debug msg grp B 
    "DC" : "0",         # debug msg grp C 
    "DD" : "0",         # debug msg grp D 
    "E"  : "0",         # expert mode (error presented in detail)
    "L"  : "1",         # create log file
    "X"  : "0",         # ...
}

# ==============================================================

def ProcessDirective( dirStr, op ) :
    """ Set or get directive

    Inputs:
        dirStr : directive string (format : @A... : begins @, followed by 1 or more alphabet, optionally followed by any non-space string)
        op     : 1 for set, 0 for read
    Output:
        (retCode, string)
            retCode = 0 for success, -1 for failure
            string  = if success and op=0, string = directive value; if failure, string = failure cause
    """
    mDir = re.search('\@([A-Z]+)(.*)', dirStr)
    if mDir :
        dirLetter = mDir.group(1)
        dirArg    = mDir.group(2)
    else :
        # directive string wrong
        input('Wrong directive specification')
    if (op == 0) :
        # read
        try :
            val = DirectiveDict[dirLetter]
        except :
            # dirLetter does not exist in dictionary
            return(-1, "directive does not exist")
        else :
            return val
        # end try
    elif (op == 1) :
        # set
        DirectiveDict[dirLetter] = dirArg
    else :
        # invalid op
        pass
    # end if
# end def ProcessDirective()


def OpenLog ( logFile ) :
    """ Open log file for writing

    Inputs:
        logFile : path to the log file
    Output:
        (none)
    """
    global      fLog

    fLog = open(logFile, 'w', encoding='utf-8')
# end def OpenLog()
#
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
#
def WriteLog1 ( logStr ) :
    """ Write 'logStr' to the logfile and print to console

    Inputs:
        logStr : string to write to the log file
    Output:
        (none)
    """
    global      fLog

    print(logStr)
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
#
def CloseLog () :
    """ Flush and close the log file

    Inputs:
        (none)
    Output:
        (none)
    """
    fLog.flush()
    fLog.close()
# end def CloseLog()


def WriteDebug ( logStr, directive ) :
    """ Write/log debug message per setting of the given directive

    Inputs:
        logStr : string to write
        directive : debug directive
    Output:
        (none)
    """
    dirStr = '@' + directive
    dbgStr = dirStr + ' : ' + logStr
    retVal = int(ProcessDirective(dirStr, 0))
    if (retVal == 0) :
        return
    # end if
    if (retVal ^ 1) :
        print(dbgStr)
    # end if
    if (retVal ^ 2) :
        WriteLog(dbgStr)
    # end if
# end def WriteDebug()

