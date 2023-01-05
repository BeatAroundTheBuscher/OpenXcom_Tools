# this file needs an folder oxcePalettes
# in which the content of /common/Palettes/ has been copied into

import sys

import commons.file_handling as fH
import commons.png_handling as pngH

paths = ["oxcePalettes"]
# pickedPalette = "UFO-JASC-SAFE"
pickedPalette = "UFO-JASC"
fileList = []


for path in paths:
    fileList = fH.populateFileList(path, fileList, [".pal"])

for x in fileList:
    if pickedPalette in x:
        palette = pngH.getPaletteJASC(x)
        print(palette)

sys.exit(0)
