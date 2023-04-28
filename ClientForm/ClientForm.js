// Global Variables

const   ExtLookupWebAdr = "https://humanum.arts.cuhk.edu.hk//Lexis/lexi-can/";
var     UserInputList = [];

// =====================================================================

function OpenForm()
    // event handler for "Create input file" button
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    console.log('OpenForm() called');
    document.getElementById("inputForm2").style.display   = "block";
    document.getElementById("inputForm1").style.display   = "none";
    document.getElementById("createButton").style.display = "none";
    document.getElementById("wordEntryHeader").innerHTML  = "Hello";
}


function LoadFile(input)
    // event handler for "Load file" button
    //
    // Inputs
    //     input : parameter passed from HTML
    // Outputs
    //     (none)
{
    console.log('LoadFile() called');
    inputFile     = input.files[0];
    inputFileName = inputFile.name;
    console.log('inputFileName = "' + inputFileName);
    //
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
    myReader = new FileReader();
    myReader.readAsText(inputFile);

    myReader.onload = function() {
        var contentAll   = myReader.result;
        var contentLines = contentAll.split(/\r\n/);
        outStr = 'Number of lines in input file = ' + contentLines.length;
        console.log(outStr);
        /*
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
        */
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


function ExtLookup()
// event handler for "Lookup" button (Jyutping item)
//
// Inputs
//     (none)
// Outputs
//     (none)
{
    window.open(ExtLookupWebAdr, "_blank");
}


function GoPrev()
    // event handler for "Prev" button
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    console.log('GoPrev() called');
}


function GoNext()
    // event handler for "Next" button
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    console.log('GoNext() called');
}


function CloseForm()
    // event handler for "Create input file" button
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    console.log('CloseForm() called');
    document.getElementById("inputForm2").style.display   = "none";
    document.getElementById("inputForm1").style.display   = "block";
    document.getElementById("createButton").style.display = "block";
}

// =============================================================================

// Comment the following lines when no input form is there
document.getElementById("inputForm2").style.display = "none";
// document.getElementById("createButton").style.display = "none";

console.log('ClientForm.js loaded')

