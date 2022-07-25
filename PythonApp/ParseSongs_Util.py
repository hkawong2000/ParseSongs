#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Functions to process data from songs
# ==============================================================

import os
import re
import sys
import string
import shutil
#
sys.path.append('./ParseSongs_Output')
from ParseSongs_Output import *

import tkinter as tk
from tkinter import *
from tkinter.messagebox import *

# ==============================================================

# Dictionaries for note mapping
Dict_Notes = {
    "1"  : 0,
    "1#" : 1,
    "2b" : 1, 
    "2"  : 2,
    "2#" : 3,
    "2b" : 3,
    "3"  : 4,
    "4" :  5,
    "4#" : 6,
    "5b" : 6,
    "5" :  7,
    "5#" : 8,
    "6b" : 8,
    "6" :  9,
    "6#" : 10,
    "7b" : 10,
    "7"  : 11,
}

# List of interval names
# ref: https://en.wikipedia.org/wiki/Interval_(music)
List_Interval = [
    "U",    # 0 - unison
    "m2",
    "M2",
    "m3",
    "M3",   # 4
    "P4",
    "A4",
    "P5",
    "m6",   # 8
    "M6",
    "m7",
    "M7",
    "P8"   # 12
]

# Interval for TTT per Yiu 2014 paper
YiuInterval = {
    # key : concatenatio of higherTarget & lowerTarget
    # value : [[list of intervals per Yiu], [list of number of semitones per Yiu]]
    "53" : [["M2", "M3"],            [2, 4]],
    "52" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "51" : [["P5", "M6", "m7", "O"], [7, 9, 10, 12]],
    "32" : [["m2", "m3"],            [1, 3]],
    "31" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "21" : [["M2", "M3"],            [2, 4]],
}

# Globals
WordCnt = 0             # number of non-rest words in the song

PrevWord   = ''         # previous chinese character
PrevTone   = 0          # tone of previous non-rest word (int 1-6); 0 if it is the 1st word of the song
PrevMelody = ''         # melody of the previous non-rest word (str); '' if it is the 1st word of the song
PrevRest   = False      # previous item is a rest
#
MinNoteDiv  = 1
UnitsPerBar = 0
UnitCount   = 0
BarsPerLine = 0
BarCount    = 0
#
wordRow_list          = list()
jyutPingRow_list      = list()
melodyRow_list        = list()
musicIntervalRow_list = list()
toneIntervalRow_list  = list()

# Return codes for Calc_YiuResult()
PREV_REST_VAL           = 0x0100
SAME_TARGET_DIFF_NOTE   = 0x0001
DIFF_TARGET_SAME_NOTE   = 0x0002
IN_YIU_RANGE            = 0x0004
OUT_YIU_RANGE           = 0x0008  

# Pointer to log file
fLog = None

# Remarks for (partial-)mismatches
RemarkCount = 0
RemarkList  = list()

# ==============================================================

def WriteLog ( logStr ) :
    """ Write 'logStr' to the logfile

    Inputs:
        logStr : string to write to the log file
    Output:
        (none)
    """
    global      fLog

    fLog.write(logStr + '\n')
# end def WriteLog()


def Calc_Note(oneNote) :
    """ Return a numeric value of a note for interval calculation, with "-1" as -12, "-2' as -10, "1" as 0, ...
    
    Inputs:
        oneNote : current musical note (text format) (e.g "-1s")

    Output:
        numeric value of a note for interval calculation
    """
    # 1) Octave
    if (oneNote[0] == '-') :
        note1     = oneNote[1:]
        octaveInc = -12 
    elif (oneNote[0] == '+') :
        note1     = oneNote[1:]
        octaveInc = 12
    else :
        note1     = oneNote
        octaveInc = 0
    # end if

    return(Dict_Notes[note1] + octaveInc)
# end def Calc_Note()
#
def Calc_MusicInterval(prevNote, curNote) :
    """ Calculate the musical interval between notes
    
    Inputs:
        prevNote : previous musical note (text format), e.g. "-5#"
        curNote  : current musical note (text format)
    Output:
        a string describing the intervals in mucical terms and number of semitones ("P5(7)")
    NOTE:
        global PrevNote will be used
    """
    note1    = Calc_Note(prevNote)
    note2    = Calc_Note(curNote)
    noteDiff = abs(note1 - note2)
    if (noteDiff == 0) :
        outStr = '0/U'
    elif (noteDiff > 12) :
        outStr = str(noteDiff) + '/P8+'
    else :
        outStr = str(noteDiff) + '/' + List_Interval[noteDiff]
    # end if
    return(outStr)
# end def Calc_MusicInterval()
#
def Calc_YiuResult(prevTone, curTone, mInterval) :
    """ Calculate the interval between notes, based on tones and intervals suggested by Suki Yiu 2013/2014
    
    Inputs:
        prevTone  : tone of previous word (numeric format, 1 to 6)
        curTone   : tone of current word (numeric format, 1 to 6)
        mInterval : interval based on melody (string format, e.g. 5/P4)
    Output:
        (retCode, yKey, result)
            retCode = a numeric value representing the condition for match (0) and mismach (>0)
            yKey    = key for indexing into YiuInterval dict()
            result  = a string for inserting in HTML table
    """
    global      fLog

    CHECK_CHAR = '&#x2713'
    targetMap  = [0, 5, 5, 3, 1, 3, 2]
    returnCode = 0
    yKey       = ''
    
    prevTarget = targetMap[prevTone]
    curTarget  = targetMap[curTone]
    if (prevTarget > curTarget) :
        higherTarget = prevTarget
        lowerTarget  = curTarget
    else :
        higherTarget = curTarget
        lowerTarget  = prevTarget
    # end if
    #x print("higherTarget = " + str(higherTarget) + ", lowerTarget = " + str(lowerTarget))

    if ((higherTarget == 0) or (lowerTarget == 0)) :
        retCode = 0
        result  = '-'
    #
    elif ((higherTarget == lowerTarget) and (mInterval == '0/U')) :
        retCode = 0
        result  = '(s)'
    #
    elif ((higherTarget == lowerTarget) and (mInterval != '0/U')) :
        # same target, different note
        if (PrevRest == True) :
            retCode    = SAME_TARGET_DIFF_NOTE + PREV_REST_VAL
            result     = '<span class="mismatchSameTone tooltip"> (sT-p) <span class="tooltiptext"> Same TT diff note after rest </span> </span>'
        else :
            retCode    = SAME_TARGET_DIFF_NOTE
            result    = '<span class="mismatchSameTone tooltip"> (sT) <span class="tooltiptext"> Same TT diff note </span> </span>'
        # end if
    #
    elif ((higherTarget != lowerTarget) and (mInterval == '0/U')) :
        # same note, different target
        yKey = str(higherTarget) + str(lowerTarget)
        if (PrevRest == True) :
            retCode = DIFF_TARGET_SAME_NOTE + PREV_REST_VAL
            result  = '<span class="mismatchSameNote tooltip"> (sN-p) <span class="tooltiptext"> Same note diff TT after rest </span> </span>'
        else :
            retCode = DIFF_TARGET_SAME_NOTE
            result = '<span class="mismatchSameNote tooltip"> (sN) <span class="tooltiptext"> Same note diff TT after rest </span> </span>'
        # end if
    #
    else :
        yKey          = str(higherTarget) + str(lowerTarget)
        yValue        = YiuInterval[yKey]
        ySemitoneList = yValue[1]
        mSemitones    = int(mInterval[0])
        if (mSemitones in ySemitoneList) :
            # match one of the defined values
            retCode = 0
            result  = CHECK_CHAR
        elif ((mSemitones >= ySemitoneList[0]) and (mSemitones <= ySemitoneList[-1])) :
            # does not match exactly the values given in Yiu, but is within the range
            if (PrevRest == True) :
                retCode = IN_YIU_RANGE + PREV_REST_VAL
                result  = '<span class="halfMatch tooltip"> (I-p) <span class="tooltiptext"> Non-match within intvl after rest </span> </span>'
            else :
                retCode = IN_YIU_RANGE
                result  = '<span class="halfMatch tooltip"> (I) <span class="tooltiptext"> Non-match within intvl </span> </span>'
            # end if
        else :
            if (PrevRest == True) :
                retCode = OUT_YIU_RANGE + PREV_REST_VAL
                result  = '<span class="noMatch tooltip"> (X-p) <span class="tooltiptext"> Non-match after rest </span> </span>'
            else :
                retCode = OUT_YIU_RANGE
                result  = '<span class="noMatch tooltip"> (X) <span class="tooltiptext"> Non-match after rest </span> </span>'
        # end if
    # end if

    return(retCode, yKey, result)
# end def Calc_YiuResult()


def GenRemark ( code, word, curTone, melody, mInterval, yKey, yiuResult ) :
    """ Generate a remark string
    
    Inputs:
        code      : return code from Calc_YiuResult()
        word      : current word
        curTone   : tone of current word (numeric format, 1 to 6)
        melody    : current melody
        mInterval : interval based on melody (string format, e.g. 5/P4)
        yKey      : key for indexing into YiuInterval dict()
        yiuResult : result string from Calc_YiuResult()
    Output:
        remarkStr : remark string
    """
    global      RemarkCount, RemarkList
    global      PrevWord, PrevTone, PrevMelody, PrevRest    
    # PrevTone = 0        # tone of previous non-rest word (int 1-6); 0 if it is the 1st word of the song
    # PrevMelody = ''     # melody of the previous non-rest word (str); '' if it is the 1st word of the song
    # PrevRest = False    # previous item is a rest

    # PREV_REST_VAL           = 0x100
    # SAME_TARGET_DIFF_NOTE   = 0x01
    # DIFF_TARGET_SAME_NOTE   = 0x02
    # IN_YIU_RANGE            = 0x04
    # OUT_YIU_RANGE           = 0x08 
    
    # DEBUG
    #x outStr = 'Word = ' + word + ', code = ' + str(hex(code))
    #x print(outStr)

    ToneList = ['', '(55)', '(35)', '(33)', '(21)', '(13)', '(22)']
    
    remarkItem  = [str(RemarkCount+100)[1:]]
    remarkItem.append(PrevWord)
    remarkItem.append(str(PrevTone) + ToneList[PrevTone])
    remarkItem.append(PrevMelody)
    remarkItem.append(word)
    remarkItem.append(str(curTone) + ToneList[curTone])
    remarkItem.append(melody)
    remarkItem.append(mInterval)
    if (PrevRest == True) :
        remarkItem.append('Y')
    else :
        remarkItem.append('-')
    # end if
    if (yKey == '') :
        remarkItem.append('(n/a)')
    else :
        idealMI = str(YiuInterval[yKey][0])
        remarkItem.append(idealMI)
    # end if
    if (code & SAME_TARGET_DIFF_NOTE) :
        remStr = '<span class="mismatchSameTone"> Same target tone for the 2 words, but different notes </span>'
    elif (code & DIFF_TARGET_SAME_NOTE) :
        remStr = '<span class="mismatchSameNote"> Same note for the 2 words, but different target tones </span>'
    elif (code & IN_YIU_RANGE) :
        remStr = '<span class="halfMatch"> Mismatch of MI and target tone for the 2 words, yet MI is within max and min limits </span>'
    elif (code & OUT_YIU_RANGE) :
        remStr = '<span class="noMatch"> Mismatch of MI and target tone for the 2 words </span>'
    # end if
    if (code & PREV_REST_VAL) :
        remStr += ' <br> but word preceded by rest'
    # end if
    remarkItem.append(remStr)
    RemarkList.append(remarkItem)
    return(remStr)

    # <td width=n%>  #         </td>        <!-- Remark idx (0) : rowspan=2 -->
    # <td width=n%>            </td>        <!-- prev/cur -->
    # <td width=n%>  Word      </td>        <!-- word (1,4) -->
    # <td width=n%>  Tone      </td>        <!-- tone (2,5)-->
    # <td width=n%>  Melody    </td>        <!-- melody (3,6) -->
    # <td width=n%>  MI        </td>        <!-- melody interval (7) : rowspan=2 -->  
    # <td width=n%>  Prev Rest </td>        <!-- prevRest (8) : rowspan=2 -->  
    # <td width=20%> Ideal MI  </td>        <!-- ideal MI (9) : rowspan=2 -->  
    # <td>           Comment   </td>        <!-- remarks (10) : rowspan=2 -->  
    
# end def GenRemark()


def ProcessOneWord ( word, jyutping, melody, duration ) :
    """ Process one word from the input file
    
    Inputs:
        word     : Chinese word
        jyutping : jyutping of the word
        melody   : melody of the word
        duration : duration of the word (int)
    Output:
         1 if it is needed to print a line to output file
         0 if word processing is OK
        <0 for errors (not yet implemented)
    """
    global      PrevWord, PrevTone, PrevMelody, PrevRest    
    # PrevTone = 0        # tone of previous non-rest word (int 1-6); 0 if it is the 1st word of the song
    # PrevMelody = ''     # melody of the previous non-rest word (str); '' if it is the 1st word of the song
    # PrevRest = False    # previous item is a rest

    global      WordCnt
    global      MinNoteDiv
    global      UnitsPerBar, UnitCount
    global      BarsPerLine, BarCount

    global      wordRow_list
    global      jyutPingRow_list
    global      melodyRow_list
    global      musicIntervalRow_list
    global      toneIntervalRow_list

    global      RemarkCount

    global      fLog
    
    outStr = 'ProcessOneWord() : word=' + word + ', jyutping=' + jyutping + ', melody=' + melody + ', duration =' + str(duration)
    #x print(outStr)
    WriteLog(outStr)
    span = int(duration)
    
    # Determine whether bar lines needed to be added to left or right
    if (UnitCount == 0) :
        barClass = ' lb'
    elif ((UnitCount + span) == UnitsPerBar) :
        barClass = ' rb'
    else :
        barClass = ''
    # end if
    
    # retrieve tone of current word
    if (word != '-') :
        mT = re.search('[\d]', jyutping)
        if mT :
            curTone = int(mT.group(0))
        else :
            errStr = 'Cannot retrieve tone for word "' + jyutping + '"'
            WriteLog(errStr)
            return(-1)
        # end if
    else :
        curTone = 0
    # end if
    
    #x print('> WordCnt = ' + str(WordCnt))
    if ((word != '-') and (WordCnt > 0)) :
        # need to calculate musicInterval and toneInterval
        musicInterval           = Calc_MusicInterval(PrevMelody, melody)
        (code, yKey, yiuResult) = Calc_YiuResult(PrevTone, curTone, musicInterval)
        if (code != 0) :
            RemarkCount += 1
            GenRemark(code, word, curTone, melody, musicInterval, yKey, yiuResult)
            supText    = ' <sup> ' + str(RemarkCount+100)[1:] + ' </sup> '
            yiuResult += supText
        # end if
    else :
        # current note is rest
        musicInterval = '-'
        yiuResult     = '-'
    # end if
    outStr = '  musicInterval = "' + musicInterval + '", yiuResult = "' + yiuResult + '"'
    WriteLog(outStr)
    #
    if (0) :
        # DEBUG
        if (barClass == ' lb') :
            print('')
        # end if
        print('DB : word=' + word + ', curTone=' + str(curTone) + ' : mi="' + musicInterval + '", yiuResult =' + yiuResult)
    # end if (1)

    # Set PrevRest for next note
    if (word == '-') :
        # rest
        PrevRest = True
    else :
        PrevWord   = word
        PrevRest   = False
        PrevTone   = curTone
        PrevMelody = melody
    # end if

    wordCell     = '  <td class="wd' + barClass + '" colspan=' + str(span) + '> ' + word          + ' </td>'
    jyutPingCell = '  <td class="jp' + barClass + '" colspan=' + str(span) + '> ' + jyutping      + ' </td>'
    melodyCell   = '  <td class="me' + barClass + '" colspan=' + str(span) + '> ' + melody        + ' </td>'
    musicIntCell = '  <td class="mi' + barClass + '" colspan=' + str(span) + '> ' + musicInterval + ' </td>'
    toneIntCell  = '  <td class="ti' + barClass + '" colspan=' + str(span) + '> ' + yiuResult     + ' </td>'
    #
    wordRow_list.append(wordCell)
    jyutPingRow_list.append(jyutPingCell)
    melodyRow_list.append(melodyCell)
    musicIntervalRow_list.append(musicIntCell)
    toneIntervalRow_list.append(toneIntCell)
    
    WordCnt   += 1
    UnitCount += span
    if (UnitCount == UnitsPerBar) :
        BarCount  += 1
        UnitCount  = 0
    # end if

    # Write out the musical score at the end of each line
    #x print('DEBUG: word=' + word + ', BarCount = ' + str(BarCount))
    if (BarCount == BarsPerLine) :
        # Write out line
        BarCount = 0
        return(1)
    else :
        return(0)
    # end if
# end def ProcessOneWord()


def ParseSong ( inFilePath, songName, minNoteDivVal, unitsPerBarVal, barsPerLineVal, browserPath ) :
    """ Parse input file into list for further processing
    
    Inputs:
        inFilePath    : full path of input file
        songName      : name of song
        minNoteDivVal : minimum note duration (number of divisions per beat)
        unitsPerBar   : number of units per bar (int)
        barsPerLine   : number of bars per line (int)
        browserPath   : path to browser program

    Output:
        (code, errStr) where code is
            0 for success; <0 for failure
    """
    global      UnitsPerBar, UnitCount
    global      BarsPerLine, BarCount
    global      MinNoteDiv
    global      WordCnt
    global      PrevTone, PrevMelody, PrevRest 
    global      fLog
    global      RemarkCount, RemarkList

    retVal = 0
    print('ParseSong() called')
    
    UnitsPerBar = unitsPerBarVal
    BarsPerLine = barsPerLineVal
    MinNoteDiv  = minNoteDivVal
    
    # Reset global variables
    UnitCount   = 0
    BarCount    = 0
    WordCnt     = 0
    PrevTone    = 0
    PrevMelody  = ''
    PrevRest    = False
    RemarkCount = 0
    RemarkList  = list()
    
    unitsPerLine = unitsPerBarVal * barsPerLineVal
    spanRow = Generate_SpanHeader(unitsPerLine)

    # showinfo(title='Information', message='ParseSong() called.')
    lineNum  = 0
    patWord = '[\s]*([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)'    # len(m.groups())
    
    # Open files for read and write
    inFileNameLastIdx = inFilePath.rindex('/')
    inFileNameLast    = inFilePath[(inFileNameLastIdx+1):]
    logFilePath       = re.sub('\.txt$', '_log.txt', inFilePath)
    logFileName       = re.sub('\.txt$', '_log.txt', inFileNameLast)
    outFilePath       = re.sub('\.txt$', '.html', inFilePath)
    outFileName       = re.sub('\.txt$', '.html', inFileNameLast)
    if (os.path.exists(outFilePath)) :
        askStr    = 'File "' + outFileName + '" already exists\nAre you sure you want to overwrite?\nIf No, please rename/backup the file'
        overWrite = askyesno(title='Warning', message=askStr)
        if (overWrite == False) :
            return (-1, 'Output file already exists')
    #
    
    #x OpenLog(logFilePath)
    fLog = open(logFilePath, 'w', encoding='utf-8')
    fi   = open(inFilePath,       encoding='utf-8')
    foH  = open(outFilePath, 'w', encoding='utf-8')
    
    headerTxt = re.sub('RR_TITLE', songName, HTML_HEADER)
    foH.write(headerTxt)
    foH.write(spanRow)
    
    for curLine in fi.readlines() :
        lineNum += 1
        if ((curLine[0] == '#') or (curLine.strip() == '')) :
            # comment line or blank line : skip
            continue
        #
        else :
            mWord = re.search(patWord, curLine)
            if mWord :
                if (len(mWord.groups()) != 4) :
                    # cannot find all 4 fields in the line
                    errStr = 'ERROR: cannot find all 4 fields on line ' + str(lineNum) + ' in file "' + inFileNameLast + '"'
                    return (-2, errStr)
                # end if
                #
                word      = mWord.group(1)
                jyutping  = mWord.group(2)
                melody    = mWord.group(3)
                length    = mWord.group(4)
                if (length == '1') :
                    duration = MinNoteDiv
                elif (length == 'H') :
                    if (MinNoteDiv == 1) :
                        return (-3, 'Min note duration longer than current note')
                    elif (MinNoteDiv == 2) :
                        duration = 1
                    elif (MinNoteDiv == 4) :
                        duration = 2
                    # end if
                elif (length[0] == 'Q') :
                    if (MinNoteDiv == 4) :
                        if ((len(length) == 1) or ((len(length) == 2) and (length[1] == '1'))) :
                            duration = 1
                        elif ((len(length) == 2) and (length[1] == '3')) :
                            duration = 3
                        # end if
                    else :
                        return (-3, 'Min note duration longer than current note')
                    # end if
                # end if
                print('DEBUG: word = ' + word + ', duration = ' + str(duration))
                writeLine = ProcessOneWord(word, jyutping, melody, duration)
                if (writeLine == 1) :
                    WriteLineH(foH, [wordRow_list, jyutPingRow_list, melodyRow_list, musicIntervalRow_list, toneIntervalRow_list], 0)
                elif (writeLine == -1) :
                    # some error has occurred
                    FlushLog()
                    CloseLog()
                    return(-10, 'ERROR: Refer to log file "' + logFileName + '" for details')
                # end if
            # end if
        # end if
    # end for

    # Check if any remaining line
    outStr = 'End of song: UnitCount = ' + str(UnitCount) + ', BarCount = ' + str(BarCount)
    WriteLog(outStr)
    #x print('DEBUG: ' + outStr)
    if ((UnitCount != 0) or (BarCount != 0)) :
        print('Remaining notes ...')
        WriteLineH(foH, 1)
    # end if
    #
    foH.write(TABLE_FOOTER)
        
    # Remarks
    print('RemarkCount = ' + str(RemarkCount) + '/' + str(len(RemarkList)))
    if (RemarkCount > 0) :
        remFilePath = re.sub('\.txt$', '_Remarks.html', inFilePath)
        foR = open(remFilePath, 'w', encoding='utf-8')
        GenRemark_HTML(foR, RemarkList, songName)
        successTxt = "Success, with remarks"
        #
        remStr  = '<p class="reminder"> Please also see remarks in '
        remStr += '<a target="_blank" href="' + remFilePath + '"> ' + remFilePath[(inFileNameLastIdx+1):] + '</a>\n'
        foH.write(remStr)
    else :
        successTxt = "Success"
    # end if
    
    # Close the output file
    foH.write(HTML_FOOTER)
    foH.flush()
    foH.close()
    foR.flush()
    foR.close()
    
    fLog.flush()
    fLog.close()
    
    # Open output file in browser
    if (1) :
        sysCmd = '"' + browserPath + '" ' + re.sub('/', '\\\\', outFilePath) + ''
        print('sysCmd = ' + sysCmd)
        os.system(sysCmd)
    else :
        print('File not opened in browser')
    # end if

    return(0, successTxt)
# end def ParseSong()
