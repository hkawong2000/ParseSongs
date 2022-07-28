// Global Variables

var inputFileSet   = false;
var inputFile      = null;
var outputFileName = null;
//
const resultButton = document.getElementById("viewResult");

// Result texts
// - header
var resHdr1 = '<html>\n\n<head>\n\n<meta charset="utf-8">\n\n';                         // head-begin and charset
var resHdr2 = '<title> Result (to be changed !!!!) </title>\n\n';                       // page title
var resHdr3 = '<link type="text/css" rel="stylesheet" href="./CheckLyrics.css">\n\n';   // style sheet
var resHdr4 = '</head>\n\n';                                                            // head-end
// - body
var resBody1 = '<body>\n\n'                                                             // body-begin
var resBody2 = '<h1> Result (to be changed !!!!) </h1>\n';                              // body-header                                                   
var resBody  = '';
// - footer
var resFooter = '\n</body>\n\n</html>\n\n';

// For storing contents of lines
var LineContentList = new Array(200);


function SaveFilePath(input)
{
    inputFile      = input.files[0];
    inputFileSet   = true;
    inputFileName  = inputFile.name;
    outputFileName = inputFileName.replace('.txt', '_out.html');
    console.log('outputFileName = ' + outputFileName);
}
 

function ProcessInputLine(idx, curLine)
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
    outStr = 'Line ' + idxStr + ' : ' + curLine;
    console.log(outStr);
    //
    if ((idx % 5) == 0)
    {
        if (curLine.trim() == '')
        {
            outContent = '(empty line)';
        }
        else
        {
            lineContent = curLine.split(/\s+/);
            if (lineContent.length != 4)
            {
                outContent = 'ERROR: line ' + idx + ' does not have 4 entires'
            }
            else
            {
                outContent = lineContent.toString();
                LineContentList[idx] = outContent;
            }
        }
        resBody += ('<p class="testResult"> Line' + idx + ' : ' + outContent + '\n');
    }
}


function WriteResult()
{
    var     outputText;
    var     resHdrAll, resBodyAll;
    
    console.log('WriteResult() called');
    resultWin = window.open();
    
    // Result page header
    resHdrAll = resHdr1 + resHdr2 + resHdr3 + resHdr4;
    resultWin.document.write(resHdrAll);
    // Result page body
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
    link.href = window.URL.createObjectURL(blob);
    //x document.body.appendChild(link);
    
    // Blob for download
    saveStr = '<a download="' + outputFileName + '" href="' + link.toString() + '">Download File</a>';
    resultWin.document.write('<hr>');
    resultWin.document.write(saveStr);

    // Result page footer
    resultWin.document.write(resFooter);

    resultButton.disabled = true;
}


function Process_CheckLyrics ()
{
    var         oneLine;

    // alert("Process_CheckLyrics() called");
    songName = document.getElementById("songName").value;
    outStr1  = 'Song name = ' + songName;
    console.log(outStr1);
    minNoteDur = document.getElementById("minNoteDur").value;
    outStr3  = 'Min note duration = ' + minNoteDur;
    console.log(outStr3);
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
                ProcessInputLine(i, oneLine);
            }
            resultButton.disabled = false;
            // WriteResult();
            alert('Process_CheckLyrics() success');
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
