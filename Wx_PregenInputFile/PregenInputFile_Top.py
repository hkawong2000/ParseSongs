#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.5 on Wed Aug  2 13:37:32 2023
#

import wx
import re
import os
import sys

sys.path.append('.')
from Pregen_InputFile import *

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):

    # Class variables
    FilePath       = ''
    InFileName     = ''
    VERSION_STRING = "Version 20230707"
    
    # Related to expert mode
    AllowExpert = 1             # expert mode allowed
    selectJP    = ''            # the selected Jyutping
    newEntry    = list()        # the reordered entry list

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((400, 250))
        self.SetTitle(u"粵拼查找程式")
        self.SetBackgroundColour(wx.Colour(240, 255, 240))

        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Version", "")
        self.Bind(wx.EVT_MENU, self.ShowVersion, item)
        self.frame_menubar.Append(wxglade_tmp_menu, "Config")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        self.FileButton = wx.Button(self.panel_1, wx.ID_ANY, u"選擇檔案")
        self.FileButton.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_2.Add(self.FileButton, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.FileNameLabel = wx.TextCtrl(self.panel_1, wx.ID_ANY, u"(未選檔案)", style=wx.TE_READONLY)
        sizer_2.Add(self.FileNameLabel, 8, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        LabelB1 = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        sizer_4.Add(LabelB1, 3, 0, 0)

        self.StartButton = wx.Button(self.panel_1, wx.ID_ANY, u"處理檔案")
        self.StartButton.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_4.Add(self.StartButton, 4, wx.ALL, 5)

        LabelB3_null = wx.StaticText(self.panel_1, wx.ID_ANY, "")
        sizer_4.Add(LabelB3_null, 3, wx.ALIGN_CENTER_VERTICAL, 10)

        static_line_1 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.EXPAND, 0)

        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)

        StatusLabel = wx.StaticText(self.panel_1, wx.ID_ANY, u"狀態", style=wx.ALIGN_CENTER_HORIZONTAL)
        StatusLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_6.Add(StatusLabel, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.StatusText = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.StatusText.SetMinSize((-1, 50))
        sizer_6.Add(self.StatusText, 8, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 15)

        static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_1.Add(static_line_2, 0, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        ModeLabel = wx.StaticText(self.panel_1, wx.ID_ANY, u"進階", style=wx.ALIGN_CENTER_HORIZONTAL)
        ModeLabel.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, 0, ""))
        ModeLabel.Hide()
        sizer_3.Add(ModeLabel, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.ModeEntry = wx.CheckBox(self.panel_1, wx.ID_ANY, "")
        self.ModeEntry.Hide()
        sizer_3.Add(self.ModeEntry, 8, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.LineText = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.LineText.SetBackgroundColour(wx.Colour(255, 255, 240))
        self.LineText.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL, 0, ""))
        self.LineText.Hide()
        sizer_1.Add(self.LineText, 0, wx.ALL | wx.EXPAND, 10)

        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)

        self.SelectBox = wx.ComboBox(self.panel_1, wx.ID_ANY, choices=[], style=wx.CB_DROPDOWN)
        self.SelectBox.SetBackgroundColour(wx.Colour(255, 255, 240))
        self.SelectBox.Hide()
        sizer_5.Add(self.SelectBox, 6, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.SubmitButton = wx.Button(self.panel_1, wx.ID_ANY, u"提交")
        self.SubmitButton.SetBackgroundColour(wx.Colour(255, 255, 240))
        self.SubmitButton.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD, 0, ""))
        self.SubmitButton.Hide()
        sizer_5.Add(self.SubmitButton, 4, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.SelectFile, self.FileButton)
        self.Bind(wx.EVT_BUTTON, self.StartProcess, self.StartButton)
        self.Bind(wx.EVT_CHECKBOX, self.ModeSelect, self.ModeEntry)
        self.Bind(wx.EVT_BUTTON, self.SelectJyutping, self.SubmitButton)
        # end wxGlade

    def ShowVersion(self, event):  # wxGlade: MyFrame.<event_handler>
        outStrV = self.VERSION_STRING
        wx.MessageBox(outStrV, 'Info', wx.OK)
    # end def ShowVersion()


    def SelectFile(self, event):  # wxGlade: MyFrame.<event_handler>
        dlg = wx.FileDialog(
            self, message="請選擇歌曲文字檔",
            # defaultDir=self.currentDirectory, 
            defaultFile="",
            wildcard="*.txt",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths           = dlg.GetPaths()
            self.FilePath   = re.sub('\\\\', '/', paths[0])
            print('self.FilePath = ' + self.FilePath)
            fileNameLastIdx = self.FilePath.rindex('/')
            self.InFileName = self.FilePath[(fileNameLastIdx+1):]
            self.FileNameLabel.SetValue(self.InFileName)
            # print('self.InFileName = ' + self.InFileName)
        # end if
        dlg.Destroy()
    # end def SelectFile()


    def StartProcess(self, event):  # wxGlade: MyFrame.<event_handler>
        if (self.FilePath == '') :
            outStr0 = '請選擇上傳檔案'
            wx.MessageBox(outStr0, 'Info', wx.OK)
            return
        # end if

        guiParam = [self.SelectJyutping, self.newEntry]
        # (code, errStr) = ProcessFile(self.FilePath, expertMode=expertVal, graphicsMode=1, guiParam=guiParam)
        (code, errStr) = ProcessFile(self.FilePath, expertMode=0, graphicsMode=1, guiParam=guiParam)
        
        if (code == 0) :
            # showinfo(title = 'Info', message='Success')
            outFile     = re.sub('.txt', '_input.txt', self.InFileName)
            noteFile    = re.sub('.txt', '_notes.txt', self.InFileName)
            successText = '成功 !\n結果在 : ' + outFile + '\n附注在 : ' + noteFile
            self.StatusText.SetValue(successText)
            #
            self.FileNameLabel.SetValue('')
            self.FileName = ''
        else :
            # showinfo(title = 'Info', message=errStr)
            StatusText['text'] = errStr
        # end if
    # end def StartProcess()


    def ModeSelect(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'ModeSelect' not implemented!")
        event.Skip()
    # end def ModeSelect()


    def SelectJyutping(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'SelectJyutping' not implemented!")
        event.Skip()
    # end def SelectJyutping()


# end of class MyFrame

class Pregen_InputFile(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class Pregen_InputFile

if __name__ == "__main__":
    Pregen_InputFile = Pregen_InputFile(0)
    Pregen_InputFile.MainLoop()
