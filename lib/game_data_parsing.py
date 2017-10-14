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
