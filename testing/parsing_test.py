import lib.game_data_parsing
import lib.loe_api

import unittest

TESTING_DATA_PATH="testing/testing-data"

class ParsingTest(unittest.TestCase):
    def testParseBuildManifest(self):
        buildManifest = lib.game_data_parsing.parseBuildManifest(readFile(TESTING_DATA_PATH + "/UnityCloudBuildManifest.json"))
        self.assertEquals("linux-lar-universal", buildManifest.cloudBuildTargetName)
        self.assertEquals("e895688f34b94a99c63316f16f190cd11914e092", buildManifest.scmCommitId)
        self.assertEquals("e895688", buildManifest.getVersionId())

    def testParseVersionJson(self):
        parsedVersion = lib.loe_api.parseLatestVersion(readFile(TESTING_DATA_PATH + "/versions3.json"))
        self.assertEquals("e895688", parsedVersion)

    def testParseVersionJson_shouldHandleMissingOsEntry(self):
        parsedVersion = lib.loe_api.parseLatestVersion(readFile(TESTING_DATA_PATH + "/versions3_withMissingOsEntries.json"))
        self.assertIsNone(parsedVersion)

    def testParseVersionJson_shouldHandleUnexpectedlyShortVersionName(self):
        parsedVersion = lib.loe_api.parseLatestVersion(readFile(TESTING_DATA_PATH + "/versions3_withUnexpectedlyShortVersionNames.json"))
        self.assertIsNone(parsedVersion)

def readFile(filePath):
    with open(filePath, "rb") as f:
        return f.read()
