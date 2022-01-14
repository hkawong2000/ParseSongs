#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ==============================================================
# Functions to print output of program to HTML files
# ==============================================================

import os
import re
import sys
import string
import shutil

# ==============================================================

# Header for HTML table flle
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

<h1 class="title_1"> RR_TITLE </h1>

</div>

<table style="table-layout: fixed; min-width:75%; max-width:90%">
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

</div>

<table style="table-layout: fixed; min-width:75%; max-width:90%">
"""
#
REMARKS_TABLE_HEADER = """
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

def Generate_SpanHeader ( unitsPerLine ) :
    """ Generate NULL row to define cell width of subsequent text
    
    Inputs:
        unitsPerLine : number of units per line
    Output:
        Generated span header row
    """
    CellsPerLine = 4            # for aesthetics

    if (unitsPerLine <= 10) :
        dataSize   = 100 // (unitsPerLine + 1)
        headerSize = 100 - (dataSize * unitsPerLine)
    else :
        dataSize0  = 1000 // (unitsPerLine + 1)
        dataSize   = dataSize0 / 10
        headerSize = (1000 - (dataSize0 * unitsPerLine)) / 10
    # end if
    #x print('unitsPerLine = ' + str(unitsPerLine) + ' : headerSize = ' + str(headerSize) + ', dataSize = ' + str(dataSize))

    headerCell = '<td width=' + str(headerSize) + '%> </td>'
    dataCell   = '<td width=' + str(dataSize) + '%> </td> '

    result = '\n<tr class="topRow">\n  ' + headerCell
    for i in range(0, unitsPerLine) :
        if (i % CellsPerLine == 0) :
            result += '\n  '
        result += dataCell
    # end for
    result += '\n</tr>\n'

    return(result)
# end def Generate_SpanHeader()


def WriteLineH ( foH, rowLists, fill=0 ) :
    """ Write one line of music and info to output file
    
    Inputs:
        foH      : pointer to HTML output file
        rowLists : list of [wordRow_list, jyutPingRow_list, melodyRow_list, musicIntervalRow_list, toneIntervalRow_list]
        fill     : fill the rest of the line with empty content 
    Output:
        (none)
    """
    wordRow_list          = rowLists[0]
    jyutPingRow_list      = rowLists[1]
    melodyRow_list        = rowLists[2]
    musicIntervalRow_list = rowLists[3]
    toneIntervalRow_list  = rowLists[4]

    wordRow_Hdr          = '\n<tr class="wordRow">\n  <td class="wd rh"> 字 </td>\n'
    jyutPingRow_Hdr      = '\n<tr class="jyutPingRow">\n  <td class="tn rh"> 粵拼 </td>\n'
    melodyRow_Hdr        = '\n<tr class="melodyRow">\n  <td class="ml rh"> &#x1D160; </td>\n'
    musicIntervalRow_Hdr = '\n<tr class="intRow">\n  <td class="in rh"> Int-Melody </td>\n'
    toneIntervalRow_Hdr  = '\n<tr class="toneIntRow">\n  <td class="ti rh"> Int-Tone </td>\n'
    endRow               = '</tr>\n'
    fillCell             = '\n  <td rowspan=5 colspan=100 class="ti rb"> &nbsp; </td> \r\n</tr>\n'

    print('WriteLineH() called')
    
    # Row for word (lyrics)
    foH.write(wordRow_Hdr)
    for oneCell in wordRow_list :
        foH.write(oneCell + '\n')
    # end for
    if (fill == 0) :
        foH.write(endRow)
    else :
        # fill the rest of all rows
        foH.write(fillCell)
    # end if
    wordRow_list[0:] = ''
    
    # Row for Jyutping
    foH.write(jyutPingRow_Hdr)
    for oneCell in jyutPingRow_list :
        foH.write(oneCell + '\n')
    # end for
    foH.write(endRow)
    jyutPingRow_list[0:] = ''
    
    # Row for melody (notes)
    foH.write(melodyRow_Hdr)
    for oneCell in melodyRow_list :
        foH.write(oneCell + '\n')
    # end for
    foH.write(endRow)
    melodyRow_list[0:] = ''

    # Row for musical interval
    foH.write(musicIntervalRow_Hdr)
    for oneCell in musicIntervalRow_list :
        foH.write(oneCell + '\n')
    # end for
    foH.write(endRow)
    musicIntervalRow_list[0:] = ''
    
    # Row for Yiu results
    foH.write(toneIntervalRow_Hdr)
    for oneCell in toneIntervalRow_list :
        foH.write(oneCell + '\n')
    # end for
    foH.write(endRow)
    toneIntervalRow_list[0:] = ''

# end def WriteLineH()


def GenRemark_HTML ( foR, remarkList, songName ) :
    """ Generate HTML file of remarks
    
    Inputs:
        fo         : pointer to output HTML file
        remarkList : list of remarks 
        songName   : name of the song
    Output:
        (none)
    """
    # Header
    print('GenRemark_HTML called().  remarkList has ' + str(len(remarkList)) + ' items')

    titleTxt  = 'Remarks for non-match words in ' + songName
    headerTxt = re.sub('RR_TITLE2', titleTxt, REMARKS_HEADER)
    foR.write(headerTxt)
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
    
# end def GenRemark_HTML()


