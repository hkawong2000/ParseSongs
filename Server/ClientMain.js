// Global Variables

//x import axios from 'axios';

// =====================================================================

const form1 = document.getElementById('inputForm1');
form1.addEventListener('submit', handleSubmit);


/*
// Ref: https://www.w3schools.com/js/js_promise.asp
function myDisplayer(sRsp) {
  console.log('MyDisplayer() called');
  console.log(sRsp);
  // document.getElementById("demo").innerHTML = some;
}
*/


async function postData1(url, data) 
  // Ref-1: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
  // Ref-2: https://stackoverflow.com/questions/40385133/retrieve-data-from-a-readablestream-object
{
  fetch(url, {method: 'POST', body: data,})
  .then(function(response) {
    return response.text();
  }).then(function(data) {
    console.log('fetch response data = {\n' + data + '\n}'); // this will be a string
    document.getElementById("myBody").innerHTML = data;
  })
}


// @param {Event} event
function handleSubmit(event) 
{
    var SongName;
    var BeatsPerBar;
    var BarsPerLine;
    
    console.log('handleSubmit() called');
    event.preventDefault();

    SongName = document.getElementById("songName").value;
    outStr1  = 'Song name = ' + SongName;
    console.log(outStr1);
    BeatsPerBar = document.getElementById("beatsPerBar").value;
    outStr2  = 'Beats per bar = ' + BeatsPerBar;
    console.log(outStr2);
    BarsPerLine = document.getElementById("barsPerLine").value;
    outStr3  = 'Bars per Line = ' + BarsPerLine;
    console.log(outStr3);
    SongFile = document.getElementById("inputFile").value;
    outStr4  = 'input file = ' + SongFile;
    console.log(outStr4);
    if (SongFile == '')
    {
        alert('Please select input file and press START again');
        return;
    }

    // ????
    // SaveFilePath();          

    // Ref: https://austingil.com/upload-files-with-javascript/
    const form = event.currentTarget;
    const url = new URL(form.action);
    const formData = new FormData(form);

    /*
    const fetchOptions = {
      method: form.method,
      body: formData,
    };
    console.log('fetchOptions = '+ JSON.stringify(fetchOptions));
    */

    /*
    if (0)
    {
      console.log('No Promise used');
      fetch(url, fetchOptions);
    }
    else
    {
      postData1(url, formData);
    }
    */
    postData1(url, formData);

    event.preventDefault();
}


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
    // resultButton.disabled = true;
    // melodyButton.disabled = true;
}


//  function SubmitForm(event)
//      // Submit the fields on the "inputForm1" form
//      //
//      // Inputs
//      //     (none)
//      // Outputs
//      //     (none)
//  {
//      var SongName;
//      var BeatsPerBar;
//      var BarsPerLine;
//      var SongFile;
//      
//      console.log('SubmitForm() called');
//      
//      SongName = document.getElementById("songName").value;
//      outStr1  = 'Song name = ' + SongName;
//      console.log(outStr1);
//      BeatsPerBar = document.getElementById("beatsPerBar").value;
//      outStr2  = 'Beats per bar = ' + BeatsPerBar;
//      console.log(outStr2);
//      BarsPerLine = document.getElementById("barsPerLine").value;
//      outStr3  = 'Bars per Line = ' + BarsPerLine;
//      console.log(outStr3);
//      SongFile = document.getElementById("inputFile").value;
//      outStr4  = 'input file = ' + SongFile;
//      console.log(outStr4);
//      if (SongFile == '')
//      {
//          alert('Please select input file and press START again');
//          return;
//      }
//  
//      // https://austingil.com/upload-files-with-javascript/
//      // Likely the submit code needs to be changed a lot
//  
//      // SaveFilePath();
//  
//      document.getElementById("inputForm1").submit();
//  }

console.log('ClientMain.js loaded')
