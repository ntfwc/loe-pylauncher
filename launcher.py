#!/usr/bin/python3

from lib.dialog import startDialog
from lib.game_launch import launchGame

def main():
    userSelectedLaunch = startDialog()
    if userSelectedLaunch:
        launchGame()


if __name__ == "__main__":
    main()
