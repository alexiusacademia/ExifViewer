from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import wx

import pprint


def get_exif(filename):
    exif_data = {}
    image = Image.open(filename)
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for gps_tag in value:
                    sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                    gps_data[sub_decoded] = value[gps_tag]
                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        lbl = wx.StaticText(self, label="Hello, World")
        box = wx.BoxSizer(wx.VERTICAL)

        exif = get_exif('alex.jpg')

        print(exif['GPSInfo']['GPSLatitude'])

        box.Add(lbl)

        self.SetSizer(box)
        self.Show()


# Define a function to convert GPS coordinates to decimal degrees
def convert_to_degrees(value):
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    return d + (m / 60.0) + (s / 3600.0)


if __name__ == '__main__':
    app = wx.App()
    win = MainFrame(None, 'Exif Viewer')
    app.MainLoop()
