# https://pillow.readthedocs.io/en/stable/reference/Image.html

import sys

from PIL import Image

# https://stackoverflow.com/posts/7051075/revisions

tileWidth = 32
tileHeight = 40
# tilesPerRow = 8
# tileRows = 21
tilePieces = []
mergedWidth = 65
mergedHeight = 57



# Tested with Xarquid
mergedList_DR21 = [\
        [0, 4, 8, 12],\
        [1, 5, 9, 13],\
        [2, 6, 10, 14],\
        [3, 7, 11, 15],\
        [16, 20, 24, 28],\
        [17, 21, 25, 29],\
        [18, 22, 26, 30],\
        [19, 23, 27, 31],\
        [32, 36, 40, 44],\
        [33, 37, 41, 45],\
        [34, 38, 42, 46],\
        [35, 39, 43, 47],\
        [48, 52, 56, 60],\
        [49, 53, 57, 61],\
        [50, 54, 58, 62],\
        [51, 55, 59, 63],\
        [64, 68, 72, 76],\
        [65, 69, 73, 77],\
        [66, 70, 74, 78],\
        [67, 71, 75, 79],\
        [80, 84, 88, 92],\
        [81, 85, 89, 93],\
        [82, 86, 90, 94],\
        [83, 87, 91, 95],\
        [96, 100, 104, 108],\
        [97, 101, 105, 109],\
        [98, 102, 106, 110],\
        [99, 103, 107, 111],\
        [112, 116, 120, 124],\
        [113, 117, 121, 125],\
        [114, 118, 122, 126],\
        [115, 119, 123, 127]]

# Tested with Triscene
mergedList_DR20 = [\
        [0, 5, 10, 15],\
        [1, 6, 11, 16],\
        [2, 7, 12, 17],\
        [3, 8, 13, 18],\
        [4, 9, 14, 19],\
        [20, 25, 30, 35],\
        [21, 26, 31, 36],\
        [22, 27, 32, 37],\
        [23, 28, 33, 38],\
        [24, 29, 34, 39],\
        [40, 45, 50, 55],\
        [41, 46, 51, 56],\
        [42, 47, 52, 57],\
        [43, 48, 53, 58],\
        [44, 49, 54, 59],\
        [60, 65, 70, 75],\
        [61, 66, 71, 76],\
        [62, 67, 72, 77],\
        [63, 68, 73, 78],\
        [64, 69, 74, 79],\
        [80, 85, 90, 95],\
        [81, 86, 91, 96],\
        [82, 87, 92, 97],\
        [83, 88, 93, 98],\
        [84, 89, 94, 99],\
        [100, 105, 110, 115],\
        [101, 106, 111, 116],\
        [102, 107, 112, 117],\
        [103, 108, 113, 118],\
        [104, 109, 114, 119],\
        [120, 125, 130, 135],\
        [121, 126, 131, 136],\
        [122, 127, 132, 137],\
        [123, 128, 133, 138],\
        [124, 129, 134, 139],\
        [140, 145, 150, 155],\
        [141, 146, 151, 156],\
        [142, 147, 152, 157],\
        [143, 148, 153, 158],\
        [144, 149, 154, 159]]

# Tested with Hallucinoid
mergedList_DR12 = [\
        [0, 8, 16, 24],\
        [1, 9, 17, 25],\
        [2, 10, 18, 26],\
        [3, 11, 19, 27],\
        [4, 12, 20, 28],\
        [5, 13, 21, 29],\
        [6, 14, 22, 30],\
        [7, 15, 23, 31]]

# Tested with Coelacanth
mergedList_DR11 = [\
        [0, 4, 8, 12],\
        [1, 5, 9, 13],\
        [2, 6, 10, 14],\
        [3, 7, 11, 15],\
        [16, 20, 24, 28],\
        [17, 21, 25, 29],\
        [18, 22, 26, 30],\
        [19, 23, 27, 31],\
        [32, 36, 40, 44],\
        [33, 37, 41, 45],\
        [34, 38, 42, 46],\
        [35, 39, 43, 47],\
        [48, 52, 56, 60],\
        [49, 53, 57, 61],\
        [50, 54, 58, 62],\
        [51, 55, 59, 63],\
        [64, 68, 72, 76],\
        [65, 69, 73, 77],\
        [66, 70, 74, 78],\
        [67, 71, 75, 79],\
        [80, 84, 88, 92],\
        [81, 85, 89, 93],\
        [82, 86, 90, 94],\
        [83, 87, 91, 95],\
        [96, 100, 104, 108],\
        [97, 101, 105, 109],\
        [98, 102, 106, 110],\
        [99, 103, 107, 111],\
        [112, 116, 120, 124],\
        [113, 117, 121, 125],\
        [114, 118, 122, 126],\
        [115, 119, 123, 127],\
        [128, 132, 136, 140],\
        [129, 133, 137, 141],\
        [130, 134, 138, 142],\
        [131, 135, 139, 143],\
        [144, 148, 152, 156],\
        [145, 149, 153, 157],\
        [146, 150, 154, 158],\
        [147, 151, 155, 159],\
        [160, 164, 168, 172],\
        [161, 165, 169, 173],\
        [162, 166, 170, 174],\
        [163, 167, 171, 175],\
        [176, 180, 184, 188],\
        [177, 181, 185, 189],\
        [178, 182, 186, 190],\
        [179, 183, 187, 191],\
        [192, 196, 200, 204],\
        [193, 197, 201, 205],\
        [194, 198, 202, 206],\
        [195, 199, 203, 207],\
        [208, 212, 216, 220],\
        [209, 213, 217, 221],\
        [210, 214, 218, 222],\
        [211, 215, 219, 223],\
        [224, 228, 232, 236],\
        [225, 229, 233, 237],\
        [226, 230, 234, 238],\
        [227, 231, 235, 239],\
        [240, 244, 248, 252],\
        [241, 245, 249, 253],\
        [242, 246, 250, 254],\
        [243, 247, 251, 255]]

# Tested with Sectopod
mergedList_DR5 = [\
        [0, 8, 16, 24],\
        [32, 36, 40, 44],\
        [33, 37, 41, 45],\
        [34, 38, 42, 46],\
        [35, 39, 43, 47],\
        [1, 9, 17, 25],\
        [48, 52, 56, 60],\
        [49, 53, 57, 61],\
        [50, 54, 58, 62],\
        [51, 55, 59, 63],\
        [2, 10, 18, 26],\
        [64, 68, 72, 76],\
        [65, 69, 73, 77],\
        [66, 70, 74, 78],\
        [67, 71, 75, 79],\
        [3, 11, 19, 27],\
        [80, 84, 88, 92],\
        [81, 85, 89, 93],\
        [82, 86, 90, 94],\
        [83, 87, 91, 95],\
        [4, 12, 20, 28],\
        [96, 100, 104, 108],\
        [97, 101, 105, 109],\
        [98, 102, 106, 110],\
        [99, 103, 107, 111],\
        [5, 13, 21, 29],\
        [112, 116, 120, 124],\
        [113, 117, 121, 125],\
        [114, 118, 122, 126],\
        [115, 119, 123, 127],\
        [6, 14, 22, 30],\
        [128, 132, 136, 140],\
        [129, 133, 137, 141],\
        [130, 134, 138, 142],\
        [131, 135, 139, 143],\
        [7, 15, 23, 31],\
        [144, 148, 152, 156],\
        [145, 149, 153, 157],\
        [146, 150, 154, 158],\
        [147, 151, 155, 159]]

# Tested with Cyberdisc
mergedList_DR3 = [\
        [0, 8, 16, 24],\
        [1, 9, 17, 25],\
        [2, 10, 18, 26],\
        [3, 11, 19, 27],\
        [4, 12, 20, 28],\
        [5, 13, 21, 29],\
        [6, 14, 22, 30],\
        [7, 15, 23, 31],\
        [56, 32, 40, 48],\
        [57, 33, 41, 49],\
        [58, 34, 42, 50],\
        [59, 35, 43, 51],\
        [60, 36, 44, 52],\
        [61, 37, 45, 53],\
        [62, 38, 46, 54],\
        [63, 39, 47, 55]]

# Tested with UFO Tank
mergedList_DR2 = [\
        [0, 8, 16, 24],\
        [1, 9, 17, 25],\
        [2, 10, 18, 26],\
        [3, 11, 19, 27],\
        [4, 12, 20, 28],\
        [5, 13, 21, 29],\
        [6, 14, 22, 30],\
        [7, 15, 23, 31],\
        [32, 40, 48, 56],\
        [33, 41, 49, 57],\
        [34, 42, 50, 58],\
        [35, 43, 51, 59],\
        [36, 44, 52, 60],\
        [37, 45, 53, 61],\
        [38, 46, 54, 62],\
        [39, 47, 55, 63],\
        [128, 104, 112, 120],\
        [129, 105, 113, 121],\
        [130, 106, 114, 122],\
        [131, 107, 115, 123],\
        [132, 108, 116, 124],\
        [133, 109, 117, 125],\
        [134, 110, 118, 126],\
        [135, 111, 119, 127]]

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
        print("Currently works for drawingRoutine 2, 3, 5, 11, 12, 20 and 21")
        sys.exit(0)

chosenMergedList = []
piecesPerRow = 0
if int(sys.argv[2]) == 2:
    chosenMergedList = mergedList_DR2 # seems to create artefacts on propulsion
    piecesPerRow = 8
    x, y = 520, 1196
elif int(sys.argv[2]) == 3:
    chosenMergedList = mergedList_DR3 # seems to create artefacts on propulsion
    piecesPerRow = 8
    x, y = 520, 114
elif int(sys.argv[2]) == 5:
    chosenMergedList = mergedList_DR5 # looks good
    piecesPerRow = 5
    x, y = 325, 456
elif int(sys.argv[2]) == 11:
    chosenMergedList = mergedList_DR11 # looks good
    piecesPerRow = 4
    x, y = 264, 1937
elif int(sys.argv[2]) == 12:
    chosenMergedList = mergedList_DR12 # looks good
    piecesPerRow = 8
    x, y = 520, 57
elif int(sys.argv[2]) == 20:
    chosenMergedList = mergedList_DR20 # looks good
    piecesPerRow = 5
    x, y = 325, 456
elif int(sys.argv[2]) == 21:
    chosenMergedList = mergedList_DR21 # looks good
    piecesPerRow = 4
    x, y = 260, 456

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
