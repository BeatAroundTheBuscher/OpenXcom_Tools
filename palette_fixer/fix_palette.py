# context about png - http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
# used library - https://pypng.readthedocs.io/en/latest/index.html
# read/write with library - https://stackoverflow.com/questions/64132945/with-pypng-how-do-i-read-a-png-with-it  # noqa
# about **metadata - https://www.geeksforgeeks.org/python-star-or-asterisk-operator/  # noqa

# python asterisk operator - https://www.geeksforgeeks.org/python-star-or-asterisk-operator  # noqa
# - Passing a  Function Using with an arbitrary number of positional argument
# type and keys of metadata
# <class 'dict'>
# dict_keys(['greyscale', 'alpha', 'planes', 'bitdepth', 'interlace', 'size', 'physical', 'palette'])  # noqa


import sys
import logging
import datetime


sys.path.insert(0, './commons')
import png_handling as pngH  # noqa
import oxce_handling as oxceH  # noqa

# grabbed from https://github.com/EttyKitty/OpenXcom_Tools/commit/19ea1661c8f20f24af9d7ed7ecf9afa6d166f622  # noqa

if len(sys.argv) < 2:
    print("Usage: fix_palette.py path-to-openxcom.log path-to-mod-root-dictionary")  # noqa
    print("OR")
    print("Usage: fix_palette.py path-to-image.png")
    sys.exit(0)

# TODO: have to create a logs folder
LOG_FILENAME = "./logs/" + ("fix_palette_" + datetime.datetime.now().strftime(
                            '%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, filemode='w')

if len(sys.argv) < 3:
    pngH.fixPalette(sys.argv[1])
else:
    filePaths = oxceH.populatePathsWithOpenXcomLogFile(sys.argv[1])

    successCounter = 0

    for x in filePaths:
        if pngH.fixPalette(x):
            successCounter += 1

    logging.info("Found " + str(len(filePaths)) +
                 " broken files by parsing OpenXcom Log")
    logging.info("Solved " + str(successCounter) +
                 " broken files ")

    sys.exit(successCounter)  # return how many were changed
