from lib.game_paths import getResourcesPath
from lib.game_data_parsing import extractBuildManifest,parseBuildManifest
import lib.loe_api

import sys

def getInstalledVersionId(gameDirectory):
    resourcesPath = getResourcesPath(gameDirectory)

    try:
        buildManifest = parseBuildManifest(extractBuildManifest(resourcesPath))
        return buildManifest.getVersionId()
    except:
        print("Failed to get installed version ID:", sys.exc_info()[1])
        return None

def fetchAvailableVersionId():
    try:
        versionsJsonBytes = lib.loe_api.downloadVersionsJson()
        if versionsJsonBytes == None:
            print("Failed to fetch available version")
            return None

        availableVersion = lib.loe_api.parseLatestVersion(versionsJsonBytes)
        if availableVersion == None:
            print("Failed to parse available version")
        return availableVersion
    except:
        print("Failed to fetch available version")
        return None
