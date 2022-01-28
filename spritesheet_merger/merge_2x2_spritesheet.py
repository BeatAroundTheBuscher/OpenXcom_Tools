# test: python3 merge_2x2_spritesheet.py sentinel_heavy_plasma.png 20

import sys
import drawing_routines

sys.path.insert(0, '../commons')
import png_handling as pngH

tilePieces = []
tileWidth = 32
tileHeight = 40
# tilesPerRow = 8
# tileRows = 21
mergedWidth = 65
mergedHeight = 57

if len(sys.argv) < 3:
        print("Usage: python merge_png.py file_to_be_merged.png drawingRoutineNumber")
        print("Currently works for drawingRoutine 2, 3, 5, 11, 12, 20 and 21, 22")
        sys.exit(0)

chosenMergedList = []
piecesPerRow = 0

x, y = 0, 0

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
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces) 
f.close()




img = pngH.mergeSpritesheet(filePath, tileWidth, tileHeight, tilePieces, mergedWidth, mergedHeight, chosenMergedList, piecesPerRow, x, y)

if int(sys.argv[2]) == 2:
    piecesPerRow = 8
    negativeOffsetY = 160 - 3
    offsetIndex = 64
    offsetMax = 104
    img = pngH.mergeGunSpritesheet(img, tileWidth, tileHeight, tilePieces, offsetIndex, offsetMax, piecesPerRow, negativeOffsetY)

elif int(sys.argv[2]) == 11:
    piecesPerRow = 8
    negativeOffsetY = 400
    offsetIndex = 256
    offsetMax = len(tilePieces)
    img = pngH.mergeGunSpritesheet(img, tileWidth, tileHeight, tilePieces, offsetIndex, offsetMax, piecesPerRow, negativeOffsetY)



img.save("merged_" + sys.argv[1])
sys.exit(0)
