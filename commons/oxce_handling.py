import re
import sys


def populatePathsWithOpenXcomLogFile(logFilePath):
    populatedPathsList = []

    log = open(logFilePath, "r")
    loglines = log.readlines()
    log.close()

    for line in loglines:
        if "has incorrect transparent color index" in line:
            # false positives for reportInvalidStringEscapeSequence
            # https://github.com/microsoft/pylance-release/issues/196
            line = re.sub("^.*WARN\]\\sImage\\s", "", line)  # type: ignore  # noqa
            line = re.sub("\\s\(.*$", "", line)  # type: ignore  # noqa
            populatedPathsList.append(sys.argv[2] + "/" + line)

    return populatedPathsList
