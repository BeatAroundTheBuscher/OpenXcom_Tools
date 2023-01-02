# test: python3 yammler.py ~/Games/openxcom_71_40k/user/mods/ROSIGMA/Ruleset ~/Games/openxcom_71_40k/user/mods/40k/Ruleset/  # noqa

import sys
import yaml
import yaml.composer

import logging
import datetime

sys.path.insert(0, '../commons')
import file_handling as fH  # noqa

if len(sys.argv) < 2:
    print("Usage: yammler.py path-to-mod-root-dictionary")  # noqa
    sys.exit(0)

# TODO: have to create a logs folder
LOG_FILENAME = "./logs/" + (datetime.datetime.now().strftime(
                            '%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')

print(sys.argv)
# os.chdir(sys.argv[1])

paths = sys.argv[1:]
fileList = []

"""
DEBUG = False

def debugPrint(debugText):
    if DEBUG:
        print(debugText)
"""


print("Searching for Ruleset Files in:")
for path in paths:
    print(path)
    fileList = fH.populateFileList(path, fileList, [".rul"])

print("Number of Ruleset Files: " + str(len(fileList)))


def yamlAdd(loader, node):
    pass
    return ""

def yamlRemove(loader, node):
    print("yamlRemover")
    print(loader)
    print(node)
    return ""

# https://stackoverflow.com/questions/45966633/yaml-error-could-not-determine-a-constructor-for-the-tag
# https://www.programcreek.com/python/example/11269/yaml.add_constructor
# https://python.hotexamples.com/examples/yaml/Loader/add_constructor/python-loader-add_constructor-method-examples.html

yaml.SafeLoader.add_constructor('!add', yamlRemove)
yaml.SafeLoader.add_constructor('!remove', yamlRemove)


def tryYamlSafeLoad(fileHandler):


    try:
        return yaml.safe_load(fileHandler)
    except yaml.constructor.ConstructorError as e:
        logging.error("Constructor Error; Affected file: " + str(fileHandler.name))
        logging.error(e)
        return dict()
    except yaml.composer.ComposerError as e:
        logging.error("Composer Error; Affected file: " + str(fileHandler.name))
        logging.error(e)
        return dict()







class yamlItemEntry:
    def __init__(self, yamlEntry):
        self.itemName = self.safeInsert(yamlEntry, "type")
        self.battleType = self.safeInsert(yamlEntry, "battleType")
        self.tuAuto = self.safeInsert(yamlEntry, "tuAuto")
        self.tuSnap = self.safeInsert(yamlEntry, "tuSnap")
        self.tuAimed = self.safeInsert(yamlEntry, "tuAimed")
        self.rosigmaComment = self.safeInsert(yamlEntry, "rosigmaComment")

    def safeInsert(self, yamlEntry, key):
        try:
            return yamlEntry[key]
        except KeyError:
            return ""


yamlEntries = []

for filePath in fileList:
    yamlFile = open(filePath, 'r')
    yamlContent = tryYamlSafeLoad(yamlFile)
    logging.debug(filePath)
    logging.debug(yamlContent.keys())
    if "items" in yamlContent.keys():
        print(filePath)
        # print(yamlContent["items"])
        # print(len(yamlContent["items"]))
        # print(type(yamlContent))
        # print(yamlContent.keys())
        for x in yamlContent["items"]:
            if "type" in x.keys():
                # print(x["type"])
                # print(x)
                yamlEntries.append(yamlItemEntry(x))
        # break
    yamlFile.close()


logging.debug("DONE - PRINTING RESULTS")
logging.debug("Type: " + str(type(yamlEntries)))
logging.debug("Length: " + str(len(yamlEntries)))
logging.debug(yamlEntries)
for x in yamlEntries:
    logging.debug(x.itemName)

