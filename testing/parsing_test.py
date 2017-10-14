# Copyright (c) 2017 ntfwc
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
