import png, re
import sys

import oxcePalettes

def fixPalette(filePath):
    filePath = re.sub("\\n", "", filePath)
    try:
        pngReader = png.Reader(filename=filePath)
        w, h, pixels, metadata = pngReader.read_flat()
    
        found = 0 # needs a cleaner way

        for x in pngReader.trns:
            if x == 0:
                break
            found += 1

        print("Wrong Transparent Index found at: " + str(found))

        for x in range(0, len(pixels)):
            if pixels[x] == found:
                pixels[x] = 0

        if "physical" in metadata.keys():
            metadata.pop("physical")

        # some kind of checker to determine which palette the rest uses
        metadata["palette"] = oxcePalettes.battlePalette


        output = open(filePath, 'wb')
        writer = png.Writer(w, h, **metadata)
        writer.write_array(output, pixels)
        output.close()
        return True

    except FileNotFoundError:
        print("Failed for " + filePath)
        return False
    except TypeError:
        print("Failed for " + filePath)
        return False
    except png.FormatError:
        print("Failed for " + filePath)
        return False



if len(sys.argv) < 3:
        print("Usage: fix_palette.py path-to-openxcom.log path-to-mod-root-dictionary")
        sys.exit(0)

log = open(sys.argv[1], "r")
loglines = log.readlines()

filePaths = []

for line in loglines:
    if "has incorrect transparent color index" in line:
        line = re.sub("^.*WARN\]\\sImage\\s", "", line)
        line = re.sub("\\s\(.*$", "", line)
        filePaths.append(sys.argv[2] + "/" + line)

for x in filePaths:
    print(x)
    fixPalette(x)



sys.exit(0) # return how many were changed

# http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html

pngReader = png.Reader(filename='ADEPTASNBlessedNurgling.png')
w, h, pixels, metadata = pngReader.read_flat()

found = 0 # needs a cleaner way

for x in pngReader.trns:
    if x == 0:
        break
    found += 1

print("Wrong Transparent Index found at: " + str(found))

for x in range(0, len(pixels)):
    if pixels[x] == found:
        pixels[x] = 0

if "physical" in metadata.keys():
    metadata.pop("physical")

# some kind of checker to determine which palette the rest uses
metadata["palette"] = oxcePalettes.battlePalette


output = open('image-with-red-dot.png', 'wb')
writer = png.Writer(w, h, **metadata)
writer.write_array(output, pixels)
output.close()
sys.exit(0)

