import sys
import logging
import datetime

sys.path.insert(0, './commons')
import file_handling as fH  # noqa
import yaml_handling as yH  # noqa

if len(sys.argv) < 2:
    print("Usage: yammler.py path-to-mod-root-dictionary")  # noqa
    sys.exit(0)

# TODO: have to create a logs folder
LOG_FILENAME = "./logs/" + ("yammler_" + datetime.datetime.now().strftime(
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

# https://stackoverflow.com/questions/45966633/yaml-error-could-not-determine-a-constructor-for-the-tag
# https://www.programcreek.com/python/example/11269/yaml.add_constructor
# https://python.hotexamples.com/examples/yaml/Loader/add_constructor/python-loader-add_constructor-method-examples.html

yH.addOXCEConstructors()

yamlEntries = []
yamlDict = {}
mainNodeFilter = ["items"]
# mainNodeFilter = []
subNodeFilter = ["type", "name", "id"]
# subNodeFilter = []

for filePath in fileList:
    yamlFile = open(filePath, 'r')
    yamlLoad = yH.tryYamlSafeLoad(yamlFile)

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
        if len(mainNodeFilter) == 0 or yamlKey in mainNodeFilter:
            if yamlKey not in yamlDict:
                yamlDict[yamlKey] = []

            yamlInsertList = yH.extractYamlItems(
                                yamlLoad, yamlKey, subNodeFilter)
            yamlDict[yamlKey].append(yamlInsertList)
    yamlFile.close()


logging.debug(yamlDict.keys())


for x in yamlDict.keys():
    with open("./output/" + str(x) + ".yaml", 'w') as file:
        yH.dumpOXCEYamlFiles(yamlDict, file)

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
