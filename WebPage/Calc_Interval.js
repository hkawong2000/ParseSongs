// Associative array for note mapping
const Dict_Notes = {
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

// List of interval names
// ref: https://en.wikipedia.org/wiki/Interval_(music)
const List_Interval = [
    "U",        // 0 - unison
    "m2",
    "M2",
    "m3",
    "M3",       // 4
    "P4",
    "A4",
    "P5",
    "m6",       // 8
    "M6",
    "m7",
    "M7",
    "P8"        // 12
]

// Associative array of Interval for TTT per Yiu 2014 paper
const YiuInterval = {
    // key : concatenatio of higherTarget & lowerTarget
    // value : [[list of intervals per Yiu], [list of number of semitones per Yiu]]
    "53" : [["M2", "M3"],            [2, 4]],
    "52" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "51" : [["P5", "M6", "m7", "O"], [7, 9, 10, 12]],
    "32" : [["m2", "m3"],            [1, 3]],
    "31" : [["m3", "P4", "m6"],      [3, 5, 8]],
    "21" : [["M2", "M3"],            [2, 4]],
}

// Return codes for Calc_YiuResult()
const   PREV_REST_VAL           = 0x0100;
const   SAME_TARGET_DIFF_NOTE   = 0x0001;
const   DIFF_TARGET_SAME_NOTE   = 0x0002;
const   IN_YIU_RANGE            = 0x0004;
const   OUT_YIU_RANGE           = 0x0008;

// Remarks for (partial-)mismatches
RemarkCount = 0
RemarkList  = [];

// =============================================================

function Calc_Note(oneNote)
    // Return a numeric value of a note for interval calculation, with "-1" as -12, "-2' as -10, "1" as 0, ...
    // 
    // Inputs:
    //     oneNote : current musical note (text format) (e.g "-1s")
    // Output:
    //     numeric value of a note for interval calculation
{
    var         note1, octaveInc, noteVal, result;

    if (oneNote[0] == '-')
    {
        note1     = oneNote.substring(1,);
        octaveInc = -12;
    }
    else if (oneNote[0] == '+')
    {
        note1     = oneNote.substring(1,);
        octaveInc = 12;
    }
    else
    {
        note1     = oneNote;
        octaveInc = 0;
    }
    noteVal = Dict_Notes[note1];
    result  = noteVal + octaveInc;
    // console.log("  note1     = " + note1     + ' ' + (typeof note1));
    // console.log("  octaveInc = " + octaveInc + ' ' + (typeof octaveInc));
    // console.log("  noteVal   = " + noteVal   + ' ' + (typeof noteVal));
    // console.log("  result    = " + result    + ' ' + (typeof result));
    return(result);
}


function Calc_MusicInterval(prevNote, curNote)
    // Calculate the musical interval between notes
    // 
    // Inputs:
    //     prevNote : previous musical note (text format), e.g. "-5#"
    //     curNote  : current musical note (text format)
    // Output:
    //     a string describing the intervals in mucical terms and number of semitones ("P5(7)")
    // NOTE:
    //     global PrevNote will be used
{
    note1    = Calc_Note(prevNote);
    note2    = Calc_Note(curNote);
    // console.log("note1 = " + note1);
    // console.log("note2 = " + note2);
    noteDiff = Math.abs(note1 - note2);
    if (noteDiff == 0)
    {
        outStr = '0/U';
    }
    else if (noteDiff > 12)
    {
        outStr = noteDiff + '/P8+';
    }
    else
    {
        outStr = noteDiff + '/' + List_Interval[noteDiff];
    }
    return(outStr);
}


function Calc_YiuResult(prevTone, curTone, mInterval, prevRest)
    // Calculate the interval between notes, based on tones and intervals suggested by Suki Yiu 2013/2014
    // 
    // Inputs:
    //     prevTone  : tone of previous word (numeric format, 1 to 6)
    //     curTone   : tone of current word (numeric format, 1 to 6)
    //     mInterval : interval based on melody (string format, e.g. 5/P4)
    //     prevRest  : previous note is rest note (true/false)
    // Output:
    //     [retCode, yKey, result]
    //         retCode = a numeric value representing the condition for match (0) and mismach (>0)
    //         yKey    = key for indexing into YiuInterval dict()
    //         result  = a string for inserting in HTML table
{
    CHECK_CHAR = '\u2713';
    targetMap  = [0, 5, 5, 3, 1, 3, 2];
    returnCode = 0;
    yKey       = '';
    
    prevTarget = targetMap[prevTone];
    curTarget  = targetMap[curTone];
    console.log('prevTarget = ' + prevTarget + ', type = ' + typeof prevTarget);
    if (prevTarget > curTarget)
    {
        higherTarget = prevTarget;
        lowerTarget  = curTarget;
    }
    else
    {
        higherTarget = curTarget;
        lowerTarget  = prevTarget;
    }
    // console.log("higherTarget = " + higherTarget + ", lowerTarget = " + lowerTarget);

    if ((higherTarget == 0) || (lowerTarget == 0))
    {
        retCode = 0;
        result  = '-';
    }
    else if ((higherTarget == lowerTarget) && (mInterval == '0/U'))
    {
        retCode = 0;
        result  = '(s)';
    }
    else if ((higherTarget == lowerTarget) && (mInterval != '0/U'))
    {
        // same target, different note
        if (PrevRest == true)
        {
            retCode = SAME_TARGET_DIFF_NOTE + PREV_REST_VAL;
            result  = '<span class="mismatchSameTone tooltip"> (sT-p) <span class="tooltiptext"> Same TT diff note after rest </span> </span>';
        }
        else
        {
            retCode = SAME_TARGET_DIFF_NOTE;
            result  = '<span class="mismatchSameTone tooltip"> (sT) <span class="tooltiptext"> Same TT diff note </span> </span>';
        }
    }
    else if ((higherTarget != lowerTarget) && (mInterval == '0/U'))
    {
        // same note, different target
        yKey = str(higherTarget) + str(lowerTarget);
        if (PrevRest == true)
        {
            retCode = DIFF_TARGET_SAME_NOTE + PREV_REST_VAL;
            result  = '<span class="mismatchSameNote tooltip"> (sN-p) <span class="tooltiptext"> Same note diff TT after rest </span> </span>';
        }
        else
        {
            retCode = DIFF_TARGET_SAME_NOTE;
            result = '<span class="mismatchSameNote tooltip"> (sN) <span class="tooltiptext"> Same note diff TT after rest </span> </span>';
        }
    }
    else
    {
        yKey          = higherTarget.toString() + lowerTarget.toString(); 
        yValue        = YiuInterval[yKey];
        ySemitoneList = yValue[1];
        mSemitones    = parseInt(mInterval[0]);
        if (ySemitoneList.includes(mSemitones))
        {
            // match one of the defined values
            retCode = 0;
            result  = CHECK_CHAR;
        }
        else if ((mSemitones >= ySemitoneList[0]) && (mSemitones <= ySemitoneList[-1]))
        {
            // does not match exactly the values given in Yiu, but is within the range
            if (prevRest == true)
            {
                retCode = IN_YIU_RANGE + PREV_REST_VAL;
                result  = '<span class="halfMatch tooltip"> (I-p) <span class="tooltiptext"> Non-match within intvl after rest </span> </span>';
            }
            else
            {
                retCode = IN_YIU_RANGE;
                result  = '<span class="halfMatch tooltip"> (I) <span class="tooltiptext"> Non-match within intvl </span> </span>';
            }
        }
        else
        {
            if (prevRest == true)
            {
                retCode = OUT_YIU_RANGE + PREV_REST_VAL;
                result  = '<span class="noMatch tooltip"> (X-p) <span class="tooltiptext"> Non-match after rest </span> </span>';
            }
            else
            {
                retCode = OUT_YIU_RANGE;
                result  = '<span class="noMatch tooltip"> (X) <span class="tooltiptext"> Non-match after rest </span> </span>';
            }
        }
    }
    console.log('retCode = ' + retCode);
    return([retCode, yKey, result]);
}


function TempTest1(inStr)
{
    alert('TempTest1() : ' + inStr);
}


if (1) 
{
    console.log('Code running from "Temp_Interval.js"');
    //
    // Calc_YiuResult(prevTone, curTone, mInterval, prevRest)
    result1 = Calc_YiuResult(1, 4, '7/P5', false);
    console.log('result1 = ' + result1)
    console.log("Calc_MusicInterval " + Calc_MusicInterval("-5", "2"));
}


alert('Calc_Interval.js imported');
