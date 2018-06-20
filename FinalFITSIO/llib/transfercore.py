# INput/Output operation module
# Kobe Arthur Scofield
# 2018-06-19
# Build 1
# Python: Anaconda3_64 5.0.1 (Python 3.6.2)
# IDE: MSVS2017_Community 15.7.4


import numpy as np
from astropy.io import fits


def add_exif(origin_exif= {}, extra_data= ()):
    """
    This function is used to append extra Exif information.
    """
    extra_stor = {}
    exiflbl, exifvlue = extra_data              # Unpack
    for label, value in zip(exiflbl, exifvlue):
        extra_stor[label] = value               # Convert
    for item in extra_stor.keys():
        origin_exif[item] = extra_stor[item]    # Add and cover
    return origin_exif
#

def exif_to_hduhead(header, exif_list = {}):
    """
    Convert Exif to FITS header information
    """
    ConvertList = {"ImageDescription": "ORIGIN", "Artist": "COPYRGHT", "Model": "TELESCOP", "Software": "INSTRUME"}
    for keys in exif_list.keys():
        if keys == "DateTime":
            strg = exif_list[keys]
            header.set("DATE", strg[0:4]+"-"+strg[5:7]+"-"+strg[8:10]+"        ")
        elif keys == "GPSInfo":
            lat = exif_list[keys][2][0][0] + exif_list[keys][2][1][0] / 60
            long = exif_list[keys][4][0][0] + exif_list[keys][4][1][0] / 60
            if exif_list[keys][1] == 'N':
                lat = lat
            else:
                lat = 0 - lat
            if exif_list[keys][3] == 'E':
                long = long
            else:
                long = 0 - long
            header.set("SITELAT", lat)
            header.set("SITELONG", long)
        elif keys == "DateTimeOriginal":
            strg = exif_list[keys]
            strg = strg[0:4] + ' ' + strg[5:7] + ' ' + strg[8:10] + 'T' + strg[11:13] + ':' + strg[14:16] + ':' + strg[17:19]
            header.set("DATE-OBS", strg)
        elif keys == "ExposureTime":
            header.set("EXPOSURE", exif_list[keys][0] / exif_list[keys][1])
        else:
            if keys in ConvertList:
                strg = exif_list[keys]
                if (len(strg) <= 8):
                    space = ""
                    for i in range(0, 8 - len(strg)):
                        space = space + ' '
                    strg = strg + space
                elif (len(strg) <= 18):
                    space = ""
                    for i in range(0, 18 - len(strg)):
                        space = space + ' '
                    strg = strg + space
                else:
                    strg = strg[0:18]
                header.set(ConvertList[keys], strg)
    return header

