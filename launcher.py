#!/usr/bin/python3
import lib.dialog
import lib.game_paths
import lib.game_dir_handling

from subprocess import Popen
import os.path
import sys

TITLE="Launcher"

GAME_PATH="/usr/bin/leafpad"

def main():
    lib.dialog.init()
    gameDirectory = lib.game_dir_handling.getGameDirectory()
    if gameDirectory == None:
        return

    print("Game Directory: " + gameDirectory)

    userSelectedLaunch = lib.dialog.runLauncherDialog(TITLE)
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
