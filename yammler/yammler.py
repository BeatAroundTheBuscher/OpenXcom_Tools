# python3 yammler.py ~/Games/openxcom_71_40k/user/mods/ROSIGMA/Ruleset ~/Games/openxcom_71_40k/user/mods/40k/Ruleset/

import sys, os
import yaml

print(sys.argv)
# os.chdir(sys.argv[1])

paths = sys.argv[1:]
fileList = []
DEBUG = False

def debugPrint(debugText):
    if DEBUG:
        print(debugText)

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

def isRulFile(path, fileName):
    stMode = os.stat(path + fileName).st_mode
    stMode //= 0x8000 # file
    if ".rul" == fileName[-4:] and stMode == 1:
        return True
    return False


def populateFileList(path): # recursive
    for x in os.listdir(path):
        path = addTrailingSlash(path)
        if isFolder(path, x):
            populateFileList(path+x)
        elif isRulFile(path, x):
            fileList.append(path+x)

print("Searching for Ruleset Files in:")
for path in paths:
    print(path)
    populateFileList(path)

print("Number of Ruleset Files: " + str(len(fileList)))

def tryYamlSafeLoad(fileHandler):
    try:
        return yaml.safe_load(yamlFile)
    except yaml.constructor.ConstructorError:
        print("Constructor Error; Affected file: " + str(fileHandler.name))
        return dict()
    except yaml.composer.ComposerError:
        print("Composer Error; Affected file: " + str(fileHandler.name))
        return dict()

class yamlItemEntry:
    def __init__(self, yamlEntry):
        itemName = self.safeInsert(yamlEntry, "type")
        battleType = self.safeInsert(yamlEntry, "battleType")
        tuAuto = self.safeInsert(yamlEntry, "tuAuto")
        tuSnap = self.safeInsert(yamlEntry, "tuSnap")
        tuAimed = self.safeInsert(yamlEntry, "tuAimed")
        rosigmaComment = self.safeInsert(yamlEntry, "rosigmaComment")

    def safeInsert(self, yamlEntry, key):
        try:
            return yamlEntry[key]
        except KeyError:
            return ""

yamlEntries = []

for filePath in fileList:
    yamlFile = open(filePath, 'r')
    yamlContent = tryYamlSafeLoad(yamlFile)
    debugPrint(filePath)
    debugPrint(yamlContent.keys())
    if "items" in yamlContent.keys():
        print(filePath)
        #print(yamlContent["items"])
        #print(len(yamlContent["items"]))
        #print(type(yamlContent))
        #print(yamlContent.keys())
        for x in yamlContent["items"]:
            if "type" in x.keys():
                print(x["type"])
                print(x)
                yamlEntries.append(yamlItemEntry(x))
        break
    yamlFile.close()

print(yamlEntries)
