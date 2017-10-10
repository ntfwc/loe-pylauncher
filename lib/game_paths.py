import os.path
import platform

def getResourcesPath(gameDirectory):
    return os.path.join(gameDirectory, "loe_Data", "resources.assets")

def determineGameExecutablePath(gameDirectory):
    gameExecutableName = __determineGameExecutableName()
    if gameExecutableName != None:
        return os.path.join(gameDirectory, gameExecutableName)
    else:
        return None

def __determineGameExecutableName():
    system = platform.system()
    if system == "Linux":
        if platform.machine() == "x86_64":
            return "loe.x86_64"
        else:
            return "loe.x86"
    elif system == "Windows":
        return "LoE.exe"
    else:
        # Mac
        return "LoE.app"

