# this file needs an folder oxcePalettes
# in which the content of /common/Palettes/ has been copied into

import sys

sys.path.insert(0, '../commons')
import file_handling as fH  # noqa
import png_handling as pngH  # noqa

paths = ["oxcePalettes"]
# pickedPalette = "UFO-JASC-SAFE"
pickedPalette = "UFO-JASC"
fileList = []


for path in paths:
    fileList = fH.populateFileList(path, fileList)

for x in fileList:
    if pickedPalette in x:
        palette = pngH.getPaletteJASC(x)
        print(palette)

sys.exit(0)
