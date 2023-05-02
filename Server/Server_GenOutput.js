// noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intTone]
// [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TONE_VAL, IDX_TONE_CODE]
const IDX_CHI       = 0;
const IDX_JP        = 1;
const IDX_TNUM      = 2;
const IDX_NOTE      = 3;
const IDX_BEAT      = 4;
const IDX_WIDTH     = 5;
const IDX_MINT      = 6;
const IDX_TONE_VAL  = 7;
const IDX_TONE_CODE = 8; 

const CHECK_CHAR = '\u2713';

const HeaderCellStart  = '    <td class="tdExt" width=10%>\n      <table class="tableInt" width=100%>\n'
const WordHdr          = '        <tr>\n          <td class="tdInt wd"> 字 </td>\n        </tr>\n';
const JyutPingHdr      = '        <tr>\n          <td class="tdInt tn"> 粵拼 </td>\n        </tr>\n';
const MelodyHdr        = '        <tr>\n          <td class="tdInt ml"> &#x1D160; </td>\n        </tr>\n';
const MusicIntervalHdr = '        <tr>\n          <td class="tdInt in"> Int-Melody </td>\n        </tr>\n';
const ToneIntervalHdr  = '        <tr>\n          <td class="tdInt ti"> Int-Tone </td>\n        </tr>\n';
const HeaderCellEnd    = '      </table>\n    </td>\n'
const Column_Hdr       =   HeaderCellStart + WordHdr + JyutPingHdr + MelodyHdr + MusicIntervalHdr + ToneIntervalHdr + HeaderCellEnd;


// =============================================================

function GenOutputTable ( OutputList, barsPerLine )
    // Function to process LineContentList, which contains data read from input file
    // 
    // Inputs
    //     OutputList  : List of processed lines for output
    //     barsPerLine : number of bars per line
    // Outputs
    //     (none)
{
    var         j;
    var         m, n;
    var         barState = false;       // true if inside bar
    var         barCount = 0;           // count of bars
    var         resBody  = '';

    console.log('GenOutputTable() called');
    resBody = '';
    
    // Table
    rowStr   = '\n<table width=95%>\n'
    resBody += rowStr
    
    // Write table content lines
    numNotes = OutputList.length;
    console.log('numNotes = ' + numNotes);
    //
    barWidth    = (90 / barsPerLine);
    barStartTxt = '    <td class="tdExt" width=' + barWidth.toString() +'%>\n';
    //x console.log('barStartTxt = ' + barStartTxt);
    //
    for (j = 0; j < numNotes; j++)
    {
        // noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intToneVal, intToneCode]
        // [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TONE_VAL, IDX_TONE_CODE]      
        oneNote = OutputList[j];
        outStr0 = 'j = ' + j + ' : [' + oneNote + ']'
        console.log(outStr0);
        //
        chiWord     = oneNote[IDX_CHI];
        jyutping    = oneNote[IDX_JP];
        noteMelody  = oneNote[IDX_NOTE];
        noteWidth   = oneNote[IDX_WIDTH];
        intMelody   = oneNote[IDX_MINT];
        intToneCode = oneNote[IDX_TONE_CODE];
        //
        if (barCount == 0)
        {
            lineHtml  = '  <tr>  <!-- row begin -->\n';
            lineHtml += Column_Hdr;
        }
        if (barState == false)
        {
            barState     = true;
            trStartTxt   = '        <tr>\n'
            wordRow      = trStartTxt;
            jyutPingRow  = trStartTxt;
            melodyRow    = trStartTxt;
            intMelodyRow = trStartTxt;
            intToneRow   = trStartTxt; 
        }
        if (chiWord != '(bar)')
        {
            wordStartTxt       = '          <td class="tdInt wd" width=' + noteWidth.toString() +'%>';
            wordRow           += (wordStartTxt      + chiWord     + '</td>\n');
            jyutPingStartTxt   = '          <td class="tdInt jp" width=' + noteWidth.toString() +'%>';
            jyutPingRow       += (jyutPingStartTxt  + jyutping    + '</td>\n');
            melodyStartTxt     = '          <td class="tdInt me" width=' + noteWidth.toString() +'%>';
            melodyRow         += (melodyStartTxt    + noteMelody  + '</td>\n');
            intMelodyStartTxt  = '          <td class="tdInt mi" width=' + noteWidth.toString() +'%>';
            intMelodyRow      += (intMelodyStartTxt + intMelody   + '</td>\n');
            intToneStartTxt    = '          <td class="tdInt ti" width=' + noteWidth.toString() +'%>';
            intToneRow        += (intToneStartTxt   + intToneCode + '</td>\n');
        }
        else
        {
            // end of bar, flush output to barHtml
            console.log('* end of bar, wordRow = ' + wordRow);
            rowEndTxt  = '        </tr>\n';
            barHtml    = barStartTxt;
            barHtml   += '      <table class="tableInt" width=100%>\n';
            barHtml   += wordRow      + rowEndTxt;
            barHtml   += jyutPingRow  + rowEndTxt;
            barHtml   += melodyRow    + rowEndTxt;
            barHtml   += intMelodyRow + rowEndTxt;
            barHtml   += intToneRow   + rowEndTxt;
            barHtml   += '      </table> <!-- tableInt -->\n';
            barHtml   += '    </td>\n';
            console.log('barHtml = ' + barHtml);
            //
            barState  = false;
            barCount += 1;
            lineHtml += barHtml;
            if (barCount == barsPerLine)
            {
                console.log('* * end of line');
                lineHtml += '  </tr> <!-- row -->\n';
                resBody  += lineHtml;
                barCount  = 0;
            }
        }
    }
    
    // Wrap up table and document
    resBody += '\n</table>\n\n<p>&nbsp;\n\n';
    console.log('ProcessData() finished');
    console.log(resBody);
    return(resBody);
}

module.exports = { GenOutputTable };
console.log('Server_GenOutput.js imported');

