#!/usr/bin/python3
import lib.dialog
from subprocess import Popen

TITLE="Launcher"
GAME_PATH="/usr/bin/leafpad"

def main():
    lib.dialog.init()
    installDirectory = lib.dialog.askUserForDirectory()
    print(installDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
