import unittest
import lib.game_data_parsing

BUILD_MANIFEST_JSON_PATH="testing/testing-data/UnityCloudBuildManifest.json"

class ParsingTest(unittest.TestCase):
    def testParseBuildManifest(self):
        buildManifest = lib.game_data_parsing.parseBuildManifest(readFile(BUILD_MANIFEST_JSON_PATH))
        self.assertEquals("linux-lar-universal", buildManifest.cloudBuildTargetName)
        self.assertEquals("e895688f34b94a99c63316f16f190cd11914e092", buildManifest.scmCommitId)
        self.assertEquals("e895688", buildManifest.getVersionId())

def readFile(filePath):
    with open(filePath, "rb") as f:
        return f.read()
