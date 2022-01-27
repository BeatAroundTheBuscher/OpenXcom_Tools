import os

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

def isFile(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x8000 # file
    if stMode == 1:
        return True
    else:
        return False

def isRulFile(path, fileName):
    if ".rul" == fileName[-4:] and isFile(path, fileName):
        return True
    else:
        return False

def isPalFile(path, fileName):
    if ".pal" == fileName[-4:] and isFile(path, fileName):
        return True
    else:
        return False

def isGifFile(path, fileName):
    if ".gif" == fileName[-4:] and isFile(path, fileName):
        return True
    else:
        return False

def populateFileList(path, fileList): # recursive
    for x in os.listdir(path):
        path = addTrailingSlash(path)
        if isFolder(path, x):
            fileList = populateFileList(path+x, fileList)
        elif isRulFile(path, x) or isPalFile(path, x) or isGifFile(path, x):
            fileList.append(path+x)
    return fileList