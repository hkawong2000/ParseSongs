#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Functions to calculate musical and tone intervals (per Yiu 2014)
# ==============================================================

import re
import sys
#
sys.path.append('.')
from ParseSongs_Util import *

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

Dict_Notes_Alpha = {
    "C"  : 0,
    "C#" : 1,
    "Db" : 1, 
    "D"  : 2,
    "D#" : 3,
    "Eb" : 3,
    "E"  : 4,
    "F" :  5,
    "F#" : 6,
    "Gb" : 6,
    "G" :  7,
    "G#" : 8,
    "Ab" : 8,
    "A" :  9,
    "A#" : 10,
    "Bb" : 10,
    "B"  : 11,
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
    # key : concatenation of higherTarget & lowerTarget
    # value : [[list of intervals per Yiu], [list of number of semitones per Yiu]]
    "53" : [["M2", "M3"],            [2, 4]],
    "52" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "51" : [["P5", "M6", "m7", "O"], [7, 9, 10, 12]],
    "32" : [["m2", "m3"],            [1, 3]],
    "31" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "21" : [["M2", "M3"],            [2, 4]],
}

# ==============================================================

def Calc_Note( oneNote, noteFormat ) :
    """ Return a numeric value of a note for interval calculation, with "-1" as -12, "-2' as -10, "1" as 0, ...
    
    Inputs:
        oneNote    : current musical note (text format) (e.g "-3#", "+Gb")
        noteFormat : 'N' for '1,2,3'; 'A' for 'C,D,E'
    Output:
        numeric value of a note for interval calculation
    """
    # Check format
    allowedCharN = '1234567#b+-'
    allowedCharA = 'abcdefgABCDEFG#b+-'
    if (noteFormat == 'N') :
        allowedChar = allowedCharN
    else :
        allowedChar = allowedCharA
    # end if
    for c in oneNote :
        if (not(c in allowedChar)) :
            # error
            return(-1)
        # end if
    # end for    
    
    # Octave
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

    if (noteFormat == 'N') :
        return(Dict_Notes[note1] + octaveInc)
    else :
        return(Dict_Notes_Alpha[note1.upper()] + octaveInc)
    # end if
# end def Calc_Note()
#
def Calc_MusicInterval( prevNote, curNote, noteFormat ) :
    """ Calculate the musical interval between notes
    
    Inputs:
        prevNote   : previous musical note (text format), e.g. "-5#"
        curNote    : current musical note (text format)
        noteFormat : 'N' for numeric, 'A' for alphabetic
    Output:
        a string describing the intervals in musical terms and number of semitones ("P5(7)")
    """
    note1 = Calc_Note(prevNote, noteFormat)
    note2 = Calc_Note(curNote, noteFormat)
    if (note2 == -1) :
        return('ERR/旋律格式有問題')
    # end if
    
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


def Gen_YiuRemark ( prevWordInfo, curWordInfo, code, mInterval, yKey, remarkCnt ) :
    """ Generate a remark string per theory of Yiu(2014)
    
    Inputs:
        curWordInfo  : list containing information of the current word
        prevWordInfo : list containing information of the previous word
        code         : return code from Calc_YiuResult()
        mInterval    : interval based on melody (string format, e.g. 5/P4)
        yKey         : key for indexing into YiuInterval dict()
        remarkCnt    : total count of remark up to now
    Note on inputs:
        Both arguments "curWordInfo" and "prevWordInfo" have the format
            [word(s), jyutping(s), melody(s), duration(s), tone(i), rest(b)]
    Output:
        remarkItem : item to insert into RemarkList 
    """
    # PREV_REST_VAL           = 0x100
    # SAME_TARGET_DIFF_NOTE   = 0x01
    # DIFF_TARGET_SAME_NOTE   = 0x02
    # IN_YIU_RANGE            = 0x04
    # OUT_YIU_RANGE           = 0x08 

    # <td width=n%>  #         </td>        <!-- Remark idx (0) : rowspan=2 -->
    # <td width=n%>            </td>        <!-- prev/cur -->
    # <td width=n%>  Word      </td>        <!-- word (1,4) -->
    # <td width=n%>  Tone      </td>        <!-- tone (2,5)-->
    # <td width=n%>  Melody    </td>        <!-- melody (3,6) -->
    # <td width=n%>  MI        </td>        <!-- melody interval (7) : rowspan=2 -->  
    # <td width=n%>  Prev Rest </td>        <!-- prevRest (8) : rowspan=2 -->  
    # <td width=20%> Ideal MI  </td>        <!-- ideal MI (9) : rowspan=2 -->  
    # <td>           Comment   </td>        <!-- remarks (10) : rowspan=2 -->  

    ToneList = ['', '(55)', '(35)', '(33)', '(21)', '(13)', '(22)']

    (curWord,  x1, curMelody,  x2, curTone,  x3)       = curWordInfo
    (prevWord, y1, prevMelody, y2, prevTone, prevRest) = prevWordInfo

    remarkCntStr = str(remarkCnt + 100)[1:]
    remarkItem   = [remarkCntStr]
    remarkItem.append(prevWord)
    remarkItem.append(str(prevTone) + ToneList[prevTone])
    remarkItem.append(prevMelody)
    remarkItem.append(curWord)
    remarkItem.append(str(curTone) + ToneList[curTone])
    remarkItem.append(curMelody)
    remarkItem.append(mInterval)
    if (prevRest == True) :
        remarkItem.append('Y')
    else :
        remarkItem.append('-')
    # end if
    
    YiuIntervalKeyList = list(YiuInterval.keys())
    if ((yKey == '') or (not(yKey in YiuIntervalKeyList))) :
        remarkItem.append('(n/a)')
    else :
        idealMI = str(YiuInterval[yKey][0])
        remarkItem.append(idealMI)
    # end if

    if (code & SAME_TARGET_DIFF_NOTE) :
        remarkStr = '<span class="mismatchSameTone"> Same target tone for the 2 words, but different notes </span>'
    elif (code & DIFF_TARGET_SAME_NOTE) :
        remarkStr = '<span class="mismatchSameNote"> Same note for the 2 words, but different target tones </span>'
    elif (code & IN_YIU_RANGE) :
        remarkStr = '<span class="halfMatch"> Mismatch of MI and target tone for the 2 words, yet MI is within max and min limits </span>'
    elif (code & OUT_YIU_RANGE) :
        remarkStr = '<span class="noMatch"> Mismatch of MI and target tone for the 2 words </span>'
    # end if
    if (code & PREV_REST_VAL) :
        remarkStr += ' <br> but word preceded by rest'
    # end if
    remarkItem.append(remarkStr)

    return(remarkItem)
# end def Gen_YiuRemark()
#
def Calc_YiuResult( curWordInfo, prevWordInfo, mInterval, remarkList ) :
    """ Calculate the interval between notes, based on tones and intervals suggested by Suki Yiu 2013/2014
    
    Inputs:
        curWordInfo  : list containing information of the current word
        prevWordInfo : list containing information of the previous word
        mInterval    : interval based on melody (string format, e.g. 5/P4)
        remarkList   : list of table of remarks
    Note on inputs:
        Both arguments "curWordInfo" and "prevWordInfo" have the format
            [word(s), jyutping(s), melody(s), duration(s), tone(i), rest(b)]
    Output:
        (retCode, result)
            retCode = a numeric value representing the condition for match (0) and mismatch (>0)
            result  = a string for inserting in HTML table
    """
    CHECK_CHAR = '&#x2713'
    targetMap  = [0, 5, 5, 3, 1, 3, 2]
    returnCode = 0

    (curWord,  x1, curMelody,  x2, curTone,  x3)       = curWordInfo
    (prevWord, y1, prevMelody, y2, prevTone, prevRest) = prevWordInfo
    
    prevTarget = targetMap[prevTone]
    curTarget  = targetMap[curTone]
    if (prevTarget > curTarget) :
        higherTarget = prevTarget
        lowerTarget  = curTarget
    else :
        higherTarget = curTarget
        lowerTarget  = prevTarget
    # end if
    #x WriteLog("higherTarget = " + str(higherTarget) + ", lowerTarget = " + str(lowerTarget))
    yKey = str(higherTarget) + str(lowerTarget)

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
        if (prevRest == True) :
            retCode = SAME_TARGET_DIFF_NOTE + PREV_REST_VAL
            result  = '<span class="mismatchSameTone tooltip"> (sT-p) <span class="tooltiptext"> Same TT diff note after rest </span> </span>'
        else :
            retCode = SAME_TARGET_DIFF_NOTE
            result  = '<span class="mismatchSameTone tooltip"> (sT) <span class="tooltiptext"> Same TT diff note </span> </span>'
        # end if
    #
    elif ((higherTarget != lowerTarget) and (mInterval == '0/U')) :
        # same note, different target
        if (prevRest == True) :
            retCode = DIFF_TARGET_SAME_NOTE + PREV_REST_VAL
            result  = '<span class="mismatchSameNote tooltip"> (sN-p) <span class="tooltiptext"> Same note diff TT after rest </span> </span>'
        else :
            retCode = DIFF_TARGET_SAME_NOTE
            result  = '<span class="mismatchSameNote tooltip"> (sN) <span class="tooltiptext"> Same note diff TT after rest </span> </span>'
        # end if
    #
    else :
        yValue        = YiuInterval[yKey]
        ySemitoneList = yValue[1]
        mSemitones    = int(mInterval[0])
        if (mSemitones in ySemitoneList) :
            # match one of the defined values
            retCode = 0
            result  = CHECK_CHAR
        elif ((mSemitones >= ySemitoneList[0]) and (mSemitones <= ySemitoneList[-1])) :
            # does not match exactly the values given in Yiu, but is within the range
            if (prevRest == True) :
                retCode = IN_YIU_RANGE + PREV_REST_VAL
                result  = '<span class="halfMatch tooltip"> (I-p) <span class="tooltiptext"> Non-match within intvl after rest </span> </span>'
            else :
                retCode = IN_YIU_RANGE
                result  = '<span class="halfMatch tooltip"> (I) <span class="tooltiptext"> Non-match within intvl </span> </span>'
            # end if
        else :
            if (prevRest == True) :
                retCode = OUT_YIU_RANGE + PREV_REST_VAL
                result  = '<span class="noMatch tooltip"> (X-p) <span class="tooltiptext"> Non-match after rest </span> </span>'
            else :
                retCode = OUT_YIU_RANGE
                result  = '<span class="noMatch tooltip"> (X) <span class="tooltiptext"> Non-match after rest </span> </span>'
        # end if
    # end if

    if (retCode != 0) :
        remarkCnt  = len(remarkList) + 1
        supText    = ' <sup> ' + str(remarkCnt+100)[1:] + ' </sup> '
        result    += supText
        WriteLog('new remark count = ' + str(remarkCnt))
        #
        remarkItem = Gen_YiuRemark(prevWordInfo, curWordInfo, retCode, mInterval, yKey, remarkCnt)
        remarkList.append(remarkItem)
    # end if

    return(retCode, result)
# end def Calc_YiuResult()

