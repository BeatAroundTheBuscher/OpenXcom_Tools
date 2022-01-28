import os


def addTrailingSlash(path):
    if path[-1] != "/":
        return (path + "/")
    else:
        return path


def isFolder(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x4000  # directory
    if stMode == 1:
        return True
    return False


def isFile(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x8000  # file
    if stMode == 1:
        return True
    else:
        return False


def isCorrectFileExtension(fileName, fileExtensions):
    found = False
    for ext in fileExtensions:
        print(-(len(ext)))
        if fileName[-(len(ext)):] == ext:
            found = True
    return found


def populateFileList(path, fileList, fileExtensions):  # recursive
    for x in os.listdir(path):
        path = addTrailingSlash(path)
        if isFolder(path, x):
            fileList = populateFileList(path+x, fileList, fileExtensions)
        elif isFile(path, x) and isCorrectFileExtension(x, fileExtensions):
            fileList.append(path+x)
    return fileList
