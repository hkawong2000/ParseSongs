// Global Variables

// =====================================================================

const form1 = document.getElementById('inputForm1');
form1.addEventListener('submit', handleSubmit);


async function postData1(url, data) 
    // ASYNC function to send data to server
    //
    // Inputs
    //     url  : url for fetch request
    //     data : data to send
    // Outputs
    //     (none)
{
    // Ref-1: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
    // Ref-2: https://stackoverflow.com/questions/40385133/retrieve-data-from-a-readablestream-object

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
    // event handler for form submit
    //
    // Inputs
    //     event: system-generated event
    // Outputs
    //     (none)
{
    var SongFile;
    
    console.log('handleSubmit() called');
    event.preventDefault();

    if (0)
    {
        var SongName;
        var BeatsPerBar;
        var BarsPerLine;

        SongName = document.getElementById("songName").value;
        outStr1  = 'Song name = ' + SongName;
        console.log(outStr1);
        BeatsPerBar = document.getElementById("beatsPerBar").value;
        outStr2  = 'Beats per bar = ' + BeatsPerBar;
        console.log(outStr2);
        BarsPerLine = document.getElementById("barsPerLine").value;
        outStr3  = 'Bars per Line = ' + BarsPerLine;
        console.log(outStr3);
    }
    //
    SongFile = document.getElementById("inputFile").value;
    if (SongFile == '')
    {
        alert('Please select input file and press START again');
        return;
    }
    else
    {
        outStr4  = 'Song File ='+ SongFile;
        console.log(outStr4);
    }

    // Ref: https://austingil.com/upload-files-with-javascript/
    const form = event.currentTarget;
    const url = new URL(form.action);
    const formData = new FormData(form);
    postData1(url, formData);

    event.preventDefault();
}

