// =============================================================
// Server for "Check Lyrics" JS code
// =============================================================

// Need to run "npm install sleep"
// var sleep = require('system-sleep');

const http = require("http");
const fs   = require('fs');
//
const ParsePostData = require("./Server_ParsePostData");
const ProcessLines  = require("./Server_ProcessLines");
const GenOutput     = require("./Server_GenOutput");

// =============================================================

const hostname = 'localhost';
const port     = 8080;

// Data sent from client
var PostData;
var SongName;
var BeatsPerBar;
var BarsPerLine;
var SongFile;
var LineList;

// Processed song lines
var OutputList;

// HTML code segments
var ParamHtml;          // HTML code to report the input parameters
var SongHtml;           // HTML code of the analysis of the song

// =============================================================

function GenParamHtml ()
    // Generate the HTML code to report the input parameters
    //
    // Inputs
    //   (none)
    // Outputs
    //   HTML code to report the input parameters
{
    var paramHtml = '';

    paramHtml += '\n';
    paramHtml += '\n<p>Input parameters:'
    paramHtml += '\n<ul>\n';
    paramHtml += '  <li class="listItem"> SongName : ' + SongName + ' </li>\n';
    paramHtml += '  <li class="listItem"> BeatsPerBar : ' + BeatsPerBar + ' </li>\n';
    paramHtml += '  <li class="listItem"> BarsPerLine : ' + BarsPerLine + ' </li>\n';
    paramHtml += '  <li class="listItem"> SongFile : ' + SongFile + ' </li>\n';
    paramHtml += '</ul>\n';
    paramHtml += '\n<hr>\n';
    return(paramHtml)
}


function SendToClient ( req, res, bodyList )
    // Send the response after processing back to client
    //
    // Inputs
    //   req, res : from serverDispatcher()
    //   bodyList : list of HTML codes for the body of the response
    // Outputs
    //   HTML code to report the input parameters
{
    var     body = '';

    res.writeHead(200, {'Content-Type': 'text/html'});
    body += ParamHtml;
    body += SongHtml;
    res.end(body);

    console.log('SendToClient() done');
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
            console.log('Finish ParsePostData()');
            ParamHtml   = GenParamHtml();
            //
            OutputList = ProcessLines.ProcessInputLines(LineList, parseInt(BeatsPerBar));
            console.log('OutputList has ' + OutputList.length + ' items');
            SongHtml = GenOutput.GenOutputTable(OutputList, BarsPerLine);
            //
            SendToClient(req, res);
            // res.end('ok');
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
}

// =============================================================

var server = http.createServer(serverDispatcher);

server.listen(port, hostname);
console.log(`ServerMain running at http://${hostname}:${port}/`);

