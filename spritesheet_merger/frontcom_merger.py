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
drawingRoutine = int(sys.argv[3])
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


if drawing_routines == 0 or drawingRoutine == 1:
    for i in range(0, 8): # NE_, E, SE, S, SW, W, NW_, N_
        if i == 0 or i == 6 or i == 7: # draw handob first
            img = pngH.drawPart(img, tilePiecesHandob[i], 32, 40, 32*i, standHeight)
            img = pngH.drawPart(img, tilePiecesUnit[i+8*30], 32, 40, 32*i, 0) # left arm
            img = pngH.drawPart(img, tilePiecesUnit[i+8*31], 32, 40, 32*i, 0) # right arm
            for j in [2, 4]: # torso+legs; 3 is kneeling
                img = pngH.drawPart(img, tilePiecesUnit[i+8*j], 32, 40, 32*i, 0)
            

        else: # draw handob last
            for j in [2, 4]: # torso+legs; 3 is kneeling
                img = pngH.drawPart(img, tilePiecesUnit[i+8*j], 32, 40, 32*i, 0)
            img = pngH.drawPart(img, tilePiecesUnit[i+8*30], 32, 40, 32*i, 0) # left arm
            img = pngH.drawPart(img, tilePiecesUnit[i+8*31], 32, 40, 32*i, 0) # right arm
            img = pngH.drawPart(img, tilePiecesHandob[i], 32, 40, 32*i, standHeight)


    img.save("merged_" + filePathUnit + "_" + filePathHandob )

    tilePiecesUnit = []
    f = open("merged_" + filePathUnit + "_" + filePathHandob, 'rb')
    pngH.xcom_crop(f, tileWidth, tileHeight, tilePiecesUnit)
    f.close()



    base_width = 16 # from 32
    wpercent = (base_width / float(tilePiecesUnit[0].size[0]))
    hsize = int((float(tilePiecesUnit[0].size[1]) * float(wpercent)))

    img = Image.new('P', (256, 40), 0)  # 'P' for paletted
    img.putpalette(palette, 'RGB')  # type: ignore
    
    for i in range(0, 8):
        tilePiecesUnit[i] = tilePiecesUnit[i].resize((base_width, hsize), resample=Image.LANCZOS)
        img = pngH.drawPart(img, tilePiecesUnit[i], base_width, hsize, 32*i, 0)
        img = pngH.drawPart(img, tilePiecesUnit[i], base_width, hsize, 16+32*i, 0)
        img = pngH.drawPart(img, tilePiecesUnit[i], base_width, hsize, 32*i, 20)
        img = pngH.drawPart(img, tilePiecesUnit[i], base_width, hsize, 16+32*i, 20)
        img = pngH.drawPart(img, tilePiecesUnit[i], base_width, hsize, 8+32*i, 10)


    # https://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio/451580#451580
    
    

    img.save("resized_" + filePathUnit + "_" + filePathHandob )

sys.exit(0)