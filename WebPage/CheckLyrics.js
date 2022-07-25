// global variables
var inputFileSet  = false;
var inputFile     = null;
var resultContent = ''
var resultHeader1 = '<html>\n\n<head>\n\n<meta charset="utf-8">\n'
var resultHeader2 = '<title> Result </title>\n'
var resultHeader3 = '<link type="text/css" rel="stylesheet" href="./CheckLyrics.css">\n'
var resultHeader4 = '</head>\n'
var resultHeader5 = '<body>\n\n<h1> Result </h1>\n'
var resultFooter  = '\n</body>\n\n</html>\n\n'


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
        // resultContent += ('<p style="font-family: monospace;">' + outStr + '\n');
        resultContent += ('<p class="testResult">' + outStr + '\n');
    }
}


function WriteResult()
{
    alert('WriteResult() called');
    console.log('WriteResult() called');
    resultWin = window.open();
    resultWin.document.write(resultHeader1);
    resultWin.document.write(resultHeader2);
    resultWin.document.write(resultHeader3);
    resultWin.document.write(resultHeader4);
    resultWin.document.write(resultHeader5);
    resultWin.document.write(resultContent);
    resultWin.document.write(resultFooter);
    alert('WriteResult() finished');
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
    alert('Check parameters 1 & 3');
    if (inputFileSet == true)
    {
        console.log(`File name: ${inputFile.name}`);
        myReader = new FileReader();
        myReader.readAsText(inputFile);

        myReader.onload = function() {
            var contentAll   = myReader.result;
            var contentLines = contentAll.split(/\r\n/);
            outStr = 'Number of lines in input file = ' + contentLines.length;
            console.log(outStr);
            for (let i = 0; i < contentLines.length; i++)
            {
                oneLine = contentLines[i];
                ProcessInputLine(i, oneLine);
            }
            WriteResult();
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
    
    console.log('Process_CheckLyrics() end')
}

console.log('CheckLyrics.js V3 loaded')
