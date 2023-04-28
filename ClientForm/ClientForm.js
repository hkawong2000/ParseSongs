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


function LoadFile()
    // event handler for "Load file" button
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    console.log('LoadFile() called');
    //
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
    // inputFile = document.getElementById("loadFile").files[0];
    // console.log('inputFile : '+ inputFile);
    //
    // myReader = new FileReader();
    // myReader.readAsText(inputFile);
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

