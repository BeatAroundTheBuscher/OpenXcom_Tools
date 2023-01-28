# pyyaml is not maintained anymore
# https://stackoverflow.com/a/36760452
# https://www.programcreek.com/python/example/103790/ruamel.yaml.org

import logging
import ruamel.yaml


class yamlAdd:
    yaml_tag = u'!add'

    def __init__(self, myList):
        # self.myTag = myTag  # is implicit
        self.myList = myList

    @classmethod
    def to_yaml(cls, representer, node):
        for i in range(0, len(node.myList)):
            node.myList[i] = node.myList[i].value
        return representer.represent_sequence(cls.yaml_tag, node.myList)
        # had to look into representer.py that one can directly pass a node
        # API was read from source code because documentation is overrated

    @classmethod
    def from_yaml(cls, constructor, node):
        if type(node.value) is list:
            return cls(node.value)
        return None


class yamlRemove:
    yaml_tag = u'!remove'

    def __init__(self, myList):
        # self.myTag = myTag  # is implicit
        self.myList = myList

    @classmethod
    def to_yaml(cls, representer, node):
        for i in range(0, len(node.myList)):
            node.myList[i] = node.myList[i].value
        return representer.represent_sequence(cls.yaml_tag, node.myList)

    @classmethod
    def from_yaml(cls, constructor, node):
        if type(node.value) is list:
            return cls(node.value)
        return None


yaml = ruamel.yaml.YAML(typ="rt")
yaml.register_class(yamlAdd)
yaml.register_class(yamlRemove)
yaml.allow_duplicate_keys = True
ruamel.yaml.add_constructor('!add', yamlAdd)
ruamel.yaml.add_constructor('!remove', yamlAdd)


def tryYamlSafeLoad(fileHandler):
    try:
        return yaml.load(fileHandler)
    except NotImplementedError as e:
        logging.error("NotImplementedError; Affected file: "
                      + str(fileHandler.name))
        logging.error(e)
        return dict()
    """
    except yaml.add_constructor.ConstructorError as e:
        logging.error("Constructor Error; Affected file: "
                      + str(fileHandler.name))
        logging.error(e)
        return dict()
    except yaml.add_composer.ComposerError as e:
        logging.error("Composer Error; Affected file: "
                      + str(fileHandler.name))
        logging.error(e)
        return dict()
    """


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
    if type(yamlLoad[yamlKey]) is ruamel.yaml.CommentedSeq:
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


def dumpOXCEYamlFiles(yamlDict, yamlKey, file):
    if len(yamlDict[yamlKey]) > 0:
        # this will order alphanumerical and not keep the original order
        # yaml.dump(yamlDict[yamlKey], file)
        yaml.dump(yamlDict[yamlKey], file)
