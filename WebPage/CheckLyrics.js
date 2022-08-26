// Global Variables

// Parameters from input form
var SongName;
var BeatsPerBar;
var MinNoteDur;
var BarsPerLine;

// Input and output files
var inputFile      = null;
var inputFileSet   = false;
var outputFileName = null;

// Buttons
const resultButton = document.getElementById("viewResult");

let StyleArray = [
    '<style>',
    '\n  table\n  {\n    table-layout: fixed;\n    border: 1px solid black;\n    border-collapse: collapse;\n  }',
    '\n  td\n  {\n    border: 1px solid black;\n  }',
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
var SubDivPerBeat  = 1;
var CellWidthNum   = 0;         // integer, as multiples of 0.1%
var HeaderWidthNum = 0;         // integer, as multiples of 0.1%


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
    if (idx < 10)
    {
        idxStr = '00' + idx;
    }
    else if (idx < 100)
    {
        idxStr = '0' + idx;
    }
    else
    {
        idxStr = '' + idx;
    }
    //
    if (curLine.trim() == '')
    {
        outContent = '(empty line)';
    }
    else if (curLine[0] == '#')
    {
        outContent = '(comment line)';
    }
    else if (curLine.substring(0,3).toLowerCase() == 'bar')
    {
        // bar
        outContent = 'bar line';
        //
        // Calculate whether there are enough beats ????????
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
            outContent = 'ERROR: line ' + idxStr + ' does not have 4 entries'
        }
        else
        {
            LineContentList.push(lineContent);
            outContent = lineContent.toString();
            //
            noteLength = lineContent[3];
            if (noteLength.includes('H'))
            {
                if ((SubDivPerBeat % 2) != 0)
                {
                    SubDivPerBeat *= 2;
                    //x console.log('New SubDivPerBeat = ' + SubDivPerBeat);
                }  
            }
            else if (noteLength.includes('Q'))
            {
                if ((SubDivPerBeat % 4) != 0)
                {
                    if ((SubDivPerBeat % 2) != 0)
                    {
                        SubDivPerBeat *= 4;
                        //x console.log('New SubDivPerBeat = ' + SubDivPerBeat);
                    }
                    else
                    {
                        SubDivPerBeat *= 2;
                        //x console.log('New SubDivPerBeat = ' + SubDivPerBeat);
                    }
                }  
            }
            else if (noteLength.includes('T'))
            {
                if ((SubDivPerBeat % 3) != 0)
                {
                    SubDivPerBeat *= 3;
                    //x console.log('New SubDivPerBeat = ' + SubDivPerBeat);
                }  
            }
        }
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
    resHdr2 = '<title> ' + SongName + ' </title>\n\n';      // song title
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


function CalcCellWidth ( noteLen )
    // Function to calculate the cell width for the required note length
    // 
    // Inputs
    //     noteLen : length of the note, one or two of the following character set ('Q', 'T', 'H', 1, 2, 3, 4)
    // Outputs
    //     cell width as a string (e.g. "1.23%")
{
    var     i;
    var     curChar      = '';
    var     curCharSpan  = 0;
    var     curCharWidth = 0;
    
    totalSpan = 0;
    strLen    = noteLen.length;
    for (i = 0; i < strLen; i++)
    {
        curChar = noteLen[i];
        if (Number.isInteger(Number(curChar)))
        {
            curCharSpan = parseInt(curChar) * SubDivPerBeat;
        }
        else
        {
            if (curChar == 'H')
            {
                curCharSpan = SubDivPerBeat / 2;
            }
            else if (curChar == 'T')
            {
                curCharSpan = SubDivPerBeat / 3;
            }
            else if (curChar == 'Q')
            {
                curCharSpan = SubDivPerBeat / 4;
            }
            else
            {
                alert('illegal noteLen ' + noteLen);
            }
        }
        totalSpan += curCharSpan;
    }    
    //
    finalCellWidth = '"' + (totalSpan * CellWidthNum / 10).toString() + '%"';    
    //x console.log('noteLen = ' + noteLen + ', finalCellWidth = ' + finalCellWidth);
    return(finalCellWidth);
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

    alert('ProcessData() called');
    
    // Table cell widths
    console.log('Final SubDivPerBeat = ' + SubDivPerBeat);
    DivPerLine     = SubDivPerBeat * BeatsPerBar * BarsPerLine;
    CellWidthNum   = Math.floor(900 / DivPerLine);
    HeaderWidthNum = 1000 - (DivPerLine * CellWidthNum);
    console.log('CellWidthNum = ' + CellWidthNum + ', HeaderWidthNum  = ' + HeaderWidthNum);
    
    // Table
    rowStr   = '\n<table width=95%>\n'
    resBody += rowStr
    
    // Write table header line
    totalCells = BeatsPerBar * BarsPerLine;
    if ((totalCells % 3) == 0)
    {
        cellsPerLine = 3;
    }
    else if ((totalCells % 4) == 0)
    {
        cellsPerLine = 4;
    }
    else
    {
        cellsPerLine = 2;
    }
    headerRowStr = '\n<tr class="tableHdr">\n  <td width=' + (HeaderWidthNum / 10).toString() + '%>'
    headerChar   = '&nbsp;';
    for (m = 0; m < totalCells; m += cellsPerLine)
    {
        for (n = 0; n < cellsPerLine; n++)
        {
            if (n == 0)
            {
                headerRowStr += '\n';
            }
            headerRowStr += '  <td width=' + (CellWidthNum / 10).toString() + '%>' + headerChar + '</td>';
        }
    }
    headerRowStr += '\n</tr>\n';
    resBody      += headerRowStr;
    
    // Write table content lines
    numNotes = LineContentList.length;
    console.log('numNotes = ' + numNotes);
    //x console.log(LineContentList);
    //
    for (j = 0; j < numNotes; j++)
    {
        oneNote = LineContentList[j];
        console.log('j = ' + j + ' : ' + oneNote);
        chiWord    = oneNote[0];
        jyutping   = oneNote[1];
        noteMelody = oneNote[2];
        noteLen    = oneNote[3];
        cellWidth  = CalcCellWidth(noteLen);
    }
    
    // Wrap up table and document
    resBody += '\n</table>\n\n<p>&nbsp;\n\n';
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
    MinNoteDur = document.getElementById("minNoteDur").value;
    outStr3  = 'Min note duration = ' + MinNoteDur;
    console.log(outStr3);
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
