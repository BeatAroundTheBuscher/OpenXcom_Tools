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

def guessPalette(metadata):
    # confidence is determined by checking 17 of 256 colors
    # the picked colors are the diagonal from NE to SW - should be good enough for approximation

    if len(metadata["palette"]) != 256:
        logging.error("Image does not have a palette with 256 colors")
        raise ValueError("Image does not have a palette with 256 colors")
        return None

    # TODO: should turn these attributes into objects
    testOrder = [oxcePalettes.battleScapeUFO, oxcePalettes.ufopaediaUFO, oxcePalettes.baseScapeUFO, oxcePalettes.geoScapeUFO]
    testOrderNames = ["battleScapeUFO", "ufopaediaUFO", "baseScapeUFO", "geoScapeUFO"]

    currentTest = 0 # TODO: won't need this anymore once testOrder is an object

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
            logging.info("Overwrote File successfully\n")
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
    

