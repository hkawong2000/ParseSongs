#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Functions to print output of program to HTML files
# ==============================================================

# import os
import re
import time
import sys
#
sys.path.append('./ParseSongs_Util')
from ParseSongs_Util import *

# ==============================================================

IDX_CHI      = 0;
IDX_JP       = 1;
IDX_TNUM     = 2;
IDX_NOTE     = 3;
IDX_BEAT     = 4;
IDX_WIDTH    = 5;
IDX_MINT     = 6;
IDX_TONE_VAL = 7;
IDX_TONE_STR = 8; 

# Header for HTML table file
HTML_HEADER = """<!DOCTYPE html>

<html lang="zh_TW" dir="ltr">

<head>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title> RR_TITLE </title>

<style>
  table
  {
    table-layout: fixed;
    border-collapse: collapse;
  }
  td
  {
    border: 1px solid grey;
    text-align: center;
  }
  .topRow
  {
    border-top: 2.5px solid brown;
  }
  .wordRow
  {
    display: table-row;
  }
  .jyutPingRow
  {
    display: table-row;
  }
  .melodyRow
  {
    display: table-row;
  }
  .intRow
  {
    display: table-row;
  }
  .toneIntRow
  {
    display: table-row;
  }
  .rh /* row header */
  {
    background-color: #F8F8F8;
    font-weight: bold;
    border-left: 2.5px solid black
  }
  .lb /* left bar */
  {
    border-left: 2.5px solid black;
  }
  .rb /* right bar */
  {
    border-right: 2.5px solid black;
  }
  .wd /* word */
  {
    color: black;
  }
  .jp /* Jyutping */
  {
    color: blue;
    font-size: 90%;
    font-style: italic;
  }
  .me /* melody */
  {
    color: red;
  }
  .mi /* music interval */
  {
    color: green;
  }
  .ti /* tone interval */
  {
    color: brown;
    border-bottom: 2.5px solid brown;
  }
  .ti sup /* superscript text in tone interval */
  {
    font-size: 67%;
  }
  .mismatchSameNote
  {
    color: brown;
  }
  .mismatchSameTone
  {
    color: goldenRod;
  }
  .halfMatch
  {
    color: orange;
  }
  .noMatch
  {
    color: red;
  }
  .tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black;
  }
  .tooltip .tooltiptext {
    font-size: 75%;
    visibility: hidden;
    width: 110px;
    background-color: #F0F080;
    color: black;
    text-align: center;
    padding: 2px 5px;
    position: absolute;
    z-index: 1;
  }
  .tooltip:hover .tooltiptext {
    visibility: visible;
  }
  .reminder {
    font-weight: bold;
    font-color: maroon;
  }
</style>

</head>

<body>

<h1> RR_TITLE </h1>
"""
#
TABLE_FOOTER = """
</table>
"""
#
HTML_FOOTER = """
<p> &nbsp;

</body>

</html>
"""

# Result table
# Table header
RESULT_HEADER = """
<table style="min-width: 50%; max-width: 90%">

  <tr>
    <td class="tdint" width="15%"><b>分析結果</b></td>
    <td class="tdint">RR_TIME</td>
  </tr>
"""
#
# Column header cell
COLUMN_HEADER_CELL = """    <td class="tdExt" width="15%">
      <table class="tableInt" width="100%">
        <tr>
          <td class="tdInt wd"> 字 </td>
        </tr>
        <tr>
          <td class="tdInt tn"> 粵拼 </td>
        </tr>
        <tr>
          <td class="tdInt ml"> 𝅘𝅥𝅮 </td>
        </tr>
        <tr>
          <td class="tdInt in"> Int-Melody </td>
        </tr>
        <tr>
          <td class="tdInt ti"> Int-Tone </td>
        </tr>
      </table>
    </td>
"""
# # Data cell header
# DATA_CELL_HEADER = """    <td class="tdExt" width="85%">
#       <table class="tableInt" width="100%">
# """
# #
# DATA_CELL_FOOTER = """      </table> <!-- tableInt -->
#     </td>
# """

# Remarks table
REMARKS_HEADER = """<!DOCTYPE html>

<html lang="zh_TW" dir="ltr">

<head>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<title> RR_TITLE2 </title>

<style>
  table
  {
    table-layout: fixed;
    border-collapse: collapse;
  }
  td
  {
    border: 1px solid grey;
    text-align: center;
  }
  .wordRow
  {
    display: table-row;
  }
  .rem
  {
    text-align: left;
    font-size: 80%;
    padding-left: 10px;
  }
  .top
  {
    border-top: 1.5px solid blue;
  }
  .mismatchSameNote
  {
    color: brown;
  }
  .mismatchSameTone
  {
    color: goldenRod;
  }
  .halfMatch
  {
    color: orange;
  }
  .noMatch
  {
    color: red;
  }
</style>

</head>

<body>

<h1 class="title_1"> RR_TITLE2 </h1>

"""
#
REMARKS_TABLE_HEADER = """<table style="table-layout: fixed; min-width:75%; max-width:90%">

<tr>
  <td width=6%>  <b> #         </b> </td>        <!-- Remark idx (0) : rowspan=2 -->
  <td width=6%>  <b>           </b> </td>        <!-- prev/cur -->
  <td width=8%>  <b> Word      </b> </td>        <!-- word (1,4) -->
  <td width=8%>  <b> Tone      </b> </td>        <!-- tone (2,5)-->
  <td width=8%>  <b> Melody    </b> </td>        <!-- melody (3,6) -->
  <td width=8%>  <b> MI        </b> </td>        <!-- melody interval (7) : rowspan=2 -->  
  <td width=8%>  <b> Prev Rest </b> </td>        <!-- prevRest (8) : rowspan=2 -->  
  <td width=20%> <b> Ideal MI  </b> </td>        <!-- ideal MI (9) : rowspan=2 -->  
  <td>           <b> Comment   </b> </td>        <!-- remarks (10) : rowspan=2 -->  
</tr>
"""

# ==============================================================

def GenOutputInfo ( songName, beatsPerBar, songFile ) :
    """ Generate file information part of output HTML file
    
    Inputs:
        songName    : name of song
        beatsPerBar : beats per bar as entered by user
        songFile    : file name containing the information of the song
    Output:
        (none)
    """
    infoHtml = '';

    infoHtml += '\n<table style="min-width: 50%; max-width: 90%; background-color: LightYellow">\n';
    infoHtml += '  <tr>\n';
    infoHtml += '    <td class="tdint" width=15%><b>歌曲資料</b></td>\n';
    infoHtml += '    <td class="tdint" width=85%></td>\n';
    infoHtml += '  </tr>\n';
    infoHtml += '  <tr>\n';
    infoHtml += '    <td class="tdint" width=15%>歌曲名稱</td>\n';
    infoHtml += '    <td class="tdint" width=85%>' + songName + '</td>\n';
    infoHtml += '  </tr>\n';
    infoHtml += '  <tr>\n';
    infoHtml += '    <td class="tdint" width=15%>每小節拍數</td>\n';
    infoHtml += '    <td class="tdint" width=85%>' + str(beatsPerBar) + '</td>\n';
    infoHtml += '  </tr>\n';
    infoHtml += '  <tr>\n';
    infoHtml += '    <td class="tdint" width=15%>歌曲文字檔</td>\n';
    infoHtml += '    <td class="tdint" width=85%>' + songFile + '</td>\n';
    infoHtml += '  </tr>\n';
    infoHtml += '</table>\n';
    return (infoHtml);
# end def GenOutputInfo()


def GenOutputTable ( itemList ) :
    """ Generate song analysis part of output HTML file
    
    Inputs:
        itemList : list of items (words and rest notes) 
    Output:
        (none)
    """
    resBody  = ''
    barState = False

    # First line header (time)
    curTime = time.strftime("%Y-%m-%d %H:%M:%S")
    header2 = re.sub('RR_TIME', curTime, RESULT_HEADER)
    resBody += header2;

    WriteLog('GenOutputTable() : length of itemList = ' + str(len(itemList)))
    expertMode = int(ProcessDirective("@E", 0))
    WriteLog1('expertMode = ' + str(expertMode))

    # items
    for oneNote in itemList :
        # WriteLog1('oneNote = ' + str(oneNote[:2]))
        chiWord     = oneNote[IDX_CHI]
        jyutping    = oneNote[IDX_JP]
        noteMelody  = oneNote[IDX_NOTE]
        noteWidth   = oneNote[IDX_WIDTH]
        intMelody   = oneNote[IDX_MINT]
        intToneVal  = oneNote[IDX_TONE_VAL]
        intToneText = oneNote[IDX_TONE_STR]
        WriteDebug(('chiWord = ' + chiWord + ', intToneVal = ' + str(intToneVal) + ', intToneText = "' + intToneText + '"'), "DA")
        if (expertMode == 0) :
            if ((intToneVal == 0) and (intToneText != '-')) :
                intToneText = '&#x2713'
            elif (intToneVal & 256) :
                intToneText = '(p)'
            elif (intToneVal > 0) :
                intToneText = '<span class="noMatch tooltip"> C </span>'
            # end if
        # end if
        #
        if (barState == False) :
            barState  = True
            #
            trStartTxt   = '        <tr>\n'
            wordRow      = trStartTxt;
            jyutPingRow  = trStartTxt;
            melodyRow    = trStartTxt;
            intMelodyRow = trStartTxt;
            intToneRow   = trStartTxt; 
        # end if
        if (chiWord != '(bar)') :
            wordStartTxt       = '          <td class="tdInt wd" width=' + str(noteWidth) +'%>';
            wordRow           += (wordStartTxt      + chiWord     + '</td>\n');
            jyutPingStartTxt   = '          <td class="tdInt jp" width=' + str(noteWidth) +'%>';
            jyutPingRow       += (jyutPingStartTxt  + jyutping    + '</td>\n');
            melodyStartTxt     = '          <td class="tdInt me" width=' + str(noteWidth) +'%>';
            melodyRow         += (melodyStartTxt    + noteMelody  + '</td>\n');
            intMelodyStartTxt  = '          <td class="tdInt mi" width=' + str(noteWidth) +'%>';
            intMelodyRow      += (intMelodyStartTxt + intMelody   + '</td>\n');
            intToneStartTxt    = '          <td class="tdInt ti" width=' + str(noteWidth) +'%>';
            intToneRow        += (intToneStartTxt   + intToneText + '</td>\n');
        else :
            # end of bar, flush output to barHtml
            WriteLog('* end of bar, wordRow = ' + wordRow);
            barStartTxt = '    <td class="tdExt" width=85%>\n';
            barHtml     = barStartTxt;
            #
            rowEndTxt  = '        </tr>\n'
            barHtml   += '      <table class="tableInt" width=100%>\n';
            barHtml   += wordRow      + rowEndTxt;
            barHtml   += jyutPingRow  + rowEndTxt;
            barHtml   += melodyRow    + rowEndTxt;
            barHtml   += intMelodyRow + rowEndTxt;
            barHtml   += intToneRow   + rowEndTxt;
            barHtml   += '      </table> <!-- tableInt -->\n';
            #
            barEndTxt  = '    </td>\n';
            barHtml   += barEndTxt
            #
            barState  = False;
            #
            lineHtml  = '\n  <tr>  <!-- row begin -->\n'
            lineHtml += COLUMN_HEADER_CELL
            lineHtml += barHtml;
            lineHtml += '  </tr> <!-- end row -->\n';
            resBody  += lineHtml;
        # end if
    # end for

    # Wrap up table and document
    resBody += '</table>\n\n<p>(end)</p>\n';
    return(resBody);
# end def GenOutputTable()


def GenOutput ( outFilePath, songName, beatsPerBar, songFile, itemList, remFilePath, remarkList ) :
    """ Generate output HTML file
    
    Inputs:
        outFilePath : path to HTML output file
        songName    : name of song
        beatsPerBar : beats per bar as entered by user
        songFile    : file name containing the information of the song
        itemList    : list of the analysis result of the song
        remFilePath : path to remark file, '' if no remark file is to be generated
    Output:
        [remarkFile] :
            remarkFile is True if remark file is generated, False otherwise
    """
    # Open HTML output file
    foH = open(outFilePath, 'w', encoding='utf-8')

    # Title
    fileTitle = songName
    header1   = re.sub('RR_TITLE', fileTitle, HTML_HEADER)
    foH.write(header1)

    # Song information
    infoHtml = GenOutputInfo(songName, beatsPerBar, songFile)
    foH.write(infoHtml)

    foH.write('\n<p>&nbsp;</p>\n')

    # Song analysis
    tableHtml = GenOutputTable(itemList)
    foH.write(tableHtml)

    expertMode = int(ProcessDirective("@E", 0))
    remarkLen  = len(remarkList)
    WriteLog('ParseSongs_GenOutput() : len of RemarkList = ' + str(remarkLen) + ' ')
    if ((remarkLen > 0) and (expertMode == 1)) :
        # Generate reference to remark file
        remarkTitle  = 'Remarks for non-match words in ' + songName
        remFileName  = re.sub('\.txt$', '_Remarks.html', songFile)
        remStr       = '\n<p class="reminder"> Please also see remarks in '
        remStr      += '<a target="_blank" href="' + remFilePath + '"> ' + remFileName + '</a> </p>\n'
        foH.write(remStr)
        #
        GenRemark_HTML(remFilePath, remarkTitle, remarkList)
        remarkGen = True
    else :
        remarkGen = False
    # end if

    # Finalize HTML output file
    foH.write(HTML_FOOTER)
    foH.flush()
    foH.close()

    # return value
    return([remarkGen])
# end def GenOutput()


def GenRemark_HTML ( remFilePath, remarkTitle, remarkList ) :
    """ Generate remark HTML file
    
    Inputs:
        remFilePath : path to remark file, '' if no remark file is to be generated
        remarkTitle : title for remark file
        remarkList  : list of remarks (content of the remark file)
    Output:
        (none)
    """
    # Header
    foR = open(remFilePath, 'w', encoding='utf-8')
    header2 = re.sub('RR_TITLE2', remarkTitle, REMARKS_HEADER)
    foR.write(header2)
    foR.write(REMARKS_TABLE_HEADER)

    # Body
    for oneItem in remarkList :
        foR.write('\n<tr>\n')
        outStr10 = '  <td class="top" rowspan=2> ' + oneItem[0] + ' </td>\n'            # remark idx
        foR.write(outStr10)
        outStr11 = '  <td class="top"> (prev) </td>\n'                                  # indicates previous word
        foR.write(outStr11)
        outStr12 = '  <td class="top"> ' + oneItem[1] + ' </td>\n'                      # prevword
        foR.write(outStr12)
        outStr13 = '  <td class="top"> ' + oneItem[2] + ' </td>\n'                      # prevtone
        foR.write(outStr13)
        outStr14 = '  <td class="top"> ' + oneItem[3] + ' </td>\n'                      # prev melody
        foR.write(outStr14)
        outStr15 = '  <td class="top" rowspan=2> ' + oneItem[7] + ' </td>\n'            # melody interval
        foR.write(outStr15)
        outStr16 = '  <td class="top" rowspan=2> ' + oneItem[8] + ' </td>\n'            # prevRest
        foR.write(outStr16)
        outStr17 = '  <td class="top" rowspan=2> ' + oneItem[9] + ' </td>\n'            # ideal MI
        foR.write(outStr17)
        outStr18 = '  <td class="top rem" rowspan=2> ' + oneItem[10] + ' </td>\n'       # remarks
        foR.write(outStr18)
        foR.write('</tr>\n')
        #
        foR.write('<tr>\n')
        outStr21 = '  <td> (cur) </td>\n'                       # indicates current word
        foR.write(outStr21)
        outStr22 = '  <td> ' + oneItem[4] + ' </td>\n'          # cur word
        foR.write(outStr22)
        outStr23 = '  <td> ' + oneItem[5] + ' </td>\n'          # cur tone
        foR.write(outStr23)
        outStr24 = '  <td> ' + oneItem[6] + ' </td>\n'          # cur melody
        foR.write(outStr24)
        foR.write('</tr>\n')
    # end for

    # Footer
    foR.write(TABLE_FOOTER)
    foR.write(HTML_FOOTER)
    foR.flush()
    foR.close()
# end def GenRemark_HTML()

