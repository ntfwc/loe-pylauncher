from lib.game_paths import getResourcesPath
from lib.game_data_parsing import extractBuildManifest,parseBuildManifest

import sys

def getInstalledVersionId(gameDirectory):
    resourcesPath = getResourcesPath(gameDirectory)

    try:
        buildManifest = parseBuildManifest(extractBuildManifest(resourcesPath))
        return buildManifest.getVersionId()
    except:
        print("Failed to get installed version ID:", sys.exc_info()[1])
        return None
