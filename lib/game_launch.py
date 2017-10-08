from subprocess import Popen

GAME_PATH="/usr/bin/leafpad"

def launchGame():
    print("Launching game!")
    Popen([GAME_PATH])
