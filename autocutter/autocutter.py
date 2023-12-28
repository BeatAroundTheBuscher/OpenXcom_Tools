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
tilePieces = []
tileWidth = 32
tileHeight = 40

f = open(filePath, 'rb')
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces)
img = pngH.recreateSpritesheet(f, tileWidth, tileHeight, tilePieces, 8)
f.close()

img.save("merged_" + sys.argv[1])
sys.exit(0)
"""


def findBottomLeft(img):
    imgWidth, imgHeight = img.size

    startPoint = (0, 0)
    endPoint = (0, 0)

    # 2 steps right, 1 step down
    for startY in range(imgHeight - 1, 0, -1):
        drawBool = True
        # x can be at most pixelToBottom * 2
        # canvas (0, 0) is top left

        # y = y0 * -0.5 * x
        # x = (y0 - y) * -2
        # y0: startY    y: currentY

        for currentY in range(startY, imgHeight - 1):
            currentX = (startY - currentY) * (-2)
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX + 1, currentY)) != 0:
                drawBool = False
                return startPoint, endPoint

        if drawBool:
            # drawing the lines between two points
            pixelsToBottom = imgHeight - 1 - startY
            pixelsToRight = pixelsToBottom * 2
            if pixelsToRight > imgWidth:
                pixelsToRight = imgWidth
                pixelsToBottom = imgWidth / 2
            startPoint = (0, startY)
            endPoint = (1 + pixelsToRight, startY + pixelsToBottom)
            # drawMulticolorLine(img, startPoint, endPoint)
    return startPoint, endPoint


def findBottomRight(inputPNG):
    imgWidth, imgHeight = img.size

    startPoint = (0, 0)
    endPoint = (0, 0)

    # 2 steps left, 1 step down
    for startY in range(imgHeight - 1, 0, -1):
        drawBool = True

        # y = y0 * -0.5 * (x_max - x)
        # x = x_max - (y0 - y) * 2
        # y0: startY    y: currentY

        for currentY in range(startY, imgHeight - 1):
            currentX = imgWidth - 1 - (currentY - startY) * 2
            if img.getpixel((currentX, currentY)) != 0 or\
               img.getpixel((currentX - 1, currentY)) != 0:
                drawBool = False
                return startPoint, endPoint

        if drawBool:
            # drawing the lines between two points
            pixelsToBottom = imgHeight - 1 - startY
            pixelsToLeft = pixelsToBottom * 2
            if pixelsToLeft > imgWidth:
                pixelsToLeft = imgWidth
                pixelsToBottom = imgWidth / 2
            startPoint = (imgWidth, startY)
            endPoint = (imgWidth - pixelsToLeft, startY + pixelsToBottom)
            # drawMulticolorLine(img, startPoint, endPoint)
    return startPoint, endPoint


def drawMulticolorLine(img, startPoint, endPoint):
    if startPoint[1] % 3 == 0:
        lineColor = "red"
    elif startPoint[1] % 3 == 1:
        lineColor = "blue"
    else:
        lineColor = "green"

    draw = ImageDraw.Draw(img)
    draw.line([startPoint, endPoint], fill=lineColor, width=1)


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
bLeftCoord1, bLeftCoord2 = findBottomLeft(img)
bRightCoord1, bRightCoord2 = findBottomRight(img)
bLeftCoord1 = (0, 72)
bLeftCoord2 = (0, 72)
bRightCoord1 = (104, 72)
bRightCoord2 = (104, 72)
showGrid(img, bLeftCoord1, bLeftCoord2, bRightCoord1, bRightCoord2)
f.close()

img.save("line_image.png")
# img.show()

