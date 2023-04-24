// =============================================================
// Parse input song for "Check Lyrics" program
// =============================================================


var     LineContentList = [];
var     ErrList = [];

// Global variables for storing previous values
PrevRest   = false;
PrevWord   = '';
PrevTone   = 0;
PrevMelody = '';

const CalcInterval = require("./Server_CalcInterval");

// const IDX_CHI       = 0;
// const IDX_JP        = 1;
// const IDX_TNUM      = 2;
// const IDX_NOTE      = 3;
// const IDX_BEAT      = 4;
// const IDX_WIDTH     = 5;
// const IDX_MINT      = 6;
// const IDX_TONE_VAL  = 7;
// const IDX_TONE_CODE = 8; 


function ProcessInputLine(lineNum, curLine, beatsPerBar)
    // Function to process one input line
    //
    // Inputs
    //     lineNum     : line number
    //     curLine     : content of the line
    //     beatsPerBar : number of beats per bar, for calculating the width of one cell
    // Outputs
    //     (none)
{
    var         noteBeat;
    var         lineNumStr;

    lineNumStr = (lineNum + 1000).toString().slice(1,);
    //
    if (curLine.trim() == '')
    {
        outContent = 'Line ' + lineNumStr + ' : (empty line)';
    }
    else if (curLine[0] == '#')
    {
        outContent = 'Line ' + lineNumStr + ' : (comment line)';
    }
    else if (curLine.substring(0,3).toLowerCase() == 'bar')
    {
        // bar
        outContent = 'Line ' + lineNumStr + ' : bar line';
        //
        // Calculate whether there are enough beats ????????
        //
        noteArray = ['(bar)', '', 0, '', '', 0]
        LineContentList.push(noteArray);
        outContent = 'Line ' + lineNumStr + ' : noteArray = [' + noteArray.toString() + ']';
    }
    else if (curLine[0] == '@')
    {
        // Special debug directive not open to user
        // @A = ...
        // @B = ...
        // ...
    }
    else
    {
        lineContent = curLine.split(/\s+/);
        if (lineContent.length < 4)
        {
            errStr = 'ERROR: line ' + lineNumStr + ' does not have 4 entries'
            console.log(errStr);
            return
        }
        //
        chiWord    = lineContent[0];
        jyutping   = lineContent[1];
        noteMelody = lineContent[2];
        noteLength = lineContent[3];
        //
        m = jyutping.match(/[a-zA-Z]+([\d])/);
        if (m != null)
        {
            curTone = m[1];
            // console.log('chiWord = ' + chiWord + ', jyytping = ' + jyutping + ', curTone = ' + curTone);
        }
        else
        {
            curTone = 0;
        }
        //
        noteBeat = 0
        for (let c of noteLength)
        {
            c1 = c.toUpperCase();
            if (c1 == 'Q')
            {
                noteBeat += 0.25;
            }
            else if (c1 == 'T')
            {
                noteBeat += 0.33;
            }
            else if (c1 == 'H')
            {
                noteBeat += 0.5;
            }
            else
            {
                noteBeat += Number(c1);
            }             
        }
        noteWidth = noteBeat * 100 / beatsPerBar;
        //
        // Calculate melody interval
        if ((chiWord != '-') && (PrevWord != ''))
        {
            intMelody = CalcInterval.Calc_MusicInterval(PrevMelody, noteMelody);
            yiuResult = CalcInterval.Calc_YiuResult(chiWord, PrevTone, curTone, intMelody, PrevRest);
            // [retCode, yKey, result]
            retCode     = yiuResult[0];
            result      = yiuResult[1];
            intToneVal  = retCode;
            intToneCode = result;
            //x console.log('  > retCode = ' + retCode + ', result  = ' + result);
        }
        else
        {
            intMelody   = '-';
            intToneVal  = -1;
            intToneCode = '-'
        }
        //
        noteArray = [chiWord, jyutping, 0, noteMelody, noteBeat, noteWidth, intMelody, intToneVal, intToneCode];
        LineContentList.push(noteArray);
        outContent = 'Line ' + lineNumStr + ' : noteArray = [' + noteArray.toString() + ']';
        console.log(outContent);
        //
        // Store values to Prev... variables
        if (chiWord == '-')
        {
            PrevRest = true;
        }
        else
        {
            PrevRest   = false;
            PrevWord   = chiWord;
            PrevTone   = curTone;
            PrevMelody = noteMelody;
        }
    }
}


function ProcessInputLines ( lineList, beatsPerBar )
    // Function to process the complete set of lines from the input file
    //
    // Inputs
    //     lineList    : the lines from the input file, one per item
    //     beatsPerBar : number of beats per bar, for calculating the width of one cell
    // Outputs
    //     (none)
{
    var     oneLine;
    var     fileStart = false;
    var     lineNum   = 0;
  
    for (let i = 0; i < lineList.length; i++)
    {
        oneLine = lineList[i];
        newLine = oneLine.trim();
        if (newLine.length == 0)
        {
            continue;;
        }
        //
        if ((fileStart == false) && (oneLine[0] == '#'))
        {
            fileStart = true;
        }
        if (fileStart = true)
        {
            lineNum++;
            ProcessInputLine(lineNum, oneLine, beatsPerBar);
        }
    }
}


module.exports = { ProcessInputLines };
console.log('Server_ProcessLines.js imported');

