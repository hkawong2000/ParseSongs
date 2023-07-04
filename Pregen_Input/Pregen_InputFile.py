#!/usr/bin/python
# -*- coding: UTF-8 -*-

### =============================================================
### Process files for Facebook page download of all articles
### =============================================================

import os
import re
import sys
import time
import string
import threading
# import shutil
#
sys.path.append('C:/Python_Lib/WriteLog')
from WriteLog import *
#
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import *

# input dictionary
WordListDict = dict()

# List for logging messages
PrevMsgLine = -1
MsgList     = list()
MsgWordList = list()

# Expert mode
# - users to decide when multiple pronunciations for the same character exist,
#   and the dictionary does not decide on the order
#   Also a new dictionary containing the users choices will be generated at the end
ExpertMode = 0

# Dictionary for previous choices for words with multiple pronunciations
# - key   = chinese character
# - value = choice made
PrevChoiceDict = dict()

# Graphics (GUI) mode and GUI select function  
GraphicsMode = 0
RootWin      = None

# New dictionary entries
NewDictEntryList = list()

# Popup window
popupResult = [ '', [] ]
popupEvent  = threading.Event()

# ------------------------------------------------------------
# Functions 
# ------------------------------------------------------------ 

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
    return
# end def UserChoiceG()


def UserChoiceT ( curLine, oneChar, wordNum, entryList ) :
    """ Let user choose Jyutping from list of characters, to be run in non-GUI mode
    
    Inputs:
        curLine   : current text line
        oneChar   : the Chinese character
        wordNum   : word number within line (for message)
        entryList : list containing the possible pronunciations
    Output:
        jyutping : the jyutping of the character selected/given by the user
    """
    global      PrevChoiceDict
    global      NewDictEntryList

    lineOut  = '\n* 在這行中的 "' + oneChar + '" 字 : '
    lineOut += curLine[:(wordNum-1)] + ' [' + oneChar + '] ' + curLine[wordNum:].strip()
    print(lineOut)
    #
    choiceIdx  = 0
    choiceLine = '  請以數字選粵拼(如選項中無合適的粵拼,請自行輸入) '
    for oneEntry in entryList :
        if (choiceIdx > 0) :
            choiceLine += ' / '
        # end if
        choiceLine += str(choiceIdx) + ':' + oneEntry
        choiceIdx  += 1
    # end for
    choiceLine += ' > '
    #
    userRsp = input(choiceLine)
    if userRsp.isnumeric() :
        # user hopefully selected one of the choices
        rspIdx = int(userRsp)
        if (rspIdx < len(entryList)) :
            jyutping = entryList[rspIdx]
            entryList.pop(rspIdx)
            entryList.insert(0, jyutping)
            entryList.insert(0, '*')
        else :
            input('Invalid choice !!!! ')
            jyutping = '?'
        # end if
    else :
        # assume user enter jyutping
        jyutping = userRsp
        entryList.insert(0, jyutping)
        entryList.insert(0, '*')
    # end if
    #x print('  selected jyutping : ' + jyutping)
    if (jyutping != '?') :
        PrevChoiceDict[oneChar] = jyutping
    # end if
    #
    return(jyutping, entryList)
# end def UserChoiceT()


def LookupJyutping ( curLine, oneChar, lineNum, wordNum ) :
    """ Lookup Jyutping of one single character
    
    Inputs:
        curLine : current text line
        oneChar : the Chinese character
        lineNum : line number in file (for message)
        wordNum : word number within line (for message)
    Output:
        jyutping of the character (maybe be suffixed with different symbols to represent different meanings)
        (or '?' if not found)
    """
    global      PrevMsgLine
    global      MsgList
    global      MsgWordList
    #
    global      PrevChoiceDict
    global      ExpertMode
    global      GraphicsMode
    global      MsgList
    global      NewDictEntryList

    # mostLikely    (M)
    # equallyLikely (E)
    # random        (R)
    # userChoice    (U)
    # previous      (P)

    #x print('    oneChar = ' + oneChar)
    try :
        entry = WordListDict[oneChar]
    except :
        # char not found in WordListDict
        msg0 = msgHdr + '找不到該字的粵拼'
        MsgList.append(msg0)
        return('?')
    else :
        if (len(entry) == 1) :
            # only one jyutping
            jyutping = entry[0]
            return(jyutping)
        else:
            # deal with multiple pronunciations
            if (lineNum == PrevMsgLine) :
                msgHdr = '第' + str(lineNum) + '行 第' + str(wordNum) + '個字 "' + oneChar + '" - '
            else :
                msgHdr = '第' + str(lineNum) + '行 <' + curLine + '> 第' + str(wordNum) + '個字 "' + oneChar + '" - '
            # end if
            #
            if (oneChar in MsgWordList) :
                # remember choice from before
                retVal  = PrevChoiceDict[oneChar]
                msgFull = 'P: ' + msgHdr + '(前面已提過)'
                MsgList.append(msgFull)
                return(retVal)
            else :
                if (entry[0] == '*') :
                    # more than one jyutping, but the first choice is most likely
                    msgFull = 'M: ' + msgHdr + '最可能是 "' + entry[1] + '" , 但仍有其他可能 : ' + str(entry[2:])
                    retVal  = entry[1] + '*'
                elif (entry[0] == '@') :
                    # more than one jyutping, but there are choices that are equally likely;
                    # in this case, the first choice is provided to the user
                    msgFull = 'E: ' + msgHdr + '有可能是 "' + entry[1] + '" , 但亦有其他可能 : ' + str(entry[2:])
                    retVal  = entry[1] + '@'
                else :
                    # more than one jyutping, let user choose which one to use
                    if (ExpertMode == 0) :
                        msgFull = 'R: ' + msgHdr + '隨機選擇了 "' + entry[0] + '" , 其他可能包括 : ' + str(entry[1:])
                        retVal  = entry[1] + '?'
                    else :
                        # Expert mode
                        if (GraphicsMode == 0) :
                            (retVal, newEntry) = UserChoiceT(curLine, oneChar, wordNum, entry)
                        else :
                            # (not yet supported)
                            # UserChoiceG(curLine, oneChar, wordNum, entry)
                            pass
                        # end if
                        msgFull = 'U: ' + msgHdr + '用戶選擇了 "' + retVal + '" , 其他可能包括 : ' + str(newEntry[2:])
                        newDictLine = '    "' + oneChar + '" : ' + str(newEntry)
                        #x print('  new dict line = ' + newDictLine)
                        NewDictEntryList.append(newDictLine)
                    # end if (ExpertMode)
                # end if (entry[0])
                MsgWordList.append(oneChar)
                MsgList.append(msgFull)
                PrevChoiceDict[oneChar] = retVal
                return(retVal)
            # end if
        # end if
    # end try
# end def LookupJyutping()


def WriteMessages ( outFile ) :
    """ Write output messages
    
    Inputs:
        Write messages to console (if any)
    Output:
        (status, message))
            status  : 0 for success, >0 for failure
            message : (used for failure) a brief error message describing the cause of the failure
    """
    global      ExpertMode
    global      GraphicsMode
    global      MsgList
    global      NewDictEntryList

    MsgList_U = list()          # userChoice    (U)
    MsgList_M = list()          # mostLikely    (M)
    MsgList_E = list()          # equallyLikely (E)
    MsgList_R = list()          # random        (R)
    MsgList_P = list()          # previous      (P)
    TitleDict = {
        'U' : '用戶選擇',
        'M' : '最可能選擇 (粵拼後有*號)',
        'E' : '有同樣可能的其他選擇 (粵拼後有@號)',
        'R' : '系統隨機選擇 (粵拼後有@號)',
        'P' : '(之前出現過的字)',
    }

    if (GraphicsMode == 1) :
        # open and write to file and alert user
        pass
    # end if
    
    # Sort messages
    if (len(MsgList) > 0) :
        for oneMsg in MsgList :
            msgType = oneMsg[0]
            if (msgType in "UMERP") :
                targetList = eval('MsgList_' + msgType)
                targetList.append(oneMsg)
            else :
                input('Error with message type : ' + oneMsg)
                continue
            # end if 
        # end for
    # end if

    # Open output file
    fo = open(outFile, 'w', encoding='utf-8')
    
    print('\n========================================\n')
    outStr = 'Please note the following messages:'
    print(outStr)
    fo.write(outStr + '\n')
    for listType in 'UMERP' :
        curList = eval('MsgList_' + listType)
        if (len(curList) > 0) :
            groupStr = '\n' + TitleDict[listType] + ' : '
            print(groupStr)
            fo.write(groupStr + '\n')
            #
            for oneItem in curList :
                print(oneItem)
                fo.write(oneItem + '\n')
            # end for
            fo.flush()
        # end if
    # end for

    if ((ExpertMode == 1) and ((len(NewDictEntryList)) > 0)) :
        outStr = '\nNew dictionary entries to be merged:\n'
        print(outStr)
        fo.write(outStr + '\n')
        for oneEntry in NewDictEntryList :
            print(oneEntry)
            fo.write(oneEntry + '\n')
        # end for
    # end if

    fo.flush()
    fo.close()
# end def WriteMessages()


def ProcessFile ( inFile, expertMode=0, graphicsMode=0, rootWin=None ) :
    """ Process input song file
    
    Inputs:
        inFile         : path to input file
        expertMode     : 1 if expert mode is used, default 0
        graphicsMode   : 1 if graphics mode is used, default 0
        selectFunction : function to let the user to select if graphics mode is used
    Output:
        (status, message))
            status  : 0 for success, >0 for failure
            message : (used for failure) a brief error message describing the cause of the failure
    """
    global      ExpertMode
    global      GraphicsMode
    global      GUI_SelectFunction

    print('ProcessFile() called for infile ' + inFile)
    outFile = re.sub('.txt', '_input.txt', inFile)
    logFile = re.sub('.txt', '.log', inFile)
    OpenLog(logFile)
    
    # Read input list and dict
    print('Load dictionary')
    inDict = 'CantoneseDict.txt'
    exec(open(inDict, encoding='utf-8').read())
    WriteLog1('Initially, WordListDict has ' + str(len(WordListDict)) + ' items')

    ExpertMode   = expertMode
    GraphicsMode = graphicsMode
    if (GraphicsMode == 1) :
        # print('selectFunction = ' + str(selectFunction))
        # GUI_SelectFunction = selectFunction
        RootWin = rootWin
    # end if

    lineWordCnt  = 0    # word count within one line
    totalWordCnt = 0    # total number of words in file
    barCnt       = 0    # total number of bars
    lineNum      = 0    # line number
    nonChiStr    = ''   # string for non-Chinese characters 

    fi = open(inFile,       encoding='utf-8')
    fo = open(outFile, 'w', encoding='utf-8')

    for curLine in fi.readlines() :
        lineNum     += 1
        lineWordCnt  = 0
        #
        if ((curLine[0] == '#') or (curLine.strip() == '')) :
            # comment line, skip
            fo.write(curLine)
            continue
        # end if
        WriteLog1('\nLine ' + str(lineNum+1000)[1:] + ' : ' + curLine.strip())
        #
        grpList = (curLine.strip()).split()
        WriteLog('\nLine ' + str(lineNum+1000)[1:] + ' : wordList = ' + str(grpList))
        grpCnt = 0
        grpNum = len(grpList)
        for oneGrp in grpList :
            grpCnt += 1
            WriteLog('  oneGrp = ' + oneGrp)
            charList = list(oneGrp)
            for oneChar in charList :
                if ((ord(oneChar) < 0x4E00) or (ord(oneChar) >= 0xA000)) :
                    # assume non-Chinese character
                    if (oneChar in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") :
                        nonChiStr += oneChar
                    # end if
                    continue
                elif (nonChiStr != '') :
                    fo.write(nonChiStr)
                    nonChiStr = ''
                # end if
                #
                lineWordCnt  += 1
                totalWordCnt += 1
                jyutping = LookupJyutping(curLine.strip(), oneChar, lineNum, lineWordCnt)
                outStrC  = oneChar + '  ' + jyutping + (' ' * (12-len(jyutping)) + '.' + '\n')
                fo.write(outStrC)
            # end for oneChar
            if (nonChiStr != '') :
                fo.write(nonChiStr)
                nonChiStr = ''
            # end if
            #
            # Rest note
            if (grpCnt != grpNum) :
                # assume rest
                outStrR = '-   -           -       .\n'
                fo.write(outStrR)
            # end if
        # end for oneGrp
        #
        if (nonChiStr != '') :
            fo.write(nonChiStr)
            nonChiStr = ''
        # end if
        #
        # bar
        outStrB  = 'bar\n\n'
        barCnt  += 1
        fo.write(outStrB)
        fo.flush()
    # end for curLine

    fi.close()

    fo.write('# end of song\n\n')
    fo.flush()
    fo.close()

    FlushLog()
    CloseLog()
    
    return(0, '')
# end def ProcessFile()

# ==============================================================================
    
# main()
if __name__ == "__main__":

    # Input file
    inFile = input('Input lyrics file: ')
    if (os.path.exists(inFile)) :
        outFile = re.sub('.txt', '_Notes.txt', inFile)
    else :
        outStr = 'File "' + inFile + '" cannot be found, program exits'
        print(outStr)
        sys.exit(0)
    # end if

    # Expert mode
    AllowExpertMode = 1
    if (AllowExpertMode) :
        rsp1 = input('Run program in expert mode? (Y or N) ')
        if (rsp1.upper() == 'Y') :
            expertMode = 1
        else :
            expertMode = 0
        # end if
    else :
        expertMode = 0
    # end if
    
    ProcessFile(inFile, expertMode, graphicsMode=0)
    WriteMessages(outFile)

    print("\nDone")
# end if __name__

