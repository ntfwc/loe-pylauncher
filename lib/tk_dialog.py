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

import lib.game_dir_handling
import lib.game_paths
import lib.version_fetching
from lib.constants import DOWNLOADS_PAGE

import tkinter
import tkinter.ttk
import tkinter.filedialog
import tkinter.messagebox

import threading
from queue import Queue
import webbrowser
import os.path
import platform

WINDOW_WIDTH = 200
TASK_QUEUE_SIZE = 10
GAME_DIRECTORY_LABEL_PREFIX = "Game Directory: "

LOCAL_VERSION_LABEL_PREFIX = "Installed version: "
LOCAL_VERSION_LABEL_CHECKING = LOCAL_VERSION_LABEL_PREFIX + "Checking..."
LOCAL_VERSION_LABEL_CHECK_FAILED = LOCAL_VERSION_LABEL_PREFIX + "Check Failed"

AVAILABLE_VERSION_LABEL_PREFIX = "Available version: "
AVAILABLE_VERSION_LABEL_CHECKING = AVAILABLE_VERSION_LABEL_PREFIX + "Checking..."
AVAILABLE_VERSION_LABEL_CHECK_FAILED = AVAILABLE_VERSION_LABEL_PREFIX + "Check Failed"

LAUNCH_ERROR_TITLE = "Launch Error"
LAUNCH_ERROR_MESSAGE = "The expected launch executable '%s' was not found"

class Application(tkinter.ttk.Frame):
    def __init__(self, gameDirectory, master=None):
        tkinter.ttk.Frame.__init__(self, master)
        self.pack()
        self.executableToLaunch = None
        self.gameDirectory = gameDirectory
        self.localVersion = None
        self.availableVersion = None

        self._createWidgets() 

        self.taskQueue = Queue(TASK_QUEUE_SIZE)
        self.master.after(200, self.runPeriodicProcessing)

        self.startLocalVersionFetcher()
        self.startAvailableVersionFetcher()

    def _createWidgets(self):
        self.labelFrame = tkinter.ttk.Frame(self)
        self.labelFrame.pack(side=tkinter.TOP, padx=5, pady=5)

        self.gameDirectoryLabel = tkinter.ttk.Label(self.labelFrame)
        self._updateGameDirectoryLabel()
        self.gameDirectoryLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.localVersionLabel = tkinter.ttk.Label(self.labelFrame)
        self._updateLocalVersionLabel()
        self.localVersionLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.availableVersionLabel = tkinter.ttk.Label(self.labelFrame)
        self._updateAvailableVersionLabel()
        self.availableVersionLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.buttonFrame = tkinter.ttk.Frame(self)
        self.buttonFrame.pack(side=tkinter.TOP, padx=5, pady=5)

        self.quitButton = self._addButton(self.buttonFrame, "Quit", self.onQuitClicked)
        self.changeGameDirButton = self._addButton(self.buttonFrame, "Change game directory", self.onChangeGameDirectoryClicked)
        self.openDownloadsPageButton = self._addButton(self.buttonFrame, "Open Downloads page", self.onOpenDownloadsPageClicked)
        self.launchButton = self._addButton(self.buttonFrame, "Launch", self.onLaunchClicked)

    def _updateGameDirectoryLabel(self):
        self.gameDirectoryLabel["text"] = GAME_DIRECTORY_LABEL_PREFIX + '"' + self.gameDirectory + '"'

    def _updateLocalVersionLabel(self):
        version = self.localVersion if self.localVersion != None else ""
        self.localVersionLabel["text"] = LOCAL_VERSION_LABEL_PREFIX + version

    def _updateAvailableVersionLabel(self):
        version = self.availableVersion if self.availableVersion != None else ""
        postfix = ""
        if self.availableVersion != None and self.localVersion != None:
            if self.availableVersion == self.localVersion:
                postfix = " (Same)"
            else:
                postfix = " (New)"

        self.availableVersionLabel["text"] = AVAILABLE_VERSION_LABEL_PREFIX + version + postfix

    def _addButton(self, frame, text, command):
        button = tkinter.ttk.Button(frame)
        button["text"] = text
        button["command"] = command;
        button.pack(side=tkinter.LEFT, padx=2)
        return button

    def startLocalVersionFetcher(self):
        self.localVersionLabel["text"] = LOCAL_VERSION_LABEL_CHECKING
        thread = threading.Thread(target=_fetchLocalVersion, args=(self.gameDirectory,self.localVersionFetcherCallback))
        thread.daemon = True
        thread.start()

    def localVersionFetcherCallback(self, version):
        def tkTask():
            self.localVersion = version
            if (version == None):
                self.localVersionLabel["text"] = LOCAL_VERSION_LABEL_CHECK_FAILED
            else:
                self._updateLocalVersionLabel()
                if self.availableVersion != None:
                    self._updateAvailableVersionLabel()
        self.runOnTkThread(tkTask)

    def startAvailableVersionFetcher(self):
        self.availableVersionLabel["text"] = AVAILABLE_VERSION_LABEL_CHECKING
        thread = threading.Thread(target=_fetchAvailableVersion, args=(self.availableVersionFetcherCallback,))
        thread.daemon = True
        thread.start()

    def availableVersionFetcherCallback(self, version):
        def tkTask():
            self.availableVersion = version
            if (version == None):
                self.availableVersionLabel["text"] = AVAILABLE_VERSION_LABEL_CHECK_FAILED
            else:
                self._updateAvailableVersionLabel()
        self.runOnTkThread(tkTask)

    def runPeriodicProcessing(self):
        self.processTaskQueue()
        self.master.after(200, self.runPeriodicProcessing)

    def processTaskQueue(self):
        while not self.taskQueue.empty():
            try:
                task = self.taskQueue.get_nowait()
                task()
            except Queue.Empty:
                pass

    def onLaunchClicked(self):
        executable = lib.game_paths.determineGameExecutablePath(self.gameDirectory)
        if os.path.exists(executable):
            self.executableToLaunch = lib.game_paths.determineGameExecutablePath(self.gameDirectory)
            self.quit()
        else:
            displayError(LAUNCH_ERROR_TITLE, LAUNCH_ERROR_MESSAGE % executable)

    def onChangeGameDirectoryClicked(self):
        gameDirectory = lib.game_dir_handling.askUserForGameDirectory()
        if gameDirectory != None:
            self.gameDirectory = gameDirectory
            lib.game_dir_handling.saveGameDirectory(gameDirectory)
            print("Changed game directory to '%s'" % gameDirectory)
            self._updateGameDirectoryLabel()
            self.startLocalVersionFetcher()

    def onOpenDownloadsPageClicked(self):
        webbrowser.open(DOWNLOADS_PAGE)

    def onQuitClicked(self):
        self.quit()

    def runOnTkThread(self, target):
        self.taskQueue.put(target)

def _fetchLocalVersion(gameDirectory, callback):
    callback(lib.version_fetching.getInstalledVersionId(gameDirectory))

def _fetchAvailableVersion(callback):
    callback(lib.version_fetching.fetchAvailableVersionId())

root=None
isRootHidden=True

def init():
    global root
    root = tkinter.Tk()
    if platform.system() == "Linux":
        # The default theme for Linux is "classic", but we can do better
        tkinter.ttk.Style().theme_use("clam")
    root.withdraw()

def askUserForDirectory(title):
    return tkinter.filedialog.askdirectory(title=title)

def askYesOrNo(title, message):
    return tkinter.messagebox.askyesno(title=title, message=message)

def displayError(title, message):
    tkinter.messagebox.showerror(title=title, message=message)

def runLauncherDialog(gameDirectory, title):
    global root,isRootHidden
    if isRootHidden:
        root.wm_deiconify()

    root.title(title)
    app = Application(gameDirectory, master=root)
    app.mainloop()
    return app.executableToLaunch
