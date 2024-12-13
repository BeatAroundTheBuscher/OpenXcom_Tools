import sys
import os
import logging
import datetime

sys.path.append(os.getcwd())
import commons.file_handling as fH # noqa
import commons.yaml_handling as yH # noqa


if len(sys.argv) < 2:
    print("Usage: yammler.py path-to-mod-root-dictionary")  # noqa
    sys.exit(0)

# TODO: have to create a logs folder
LOG_FILENAME = "./logs/" + ("yammler_" + datetime.datetime.now().strftime(
                            '%Y-%m-%d_%H:%M:%S.log'), 'a')[0]
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')

paths = sys.argv[1:]

# mainNodeFilter = ["items"]
# mapScripts cannot be deleted
# terrains which are deleted and recreated in the submod require
# the MAP/TERRAINS/ROUTES files inside the submod
# if you only want to change the terrains just edit them

mainNodeFilter = ["alienDeployments", "alienMissions", "alienRaces",
                  "arcScripts", "armors", "eventScripts", "items",
                  "manufacture", "crafts", "craftWeapons",
                  "events", "eventScripts",
                  "missionScripts", "enviroEffects", "units", "soldiers",
                  "soldierBonuses", "commendations",
                  "facilities", "research", "ufopaedia"]

subNodeFilter = ["type", "name", "id"]

"""
mainNodeFilter = ["research"]
subNodeFilter = []
"""

for path in paths:
    print(path)

    fileList = []

    logging.info("Searching for Ruleset Files in:")
    logging.info(path)
    fileList = fH.populateFileList(path, fileList, [".rul"])

    logging.info("Number of Ruleset Files: " + str(len(fileList)))

    # https://stackoverflow.com/questions/45966633/yaml-error-could-not-determine-a-constructor-for-the-tag
    # https://www.programcreek.com/python/example/11269/yaml.add_constructor
    # https://python.hotexamples.com/examples/yaml/Loader/add_constructor/python-loader-add_constructor-method-examples.html

    yamlEntries = []
    yamlDict = {}

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
        try:
            logging.debug(yamlLoad.keys())

            for yamlKey in yamlLoad.keys():
                if len(mainNodeFilter) == 0 or yamlKey in mainNodeFilter:
                    if yamlKey not in yamlDict:
                        yamlDict[yamlKey] = []

                    yamlInsertList = yH.extractYamlItems(
                                        yamlLoad, yamlKey, subNodeFilter)
                    yamlDict[yamlKey].append(yamlInsertList)
        except AttributeError as e:
            logging.debug(e)
        yamlFile.close()

    logging.debug(yamlDict.keys())

    for yamlKey in yamlDict.keys():
        with open("./output/" + str((path.split("/")[-1])) +
                  "_" + str(yamlKey) + ".yaml", 'w') as file:
            yH.dumpOXCEYamlFiles(yamlDict, yamlKey, file)

print("end")
