import lib.dialog
from lib.file_io import readFile,writeFile

import os.path
import sys

TITLE="Launcher"
GAME_DIR_DIALOG_TITLE="Please select the game directory"
INVALID_GAME_DIR_TITLE="Invalid game directory"
INVALID_GAME_DIR_RETRY_MESSAGE='The game directory "%s" does not look valid. Select a different directory?'

GAME_DIR_CFG_FILE="game_dir.cfg"

def getGameDirectory():
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
    gameDirCfgPath = os.path.join(scriptDir, GAME_DIR_CFG_FILE)
    if os.path.exists(gameDirCfgPath):
        gameDirectory = readFile(gameDirCfgPath)
        if validateGameDirectory(gameDirectory):
            return gameDirectory
        print("Configured game directory '%s' is not valid" % gameDirectory)

    gameDirectory = askUserForGameDirectory()
    if (gameDirectory != None):
        saveGameDirectory(gameDirectory, gameDirCfgPath=gameDirCfgPath)
    return gameDirectory

def askUserForGameDirectory():
    while True:
        gameDirectory = lib.dialog.askUserForDirectory(GAME_DIR_DIALOG_TITLE)
        if gameDirectory == ():
            return None
        if validateGameDirectory(gameDirectory):
            return gameDirectory
        if not lib.dialog.askYesOrNo(INVALID_GAME_DIR_TITLE,INVALID_GAME_DIR_RETRY_MESSAGE % gameDirectory):
            return None

def saveGameDirectory(gameDirectory, gameDirCfgPath=None):
    if gameDirCfgPath == None:
        scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
        gameDirCfgPath = os.path.join(scriptDir, GAME_DIR_CFG_FILE)
    writeFile(gameDirCfgPath, gameDirectory)

def validateGameDirectory(gameDirectory):
    return os.path.exists(lib.game_paths.getResourcesPath(gameDirectory))

def getScriptDir():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
