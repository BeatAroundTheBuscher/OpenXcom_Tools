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

def guessPalette(metadata):
    # confidence is determined by checking 16 of 256 colors and correctNumber/16
    # the picked colors are the diagonal from NE to SW - should be good enough for approximation

    if len(metadata["palette"]) != 256:
        logging.error("Image does not have a palette with 256 colors")
        raise ValueError("Image does not have a palette with 256 colors")
        return None

    testOrder = [oxcePalettes.battleScapeUFO, oxcePalettes.ufopaediaUFO, oxcePalettes.baseScapeUFO, oxcePalettes.geoScapeUFO]
    testOrderNames = ["battleScapeUFO", "ufopaediaUFO", "baseScapeUFO", "geoScapeUFO"]

    currentTest = 0

    for test in testOrder:
        confidence = 0 
        for i in [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255]:
            logging.debug("test value: " + str(test[i]))
            logging.debug("palette value: " + str(metadata["palette"][i]))
            if test[i][0:3] == metadata["palette"][i][0:3]:
                confidence += 1
        logging.debug("\nConfidence: " + str(confidence))

        if confidence > 13: # of 17
            logging.info("Guessed Palette: " + testOrderNames[currentTest])
            return test
        
        currentTest += 1

    logging.info("Failed to guess palette")
    raise ValueError("No known palette")
    return None

def fixPalette(filePath):
    logging.info("Running filePath: " + filePath)

    filePath = re.sub("\\n", "", filePath)
    try:
        pngReader = png.Reader(filename=filePath)
        w, h, pixels, metadata = pngReader.read_flat()
    
        guessedPalette = guessPalette(metadata) # 1CH.png

        found = 0 # needs a cleaner way

        if pngReader.trns != None: # todo: Scan for what the log actually says
            for x in pngReader.trns:
                if x == 0:
                    break
                found += 1

            logging.info("Wrong Transparent Index found at: " + str(found))
            if found == 0:
                logging.warning("Wrong Transparent Index SHOULD NOT BE 0")

        if found != 0:
            for x in range(0, len(pixels)): # change picture to set palette index 0 for background
                if pixels[x] == found:
                    pixels[x] = 0
        

        logging.debug("Removing 'physical' key from 'metadata'")
        if "physical" in metadata.keys():
            metadata.pop("physical")

        if guessedPalette is not None:
            metadata["palette"] = guessedPalette

            output = open(filePath, 'wb') # save result
            writer = png.Writer(w, h, **metadata)
            writer.write_array(output, pixels)
            output.close()
            return True
        else:
            return False
    
    except FileNotFoundError: # may hide other errors
        logging.warning("Failed with FileNotFoundError " + filePath)
        return False
    except TypeError as e:
        logging.warning("Failed with TypeError " + filePath)
        logging.warning(e)
        return False
    except png.FormatError:
        logging.warning("Failed with png.FormatError " + filePath)
        return False
    except ValueError: # contains custom raises
        logging.warning("Failed with ValueError " + filePath)
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
LOG_FILENAME = "./logs/" + (datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')


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

    logging.info("Found " + str(len(filePaths)) + " broken files by parsing OpenXcom Log")
    logging.info("Solved " + str(successCounter) + " broken files ")

    sys.exit(successCounter) # return how many were changed

