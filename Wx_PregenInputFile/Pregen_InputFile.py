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
#
sys.path.append('.')
from CantoneseDict import *

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

# Function for user to select input in GUI mode
GUI_Parameters = list()
UserChoiceG    = None       # GUI function for user to choose jyutping 

# Popup window
popupResult = [ '', [] ]
popupEvent  = threading.Event()

# ------------------------------------------------------------
# Functions 
# ------------------------------------------------------------ 

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

    lineOut  = '\n* 在這行中的 「' + oneChar + '」 字 : '
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


def FormatQuotes ( inStr ) :
    """ Format quotes for English quotes to use Chinese quotes 「」
    
    Inputs:
        inStr : input string
    Output:
        outStr : output string
    """
    outStr1 = re.sub("'([a-z])", "「\\1", inStr)
    outStr2 = re.sub("([\d])'",  "\\1」", outStr1)
    outStr3 = re.sub('\[', '', outStr2)
    outStr4 = re.sub('\]', '', outStr3)
    outStr  = outStr4
    return(outStr)
# end def FormatQuotes()


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
    #
    global      GUI_Parameters
    global      UserChoiceG

    # not found     (X)
    # mostLikely    (M)
    # equallyLikely (E)
    # random        (R)
    # userChoice    (U)
    # previous      (P)

    #x print('    oneChar = ' + oneChar)
    if (lineNum == PrevMsgLine) :
        msgHdr = '第' + str(lineNum) + '行 第' + str(wordNum) + '個字 「' + oneChar + '」 - '
    else :
        msgHdr = '第' + str(lineNum) + '行 「' + curLine + '」 第' + str(wordNum) + '個字 「' + oneChar + '」 - '
    # end if
    #
    try :
        entry = WordListDict[oneChar]
    except :
        # char not found in WordListDict
        msg0 = 'X: ' + msgHdr + '找不到該字的粵拼'
        MsgList.append(msg0)
        if (ExpertMode == 0) :
            return('?')
        else :
            # Enter Jyutping manually
            lineOut  = '\n* 在這行中的 「' + oneChar + '」 字 : '
            lineOut += curLine[:(wordNum-1)] + ' [' + oneChar + '] ' + curLine[wordNum:].strip()
            print(lineOut)
            #
            jyutping = input('請輸入粵拼 : ')
            PrevChoiceDict[oneChar] = jyutping
            #
            newDictLine = '    "' + oneChar + '" : [\'' + jyutping + '\'],'
            #x print('  new dict line = ' + newDictLine)
            NewDictEntryList.append(newDictLine)
        # end if
    else :
        if (len(entry) == 1) :
            # only one jyutping
            jyutping = entry[0]
            return(jyutping)
        else:
            # deal with multiple pronunciations
            if (oneChar in MsgWordList) :
                # remember choice from before
                retVal  = PrevChoiceDict[oneChar]
                msgFull = 'P: ' + msgHdr + '(請參見前文)'
                MsgList.append(msgFull)
                return(retVal)
            else :
                if (entry[0] == '*') :
                    # more than one jyutping, but the first choice is most likely
                    msgFull = 'M: ' + msgHdr + '最可能是 「' + entry[1] + '」 , 但仍有其他可能 : ' + FormatQuotes(str(entry[2:]))
                    retVal  = entry[1] + '*'
                elif (entry[0] == '@') :
                    # more than one jyutping, but there are choices that are equally likely;
                    # in this case, the first choice is provided to the user
                    msgFull = 'E: ' + msgHdr + '有可能是 「' + entry[1] + '」 , 但亦有其他可能 : ' + FormatQuotes(str(entry[2:]))
                    retVal  = entry[1] + '@'
                else :
                    # more than one jyutping, let user choose which one to use
                    if (ExpertMode == 0) :
                        msgFull = 'R: ' + msgHdr + '隨機選擇了 「' + entry[0] + '」 , 其他可能包括 : ' + FormatQuotes(str(entry[1:]))
                        retVal  = entry[0] + '?'
                    else :
                        # Expert mode
                        if (GraphicsMode == 0) :
                            (retVal, newEntry) = UserChoiceT(curLine, oneChar, wordNum, entry)
                        else :
                            print('2: UserChoiceG = ' + str(UserChoiceG))
                            (retVal, newEntry) = UserChoiceG(curLine, oneChar, wordNum, entry)
                            if (retVal == '') :
                                print('Hi')
                                # function for GUI not yet written - same result as random choice
                                retVal   = entry[0]
                                newEntry = entry
                            # end if
                        # end if
                        msgFull = 'U: ' + msgHdr + '用戶選擇了 「' + retVal + '」 , 其他可能包括 : ' + FormatQuotes(str(entry[2:]))
                        newDictLine = '    「' + oneChar + '」 : ' + str(newEntry)
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

    MsgList_X = list()          # notInDict     (X)
    MsgList_U = list()          # userChoice    (U)
    MsgList_M = list()          # mostLikely    (M)
    MsgList_E = list()          # equallyLikely (E)
    MsgList_R = list()          # random        (R)
    MsgList_P = list()          # previous      (P)
    TitleDict = {
        'X' : '字典未收藏',
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
            if (msgType in "XUMERP") :
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
    for listType in 'XUMERP' :
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


def ProcessFile ( inFile, expertMode=0, graphicsMode=0, guiParam=None ) :
    """ Process input song file
    
    Inputs:
        inFile       : path to input file
        expertMode   : 1 if expert mode is used, default 0
        graphicsMode : 1 if graphics mode is used, default 0
        guiParam     : parameters for GUI mode
                       [0] = callback function
                       [1] = new entry List
    Output:
        (status, message))
            status  : 0 for success, >0 for failure
            message : (used for failure) a brief error message describing the cause of the failure
    """
    global      ExpertMode
    global      GraphicsMode
    global      GUI_Parameters
    global      UserChoiceG
    #
    global      MsgWordList
    global      PrevChoiceDict
    global      MsgList
    global      NewDictEntryList

    print('ProcessFile() called for infile ' + inFile)
    outFile  = re.sub('.txt', '_input.txt', inFile)
    noteFile = re.sub('.txt', '_notes.txt', inFile)
    logFile  = re.sub('.txt', '.log', inFile)
    
    MsgWordList      = list()
    PrevChoiceDict   = dict()
    MsgList          = list()
    NewDictEntryList = list()

    if (0) :
        # dynamically load dictionary
        print('Load dictionary')
        inDict = 'CantoneseDict.txt'
        exec(open(inDict, encoding='utf-8').read())
    # end if
    print('Initially, WordListDict has ' + str(len(WordListDict)) + ' items')

    ExpertMode   = expertMode
    GraphicsMode = graphicsMode
    if (GraphicsMode == 1) :
        GUI_Parameters = guiParam
        UserChoiceG    = GUI_Parameters[0]
        #x print('GUI_Parameters = ' + str(GUI_Parameters))
        #x print('1: UserChoiceG = ' + str(UserChoiceG))
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
        print('\nLine ' + str(lineNum+1000)[1:] + ' : ' + curLine.strip())
        #
        grpList = (curLine.strip()).split()
        print('\nLine ' + str(lineNum+1000)[1:] + ' : wordList = ' + str(grpList))
        grpCnt = 0
        grpNum = len(grpList)
        for oneGrp in grpList :
            grpCnt += 1
            print('  oneGrp = ' + oneGrp)
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

    # close input and output files
    fi.close()
    fo.write('# end of song\n\n')
    fo.flush()
    fo.close()

    # Write notes file
    WriteMessages(noteFile)
    
    return(0, '')
# end def ProcessFile()

