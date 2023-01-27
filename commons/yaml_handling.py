# pyyaml is not maintained anymore
# https://stackoverflow.com/a/36760452
# import yaml
# import yaml.composer
import logging
from ruamel import yaml


def yamlAdd(loader, node):
    pass
    return ""


def yamlRemove(loader, node):
    pass
    """
    print("yamlRemover")
    print(loader)
    print(node)
    """
    return ""


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


def extractYamlItems(yamlLoad, yamlKey, subNodeFilter):
    yamlInsertList = []
    if type(yamlLoad[yamlKey]) is list:
        # logging.debug("yamlLoad[yamlKey]: " + str(yamlLoad[yamlKey]))
        for yamlItem in yamlLoad[yamlKey]:
            yamlInsertList.append(yamlItem)
            """
            # logging.debug("yamlItem: " + str(yamlItem))
            if type(yamlItem) is dict:
                for node in yamlItem.keys():
                    # logging.debug("node: " + str(node))
                    if len(subNodeFilter) == 0 or node in subNodeFilter:
                        # exception for unit names after type
                        if node == "name" and "type" in yamlItem.keys():
                            pass
                        else:
                            yamlInsertDict = {node: yamlItem}
                            yamlInsertList.append(yamlInsertDict)
            """
    return yamlInsertList


def addOXCEConstructors():
    yaml.SafeLoader.add_constructor('!add', yamlAdd)
    yaml.SafeLoader.add_constructor('!remove', yamlRemove)


def dumpOXCEYamlFiles(yamlDict, yamlKey, file):
    if len(yamlDict[yamlKey]) > 0:
        # this will order alphanumerical and not keep the original order
        # yaml.dump(yamlDict[yamlKey], file) 
        yaml.dump(yamlDict[yamlKey], file, Dumper=yaml.RoundTripDumper)
