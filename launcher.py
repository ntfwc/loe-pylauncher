#!/usr/bin/python3
import lib.dialog
import lib.game_paths

from subprocess import Popen
from os.path import exists

TITLE="Launcher"
GAME_DIR_DIALOG_TITLE="Please select the game directory"
INVALID_GAME_DIR_TITLE="Invalid game directory"
INVALID_GAME_DIR_RETRY_MESSAGE="The game directory does not look valid. Select a different directory?"

GAME_PATH="/usr/bin/leafpad"

def main():
    lib.dialog.init()

    gameDirectory = getGameDirectory()
    if gameDirectory == None:
        return

    print("Game Directory: " + gameDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def getGameDirectory():
    while True:
        gameDirectory = lib.dialog.askUserForDirectory(GAME_DIR_DIALOG_TITLE)
        if gameDirectory == ():
            return None
        if validateGameDirectory(gameDirectory):
            return gameDirectory
        if not lib.dialog.askYesOrNo(INVALID_GAME_DIR_TITLE,INVALID_GAME_DIR_RETRY_MESSAGE):
            return None

def validateGameDirectory(gameDirectory):
    return exists(lib.game_paths.getResourcesPath(gameDirectory))

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
