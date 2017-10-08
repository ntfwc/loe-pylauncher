#!/usr/bin/python3
from lib.dialog import startDialog
from subprocess import Popen

GAME_PATH="/usr/bin/leafpad"

def main():
    userSelectedLaunch = startDialog()
    if userSelectedLaunch:
        launchGame(GAME_PATH)

def launchGame(gamePath):
    print("Launching game...")
    Popen([gamePath])

if __name__ == "__main__":
    main()
