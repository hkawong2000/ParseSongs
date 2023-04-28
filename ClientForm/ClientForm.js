// Global Variables

const ExtLookupWebAdr = "https://humanum.arts.cuhk.edu.hk//Lexis/lexi-can/";

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


function ExtLookup()
    // event handler for "Lookup" button associated with the "Jyutping" item
    //
    // Inputs
    //     (none)
    // Outputs
    //     (none)
{
    window.open(ExtLookupWebAdr, "_blank");
}


// Comment the following lines when no input form is there
document.getElementById("inputForm2").style.display = "none";
// document.getElementById("createButton").style.display = "none";

console.log('ClientForm.js loaded')
