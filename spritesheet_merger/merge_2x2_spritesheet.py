# test: python3 merge_2x2_spritesheet.py sentinel_heavy_plasma.png 20

import sys
import drawing_routines

import commons.png_handling as pngH

tilePieces = []
tileWidth = 32
tileHeight = 40
# tilesPerRow = 8
# tileRows = 21
mergedWidth = 65
mergedHeight = 57

if len(sys.argv) < 3:
    print("Usage: python merge_png.py file_to_be_merged.png drawingRoutineNumber")  # noqa
    print("Currently works for drawingRoutine 2, 3, 5, 11, 12, 20 and 21, 22")
    sys.exit(0)

chosenMergedList = []
piecesPerRow = 0

x, y = 0, 0

if int(sys.argv[2]) == 2:
    # seems to create artefacts on propulsion
    chosenMergedList = drawing_routines.mergedList_DR2
    piecesPerRow = 8
    x, y = 520, 1196

elif int(sys.argv[2]) == 3:
    # seems to create artefacts on propulsion
    chosenMergedList = drawing_routines.mergedList_DR3
    piecesPerRow = 8
    x, y = 520, 114

elif int(sys.argv[2]) == 5:
    # looks good
    chosenMergedList = drawing_routines.mergedList_DR5
    piecesPerRow = 5
    x, y = 325, 456

elif int(sys.argv[2]) == 11:
    # looks good
    chosenMergedList = drawing_routines.mergedList_DR11
    piecesPerRow = 4
    x, y = 264, 1937

elif int(sys.argv[2]) == 12:
    # looks good
    chosenMergedList = drawing_routines.mergedList_DR12
    piecesPerRow = 8
    x, y = 520, 57
elif int(sys.argv[2]) == 20:
    # looks good
    chosenMergedList = drawing_routines.mergedList_DR20
    piecesPerRow = 5
    x, y = 325, 456
elif int(sys.argv[2]) == 21:
    # looks good
    chosenMergedList = drawing_routines.mergedList_DR21
    piecesPerRow = 4
    x, y = 260, 456
elif int(sys.argv[2]) == 22:
    # seems to create artefacts on propulsion
    chosenMergedList = drawing_routines.mergedList_DR22
    piecesPerRow = 8
    x, y = 520, 114

if len(chosenMergedList) == 0:
    print("Unsupported drawingRoutine")
    sys.exit(1)

filePath = sys.argv[1]

f = open(filePath, 'rb')
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces)
f.close()


img = pngH.mergeSpritesheet(filePath, tileWidth, tileHeight, tilePieces,
                            mergedWidth, mergedHeight, chosenMergedList,
                            piecesPerRow, x, y)

if int(sys.argv[2]) == 2:
    piecesPerRow = 8
    negativeOffsetY = 160 - 3
    offsetIndex = 64
    offsetMax = 104
    img = pngH.mergeGunSpritesheet(img, tileWidth, tileHeight, tilePieces,
                                   offsetIndex, offsetMax, piecesPerRow,
                                   negativeOffsetY)

elif int(sys.argv[2]) == 11:
    piecesPerRow = 8
    negativeOffsetY = 400
    offsetIndex = 256
    offsetMax = len(tilePieces)
    img = pngH.mergeGunSpritesheet(img, tileWidth, tileHeight, tilePieces,
                                   offsetIndex, offsetMax, piecesPerRow,
                                   negativeOffsetY)


img.save("merged_" + sys.argv[1])
sys.exit(0)
