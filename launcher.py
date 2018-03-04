#!/usr/bin/python3
#
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
import lib.game_paths
import lib.game_dir_handling

from subprocess import Popen
import os.path
import sys
import argparse

TITLE="Launcher"

def parse_argv():
    parser = argparse.ArgumentParser(description='A launcher for Legends of Equestria')
    parser.add_argument('-t', action='store_true', help='always use the Tk interface')
    return parser.parse_args()

def main():
    if sys.version_info[0] != 3:
        print("This script is being run on an unsupported Python version. Python 3 is required")
        return
    parsed_args = parse_argv()

    lib.dialog.init(parsed_args.t)
    gameDirectory = lib.game_dir_handling.getGameDirectory()
    if gameDirectory == None:
        return

    print("Game Directory: " + gameDirectory)

    gameExecutable = lib.dialog.runLauncherDialog(gameDirectory, TITLE)
    if gameExecutable != None:
        launchGame(gameExecutable)

def launchGame(gameExecutable):
    print("Launching game...")
    Popen([gameExecutable])

if __name__ == "__main__":
    main()
