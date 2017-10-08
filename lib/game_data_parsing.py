import mmap
import json

class BuildManifest(object):
    def __init__(self, cloudBuildTargetName, scmCommitId):
        self.cloudBuildTargetName = cloudBuildTargetName
        self.scmCommitId = scmCommitId

    def getVersionId(self):
        """ Truncates the commit ID to get a version ID that matches what is
        found on downloads
        """
        return self.scmCommitId[:7]

    def __repr__(self):
        return "BuildManifest[cloudBuildTargetName=%s,scmCommitId=%s]" % (self.cloudBuildTargetName, self.scmCommitId)

def extractBuildManifest(resourcesPath):
    """Extracts the bytes of the build manifest json from the resources archive"""
    with open(resourcesPath, 'rb') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        buildManifestLocation = mm.rfind(b'UnityCloudBuildManifest.json')
        if (buildManifestLocation == -1):
            return None

        start = mm.find(b'{', buildManifestLocation)
        if (start == -1):
            return None

        end = mm.find(b'}', start)
        if (end == -1):
            return None

        return mm[start:end+1]

def parseBuildManifest(buildManifestBytes):
    """Parses a build manifest object from bytes

    :raises JSONDecodeError: If the data is not valid
    :raises KeyError: If an expected value is missing"""
    jsonBuildManifest = json.loads(buildManifestBytes.decode('utf-8'))
    return BuildManifest(jsonBuildManifest["cloudBuildTargetName"], jsonBuildManifest["scmCommitId"])
