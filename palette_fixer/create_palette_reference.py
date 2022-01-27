# this file needs an folder oxcePalettes in which the content of /common/Palettes/ has been copied into

import os, sys

sys.path.insert(0, '../commons')
import file_handling as fh
import png_handling as pngH

paths = ["oxcePalettes"]
# pickedPalette = "UFO-JASC-SAFE"
pickedPalette = "UFO-JASC"
fileList = []


for path in paths:
    fileList = fh.populateFileList(path, fileList)

for x in fileList:
    if pickedPalette in x:
        palette = pngH.getPaletteJASC(x)
        print(palette)

sys.exit(0)

