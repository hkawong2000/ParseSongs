// =============================================================
// Parse data in POST packet
// =============================================================

// Need to run "npm install sleep"
// var sleep = require('system-sleep');

const http = require("http");
const fs   = require('fs');

// =============================================================

const NonFileArgList = ["songName", "beatsPerBar", "barsPerLine"];
// const NonFileArgMap  = {
//   "songName"    : SongName, 
//   "beatsPerBar" : BeatsPerBar,
//   "barsPerLine" : BarsPerLine,
// };
const FileArgList    = ["inputFile"];
// const FileArgMap     = {
//   "inputFile" : SongFile,
// };

var argSongName;
var argBeatsPerBar;
var argBarsPerLine;
var argSongFile;
var argLineList;

// =============================================================

/*
function ProcessStartRequest (reqStr, res)
{
  var argList, keyValPair, eqIdx, key, val;
  var keyValStr = '';

  argList = reqStr.split('&');
  for (i in argList)
  {
      keyValPair = argList[i];
      eqIdx      = keyValPair.indexOf("=");
      key        = keyValPair.slice(0, eqIdx);
      val        = keyValPair.slice((eqIdx+1),);
      // console.log('key = '+ key + ', val = '+ val);
      keyValStr += ('<p> key = '+ key + ', val = '+ val + '\n');
  }
  // console.log('keyValStr = ' + keyValStr);

  // Temp return
  res.writeHead(200);
  header  = '<html>\n<meta charset="utf-8">\n<body>\n';
  body    = 'reqStr = ' + reqStr + '\n';
  body   += keyValStr + '\n\n';
  footer  = '</body>\n</html>';
  outStr  = header + body + footer;
  res.end(outStr);  
}
*/


function ParseFileArg ( fileStr )
  // Parse string which contains file (including file content)
  // 
  // Inputs
  //  fileStr : string containing file name and file content
  // Outputs
  //  list of [fileName, contentType, contentList]
  //    fileName    : name of file
  //    contentType : content type of file
  //    contentList : (for text file content only), one line per list entry
{
  // return input file name and content lines in list

  var fileName, contentType;
  var remFileStr, contentStr;
  var contentList = [];

  let m0 = fileStr.match(/.*filename="([\S]+)"/);
  if (m0 == null)
  {
    console.log('Problem processing fileName:{\n' + fileStr + '}');
    return(['', fileContent]);
  }
  fileName = m0[1];
  // console.log('fileName = {' + fileName + '}');
  //
  let pos_m0 = fileStr.indexOf(m0[0]);
  let len_m0 = m0[0].length;
  remFileStr = fileStr.slice((pos_m0 + len_m0),);

  let m1 = remFileStr.match(/.*Content-Type: ([\S]+)/);
  if (m1 == null)
  {
    console.log('Problem processing content-type:{\n' + remFileStr + '}');
    return(['', '', true, fileContent]);    
  }
  contentType = m1[1];
  // console.log('contentType = ' + contentType);
  //
  let pos_m1 = remFileStr.indexOf(m1[0]);
  let len_m1 = m1[0].length;
  contentStr = remFileStr.slice((pos_m1 + len_m1),); 
  //
  contentList    = contentStr.split('\n');
  contentListLen = contentList.length;
  if (0)
  {
    // (debug code)
    for (i in contentList)
    {
      console.log(i + ' : ' + contentList[i]);
    }
  }
  //
  return[fileName, contentType, contentList];
}


function ParseArg ( argStr )
  // Parse string which contains argument and value (including file)
  // 
  // Inputs
  //   argStr : string containing argument and value
  // Outputs
  //   list of [argName, argVal, isFile, content]
  //     argName : name of argument
  //     argVal  : value of argument
  //     isFile  : true if argVal is filename, false otherwise
  //     content : if argument is file, contents of the file.  Otherwise empty string
{
  var   remStr;
  var   argName, argVal, isFile;
  var   fileParam, fileName;
  var   fileContent = [];
  
  let m0 = argStr.match(/.*form-data\; name="([\S]+)"/);
  if (m0 == null)
  {
    console.log('Problem processing argName:{\n' + argStr + '}');
    return(['', '', false, fileContent]);
  }
  argName = m0[1];
  //
  let pos_m0 = argStr.indexOf(m0[0]);
  let len_m0 = m0[0].length;
  remStr = argStr.slice((pos_m0 + len_m0),);

  if (NonFileArgList.includes(argName))
  {
    argVal = remStr.slice(4,-1);
    isFile = false;
    // console.log('argName = {' + argName + '} is non-file argument');
    // console.log('argVal  = {' + argVal + '}');
    switch(argName)
    {
      case 'songName' :
        argSongName = argVal;
        break;
      case 'beatsPerBar' :
        argBeatsPerBar = parseInt(argVal);
        break;
      case 'barsPerLine' :
        argBarsPerLine = parseInt(argVal);
        break;
    }
  }
  else if (FileArgList.includes(argName))
  {
    // console.log('argName = {' + argName + '} is file argument');
    isFile      = true;
    fileParam   = ParseFileArg(remStr);
    fileName    = fileParam[0];
    contentType = fileParam[1]
    lineList    = fileParam[2];
    switch(argName)
    {
      case 'inputFile' :
        argSongFile = fileName;
        argLineList = lineList;
        break;
    }
  }
  else
  {
    console.log('argName = {' + argName + '} is NOT handled !');
  }

  // Return result
  return([argName, argVal, isFile, fileContent]);
}


function ParsePostData( postStr )
  // Parse the complete data packet from POST
  //
  // Inputs
  //   postStr : the string from POST
  // Outputs
  //   list of [SongName, BeatsPerBar, BarsPerLine, SongFile, LineList]
{
  var startIdx, nextIdx;
  var remStr, tempStr, curStr;

  const startStr    = "------WebKit";
  const startStrLen = startStr.length;

  remStr = postStr;
  console.log('postStr length = '+ postStr.length);
  while (1)
  {
    startIdx = remStr.indexOf(startStr);
    if (startIdx == -1)
    {
      break;
    }
    else
    {
      tempStr = remStr.slice((startIdx + startStrLen),);
      nextIdx = tempStr.indexOf(startStr);
      if (nextIdx != -1)
      {
        curStr  = remStr.slice(startIdx, (nextIdx + startStrLen));
        argInfo = ParseArg(curStr);
        remStr  = remStr.slice(nextIdx + startStrLen);
      }
      else
      {
        // Last element
        // curStr = remStr.slice(startIdx,);
        remStr = '';
      }
    }
  }
  
  // Return result
  return([argSongName, argBeatsPerBar, argBarsPerLine, argSongFile, argLineList]);
}

module.exports = { ParsePostData };
console.log('Server_ReadPostData.js loaded');

