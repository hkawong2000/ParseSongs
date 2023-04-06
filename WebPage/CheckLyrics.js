// Global Variables

// Parameters from input form
var SongName;
var BeatsPerBar;
var BarsPerLine;

// Input and output files
var inputFile      = null;
var inputFileSet   = false;
var outputFileName = null;

// Buttons
const resultButton = document.getElementById("viewResult");
const melodyButton = document.getElementById("playMelody");

let StyleArray = [
    '<style>',
    '\n  table\n  {\n    table-layout: fixed;\n    border: 1px solid black;\n    border-collapse: collapse;\n  }',
    '\n  tdExt\n  {\n    border: 1px solid black;\n  }',
    '\n  .tdInt\n  {\n    border: none;\n    table-layout: fixed;\n  }',
    '\n  label\n  {\n    display: inline-block;\n    width: 150px;\n  }',
    '\n  input\n  {\n    display: inline-block;\n    width: 250px;\n  }',
    '\n  select\n  {\n    display: inline-block;\n    width: 250px;\n  }',
    '\n  .testResult\n  {\n    font-family: monospace;\n  }',
    '\n</style>\n\n',
]

// Result texts
// - header
var resHdr1 = '<html>\n\n<head>\n\n<meta charset="utf-8">\n\n';                         // head-begin and charset
var resHdr2 = '';                                                                       // page title (to be generated)
var resHdr3 = '';                                                                       // style sheet (to be generated from StyleArray)
var resHdr4 = '</head>\n\n';                                                            // head-end
// - body
var resBody1 = '<body>\n\n'     // body-begin
var resBody2 = '';              // <h1> (to be generated)                                                 
var resBody  = '';
// - footer
var resFooter = '</body>\n\n</html>\n\n';

// For storing contents of lines
var LineContentList = new Array(0);
var ContentCnt      = 0

// For storing HTML body (table content mainly)
var BodyLines = new Array(0);

// Subdivisions per beat (for column width)
// var SubDivPerBeat  = 1;
var CellWidthNum   = 0;         // integer, as multiples of 0.1%
var HeaderWidthNum = 0;         // integer, as multiples of 0.1%

// noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intTone]
// [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TINT]
const IDX_CHI   = 0;
const IDX_JP    = 1;
const IDX_TN    = 2;
const IDX_NOTE  = 3;
const IDX_BEAT  = 4;
const IDX_WIDTH = 5;
const IDX_MINT  = 6;
const IDX_TINT  = 7;

const CHECK_CHAR = '\u2713';


// =====================================================================

function SaveFilePath(input)
    // Function to save input file and generate name for output file
    //
    // Inputs
    //     input : parameter passed from HTML
    // Outputs
    //     (none)
{
    inputFile      = input.files[0];
    inputFileSet   = true;
    inputFileName  = inputFile.name;
    outputFileName = inputFileName.replace('.txt', '_out.html');
    console.log('outputFileName = ' + outputFileName);
    resultButton.disabled = true;
    melodyButton.disabled = true;
}
 

function ProcessInputLine(idx, curLine)
    // Function to process one input line
    //
    // Inputs
    //     idx     : line number
    //     curLine : content of the line
    // Outputs
    //     (none)
{
    var         noteBeat;

    // if (idx < 10)
    // {
    //     idxStr = '00' + idx;
    // }
    // else if (idx < 100)
    // {
    //     idxStr = '0' + idx;
    // }
    // else
    // {
    //     idxStr = '' + idx;
    // }
    // //
    if (curLine.trim() == '')
    {
        outContent = 'Line ' + idx + ' : (empty line)';
    }
    else if (curLine[0] == '#')
    {
        outContent = 'Line ' + idx + ' : (comment line)';
    }
    else if (curLine.substring(0,3).toLowerCase() == 'bar')
    {
        // bar
        outContent = 'Line ' + idx + ' : bar line';
        //
        // Calculate whether there are enough beats ????????
        //
        noteArray = ['(bar)', '', 0, '', '', 0]
        LineContentList.push(noteArray);
        outContent = 'Line ' + idx + ' : noteArray = [' + noteArray.toString() + ']';
    }
    else if (curLine[0] == '@')
    {
        // Special debug directive not open to user - to be removed upon release of program
        // @A = ...
        // @B = ...
        // ...
    }
    else
    {
        lineContent = curLine.split(/\s+/);
        if (lineContent.length != 4)
        {
            errStr = 'ERROR: line ' + idx + ' does not have 4 entries'
            console.log(errStr);
            return
        }
        //
        chiWord    = lineContent[0];
        jyutping   = lineContent[1];
        noteMelody = lineContent[2];
        noteLength = lineContent[3];
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
        noteWidth = noteBeat * 100 / BeatsPerBar;
        //
        // Temp ????????
        intMelody = '0/U';
        intTone   = CHECK_CHAR;
        //
        noteArray = [chiWord, jyutping, 0, noteMelody, noteBeat, noteWidth, intMelody, intTone];
        LineContentList.push(noteArray);
        outContent = 'Line ' + idx + ' : noteArray = [' + noteArray.toString() + ']';
    }
    if (0)
    {
        console.log(outContent);
    }
}


function WriteResult()
    // Function to write result to output test page
    // 
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    var     i;
    var     outputText;
    var     resHdrAll, resBodyAll;
    
    console.log('WriteResult() called');
    resultWin = window.open();
    
    // Result page header
    resHdr2 = '<title> ' + SongName + ' (Generated output) </title>\n\n';      // song title
    resHdr3 = ''                                            // CSS styles
    for (i = 0; i < StyleArray.length; i++)
    {
        resHdr3 += StyleArray[i];
    }
    resHdrAll = resHdr1 + resHdr2 + resHdr3 + resHdr4;
    resultWin.document.write(resHdrAll);
    // Result page body
    resBody2 = '<h1> ' + SongName + ' </h1>\n';  
    resBodyAll = resBody1 + resBody2 + resBody;
    resultWin.document.write(resBodyAll);
    
    outputText = resHdrAll + resBodyAll + resFooter;

    // Save result in file
    // ref: https://stackoverflow.com/questions/32326973/file-write-operation-in-javascript
    var filename   = outputFileName;
    var text       = outputText;
    var blob       = new Blob([text], {type:'text/plain'});
    var link       = document.createElement("a");
    link.download  = filename;
    link.innerHTML = "Download File";
    link.href      = window.URL.createObjectURL(blob);
    //x document.body.appendChild(link);
    
    // Blob for download
    saveStr = '<a download="' + outputFileName + '" href="' + link.toString() + '">Download File</a>';
    resultWin.document.write('<hr>');
    resultWin.document.write(saveStr);

    // Result page footer
    resultWin.document.write(resFooter);

    resultButton.disabled = true;
}


function ProcessData ()
    // Function to process LineContentList, which contains data read from input file
    // 
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    var         j;
    var         m, n;
    var         barState = false;       // true if inside bar
    var         barCount = 0;           // count of bars

    alert('ProcessData() called');
    
    // Table
    rowStr   = '\n<table width=95%>\n'
    resBody += rowStr
    
    // Write table content lines
    numNotes = LineContentList.length;
    console.log('numNotes = ' + numNotes);
    //
    if (0)
    {
        // Fake line
        resBody += '\n<tr> <td width=50%>Temp row with 2 cells </td> <td>&nbsp; </td> </tr>\n'
    }
    //
    barWidth    = (100 / BarsPerLine);
    barStartTxt = '    <td width=' + barWidth.toString() +'%>\n';
    console.log('barStartTxt = ' + barStartTxt);
    //
    for (j = 0; j < numNotes; j++)
    {
        // noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intTone]
        // [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TINT]      
        oneNote = LineContentList[j];
        outStr0 = 'j = ' + j + ' : [' + oneNote + ']'
        console.log(outStr0);
        chiWord    = oneNote[IDX_CHI];
        jyutping   = oneNote[IDX_JP];
        noteMelody = oneNote[IDX_NOTE];
        noteWidth  = oneNote[IDX_WIDTH];
        intMelody  = oneNote[IDX_MINT];
        intTone    = oneNote[IDX_TINT];
        //
        if (barCount == 0)
        {
            lineHtml  = '  <tr>  <!-- row begin -->\n';
        }
        if (barState == false)
        {
            barState     = true;
            trStartTxt   = '        <tr>\n'
            wordRow      = trStartTxt;
            juytPingRow  = trStartTxt;
            melodyRow    = trStartTxt;
            intMelodyRow = trStartTxt;
            intToneRow   = trStartTxt; 
        }
        if (chiWord != '(bar)')
        {
            tdStartTxt    = '          <td width=' + noteWidth.toString() +'%>';
            wordRow      += (tdStartTxt + chiWord + '</td>\n');
            juytPingRow  += (tdStartTxt + jyutping + '</td>\n');
            melodyRow    += (tdStartTxt + noteMelody + '</td>\n');
            intMelodyRow += (tdStartTxt + intMelody + '</td>\n');
            intToneRow   += (tdStartTxt + intTone + '</td>\n');
        }
        else
        {
            // end of bar, flush output to barHtml
            // console.log('* end of bar, wordRow = ' + wordRow);
            console.log('* end of bar');
            rowEndTxt  = '        </tr>\n';
            barHtml    = barStartTxt;
            barHtml   += '      <table class="tableInt" width=100%>\n';
            barHtml   += wordRow      + rowEndTxt;
            barHtml   += juytPingRow  + rowEndTxt;
            barHtml   += melodyRow    + rowEndTxt;
            barHtml   += intMelodyRow + rowEndTxt;
            barHtml   += intToneRow   + rowEndTxt;
            barHtml   += '      </table> <!-- tableInt -->\n';
            barHtml   += '    </td>\n';
            //
            barState  = false;
            barCount += 1;
            lineHtml += barHtml;
            if (barCount == BarsPerLine)
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
    alert('ProcessData() finished');
    console.log(resBody);
}


function Process_CheckLyrics ()
{
    var         oneLine;

    // alert("Process_CheckLyrics() called");
    
    // Get parameters from input form
    SongName = document.getElementById("songName").value;
    outStr1  = 'Song name = ' + SongName;
    console.log(outStr1);
    BeatsPerBar = document.getElementById("beatsPerBar").value;
    outStr2  = 'Beats per bar = ' + BeatsPerBar;
    console.log(outStr2);
    // MinNoteDur = document.getElementById("minNoteDur").value;
    // outStr3  = 'Min note duration = ' + MinNoteDur;
    // console.log(outStr3);
    BarsPerLine = document.getElementById("barsPerLine").value;
    outStr4  = 'Bars per Line = ' + BarsPerLine;
    console.log(outStr4);
    //
    LineContentList = new Array(0);
    
    // Check input file
    if (inputFileSet == true)
    {
        console.log(`File name: ${inputFile.name}`);
        myReader = new FileReader();
        myReader.readAsText(inputFile);

        myReader.onload = function() {
            resBody = '';
            //
            var contentAll   = myReader.result;
            var contentLines = contentAll.split(/\r\n/);
            outStr = 'Number of lines in input file = ' + contentLines.length;
            console.log(outStr);
            for (let i = 0; i < contentLines.length; i++)
            {
                oneLine = contentLines[i];
                ProcessInputLine(i+1, oneLine);
            }
            //
            ProcessData()
            resultButton.disabled = false;
            melodyButton.disabled = false;
            alert('Process_CheckLyrics() success');
            myReader = null;
        };

        myReader.onerror = function() {
            alert('myReader error')
            alert(myReader.error.name);
            console.log('myReader error');
            console.log(myReader.error);
            console.log(myReader.error.name);
        };
    }
    else
    {
        alert('No input file specified')
    }
}

const myForm = document.querySelector('#inputForm');
//
myForm.addEventListener('submit', function(event){
    event.preventDefault();
    Process_CheckLyrics();
})

console.log('CheckLyrics.js loaded')
