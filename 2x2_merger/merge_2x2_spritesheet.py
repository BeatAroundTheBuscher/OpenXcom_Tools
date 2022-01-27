# https://pillow.readthedocs.io/en/stable/reference/Image.html

import sys

from PIL import Image

import drawing_routines

# https://stackoverflow.com/posts/7051075/revisions

tileWidth = 32
tileHeight = 40
# tilesPerRow = 8
# tileRows = 21
tilePieces = []
mergedWidth = 65
mergedHeight = 57




def xcom_crop(inputPNG, width, height):
    img = Image.open(inputPNG)
    imgWidth, imgHeight = img.size
    for y in range(0, imgHeight, height):
        for x in range(0, imgWidth, width):
            box = (x, y, x+width, y+height)
            pic = img.crop(box)
            tilePieces.append(pic)
    return tilePieces

"""
# test putting split parts back to sprite sheet
def recreateSpritesheet(tilePiecesList):
    img = Image.open("template.png") # contains palette
    for listIndex in range(0, len(tilePiecesList)):
        tileX = int(listIndex % tilesPerRow)
        tileY = int(listIndex / tilesPerRow)
        selectedTile = tilePiecesList[listIndex]
        for pixelIndex in range(0, tileWidth*tileHeight):
            relativePixelX = int (pixelIndex % tileWidth)
            relativePixelY = int (pixelIndex / tileWidth)
            pixel = int(selectedTile.getpixel((\
                relativePixelX, relativePixelY)))
            if pixel != 0:
                img.putpixel((\
                    tileX * tileWidth + relativePixelX,\
                    tileY * tileHeight + relativePixelY),\
                    pixel)
    
    return img

img = recreateSpritesheet(tilePieces)
"""



def mergeSpritesheet(readFilePath, tilePiecesList, mergedList, piecesPerRow, x, y):
    img = Image.open(readFilePath) # contains palette
    palette = img.getpalette()
    # https://stackoverflow.com/questions/52307290/what-is-the-difference-between-images-in-p-and-l-mode-in-pil
    img = Image.new('P',(x,y),0) # 'P' for paletted 
    img.putpalette(palette, 'RGB')
    for i in range(0, len(mergedList)):
        # selectedTiles
        tile0 = tilePiecesList[mergedList[i][0]]
        tile1 = tilePiecesList[mergedList[i][1]]
        tile2 = tilePiecesList[mergedList[i][2]]
        tile3 = tilePiecesList[mergedList[i][3]]

        offsetX = int(i % piecesPerRow) * mergedWidth
        offsetY = int(i / piecesPerRow) * mergedHeight

        img = drawPart(img, tile0, offsetX + 16, offsetY + 0)  # top
        img = drawPart(img, tile1, offsetX + 32, offsetY + 8)  # right
        img = drawPart(img, tile2, offsetX + 0, offsetY + 8)   # left
        img = drawPart(img, tile3, offsetX + 16, offsetY + 16) # bottom
    return img

def mergeGunSpritesheet(img, tilePieces, offsetIndex, offsetMax, piecesPerRow, negativeOffsetY):
    for i in range(offsetIndex, offsetMax):
        offsetX = int(i % piecesPerRow) * (tileWidth + 1)
        offsetY = int(i / piecesPerRow) * (tileHeight + 1)
        img = drawPart(img, tilePieces[i], offsetX, offsetY - negativeOffsetY)
    return img

def drawPart(img, selectedTile, offsetX, offsetY):
    for pixelIndex in range(0, tileWidth*tileHeight):
        relativePixelX = int(pixelIndex % tileWidth)
        relativePixelY = int(pixelIndex / tileWidth)
        pixel = int(selectedTile.getpixel((\
            relativePixelX, relativePixelY)))
        if pixel != 0:
            img.putpixel((\
                offsetX + relativePixelX,\
                offsetY + relativePixelY),\
                pixel)
    return img

if len(sys.argv) < 3:
        print("Usage: python merge_png.py file_to_be_merged.png drawingRoutineNumber")
        print("Currently works for drawingRoutine 2, 3, 5, 11, 12, 20 and 21, 22")
        sys.exit(0)

chosenMergedList = []
piecesPerRow = 0
if int(sys.argv[2]) == 2:
    chosenMergedList = drawing_routines.mergedList_DR2 # seems to create artefacts on propulsion
    piecesPerRow = 8
    x, y = 520, 1196
elif int(sys.argv[2]) == 3:
    chosenMergedList = drawing_routines.mergedList_DR3 # seems to create artefacts on propulsion
    piecesPerRow = 8
    x, y = 520, 114
elif int(sys.argv[2]) == 5:
    chosenMergedList = drawing_routines.mergedList_DR5 # looks good
    piecesPerRow = 5
    x, y = 325, 456
elif int(sys.argv[2]) == 11:
    chosenMergedList = drawing_routines.mergedList_DR11 # looks good
    piecesPerRow = 4
    x, y = 264, 1937
elif int(sys.argv[2]) == 12:
    chosenMergedList = drawing_routines.mergedList_DR12 # looks good
    piecesPerRow = 8
    x, y = 520, 57
elif int(sys.argv[2]) == 20:
    chosenMergedList = drawing_routines.mergedList_DR20 # looks good
    piecesPerRow = 5
    x, y = 325, 456
elif int(sys.argv[2]) == 21:
    chosenMergedList = drawing_routines.mergedList_DR21 # looks good
    piecesPerRow = 4
    x, y = 260, 456
elif int(sys.argv[2]) == 22:
    chosenMergedList = drawing_routines.mergedList_DR22 # seems to create artefacts on propulsion
    piecesPerRow = 8
    x, y = 520, 114

if len(chosenMergedList) == 0:
    print("Unsupported drawingRoutine")
    sys.exit(1)

filePath = sys.argv[1]

f = open(filePath, 'rb')
tilePieces = xcom_crop(f, tileWidth, tileHeight) 
f.close()




img = mergeSpritesheet(filePath, tilePieces, chosenMergedList, piecesPerRow, x, y)

if int(sys.argv[2]) == 2:
    piecesPerRow = 8
    negativeOffsetY = 160 - 3
    offsetIndex = 64
    offsetMax = 104
    img = mergeGunSpritesheet(img, tilePieces, offsetIndex, offsetMax, piecesPerRow, negativeOffsetY)

elif int(sys.argv[2]) == 11:
    piecesPerRow = 8
    negativeOffsetY = 400
    offsetIndex = 256
    offsetMax = len(tilePieces)
    img = mergeGunSpritesheet(img, tilePieces, offsetIndex, offsetMax, piecesPerRow, negativeOffsetY)



img.save("merged_" + sys.argv[1])
sys.exit(0)
