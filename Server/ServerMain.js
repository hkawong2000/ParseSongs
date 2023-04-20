// =============================================================
// Server for "Check Lyrics" JS code
// =============================================================

// Need to run "npm install sleep"
// var sleep = require('system-sleep');

const http = require("http");
const fs   = require('fs');
//
const ParsePostData = require("./Server_ParsePostData");

// =============================================================

const hostname = 'localhost';
const port = 8080;

// Data sent from client
var PostData;
var SongName;
var BeatsPerBar;
var BarsPerLine;
var SongFile;
var LineList;

// =============================================================

function SendToClient ( req, res )
{
  console.log('SendToClient() called');
  console.log('  ' + Date.now() + ' : req.method = ' + req.method + ' with content {' + req.url + '}');
  console.log('  ' + 'req = ' + JSON.stringify(req))
  console.log('  ' + 'res = ' + JSON.stringify(res))

  res.writeHead(200, {'Content-Type': 'text/html'});
  header   = '<html>\n<meta charset="utf-8">\n<body>\n';
  body     = '';
  body    += '<p>Welcome\n';
  footer   = '</body>\n</html>\n';
  res.write(header);
  res.write(body);
  res.end(footer);
}


var serverDispatcher = function( req, res )
  // Server dispatcher to handle incoming packets from client
  //
  // Inputs/Outputs : standard
{
  urlStr = req.url;
  console.log(Date.now() + ' : req.method = ' + req.method + ' with content {' + req.url + '}');

  fileLoc = '';
  if (req.method == 'POST')
  {
    // Reference: https://itnext.io/how-to-handle-the-post-request-body-in-node-js-without-using-a-framework-cd2038b93190
    //            https://plainenglish.io/blog/parsing-post-data-3-different-ways-in-node-js-e39d9d11ba8

    console.log(Date.now() +': POST request was made : "' + req.url + '"');
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString(); // convert Buffer to string
    });
    req.on('end', () => {
      PostData    = ParsePostData.ParsePostData(body);
      SongName    = PostData[0];
      BeatsPerBar = PostData[1];
      BarsPerLine = PostData[2];
      SongFile    = PostData[3];
      LineList    = PostData[4];
      if (1)
      {
        argStr1 = 'Songname = {' + SongName + '} with datatype ' + (typeof SongName);
        console.log(argStr1);
        argStr2 = 'BeatsPerBar = {' + BeatsPerBar + '} with datatype ' + (typeof BeatsPerBar);
        console.log(argStr2);
        argStr3 = 'BarsPerLine = {' + BarsPerLine + '} with datatype ' + (typeof BarsPerLine);
        console.log(argStr3);
        argStr4 = 'SongFile = {' + SongFile + '} with datatype ' + (typeof SongFile);
        console.log(argStr4);
        argStr5 = 'contentList has length ' + LineList.length;
        console.log(argStr5);
      }
      console.log('Finish ParsePostData()');
      res.end('ok');
    });
  }
  else if (req.method == 'GET')
  {
    if ((urlStr == '/') || (urlStr == '/Index.html'))
    {
      fileLoc = '/Index.html';
      res.writeHead(200, {'Content-Type': 'text/html'});
    }
    else if (urlStr == '/ClientMain.css')
    {
      fileLoc = '/ClientMain.css';
      res.writeHead(200, {'Content-Type': 'text/css'});
    }
    else if (urlStr == '/ClientMain.js')
    {
      fileLoc = '/ClientMain.js';
      res.writeHead(200, {'Content-Type': 'application/javascript'});
    }
    else if (urlStr == '/favicon.ico')
    {
      // favicon.ico not defined
      res.writeHead(204, {'Content-Type': 'text/plain'});
      res.end('');
    }
    else
    {
      // Breakpoint for further processing
      console.log('Received GET something else ...');
      i = 1;
    }
    //
    // code to send file stream
    if (fileLoc != '')
    {
      var myReadStream = fs.createReadStream(__dirname + fileLoc, 'utf8');
      myReadStream.pipe(res);
    }
  }
  else
  {
    // Breakpoint for further processing
    console.log('Received neither GET nor POST ...');
    i = 1;
  }

  // V01
  // res.writeHead(200);
  // res.end("My first server!");

  // V02
  // res.writeHead(200);
  // res.end(`<html><body><p>This is HTML</p></body></html>`);
}

// =============================================================

var server = http.createServer(serverDispatcher);

server.listen(port, hostname);
console.log(`Server running at http://${hostname}:${port}/`);

