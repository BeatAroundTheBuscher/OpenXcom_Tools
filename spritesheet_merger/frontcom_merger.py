import sys
import os
import drawing_routines
from PIL import Image

sys.path.append(os.getcwd())
import commons.png_handling as pngH  # noqa

tilePiecesUnit = []
tilePiecesHandob = []
tileWidth = 32
tileHeight = 40


filePathUnit = sys.argv[1]
filePathHandob = sys.argv[2]
drawingRoutine = sys.argv[3]
standHeight = int(sys.argv[4])

f = open(filePathUnit, 'rb')
pngH.xcom_crop(f, tileWidth, tileHeight, tilePiecesUnit)
f.close()

f = open(filePathHandob, 'rb')
pngH.xcom_crop(f, tileWidth, tileHeight, tilePiecesHandob)
f.close()

img = Image.open(filePathUnit)  # contains palette
palette = img.getpalette()
img = Image.new('P', (256, 40), 0)  # 'P' for paletted
img.putpalette(palette, 'RGB')  # type: ignore

for i in range(0, 8): # NE_, E, SE, S, SW, W, NW_, N_
    if i == 0 or i == 6 or i == 7: # draw handob first
        print("draw handob first")
        img = pngH.drawPart(img, tilePiecesHandob[i], 32, 40, 32*i, standHeight)
        for j in range(2, 5):
            img = pngH.drawPart(img, tilePiecesUnit[i+8*j], 32, 40, 32*i, 0)
        img = pngH.drawPart(img, tilePiecesUnit[i+8*30], 32, 40, 32*i, 0) # left arm
        img = pngH.drawPart(img, tilePiecesUnit[i+8*31], 32, 40, 32*i, 0) # right arm
    else: # draw handob last
        for j in range(2, 5):
            img = pngH.drawPart(img, tilePiecesUnit[i+8*j], 32, 40, 32*i, 0)
        img = pngH.drawPart(img, tilePiecesUnit[i+8*30], 32, 40, 32*i, 0) # left arm
        img = pngH.drawPart(img, tilePiecesUnit[i+8*31], 32, 40, 32*i, 0) # right arm
        img = pngH.drawPart(img, tilePiecesHandob[i], 32, 40, 32*i, standHeight)
        print("draw handob last")


img.save("merged_" + filePathUnit + "_" + filePathHandob )

# https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio/451580#451580
base_width = 64
wpercent = (base_width / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((base_width, hsize), resample=Image.LANCZOS)
img.save("resized" + filePathUnit + "_" + filePathHandob )

sys.exit(0)