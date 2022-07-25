// Global Variables

var inputFileSet = false;
var inputFile    = null;
//
const resultButton = document.getElementById("viewResult");
//
var resultContent = '';
var resultHeader1 = '<html>\n\n<head>\n\n<meta charset="utf-8">\n';
var resultHeader2 = '<title> Result </title>\n';
var resultHeader3 = '<link type="text/css" rel="stylesheet" href="./CheckLyrics.css">\n';
var resultHeader4 = '</head>\n';
var resultHeader5 = '<body>\n\n<h1> Result </h1>\n';
var resultFooter  = '\n</body>\n\n</html>\n\n';

var LineContentList = new Array(200);


function SaveFilePath(input)
{
    inputFile = input.files[0];
    inputFileSet = true;
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
        resultContent += ('<p class="testResult"> Line' + idx + ' : ' + outContent + '\n');
    }
}


function WriteResult()
{
    console.log('WriteResult() called');
    resultWin = window.open();
    resultWin.document.write(resultHeader1);
    resultWin.document.write(resultHeader2);
    resultWin.document.write(resultHeader3);
    resultWin.document.write(resultHeader4);
    resultWin.document.write(resultHeader5);
    resultWin.document.write(resultContent);
    resultWin.document.write(resultFooter);
    console.log('WriteResult() end');
    resultButton.disabled = true;
}


function Process_CheckLyrics ()
{
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
            resultContent    = ''
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
    // console.log('password field is ' + userPwd);
    // currentHref = window.location.href;
})

console.log('CheckLyrics.js loaded')
