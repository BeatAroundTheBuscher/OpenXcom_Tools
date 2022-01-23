
# context about png - http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html
# used library - https://pypng.readthedocs.io/en/latest/index.html
# read/write with library - https://stackoverflow.com/questions/64132945/with-pypng-how-do-i-read-a-png-with-it
# about **metadata - https://www.geeksforgeeks.org/python-star-or-asterisk-operator/

# python asterisk operator - https://www.geeksforgeeks.org/python-star-or-asterisk-operator
# - Passing a  Function Using with an arbitrary number of positional argument
# type and keys of metadata
# <class 'dict'>
# dict_keys(['greyscale', 'alpha', 'planes', 'bitdepth', 'interlace', 'size', 'physical', 'palette'])


import png, re
import sys
import logging, datetime

import oxcePalettes

def fixPalette(filePath):
    logging.debug("Running filePath: " + filePath)

    filePath = re.sub("\\n", "", filePath)
    try:
        pngReader = png.Reader(filename=filePath)
        w, h, pixels, metadata = pngReader.read_flat()
    
        found = 0 # needs a cleaner way

        for x in pngReader.trns:
            if x == 0:
                break
            found += 1

        logging.info("Wrong Transparent Index found at: " + str(found))

        for x in range(0, len(pixels)):
            if pixels[x] == found:
                pixels[x] = 0
        

        logging.debug("Removing 'physical' key from 'metadata'")
        if "physical" in metadata.keys():
            metadata.pop("physical")

        logging.debug("TODO: Determine palette by parsing the read palette")
        # some kind of checker to determine which palette the rest uses
        metadata["palette"] = oxcePalettes.battlePalette


        output = open(filePath, 'wb')
        writer = png.Writer(w, h, **metadata)
        writer.write_array(output, pixels)
        output.close()
        return True

    except FileNotFoundError:
        logging.warning("Failed with FileNotFoundError " + filePath)
        return False
    except TypeError as e:
        logging.warning("Failed with TypeError " + filePath)
        logging.warning(e)
        raise
        return False
    except png.FormatError:
        logging.warning("Failed with png.FormatError " + filePath)
        return False

def populatePathsWithOpenXcomLogFile(logFilePath):
    populatedPathsList = []

    log = open(logFilePath, "r")
    loglines = log.readlines()
    log.close()

    for line in loglines: 
        if "has incorrect transparent color index" in line:
            line = re.sub("^.*WARN\]\\sImage\\s", "", line)
            line = re.sub("\\s\(.*$", "", line)
            populatedPathsList.append(sys.argv[2] + "/" + line)

    return populatedPathsList

# grabbed from https://github.com/EttyKitty/OpenXcom_Tools/commit/19ea1661c8f20f24af9d7ed7ecf9afa6d166f622
#LOG_FILENAME = ('crashlog.txt')
LOG_FILENAME = "./logs/" + (datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, filemode='w')



if len(sys.argv) < 2:
    print("Usage: fix_palette.py path-to-openxcom.log path-to-mod-root-dictionary")
    print("OR")
    print("Usage: fix_palette.py path-to-image.png")
    sys.exit(0)

if len(sys.argv) < 3:
    fixPalette(sys.argv[1])
else:
    filePaths = populatePathsWithOpenXcomLogFile(sys.argv[1])

    successCounter = 0

    for x in filePaths:
        if fixPalette(x):
            successCounter += 1

    logging.warning("Found " + str(len(filePaths)) + "broken files by parsing OpenXcom Log")
    logging.warning("Solved " + str(successCounter) + "broken files ")

    sys.exit(successCounter) # return how many were changed

