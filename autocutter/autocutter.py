import sys
import logging
import datetime

from PIL import Image, ImageDraw

sys.path.insert(0, '.')
import commons.png_handling as pngH  # noqa

# TODO: requires logs folder to be created first
LOG_FILENAME = "./logs/" + (datetime.datetime.now().strftime(
                            '%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')

if len(sys.argv) < 2:
    print("Usage: autocutter.py path-to-image.png")
    sys.exit(0)

filePath = sys.argv[1]


"""
f = open(filePath, 'rb')
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces)
img = pngH.recreateSpritesheet(f, tileWidth, tileHeight, tilePieces, 8)
f.close()

img.save("merged_" + sys.argv[1])
sys.exit(0)
"""


def findTopLeft(img):
    imgWidth, imgHeight = img.size
    startPoint = (0, 0)
    endPoint = (0, 0)

    for startY in range(0, imgHeight - 1):
        for currentY in range(0, startY):
            currentX = (startY - currentY) * 2
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX + 1, currentY)) != 0:
                return startPoint, endPoint

        pixelsToBottom, pixelsToRight = pixelSanityCheck(img, startY)
        startPoint = (0, startY)
        # TODO: is that X sane?
        endPoint = (1 + (imgHeight - pixelsToBottom) * 2, 0)
    return startPoint, endPoint


def findTopRight(img):
    imgWidth, imgHeight = img.size
    startPoint = (0, 0)
    endPoint = (0, 0)

    for startY in range(0, imgHeight - 1):
        for currentY in range(0, startY):
            currentX = currentX = imgWidth - 1 - (currentY - startY) * (-2)
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX - 1, currentY)) != 0:
                return startPoint, endPoint

        pixelsToBottom, pixelsToLeft = pixelSanityCheck(img, startY)
        startPoint = (imgWidth, startY)
        # TODO: is that X sane?
        endPoint = (pixelsToBottom, 0)
    return startPoint, endPoint


def findBottomLeft(img):
    imgWidth, imgHeight = img.size
    startPoint = (0, 0)
    endPoint = (0, 0)

    for startY in range(imgHeight - 1, 0, -1):
        for currentY in range(startY, imgHeight - 1):
            currentX = (startY - currentY) * (-2)
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX + 1, currentY)) != 0:
                return startPoint, endPoint

        pixelsToBottom, pixelsToRight = pixelSanityCheck(img, startY)
        startPoint = (0, startY)
        endPoint = (1 + pixelsToRight, startY + pixelsToBottom)
    return startPoint, endPoint


# TODO: Figure out how to fix that one line too few
def findBottomRight(img):
    imgWidth, imgHeight = img.size
    startPoint = (0, 0)
    endPoint = (0, 0)

    for startY in range(imgHeight - 1, 0, -1):
        for currentY in range(startY, imgHeight - 1):
            currentX = imgWidth - 1 - (currentY - startY) * 2
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX - 1, currentY)) != 0:
                return startPoint, endPoint

        pixelsToBottom, pixelsToLeft = pixelSanityCheck(img, startY)
        startPoint = (imgWidth, startY)
        endPoint = (imgWidth - pixelsToLeft, startY + pixelsToBottom)
    return startPoint, endPoint


def pixelSanityCheck(img, startY):
    imgWidth, imgHeight = img.size
    # pixelsToTop = startY
    pixelsToBottom = imgHeight - 1 - startY
    pixelToSide = pixelsToBottom * 2
    if pixelToSide > imgWidth:
        pixelToSide = imgWidth
        pixelsToBottom = imgWidth / 2

    return pixelsToBottom, pixelToSide


def drawMulticolorLine(img, startPoint, endPoint):
    if startPoint[1] % 3 == 0:
        lineColor = "red"
    elif startPoint[1] % 3 == 1:
        lineColor = "blue"
    else:
        lineColor = "green"

    draw = ImageDraw.Draw(img)
    draw.line([startPoint, endPoint], fill=lineColor, width=1)


def showSingle(img, tLeftCoord1, tLeftCoord2, tRightCoord1, tRightCoord2,
               bLeftCoord1, bLeftCoord2, bRightCoord1, bRightCoord2):
    drawMulticolorLine(img, tLeftCoord1, tLeftCoord2)
    drawMulticolorLine(img, tRightCoord1, tRightCoord2)
    drawMulticolorLine(img, bLeftCoord1, bLeftCoord2)
    drawMulticolorLine(img, bRightCoord1, bRightCoord2)


def showGrid(img, bLeftCoord1, bLeftCoord2, bRightCoord1, bRightCoord2):
    imgWidth, imgHeight = img.size
    for x in range(0, int(imgWidth/16)+1):
        drawMulticolorLine(img, bLeftCoord1, bLeftCoord2)
        bLeftCoord1 = (bLeftCoord1[0], bLeftCoord1[1] - 16)
        bLeftCoord2 = (bLeftCoord2[0] + 32, bLeftCoord2[1])
        print("bLeftCoord1: " + str(bLeftCoord1))
        print("bLeftCoord2: " + str(bLeftCoord2))

    for x in range(0, int(imgHeight/8)+1):
        drawMulticolorLine(img, bRightCoord1, bRightCoord2)
        bRightCoord1 = (bRightCoord1[0], bRightCoord1[1] - 16)
        bRightCoord2 = (bRightCoord2[0] - 32, bRightCoord2[1])
        print("bRightCoord1: " + str(bRightCoord1))
        print("bRightCoord2: " + str(bRightCoord2))


f = open(filePath, 'rb')
img = Image.open(f)
tLeftCoord1, tLeftCoord2 = findTopLeft(img)
tRightCoord1, tRightCoord2 = findTopRight(img)
bLeftCoord1, bLeftCoord2 = findBottomLeft(img)
bRightCoord1, bRightCoord2 = findBottomRight(img)
# bLeftCoord1 = (0, 72)
# bLeftCoord2 = (0, 72)
# bRightCoord1 = (104, 72)
# bRightCoord2 = (104, 72)
showSingle(img, tLeftCoord1, tLeftCoord2,
           tRightCoord1, tRightCoord2,
           bLeftCoord1, bLeftCoord2,
           bRightCoord1, bRightCoord2)
# showGrid(img, bLeftCoord1, bLeftCoord2, bRightCoord1, bRightCoord2)
f.close()
img.save("line_image.png")


"""
tilePieces = []
tileWidth = 32
tileHeight = 40

f = open(filePath, 'rb')
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces)
img = pngH.recreateSpritesheet(f, tileWidth, tileHeight, tilePieces, 8)
img.save("merged_" + sys.argv[1])
"""


# img.show()
