# INput/Output operation module
# Kobe Arthur Scofield
# 2018-06-19
# Build 4
# Partial extracted
# Python: Anaconda3_64 5.0.1 (Python 3.6.2)
# IDE: MSVS2017_Community 15.7.4

import numpy as np
import pandas as pd
from PIL import Image
from PIL import ExifTags as exif
import matplotlib.pyplot as mtpl

def filepath_trim(path):
    """
    Trimming Path to prevent unexpected quotes problem.
    """
    if (path[0] == '"') or (path[0] == "'"):
        path = path[1:]
    if (path[-1] == '"') or (path[-1] == "'"):
        path = path[:-1]
    return path
#

def get_image_with_exif(path):
    """
    Return image raster and its Exif information.
    If No Exif imformation found, return raster and null Exif
    """
    img = Image.open(path)      # Data includes Exif
    exifinfo = img._getexif()   # Abstract Exif
    if (exifinfo != None):
        exifrt = {}
        for exiftag, exifvalue in exifinfo.items():     # Copy Exif
            tmptag = exif.TAGS.get(exiftag, exiftag)
            exifrt[tmptag] = exifvalue
        return (np.array(img), exifrt)
    else:
        return (np.array(img), None)
#

def dget_csv_data(file_name, x_data, y_data):
    """
    Directly read X-Y Data from a CSV file.
    Parameters:
    file_name: The path of the csv data
    x_data: The label of X data in CSV file
    y_data: The label of Y data in CSV file
    """
    data = pd.read_csv(file_name)
    X_parameter = []
    Y_parameter = []
    for xdt ,ydt in zip(data[x_data], data[y_data]):   # To pack them all and send data to two variables
        X_parameter.append(xdt) # Parameter required (and I don't know why)
        Y_parameter.append(ydt)
    return X_parameter,Y_parameter
#

def imagesvdp(imgdata, showaxis = False, figsize = (8, 4), dpi = 72,save = True, saveasfig = False, display = True, filepath = "", **kwargs):
    """
    This function is used to save and display the figure.
    """
    mtpl.figure(figsize= figsize, dpi= dpi)
    mtpl.imshow(imgdata, interpolation= "none", **kwargs)
    if (save and len(filepath)):    # len(filepath) checks if you've not input a null string
        if saveasfig:
            mtpl.savefig(filepath)
        else:
            mtpl.imsave(arr= imgdata, fname= filepath)
    if display:     # Display the figure
        if showaxis:
            mtpl.axis("on")
        else:
            mtpl.axis("off")
        mtpl.show()
#
