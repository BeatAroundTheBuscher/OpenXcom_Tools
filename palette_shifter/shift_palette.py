# test: python3 shift_palette.py merged_sentinel_heavy_plasma.png replace 4 8

# https://pillow.readthedocs.io/en/stable/reference/Image.html

import sys

from PIL import Image


if len(sys.argv) < 3:
        print("Usage: python shift_palette.py file_to_be_shifted.png command[show|replace] previous_palette_group new_palette_group")
        sys.exit(0)


filePath = sys.argv[1]
command = sys.argv[2]


f = open(filePath, 'rb')
f.close()


img = Image.open(filePath)
palette = img.getpalette()
imgWidth, imgHeight = img.size


for pixelIndex in range(0, imgWidth*imgHeight):
    PixelX = int(pixelIndex % imgWidth)
    PixelY = int(pixelIndex / imgWidth)
    pixel = int(img.getpixel((PixelX, PixelY)))

    if command == "show":
        currentGroup = pixel // 16
        currentGroupIndex = pixel % 16
        if (currentGroup != 0 and currentGroupIndex != 0):
            print("X: {} - Y: {} - GroupIndex: {} - Index % 16: {}".format(PixelX, PixelY, currentGroup, currentGroupIndex))

    elif command == "replace":
        if len(sys.argv) < 5:
            print("insufficient arguments for replace")
            sys.exit(1)
        previousGroup = int(sys.argv[3])
        newGroup = int(sys.argv[4])
        currentGroup = pixel // 16
        currentGroupIndex = pixel % 16
        # print(previousGroup, newGroup, currentGroup)
        if currentGroup == previousGroup:
            currentGroup = newGroup
            pixel = int(currentGroup * 16 + currentGroupIndex)
            print(pixel)
            # print((PixelX, PixelY), pixel)
        if pixel != 0:
            img.putpixel((PixelX, PixelY), pixel)

if command == "replace":
    img.save("shifted_" + sys.argv[1][:-3] + "png", format="png")

sys.exit(0)

