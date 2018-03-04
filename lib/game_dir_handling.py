# Copyright (c) 2017 ntfwc
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
        if gameDirectory == None or len(gameDirectory) == 0:
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
