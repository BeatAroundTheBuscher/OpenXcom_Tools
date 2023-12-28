import sys
import logging
import datetime

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


def findBottomLeft(inputPNG):
    from PIL import Image, ImageDraw
    img = Image.open(inputPNG)
    imgWidth, imgHeight = img.size
    """
    count = 0
    count_zero = 0
    for x in range(0, imgWidth):
        for y in range(0, imgHeight):
            if img.getpixel((x, y)) != 0:
                count += 1
                print(x, y, img.getpixel((x, y)))
            else:
                count_zero += 1
    print("Count: " + str(count))
    print("Count Zero: " + str(count_zero))
    """

    # 2 steps right, 1 step down
    for startY in range(imgHeight - 1, 0, -1):
        lineColor = "black"
        # x can be at most pixelToBottom * 2
        # canvas (0, 0) is top left
        pixelsToBottom = imgHeight - 1 - startY
        pixelsToRight = pixelsToBottom * 2
        if pixelsToRight > imgWidth:
            pixelsToRight = imgWidth
            pixelsToBottom = imgWidth / 2

        # this scans cubicly and not in forms of triangles
        """
        for x in range(0, pixelsToRight, 2):
            if img.getpixel((x, startY)) != 0 or img.getpixel((x + 1, startY)) != 0:
                lineColor = "red"
                print("red for: " + str(x) + ":" + str(startY) + "\t" +
                        "pixelsToRight: " + str(pixelsToRight) + "\t" +
                        "First Pixel: " + str(img.getpixel((x, startY))) + "\t"
                        "Second Pixel: " + str(img.getpixel((x + 1, startY))))
                break
        """

        # y = y0 * -0.5 * x
        # x = (y0 - y) * -2
        # y0: startY    y: currentY

        for currentY in range(startY, imgHeight - 1):
            currentX = (startY - currentY) * (-2)
            if img.getpixel((currentX, currentY)) != 0 or img.getpixel((currentX + 1, currentY)) != 0:
                lineColor = ""
                print("red for: " + str(currentX) + ":" + str(currentY) + "\t" +
                      "pixelsToRight: " + str(pixelsToRight) + "\t" +
                      "First Pixel: " + str(img.getpixel((currentX, currentY))) + "\t"
                      "Second Pixel: " + str(img.getpixel((currentX + 1, currentY))))
                break

        startPoint = (0, startY)
        endPoint = (1 + pixelsToRight, startY + pixelsToBottom)

        if lineColor != "":

            if startY % 4 == 0:
                lineColor = "black"
            elif startY % 4 == 1:
                lineColor = "blue"
            else:
                lineColor = "green"

            draw = ImageDraw.Draw(img)
            draw.line([startPoint, endPoint], fill=lineColor, width=1)
            print("startPoint: " + str(startPoint[0]) + ":" + str(startPoint[1]))
            print("endPoint: " + str(endPoint[0]) + ":" + str(endPoint[1]) + "\ty: " + str(startY) + "\tpixelsToBottom: " + str(pixelsToBottom))

    img.save("line_image.png")
    # img.show()

        






f = open(filePath, 'rb')
findBottomRight(f)
