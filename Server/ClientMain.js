// Global Variables

//x import axios from 'axios';

//  // Parameters from input form
//  var SongName;
//  var BeatsPerBar;
//  var BarsPerLine;
//  
//  // Input and output files
//  var inputFile      = null;
//  var inputFileSet   = false;
//  var outputFileName = null;
//  
//  // Buttons
//  const resultButton = document.getElementById("viewResult");
//  const melodyButton = document.getElementById("playMelody");
//  
//  let StyleArray = [
//      '<style>',
//      '\n  table\n  {\n    table-layout: fixed;\n    border: 1px solid black;\n    border-collapse: collapse;\n  }',
//      '\n  .tdExt\n  {\n    border: 1px solid black;\n    border-collapse: collapse;\n  }',
//      '\n  .tdInt\n  {\n    border: 1px solid lightgrey;\n    table-layout: fixed;\n  }',
//      '\n  label\n  {\n    display: inline-block;\n    width: 150px;\n  }',
//      '\n  input\n  {\n    display: inline-block;\n    width: 250px;\n  }',
//      '\n  select\n  {\n    display: inline-block;\n    width: 250px;\n  }',
//      '\n  .testResult\n  {\n    font-family: monospace;\n  }',
//      '\n</style>\n\n',
//  ]
//  
//  // Result texts
//  // - header
//  var resHdr1 = '<html>\n\n<head>\n\n<meta charset="utf-8">\n\n';                         // head-begin and charset
//  var resHdr2 = '';                                                                       // page title (to be generated)
//  var resHdr3 = '';                                                                       // style sheet (to be generated from StyleArray)
//  var resHdr4 = '</head>\n\n';                                                            // head-end
//  // - body
//  var resBody1 = '<body>\n\n'     // body-begin
//  var resBody2 = '';              // <h1> (to be generated)                                                 
//  var resBody  = '';
//  // - footer
//  var resFooter = '</body>\n\n</html>\n\n';
//  
//  // For storing contents of lines
//  var LineContentList = new Array(0);
//  var ContentCnt      = 0
//  
//  // For storing HTML body (table content mainly)
//  var BodyLines = new Array(0);
//  
//  // Subdivisions per beat (for column width)
//  // var SubDivPerBeat  = 1;
//  var CellWidthNum   = 0;         // integer, as multiples of 0.1%
//  var HeaderWidthNum = 0;         // integer, as multiples of 0.1%
//  
//  // noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intTone]
//  // [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TINT]
//  const IDX_CHI   = 0;
//  const IDX_JP    = 1;
//  const IDX_TN    = 2;
//  const IDX_NOTE  = 3;
//  const IDX_BEAT  = 4;
//  const IDX_WIDTH = 5;
//  const IDX_MINT  = 6;
//  const IDX_TINT  = 7;
//  
//  const CHECK_CHAR = '\u2713';
//  
//  // Global variables
//  var PrevRest   = true;
//  var PrevWord   = '';
//  var PrevTone   = 0;
//  var PrevMelody = '';
//  
//  const HeaderCellStart  = '    <td class="tdExt" width=10%>\n      <table class="tableInt" width=100%>\n'
//  const WordHdr          = '        <tr>\n          <td class="tdInt wd rh"> 字 </td>\n        </tr>\n';
//  const JyutPingHdr      = '        <tr>\n          <td class="tdInt tn rh"> 粵拼 </td>\n        </tr>\n';
//  const MelodyHdr        = '        <tr>\n          <td class="tdInt ml rh"> &#x1D160; </td>\n        </tr>\n';
//  const MusicIntervalHdr = '        <tr>\n          <td class="tdInt in rh"> Int-Melody </td>\n        </tr>\n';
//  const ToneIntervalHdr  = '        <tr>\n          <td class="tdInt ti rh"> Int-Tone </td>\n        </tr>\n';
//  const HeaderCellEnd    = '      </table>\n    </td>\n'
//  const Column_Hdr       =   HeaderCellStart + WordHdr + JyutPingHdr + MelodyHdr + MusicIntervalHdr + ToneIntervalHdr + HeaderCellEnd;


// =====================================================================

const form1 = document.getElementById('inputForm1');
//x console.log('form1 = '+ form1);
form1.addEventListener('submit', handleSubmit);


// Ref: https://www.w3schools.com/js/js_promise.asp
function myDisplayer(sRsp) {
  console.log('MyDisplayer() called');
  console.log(sRsp);
  // document.getElementById("demo").innerHTML = some;
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
    // console.log('form1 = '+ JSON.stringify(form));
    const url = new URL(form.action);
    // console.log('url = '+ url);
    const formData = new FormData(form);
    // console.log('formData = '+ JSON.stringify(formData));

    // @type {Parameters<fetch>[1]}
    const fetchOptions = {
      method: form.method,
      body: formData,
    };
    console.log('fetchOptions = '+ JSON.stringify(fetchOptions));

    if (1)
    {
      console.log('No Promise used');
      fetch(url, fetchOptions);
    }
    else
    {
      console.log('Promise is used');
      let myPromise = new Promise(function(myResolve, myReject) {
        fetch(url, fetchOptions);
        // let req = new XMLHttpRequest();
        // req.open('GET', "mycar.htm");
        // req.onload = function() {
        //   if (req.status == 200) {
        //     myResolve(req.response);
        //   } else {
        //     myReject("File not Found");
        //   }
        // };
        // req.send();
      });

      myPromise.then(
        function(value) {myDisplayer(value);},
        function(error) {myDisplayer(error);}
      );
    }

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


//  function ProcessInputLine(idx, curLine)
//      // Function to process one input line
//      //
//      // Inputs
//      //     idx     : line number
//      //     curLine : content of the line
//      // Outputs
//      //     (none)
//  {
//      var         noteBeat;
//  
//      // if (idx < 10)
//      // {
//      //     idxStr = '00' + idx;
//      // }
//      // else if (idx < 100)
//      // {
//      //     idxStr = '0' + idx;
//      // }
//      // else
//      // {
//      //     idxStr = '' + idx;
//      // }
//      // //
//      if (curLine.trim() == '')
//      {
//          outContent = 'Line ' + idx + ' : (empty line)';
//      }
//      else if (curLine[0] == '#')
//      {
//          outContent = 'Line ' + idx + ' : (comment line)';
//      }
//      else if (curLine.substring(0,3).toLowerCase() == 'bar')
//      {
//          // bar
//          outContent = 'Line ' + idx + ' : bar line';
//          //
//          // Calculate whether there are enough beats ????????
//          //
//          noteArray = ['(bar)', '', 0, '', '', 0]
//          LineContentList.push(noteArray);
//          outContent = 'Line ' + idx + ' : noteArray = [' + noteArray.toString() + ']';
//      }
//      else if (curLine[0] == '@')
//      {
//          // Special debug directive not open to user - to be removed upon release of program
//          // @A = ...
//          // @B = ...
//          // ...
//      }
//      else
//      {
//          lineContent = curLine.split(/\s+/);
//          if (lineContent.length != 4)
//          {
//              errStr = 'ERROR: line ' + idx + ' does not have 4 entries'
//              console.log(errStr);
//              return
//          }
//          //
//          chiWord    = lineContent[0];
//          jyutping   = lineContent[1];
//          noteMelody = lineContent[2];
//          noteLength = lineContent[3];
//          //
//          // Check Jyutping tone validity
//          // curTone = GetToneNumber(jyutping);       ????????????????????????????
//          //     ???? and case when chiWord has no tone
//          curTone = jyutping.slice(-1,);
//          //
//          noteBeat = 0
//          for (let c of noteLength)
//          {
//              c1 = c.toUpperCase();
//              if (c1 == 'Q')
//              {
//                  noteBeat += 0.25;
//              }
//              else if (c1 == 'T')
//              {
//                  noteBeat += 0.33;
//              }
//              else if (c1 == 'H')
//              {
//                  noteBeat += 0.5;
//              }
//              else
//              {
//                  noteBeat += Number(c1);
//              }             
//          }
//          noteWidth = noteBeat * 100 / BeatsPerBar;
//          //
//          // Calculate melody interval
//          if ((chiWord != '-') && (PrevWord != ''))
//          {
//              intMelody = Calc_MusicInterval(PrevMelody, noteMelody);
//          }
//          else
//          {
//              intMelody = '-';
//          }
//          //        
//          // Temp ???????? (Calculate Yiu interval tones)
//          intTone   = CHECK_CHAR;
//          // intTone = Calc_YiuResult(PrevTone, curTone, intMelody, PrevRest);
//          //
//          noteArray = [chiWord, jyutping, 0, noteMelody, noteBeat, noteWidth, intMelody, intTone];
//          LineContentList.push(noteArray);
//          outContent = 'Line ' + idx + ' : noteArray = [' + noteArray.toString() + ']';
//          //
//          // Store values to Prev... variables
//          if (chiWord == '-')
//          {
//              PrevRest = true;
//          }
//          else
//          {
//              PrevRest   = false;
//              PrevWord   = chiWord;
//              PrevTone   = curTone;
//              PrevMelody = noteMelody;
//          }
//      }
//      if (0)
//      {
//          console.log(outContent);
//      }
//  }
//  
//  
//  function WriteResult()
//      // Function to write result to output test page
//      // 
//      // Inputs
//      //     (none)
//      // Outputs
//      //     (none)
//  {
//      var     i;
//      var     outputText;
//      var     resHdrAll, resBodyAll;
//      
//      console.log('WriteResult() called');
//      resultWin = window.open();
//      
//      // Result page header
//      resHdr2 = '<title> ' + SongName + ' (Generated output) </title>\n\n';      // song title
//      resHdr3 = ''                                            // CSS styles
//      for (i = 0; i < StyleArray.length; i++)
//      {
//          resHdr3 += StyleArray[i];
//      }
//      resHdrAll = resHdr1 + resHdr2 + resHdr3 + resHdr4;
//      resultWin.document.write(resHdrAll);
//      // Result page body
//      resBody2 = '<h1> ' + SongName + ' </h1>\n';  
//      resBodyAll = resBody1 + resBody2 + resBody;
//      resultWin.document.write(resBodyAll);
//      
//      outputText = resHdrAll + resBodyAll + resFooter;
//  
//      // Save result in file
//      // ref: https://stackoverflow.com/questions/32326973/file-write-operation-in-javascript
//      var filename   = outputFileName;
//      var text       = outputText;
//      var blob       = new Blob([text], {type:'text/plain'});
//      var link       = document.createElement("a");
//      link.download  = filename;
//      link.innerHTML = "Download File";
//      link.href      = window.URL.createObjectURL(blob);
//      //x document.body.appendChild(link);
//      
//      // Blob for download
//      saveStr = '<a download="' + outputFileName + '" href="' + link.toString() + '">Download File</a>';
//      resultWin.document.write('<hr>');
//      resultWin.document.write(saveStr);
//  
//      // Result page footer
//      resultWin.document.write(resFooter);
//  
//      resultButton.disabled = true;
//  }
//  
//  
//  function ProcessData ()
//      // Function to process LineContentList, which contains data read from input file
//      // 
//      // Inputs
//      //     (none)
//      // Outputs
//      //     (none)
//  {
//      var         j;
//      var         m, n;
//      var         barState = false;       // true if inside bar
//      var         barCount = 0;           // count of bars
//  
//      alert('ProcessData() called');
//      
//      // Table
//      rowStr   = '\n<table width=95%>\n'
//      resBody += rowStr
//      
//      // Write table content lines
//      numNotes = LineContentList.length;
//      console.log('numNotes = ' + numNotes);
//      //
//      barWidth    = (90 / BarsPerLine);
//      barStartTxt = '    <td class="tdExt" width=' + barWidth.toString() +'%>\n';
//      console.log('barStartTxt = ' + barStartTxt);
//      //
//      for (j = 0; j < numNotes; j++)
//      {
//          // noteArray = [chiWord, jyutping, 0, noteMelody, noteLength, noteWidth, intMelody, intTone]
//          // [IDX_CHI, IDX_JP, IDX_TNUM, IDX_NOTE, IDX_BEAT, IDX_WIDTH, IDX_MINT, IDX_TINT]      
//          oneNote = LineContentList[j];
//          outStr0 = 'j = ' + j + ' : [' + oneNote + ']'
//          console.log(outStr0);
//          chiWord    = oneNote[IDX_CHI];
//          jyutping   = oneNote[IDX_JP];
//          noteMelody = oneNote[IDX_NOTE];
//          noteWidth  = oneNote[IDX_WIDTH];
//          intMelody  = oneNote[IDX_MINT];
//          intTone    = oneNote[IDX_TINT];
//          //
//          if (barCount == 0)
//          {
//              lineHtml  = '  <tr>  <!-- row begin -->\n';
//              lineHtml += Column_Hdr;
//          }
//          if (barState == false)
//          {
//              barState     = true;
//              trStartTxt   = '        <tr>\n'
//              wordRow      = trStartTxt;
//              juytPingRow  = trStartTxt;
//              melodyRow    = trStartTxt;
//              intMelodyRow = trStartTxt;
//              intToneRow   = trStartTxt; 
//          }
//          if (chiWord != '(bar)')
//          {
//              tdStartTxt    = '          <td class="tdInt" width=' + noteWidth.toString() +'%>';
//              wordRow      += (tdStartTxt + chiWord + '</td>\n');
//              juytPingRow  += (tdStartTxt + jyutping + '</td>\n');
//              melodyRow    += (tdStartTxt + noteMelody + '</td>\n');
//              intMelodyRow += (tdStartTxt + intMelody + '</td>\n');
//              intToneRow   += (tdStartTxt + intTone + '</td>\n');
//          }
//          else
//          {
//              // end of bar, flush output to barHtml
//              // console.log('* end of bar, wordRow = ' + wordRow);
//              console.log('* end of bar');
//              rowEndTxt  = '        </tr>\n';
//              barHtml    = barStartTxt;
//              barHtml   += '      <table class="tableInt" width=100%>\n';
//              barHtml   += wordRow      + rowEndTxt;
//              barHtml   += juytPingRow  + rowEndTxt;
//              barHtml   += melodyRow    + rowEndTxt;
//              barHtml   += intMelodyRow + rowEndTxt;
//              barHtml   += intToneRow   + rowEndTxt;
//              barHtml   += '      </table> <!-- tableInt -->\n';
//              barHtml   += '    </td>\n';
//              //
//              barState  = false;
//              barCount += 1;
//              lineHtml += barHtml;
//              if (barCount == BarsPerLine)
//              {
//                  console.log('* * end of line');
//                  lineHtml += '  </tr> <!-- row -->\n';
//                  resBody  += lineHtml;
//                  barCount  = 0;
//              }
//          }
//      }
//      
//      // Wrap up table and document
//      resBody += '\n</table>\n\n<p>&nbsp;\n\n';
//      alert('ProcessData() finished');
//      // console.log(resBody);
//  }
//  
//  
//  function Process_CheckLyrics ()
//  {
//      var         oneLine;
//  
//      // alert("Process_CheckLyrics() called");
//      
//      //x import { TestAlert1 } from 'PlayTone.js'
//      //x TestAlert1('Test using function from another js file');
//      
//      // Get parameters from input form
//      SongName = document.getElementById("songName").value;
//      outStr1  = 'Song name = ' + SongName;
//      console.log(outStr1);
//      BeatsPerBar = document.getElementById("beatsPerBar").value;
//      outStr2  = 'Beats per bar = ' + BeatsPerBar;
//      console.log(outStr2);
//      // MinNoteDur = document.getElementById("minNoteDur").value;
//      // outStr3  = 'Min note duration = ' + MinNoteDur;
//      // console.log(outStr3);
//      BarsPerLine = document.getElementById("barsPerLine").value;
//      outStr4  = 'Bars per Line = ' + BarsPerLine;
//      console.log(outStr4);
//      //
//      LineContentList = new Array(0);
//      
//      // Check input file
//      if (inputFileSet == true)
//      {
//          console.log(`File name: ${inputFile.name}`);
//          myReader = new FileReader();
//          myReader.readAsText(inputFile);
//  
//          myReader.onload = function() {
//              resBody = '';
//              //
//              var contentAll   = myReader.result;
//              var contentLines = contentAll.split(/\r\n/);
//              outStr = 'Number of lines in input file = ' + contentLines.length;
//              console.log(outStr);
//              for (let i = 0; i < contentLines.length; i++)
//              {
//                  oneLine = contentLines[i];
//                  ProcessInputLine(i+1, oneLine);
//              }
//              //
//              ProcessData()
//              resultButton.disabled = false;
//              melodyButton.disabled = false;
//              alert('Process_CheckLyrics() success');
//              myReader = null;
//          };
//  
//          myReader.onerror = function() {
//              alert('myReader error')
//              alert(myReader.error.name);
//              console.log('myReader error');
//              console.log(myReader.error);
//              console.log(myReader.error.name);
//          };
//      }
//      else
//      {
//          alert('No input file specified')
//      }
//  }

/* 
const myForm = document.querySelector('#inputForm');
//
myForm.addEventListener('submit', function(event){
    event.preventDefault();
    Process_CheckLyrics();
})
*/

console.log('ClientMain.js loaded')
