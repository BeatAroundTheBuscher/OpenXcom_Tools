def populatePathsWithOpenXcomLogFile(logFilePath):
    populatedPathsList = []

    log = open(logFilePath, "r")
    loglines = log.readlines()
    log.close()

    for line in loglines: 
        if "has incorrect transparent color index" in line:
            line = re.sub("^.*WARN\]\\sImage\\s", "", line)
            line = re.sub("\\s\(.*$", "", line)
            populatedPathsList.append(sys.argv[2] + "/" + line)

    return populatedPathsList