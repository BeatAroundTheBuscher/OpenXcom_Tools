# this file needs an folder oxcePalettes in which the content of /common/Palettes/ has been copied into

import os, sys

sys.path.insert(0, '../commons')
import file_handling as fh

paths = ["oxcePalettes"]
# pickedPalette = "UFO-JASC-SAFE"
pickedPalette = "UFO-JASC"
fileList = []


def getPaletteJASC(path):
    palette = []
    print("getPalette for " + path)
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    # first three lines are metadata
    for x in range(3, 3+256):
        lines[x] = lines[x].replace(" ", ", ")
        if x == 3:
            lines[x] = "(" + lines[x][:-1] + ", 0)" # first one is transparent
        else:
            lines[x] = "(" + lines[x][:-1] + ", 255)" # last symbol of lines[x] is \n
        palette.append(lines[x])

    return palette

for path in paths:
    fileList = fh.populateFileList(path, fileList)

for x in fileList:
    if pickedPalette in x:
        palette = getPaletteJASC(x)
        print(palette)

sys.exit(0)

