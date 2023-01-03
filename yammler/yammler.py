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


logging.info("Searching for Ruleset Files in:")
for path in paths:
    logging.info(path)
    fileList = fH.populateFileList(path, fileList, [".rul"])

logging.info("Number of Ruleset Files: " + str(len(fileList)))


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


yaml.SafeLoader.add_constructor('!add', yamlAdd)
yaml.SafeLoader.add_constructor('!remove', yamlRemove)


def tryYamlSafeLoad(fileHandler):
    try:
        return yaml.safe_load(fileHandler)
    except yaml.constructor.ConstructorError as e:
        logging.error("Constructor Error; Affected file: "
                      + str(fileHandler.name))
        logging.error(e)
        return dict()
    except yaml.composer.ComposerError as e:
        logging.error("Composer Error; Affected file: "
                      + str(fileHandler.name))
        logging.error(e)
        return dict()


class yamlItemEntry:
    def __init__(self, yamlEntry):
        self.name = self.safeInsert(yamlEntry, "name")
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
yamlDict = {}
filter = ["manufacture", "soldiers", "items"]
filter = []

for filePath in fileList:
    yamlFile = open(filePath, 'r')
    yamlLoad = tryYamlSafeLoad(yamlFile)

    # tryYamlSafeLoad returns a dict
    # that includes a list that consists of dicts
    # <class 'dict'> # print(type(yamlLoad))
    # <class 'list'> # print(type(yamlLoad["manufacture"]))
    # <class 'dict'> # print(type(yamlLoad["manufacture"][0]))
    # final entries like name returns 'str'
    # entries with lists like requires return another list with 'str'

    logging.debug(filePath)
    logging.debug(yamlLoad.keys())

    for yamlKey in yamlLoad.keys():
        if len(filter) == 0 or yamlKey in filter:
            if yamlKey not in yamlDict:
                yamlDict[yamlKey] = []

            yamlDict[yamlKey].append(yamlLoad[yamlKey])

    yamlFile.close()


logging.debug(yamlDict.keys())


with open('names.yaml', 'w') as file:
    yaml.dump(yamlDict, file)

# for x in yamlDict.keys():
#    logging.debug(x)
#    logging.debug(yamlDict[x])


"""
logging.debug("DONE - PRINTING RESULTS")
logging.debug("Type: " + str(type(yamlEntries)))
logging.debug("Length: " + str(len(yamlEntries)))
for x in yamlEntries:
    logging.debug(x.itemName)
"""

"""
        try:
            for yamlContent in yamlLoad[yamlKey]:
                print(yamlContent)
                print(type(yamlContent))
                if"name" in yamlContent.keys():
                    print(yamlContent["name"])
                if "id" in yamlContent.keys():
                    print(yamlContent["id"])
                if "type" in yamlContent.keys():
                    print(yamlContent["type"])
                yamlDict[yamlKey].append(yamlContent)
        except TypeError:
            logging.warn("TypeError: Ignored " + str(yamlKey))
        # sys.exit(1)

"""

"""
    if "items" in yamlLoad.keys():
        print(filePath)
        # print(yamlLoad["items"])
        # print(len(yamlLoad["items"]))
        # print(type(yamlLoad))
        # print(yamlLoad.keys())
        for x in yamlLoad["items"]:
            if "type" in x.keys():
                # print(x["type"])
                # print(x)
                yamlEntries.append(yamlItemEntry(x))
        # break
"""
