#!/usr/bin/python3
import lib.dialog
import lib.game_paths
import lib.game_dir_handling

from subprocess import Popen
import os.path
import sys

TITLE="Launcher"

def main():
    lib.dialog.init()
    gameDirectory = lib.game_dir_handling.getGameDirectory()
    if gameDirectory == None:
        return

    print("Game Directory: " + gameDirectory)

    gameExecutable = lib.dialog.runLauncherDialog(TITLE)
    if gameExecutable != None:
        launchGame(gameExecutable)

def launchGame(gameExecutable):
    print("Launching game...")
    Popen([gameExecutable])

if __name__ == "__main__":
    main()
