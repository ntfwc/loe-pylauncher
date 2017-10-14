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

import lib.web_io

import json

VERSIONS_URL="https://patches.legendsofequestria.com/zsync/versions3.json"

def downloadVersionsJson():
    return lib.web_io.downloadUrlContent(VERSIONS_URL, 10000, 5)

OS_ENTRY_TO_CHECK="win64"
def parseLatestVersion(versionsJsonBytes):
    versionsJson = json.loads(versionsJsonBytes.decode('utf-8'))
    if OS_ENTRY_TO_CHECK not in versionsJson:
        return None
    versionName = versionsJson[OS_ENTRY_TO_CHECK]
    if len(versionName) < 7:
        return None
    return versionName[-7:]
