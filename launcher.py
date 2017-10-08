#!/usr/bin/python3
import lib.dialog
from subprocess import Popen

TITLE="Launcher"
GAME_DIR_DIALOG_TITLE="Please select the game directory"
INVALID_GAME_DIR_TITLE="Invalid game directory"
INVALID_GAME_DIR_RETRY_MESSAGE="The game directory does not look valid. Select a different directory?"

GAME_PATH="/usr/bin/leafpad"

def main():
    lib.dialog.init()
    installDirectory = lib.dialog.askUserForDirectory(GAME_DIR_DIALOG_TITLE)
    print(installDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
