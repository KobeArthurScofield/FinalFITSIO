# FITS Data write-in

# Kobe Arthur Scofield
# June 2018
# Python 3.6.2 / Anaconda 5.1.0 (x86-64)
# IDE: Microsoft Visual Studio 15.7.3
# IDE: Microsoft Visual Studio 15.7.4


### Public libraries loading stage
#   Some libraries have to be used in multiple privare packages can loaded at here
print("Loading public libraries...")
import numpy as np;                 print(np)
import matplotlib.pyplot as mtpl;   print(mtpl)
from PIL import Image;              print(Image)
from PIL import ExifTags as exif;   print(exif)
from astropy.io import fits;        print(fits)
#   Private library place here to load. Some public libraries included may have loaded before.
print("Loading private libraries...")
from llib import iodp;                  print(iodp)
from llib import transfercore as tfcr;  print(tfcr)
print("Library loaded.\n")


### Input image data for transferring
src_imagepath = iodp.filepath_trim(input("Input path of the source image: "))
imgarray, exifdata = iodp.get_image_with_exif(src_imagepath)

del src_imagepath


### Set extra Exif data input
extraexif_path = iodp.filepath_trim(input("Input extra Exif csv data path, type 'none' if not included: "))
if (extraexif_path != "none"):
    exifdata = tfcr.add_exif(exifdata, iodp.dget_csv_data(extra_path, "ExifLabel", "ExifValue"))
del extraexif_path


### Encapsuling image in FITS data format
exportpath = iodp.filepath_trim(input("Input path of export FITS: "))
hdu = fits.PrimaryHDU(imgarray)
hdulist = fits.HDUList([hdu])
hdulist.writeto(exportpath + ".temp", overwrite= True)  # Prevent OS filesystem error alarm
hdulist.close()
del hdu
del hdulist


### Adding header contents
FITSdata, FITSheader = fits.getdata(exportpath + ".temp", header= True)
FITSheader = tfcr.exif_to_hduhead(FITSheader, exifdata)
fits.writeto(exportpath, FITSdata, FITSheader, overwrite=True)
del FITSdata
del FITSheader


### Reload
NFITSdata, NFITSheader = fits.getdata(exportpath, header= True)
print(NFITSheader)
mtpl.imshow(NFITSdata, cmap= "gray")
mtpl.show()
