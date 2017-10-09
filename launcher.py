#!/usr/bin/python3
import lib.dialog
import lib.game_paths

from subprocess import Popen
import os.path
import sys


TITLE="Launcher"
GAME_DIR_DIALOG_TITLE="Please select the game directory"
INVALID_GAME_DIR_TITLE="Invalid game directory"
INVALID_GAME_DIR_RETRY_MESSAGE="The game directory does not look valid. Select a different directory?"

GAME_DIR_CFG_FILE="game_dir.cfg"
GAME_PATH="/usr/bin/leafpad"

script_dir = None

def main():
    global script_dir
    script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

    lib.dialog.init()
    gameDirectory = getGameDirectory()
    if gameDirectory == None:
        return

    print("Game Directory: " + gameDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def getGameDirectory():
    gameDirCfgPath = os.path.join(script_dir, GAME_DIR_CFG_FILE)
    if os.path.exists(gameDirCfgPath):
        gameDirectory = readFile(gameDirCfgPath)
        if validateGameDirectory(gameDirectory):
            return gameDirectory
        print("Configured game directory '%s' is not valid" % gameDirectory)

    while True:
        gameDirectory = lib.dialog.askUserForDirectory(GAME_DIR_DIALOG_TITLE)
        if gameDirectory == ():
            return None
        if validateGameDirectory(gameDirectory):
            writeFile(gameDirCfgPath, gameDirectory)
            return gameDirectory
        if not lib.dialog.askYesOrNo(INVALID_GAME_DIR_TITLE,INVALID_GAME_DIR_RETRY_MESSAGE):
            return None

def validateGameDirectory(gameDirectory):
    return os.path.exists(lib.game_paths.getResourcesPath(gameDirectory))

def readFile(filePath):
    with open(filePath, "r") as f:
        return f.read()

def writeFile(filePath, text):
    with open(filePath, "w") as f:
        return f.write(text)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
