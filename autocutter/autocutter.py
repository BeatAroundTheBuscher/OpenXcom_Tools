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
    print("Usage: fix_palette.py path-to-image.png")
    sys.exit(0)

filePath = sys.argv[1]

tilePieces = []
tileWidth = 32
tileHeight = 40

f = open(filePath, 'rb')
tilePieces = pngH.xcom_crop(f, tileWidth, tileHeight, tilePieces)
img = pngH.recreateSpritesheet(f, tileWidth, tileHeight, tilePieces, 8)
f.close()

img.save("merged_" + sys.argv[1])
sys.exit(0)
