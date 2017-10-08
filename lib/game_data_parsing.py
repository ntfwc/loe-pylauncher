import mmap

def extractBuildManifest(resourcesPath):
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
