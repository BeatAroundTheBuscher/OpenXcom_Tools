# this file needs an folder oxcePalettes in which the content of /common/Palettes/ has been copied into

import os, sys

def addTrailingSlash(path):
    if path[-1] != "/":
        return (path + "/")
    else:
        return path

def isFolder(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x4000 # directory
    if stMode == 1:
        return True
    return False

def isPalFile(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x8000 # file
    if ".pal" == fileName[-4:] and stMode == 1:
        return True
    return False

def populateFileList(path): # recursive
    for x in os.listdir(path):
        path = addTrailingSlash(path)
        if isFolder(path, x):
            populateFileList(path+x)
        elif isPalFile(path, x) and pickedPalette in path:
            fileList.append(path+x)

paths = ["oxcePalettes"]
# pickedPalette = "UFO-JASC-SAFE"
pickedPalette = "UFO-JASC"
fileList = []


for path in paths:
    print(path)
    populateFileList(path)

def getPalette(path):
    palette = []
    print("getPalette for " + path)
    f = open(path, 'r')
    lines = f.readlines()
    f.close()

    # first three lines are metadata
    for x in range(3, 3+256):
        lines[x] = lines[x].replace(" ", ", ")
        if x == 3:
            lines[x] = "(" + lines[x][:-1] + ", 0)" # first one is transparent
        else:
            lines[x] = "(" + lines[x][:-1] + ", 255)" # last symbol of lines[x] is \n
        palette.append(lines[x])

    return palette

for x in fileList:
    palette = getPalette(x)
    print(palette)
    # sys.exit(0)

