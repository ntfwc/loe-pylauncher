#!/usr/bin/python3
import lib.dialog
from subprocess import Popen

TITLE="Launcher"
LOE_DIRECTORY_DIALOG_TITLE="Please select the game directory"
GAME_PATH="/usr/bin/leafpad"

def main():
    lib.dialog.init()
    installDirectory = lib.dialog.askUserForDirectory(LOE_DIRECTORY_DIALOG_TITLE)
    print(installDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
