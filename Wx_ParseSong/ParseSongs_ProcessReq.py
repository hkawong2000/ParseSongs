#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys

sys.path.append('.')
from ParseSongs_Util import *
from ParseSongs_CalcInterval import *
from ParseSongs_GenOutput import *
#
import wx

# Globals
ItemCnt = 0             # Number of items (words + rest-notes + bars)

# Information from GUI/Calling program
Song_NoteFormat  = ''
Song_BeatsPerBar = 0
BeatsInBar       = [0, 0]   # number of beats (except 1/3), number of 1/3

# Word information
# list of 6 items [word(s), jyutping(s), melody(s), duration(s), tone(i), rest(b)]
CurWordInfo  = None
PrevWordInfo = None

# Parsed information of song
SongInfo_List = list()

# Remarks for (partial-)mismatches
RemarkList = list()

# First word of song
FirstWord = True

# ==============================================================
# Functions to process input file
# ==============================================================

def Check_Beats ( opt ) :
    """ Check number of beats is correct for the given Song_BeatsPerBar
    
    Inputs:
        opt : 1 to check if the number of beats is not enough for a bar
              0 to check if the number of beats exceeds that for a bar
    Output:
        result : 0 for pass, <0 for fail
    """
    global      Song_BeatsPerBar
    global      BeatsInBar
    
    totalBeats = BeatsInBar[0] + (BeatsInBar[1]/3)
    WriteLog('  @ beatsInBar = ' + str(totalBeats))
    if (opt == 0) :
        if (totalBeats > Song_BeatsPerBar) :
            return(-1)
        # end if
    elif (opt == 1) :
        if (totalBeats < Song_BeatsPerBar) :
            return(-1)
        # end if
    # end if
    return(0)
# end def Check_Beats()
#
def Calc_Duration(durationStr, beatsPerBar) :
    """ Calculate the duration and span width of one note
    
    Inputs:
        durationStr : string representing the duration of the note
        beatsPerBar : number of beats per bar
    Output:
        (durationNum, spanWidth) where
            durationNum = numeric value of duration (in beats);
                          <0 if there is error
            spanWidth   = span of note in output table
                          error descrption if there is error
    """
    global      BeatsInBar

    # Check if format is valid
    allowedChar = '0123456789.HhTtQq'
    for c in durationStr :
        if (not(c in allowedChar)) :
            # error
            return(-1, '拍數 ' + durationStr + ' 格式有問題')
        # end if
    # end for
    
    mNum = re.search('^[0-9.]+$', durationStr)
    if mNum :
        # is a pure number (float or int)
        try :
            durTotal = float(durationStr)
        except :
            return(-1, '拍數 ' + durationStr + ' 格式有問題')
        else :
            BeatsInBar[0] += durTotal
        # end if
    else :
        durTotal = 0
        for c in durationStr :
            if (c.upper() == 'Q') :
                newVal = 0.25
            elif (c.upper() == 'T') :
                newVal = 0.33
            elif (c.upper() == 'H') :
                newVal = 0.5
            else :
                newVal = int(c)
            # end newVal
            durTotal += newVal
            if (newVal == 0.33) :
                BeatsInBar[1] += 1
            else :
                BeatsInBar[0] += newVal
            # end if
        # end for
    # end if
    spanWidth = durTotal * 100 / beatsPerBar

    retVal0 = Check_Beats(0)
    if (retVal0 == 0) :
        return(durTotal, spanWidth)
    else :
        # too many beats in a bar
        return(-2, '小節拍數過多')
    # end if
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
        list is ['ERR', cause] if there is some error with cause indicating the cause
    """
    global      Song_NoteFormat
    global      SongInfo_List
    global      ErrList
    global      PrevWordInfo, CurWordInfo
    global      ItemCnt
    global      BeatsInBar
    global      FirstWord

    outStr = 'ProcessOneWord() : word=' + word + ', jyutping=' + jyutping + ', melody=' + melody + ', duration=' + str(duration)
    WriteLog(outStr)

    if (word == 'bar') :
        retVal = Check_Beats(1)
        if (retVal < 0) :
            # not enough beats before bar line
            return(['ERR', '小節拍數過少'])
        # end if
        BeatsInBar = [0, 0]
        noteArray = ['(bar)', '', 0, '', 0, 0, '', 0, ''];
        SongInfo_List.append(noteArray)
        return(noteArray)
    # end if
    
    # Retrieve tone of current word
    curTone = 0
    if (word != '-') :
        mT = re.search('[\d]', jyutping)
        if mT :
            curTone = int(mT.group(0))
        else :
            curTone = 0
        # end if
        CurWordInfo = [word, jyutping, melody, duration, curTone, False]
    else :
        CurWordInfo = [word, jyutping, melody, duration, 0, True]
    # end if

    # Calculate duration of word/rest
    (durationNum, spanWidth) = Calc_Duration(duration, Song_BeatsPerBar)
    if (durationNum < 0) :
        # error in formatting
        return['ERR', spanWidth]
    # end if
    
    if ((word != '-') and (ItemCnt > 0) and (FirstWord == False)) :
        # need to calculate musicInterval and toneInterval
        prevMelody        = PrevWordInfo[2]
        musicInterval     = Calc_MusicInterval(prevMelody, melody, Song_NoteFormat)
        if (musicInterval[:3] == 'ERR') :
            # error in formatting
            return(['ERR', '旋律 ' + melody + ' 格式有問題'])
        # end if
        (code, yiuResult) = Calc_YiuResult(CurWordInfo, PrevWordInfo, musicInterval, RemarkList) 
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
        PrevWordInfo[-1] = True
    else :
        # copy CurWordInfo to PrevWordInfo
        PrevWordInfo = list()
        for oneField in CurWordInfo :
            PrevWordInfo.append(oneField)
        # end for
        FirstWord = False
    # end if
    
    FlushLog()
    return(noteArray)
# end def ProcessOneWord()


def ParseSong ( inFilePath ) :
    """ Parse input file into list for further processing
    
    Inputs:
        inFilePath : full path of input file
    Output:
        (retCode, errStr) where
            retCode : 0 for success, <0 for failure
                        -1 for file format error
            errStr  : a string describing the error
    """
    global      BeatsInBar
    global      RemarkList
    global      Song_NoteFormat
    global      FirstWord

    # Reset variables
    BeatsInBar = [0, 0]
    RemarkList = list()
    FirstWord  = True

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
            ProcessDirective(curLine.strip(), 1)
        else :
            mBar  = re.search('^bar',  curLine)
            mWord = re.search(patWord, curLine)
            if mBar :
                resultB = ProcessOneWord('bar', '', '', '')
                if (resultB[0] == 'ERR') :
                    errStr = '第' + str(lineNum) + '行 : ' + resultB[1]
                    return(-1, errStr)
                # end if                
            elif mWord :
                if (len(mWord.groups()) < 4) :
                    # cannot find all 4 fields in the line
                    errStr = '第' + str(lineNum) + '行 : ' + '欄數不足'
                    return(-1, errStr)
                # end if
                #
                word     = mWord.group(1)
                jyutping = mWord.group(2)
                melody   = mWord.group(3)
                duration = mWord.group(4)
                result1  = ProcessOneWord(word, jyutping, melody, duration)
                if (result1[0] == 'ERR') :
                    errStr = '第' + str(lineNum) + '行 : ' + result1[1]
                    return(-1, errStr)
                # end if
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
        return (-1, "歌曲文字檔形式要修正")
    else :
        return (0, "成功")
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
    global      Song_BeatsPerBar, Song_NoteFormat
    global      PrevWordInfo
    global      ItemCnt

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
        askStr    = '輸出檔案 "' + outFilePath + '" 已存在\n要不要舊的結果被新的結果取代?\n如果不想的話, 請把原來的檔案更名或備份'
        # (following lines for Tk)
        # overWrite = askyesno(title='Warning', message=askStr)
        # if (overWrite == False) :
        overWrite = wx.MessageBox(askStr, "Warning", wx.YES_NO)
        if (overWrite == wx.NO) :
            return (-1, '輸出檔案已存在')
        # end if
    # end if

    # Open log file
    OpenLog(logFilePath)

    # Parse input song
    ItemCnt = 0
    SongInfo_List.clear()
    RemarkList.clear()
    PrevWordInfo = ['', '', '', '', 0, True]
    #
    print('inFilePath = ' + inFilePath)
    (retVal, errStr) = ParseSong(inFilePath)
    if (retVal == -1) :
        return(-1, errStr)
    # end if

    # Generate output HTML file
    GenOutput_retVal = GenOutput(outFilePath, songName, beatsPerBar, inFileNameLast, SongInfo_List, remFilePath, RemarkList)
    remarkGen        = GenOutput_retVal[0]
    if (remarkGen) :
        WriteLog1('RemarkFile is generated')
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
    
    return(0, "成功")
# end def ProcessRequest()

