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
