# https://pillow.readthedocs.io/en/stable/reference/Image.html
# https://stackoverflow.com/posts/7051075/revisions

from PIL import Image
import logging
import png
import re
import commons.oxcePalettes as oxcePal


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
            # first one is transparent
            lines[x] = "(" + lines[x][:-1] + ", 0)"
        else:
            # last symbol of lines[x] is \n
            lines[x] = "(" + lines[x][:-1] + ", 255)"
        palette.append(lines[x])

    return palette


def guessPalette(metadata):
    # confidence is determined by checking 17 of 256 colors
    # the picked colors are the diagonal from NE to SW
    # should be good enough for approximation

    if len(metadata["palette"]) != 256:
        logging.error("Image does not have a palette with 256 colors")
        raise ValueError("Image does not have a palette with 256 colors")
        return None

    testVector = [oxcePal.paletteBattleScapeUFO,
                  oxcePal.paletteUfopaediaUFO,
                  oxcePal.paletteBaseScapeUFO,
                  oxcePal.paletteGeoScapeUFO,
                  oxcePal.paletteBattlePediaUFO,
                  oxcePal.paletteGraphsUFO,
                  oxcePal.paletteBattleCommonUFO,
                  oxcePal.paletteBackgroundUFO]

    for test in testVector:
        confidence = 0
        for i in [15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195,
                  210, 225, 240, 255]:
            logging.debug("test value: " + str(test.paletteData[i]))
            logging.debug("palette value: " + str(metadata["palette"][i]))
            if test.paletteData[i][0:3] == metadata["palette"][i][0:3]:
                confidence += 1
        logging.debug("\nConfidence: " + str(confidence))

        if confidence > 13:  # of 17
            logging.info("Guessed Palette: " + test.name)
            return test.paletteData

    logging.info("Failed to guess palette")
    raise ValueError("No known palette")
    return None


def fixPalette(filePath):
    logging.info("Running filePath: " + filePath)

    filePath = re.sub("\\n", "", filePath)
    try:
        pngReader = png.Reader(filename=filePath)
        w, h, pixels, metadata = pngReader.read_flat()

        guessedPalette = guessPalette(metadata)  # 1CH.png

        found = 0  # needs a cleaner way

        # TODO: Scan for what the oxce log actually says
        if pngReader.trns is not None:
            for x in pngReader.trns:
                if x == 0:
                    break
                found += 1

            logging.info("Wrong Transparent Index found at: " + str(found))
            if found == 0:
                logging.warning("Wrong Transparent Index SHOULD NOT BE 0")

        if found != 0:
            # change picture to set palette index 0 for background
            for x in range(0, len(pixels)):
                if pixels[x] == found:
                    pixels[x] = 0

        logging.debug("Removing 'physical' key from 'metadata'")
        if "physical" in metadata.keys():
            metadata.pop("physical")

        if guessedPalette is not None:
            metadata["palette"] = guessedPalette

            output = open(filePath, 'wb')  # save result
            writer = png.Writer(w, h, **metadata)
            writer.write_array(output, pixels)
            output.close()
            logging.info("Overwrote File successfully\n")
            return True
        else:
            return False

    except FileNotFoundError:  # may hide other errors
        logging.warning("Failed with FileNotFoundError " + filePath)
        return False
    except TypeError as e:
        logging.warning("Failed with TypeError " + filePath)
        logging.warning(e)
        return False
    except png.FormatError:
        logging.warning("Failed with png.FormatError " + filePath)
        return False
    except ValueError:  # contains custom raises
        logging.warning("Failed with ValueError " + filePath)
        return False


def xcom_crop(inputPNG, width, height, tilePieces):
    img = Image.open(inputPNG)
    imgWidth, imgHeight = img.size
    for y in range(0, imgHeight, height):
        for x in range(0, imgWidth, width):
            box = (x, y, x+width, y+height)
            pic = img.crop(box)
            tilePieces.append(pic)
    return tilePieces


def prepareOutputFile(readFilePath, sheetSizeX, sheetSizeY):
    img = Image.open(readFilePath)  # contains palette
    palette = img.getpalette()
    # https://stackoverflow.com/questions/52307290/what-is-the-difference-between-images-in-p-and-l-mode-in-pil
    img = Image.new('P', (sheetSizeX, sheetSizeY), 0)  # 'P' for paletted
    # TODO: Figure out how to set palette properly
    img.putpalette(palette, 'RGB')  # type: ignore

    return img


# test putting split parts back to sprite sheet
def recreateSpritesheet(readFilePath, tileWidth, tileHeight,
                        tilePiecesList, tilesPerRow):
    img = prepareOutputFile(readFilePath, 1000, 1000)
    for listIndex in range(0, len(tilePiecesList)):
        tileX = int(listIndex % tilesPerRow)
        tileY = int(listIndex / tilesPerRow)
        selectedTile = tilePiecesList[listIndex]
        for pixelIndex in range(0, tileWidth*tileHeight):
            relativePixelX = int(pixelIndex % tileWidth)
            relativePixelY = int(pixelIndex / tileWidth)
            pixel = int(selectedTile.getpixel((
                relativePixelX, relativePixelY)))
            if pixel != 0:
                img.putpixel((tileX * tileWidth + relativePixelX,
                              tileY * tileHeight + relativePixelY),
                             pixel)

    return img


def mergeSpritesheet(readFilePath, tileWidth, tileHeight, tilePiecesList,
                     mergedWidth, mergedHeight, mergedList, piecesPerRow,
                     sheetSizeX, sheetSizeY):
    img = prepareOutputFile(readFilePath, sheetSizeX, sheetSizeY)
    for i in range(0, len(mergedList)):
        # selectedTiles
        tile0 = tilePiecesList[mergedList[i][0]]
        tile1 = tilePiecesList[mergedList[i][1]]
        tile2 = tilePiecesList[mergedList[i][2]]
        tile3 = tilePiecesList[mergedList[i][3]]

        offsetX = int(i % piecesPerRow) * mergedWidth
        offsetY = int(i / piecesPerRow) * mergedHeight

        img = drawPart(img, tile0, tileWidth, tileHeight,
                       offsetX + 16, offsetY + 0)       # top
        img = drawPart(img, tile1, tileWidth, tileHeight,
                       offsetX + 32, offsetY + 8)       # right
        img = drawPart(img, tile2, tileWidth, tileHeight,
                       offsetX + 0, offsetY + 8)        # left
        img = drawPart(img, tile3, tileWidth, tileHeight,
                       offsetX + 16, offsetY + 16)      # bottom
    return img


def mergeGunSpritesheet(img, tileWidth, tileHeight, tilePieces, offsetIndex,
                        offsetMax, piecesPerRow, negativeOffsetY):
    for i in range(offsetIndex, offsetMax):
        offsetX = int(i % piecesPerRow) * (tileWidth + 1)
        offsetY = int(i / piecesPerRow) * (tileHeight + 1)
        img = drawPart(img, tilePieces[i], tileWidth, tileHeight, offsetX,
                       offsetY - negativeOffsetY)
    return img


def drawPart(img, selectedTile, tileWidth, tileHeight, offsetX, offsetY):
    for pixelIndex in range(0, tileWidth*tileHeight):
        relativePixelX = int(pixelIndex % tileWidth)
        relativePixelY = int(pixelIndex / tileWidth)
        pixel = int(selectedTile.getpixel((
            relativePixelX, relativePixelY)))
        if pixel != 0:
            img.putpixel((
                offsetX + relativePixelX,
                offsetY + relativePixelY),
                pixel)
    return img
