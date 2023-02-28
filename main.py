from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import wx


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

        lbl_title = wx.StaticText(self, label="Exif Viewer")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(lbl_title, 0, wx.ALIGN_CENTER_HORIZONTAL)
        box.AddSpacer(30)

        exif = get_exif('image.jpg')

        if 'GPSInfo' in exif:
            latitude = exif['GPSInfo']['GPSLatitude']
            longitude = exif['GPSInfo']['GPSLongitude']
            latitude_ref = exif['GPSInfo']['GPSLatitudeRef']
            longitude_ref = exif['GPSInfo']['GPSLongitudeRef']

            lbl_latitude_ref = wx.StaticText(self, label=latitude_ref)
            lbl_latitude_ref.SetSize((50, -1))
            txt_latitude = wx.TextCtrl(self, value=str(latitude), style=wx.TE_CENTER)
            txt_latitude.SetMinSize(wx.Size((250, -1)))

            lbl_longitude_ref = wx.StaticText(self, label=longitude_ref)
            lbl_longitude_ref.SetSize((50, -1))
            txt_longitude = wx.TextCtrl(self, value=str(longitude), style=wx.TE_CENTER)
            txt_longitude.SetMinSize(wx.Size((250, -1)))

            hbox_latitude = wx.BoxSizer(wx.HORIZONTAL)
            hbox_latitude.AddSpacer(10)
            hbox_latitude.Add(lbl_latitude_ref, 0)
            hbox_latitude.AddSpacer(10)
            hbox_latitude.Add(txt_latitude, 1)
            hbox_latitude.AddSpacer(10)

            hbox_longitude = wx.BoxSizer(wx.HORIZONTAL)
            hbox_longitude.AddSpacer(10)
            hbox_longitude.Add(lbl_longitude_ref, 0)
            hbox_longitude.AddSpacer(10)
            hbox_longitude.Add(txt_longitude, 1)

            box.Add(hbox_longitude)
            box.AddSpacer(10)
            box.Add(hbox_latitude)
            box.AddSpacer(10)

        else:
            # The photo doesn't contain exif info
            wx.MessageDialog(self, 'The photo provided doesn\'t contain exif data', 'Error').ShowModal()

        self.SetSizerAndFit(box)
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
