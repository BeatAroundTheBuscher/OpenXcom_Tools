# pyyaml is not maintained anymore
# https://stackoverflow.com/a/36760452
# import yaml
# import yaml.composer
import logging
# from ruamel.yaml import YAML
import ruamel.yaml


class yamlAdd:
    yaml_tag = u'!add'

    def __init__(self):
        pass

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag, "")

    @classmethod
    def from_yaml(cls, constructor, node):
        return None  # cls(*node.value.split('-'))


class yamlRemove:
    yaml_tag = u'!remove'

    def __init__(self):
        pass

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_scalar(cls.yaml_tag, "")

    @classmethod
    def from_yaml(cls, constructor, node):
        return None  # cls(*node.value.split('-'))


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
    a = type(yamlLoad[yamlKey])
    print(a)
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
