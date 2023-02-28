import wx
import wx.html2
import markdown

import os


class HelpDialog(wx.Dialog):
    def __init__(self, parent, title='Help'):
        super().__init__(parent, title=title)

        self.panel = wx.Panel(self)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)

        with open(f"{dir_path}/readme.md", "r") as f:
            markdown_text = f.read()

        html_text = markdown.markdown(markdown_text)

        self.webview = wx.html2.WebView.New(self.panel)
        self.webview.SetPage(html_text, "")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.webview, 1, wx.EXPAND)
        self.panel.SetSizer(sizer)
