#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

sys.path.append('./ParseSongs_Util')
from ParseSongs_Util import *
#
sys.path.append('./ParseSongs_CalcInterval')
from ParseSongs_CalcInterval import *
#
sys.path.append('./ParseSongs_GenOutput')
from ParseSongs_GenOutput import *

# Globals
ItemCnt = 0             # Number of items (words + rest-notes)


# ==============================================================
# Functions to process input file
# ==============================================================

def Calc_Duration(durationStr, beatsPerBar) :
    """ Calculate the duration and span width of one note
    
    Inputs:
        durationStr : string representing the duration of the note
        beatsPerBar : number of beats per bar
    Output:
        (durationNum, spanWidth) where
            durationNum = numeric value of duration (in beats)
            spanWidth   = span of note in output table
    """
    mNum = re.search('^[0-9.]+$', durationStr)
    if mNum :
        # is a pure number (float or int)
        durTotal  = float(durationStr)
    else :
        durTotal = 0
        for c in durationStr :
            if (c.upper() == 'Q') :
                durTotal += 0.25
            elif (c.upper() == 'T') :
                durTotal += 0.33
            elif (c.upper() == 'H') :
                durTotal += 0.5
            else :
                # assume numeric
                durTotal += int(c)
            # end if
        # end for
    # end if
    spanWidth = durTotal * 100 / beatsPerBar
    return(durTotal, spanWidth)
# end def Calc_Duration()


def ProcessOneWord ( word, jyutping, melody, duration ) :
    """ Process one word from the input file
    
    Inputs:
        word     : Chinese word
        jyutping : jyutping of the word
        melody   : melody of the word
        duration : duration of the word (int)
    NOTE:
        list of info for the word, which includes:
            [chiWord, jyutping, toneNum, noteMelody, noteBeat, noteWidth, intMelody, intToneVal, intToneCode];
        list is [] if there is some error
    """
    global      Song_NoteFormat
    global      SongInfo_List
    global      ErrList
    global      PrevWord, PrevTone, PrevMelody, PrevRest
    global      ItemCnt
    global      RemarkCount

    outStr = 'ProcessOneWord() : word=' + word + ', jyutping=' + jyutping + ', melody=' + melody + ', duration=' + str(duration)
    WriteLog(outStr)

    if (word == 'bar') :
        noteArray = ['(bar)', '', 0, '', 0, 0, '', 0, ''];
        SongInfo_List.append(noteArray)
        return
    # end if
    
    # Retrieve tone of current word
    curTone = 0
    if (word != '-') :
        mT = re.search('[\d]', jyutping)
        if mT :
            curTone = int(mT.group(0))
        # end if
    # end if

    # Calculate duration of word/rest
    (durationNum, spanWidth) = Calc_Duration(duration, Song_BeatsPerBar)
    
    if ((word != '-') and (ItemCnt > 0)) :
        # need to calculate musicInterval and toneInterval
        musicInterval     = Calc_MusicInterval(PrevMelody, melody, Song_NoteFormat)
        (code, yiuResult) = Calc_YiuResult(word, curTone, melody, musicInterval, PrevWord, PrevTone, PrevMelody, PrevRest)
        WriteLog('  YiuResult : word = ' + word + ', code = ' + str(code) + ', yiuResult = ' + str(yiuResult))
    else :
        # current note is rest
        code          = 0
        musicInterval = '-'
        yiuResult     = '-'
    # end if

    ItemCnt += 1

    # [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TONE_CODE, IDX_TONE_STR]
    noteArray = [word, jyutping, curTone, melody, durationNum, spanWidth, musicInterval, code, yiuResult];
    SongInfo_List.append(noteArray)

    # Set PrevRest for next note
    if (word == '-') :
        # rest
        PrevRest = True
    else :
        PrevRest   = False
        PrevTone   = curTone
        PrevMelody = melody
        PrevWord   = word
    # end if
# end def ProcessOneWord()


def ParseSong ( inFilePath ) :
    """ Parse input file into list for further processing
    
    Inputs:
        inFilePath : full path of input file
    Output:
        0 for success, <0 for failure 
            -1 for file format error
    """
    global      RemarkCount, RemarkList
    global      Song_NoteFormat

    # Reset variables
    RemarkCount = 0
    RemarkList  = list()

    lineNum = 0
    patWord = '[\s]*([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)'        # len(m.groups())

    fi = open(inFilePath, encoding='utf-8')
    for curLine in fi.readlines() :
        lineNum += 1
        if ((curLine[0] == '#') or (curLine.strip() == '')) :
            # comment line or blank line : skip
            continue
        #
        elif (curLine[0] == '@') :
            # Special directives
            pass
        else :
            mBar  = re.search('^bar',  curLine)
            mWord = re.search(patWord, curLine)
            if mBar :
                ProcessOneWord('bar', '', '', '')
            elif mWord :
                if (len(mWord.groups()) != 4) :
                    # cannot find all 4 fields in the line
                    errStr = 'ERROR: cannot find all 4 fields on line ' + str(lineNum) + ' in input file'
                    ErrList.append(errStr)
                    continue
                # end if
                #
                word     = mWord.group(1)
                jyutping = mWord.group(2)
                melody   = mWord.group(3)
                duration = mWord.group(4)
                ProcessOneWord(word, jyutping, melody, duration)
            # end if
        # end if
    # end for curLine
    fi.close()

    # DEBUG
    if (0) :
        WriteLog1('\nParseSong() : Debug - SongInfo_List')
        i = 0
        for oneItem in SongInfo_List :
            i += 1
            str1   = str(i+100)[1:] + ' : ' + str(oneItem[:2])
            space1 = ' ' * (28 - len(str1))
            str2   = str(oneItem[2:])
            WriteLog1('- ' + str1 + space1 + str2)
        # end for
        WriteLog1('End - SongInfo_List\n')
    # end if

    # Return value
    if (len(ErrList) > 0) :
        return -1
    else :
        return 0
    # end if
# end def ParseSong()


def ProcessRequest ( inFilePath, songName, beatsPerBar, noteFormat, browserPath ) :
    """ Parse input file into list for further processing
    
    Inputs:
        inFilePath  : full path of input file
        songName    : name of song
        beatsPerBar : number of beats per bar (int)
        noteFormat  : 'A' (for C,D,E) or 'N' (for 1,2,3)
        browserPath : path to browser program

    Output:
        (code, errStr) where code is
            0 for success; <0 for failure
    """
    global      ErrList
    global      RemarkCount
    global      Song_BeatsPerBar, Song_NoteFormat

    retVal = 0
    print('ProcessRequest() called')
    # showinfo(title='Information', message='ProcessRequest() called.')

    # Set global variables
    Song_BeatsPerBar = beatsPerBar
    Song_NoteFormat  = noteFormat
    
    # Files for read and write
    inFileNameLastIdx = inFilePath.rindex('/') + 1
    inFileNameLast    = inFilePath[inFileNameLastIdx:]
    inFileFolder      = inFilePath[:inFileNameLastIdx]
    #
    logFileFolder = inFileFolder
    logFilePath   = logFileFolder + re.sub('\.txt$', '_log.txt', inFileNameLast)
    outFileFolder = inFileFolder
    outFilePath   = outFileFolder + re.sub('\.txt$', '.html', inFileNameLast)
    remFileFolder = inFileFolder
    remFilePath   = remFileFolder + re.sub('\.txt$', '_Remarks.html', inFileNameLast)
    if (os.path.exists(outFilePath)) :
        askStr    = 'File "' + outFilePath + '" already exists\nAre you sure you want to overwrite?\nIf No, please rename/backup the file'
        overWrite = askyesno(title='Warning', message=askStr)
        if (overWrite == False) :
            return (-1, 'Output file already exists')
        # end if
    # end if

    # Open log file
    OpenLog(logFilePath)

    # Parse input song
    SongInfo_List.clear()
    retVal1 = ParseSong(inFilePath)
    if (retVal1 == -1) :
        return(-1, "Input file format error")
    # end if

    # Generate output HTML file
    retVal2 = GenOutput(outFilePath, songName, beatsPerBar, inFileNameLast, SongInfo_List, remFilePath)
    remarkFile = retVal2[0]
    # end if

    # Open output file in browser
    if (1) :
        sysCmd = '"' + browserPath + '" ' + re.sub('/', '\\\\', outFilePath) + ''
        WriteLog1('sysCmd = ' + sysCmd)
        os.system(sysCmd)
    else :
        WriteLog1('File not opened in browser')
    # end if

    # Close log file
    CloseLog()
    
    return(0, "Success")
# end def ProcessRequest()

