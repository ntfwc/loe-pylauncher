import lib.game_dir_handling
import lib.game_paths
import lib.version_fetching

import tkinter
import tkinter.filedialog
import tkinter.messagebox
import threading
from queue import Queue

WINDOW_WIDTH = 200
TASK_QUEUE_SIZE = 10
GAME_DIRECTORY_LABEL_PREFIX = "Game Directory: "

LOCAL_VERSION_LABEL_PREFIX = "Installed version: "
LOCAL_VERSION_LABEL_CHECKING = LOCAL_VERSION_LABEL_PREFIX + "Checking..."
LOCAL_VERSION_LABEL_CHECK_FAILED = LOCAL_VERSION_LABEL_PREFIX + "Check Failed"

AVAILABLE_VERSION_LABEL_PREFIX = "Available version: "
AVAILABLE_VERSION_LABEL_CHECKING = AVAILABLE_VERSION_LABEL_PREFIX + "Checking..."


class Application(tkinter.Frame):
    def __init__(self, gameDirectory, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self.launchGame = False
        self.gameDirectory = gameDirectory
        self.localVersion = None
        self.availableVersion = None

        self._createWidgets() 

        self.taskQueue = Queue(TASK_QUEUE_SIZE)
        self.master.after(200, self.runPeriodicProcessing)

        self.startLocalVersionFetcher()

    def _createWidgets(self):
        self.labelFrame = tkinter.Frame(self)
        self.labelFrame.pack(side=tkinter.TOP, padx=5, pady=5)

        self.gameDirectoryLabel = tkinter.Label(self.labelFrame)
        self._updateGameDirectoryLabel()
        self.gameDirectoryLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.localVersionLabel = tkinter.Label(self.labelFrame)
        self._updateLocalVersionLabel()
        self.localVersionLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.availableVersionLabel = tkinter.Label(self.labelFrame)
        self._updateAvailableVersionLabel()
        self.availableVersionLabel.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.buttonFrame = tkinter.Frame(self)
        self.buttonFrame.pack(side=tkinter.TOP, padx=5, pady=5)

        self.quitButton = self._addButton(self.buttonFrame, "Quit", self.onQuitPressed)
        self.changeGameDirButton = self._addButton(self.buttonFrame, "Change game directory", self.onChangeGameDirectory)
        self.launchButton = self._addButton(self.buttonFrame, "Launch", self.onLaunchPressed)

    def _updateGameDirectoryLabel(self):
        self.gameDirectoryLabel["text"] = GAME_DIRECTORY_LABEL_PREFIX + '"' + self.gameDirectory + '"'

    def _updateLocalVersionLabel(self):
        version = self.localVersion if self.localVersion != None else ""
        self.localVersionLabel["text"] = LOCAL_VERSION_LABEL_PREFIX + version

    def _updateAvailableVersionLabel(self):
        version = self.availableVersion if self.availableVersion != None else ""
        self.availableVersionLabel["text"] = AVAILABLE_VERSION_LABEL_PREFIX + version

    def _addButton(self, frame, text, command):
        button = tkinter.Button(frame)
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

    def onLaunchPressed(self):
        self.launchGame = True
        self.quit()

    def onChangeGameDirectory(self):
        gameDirectory = lib.game_dir_handling.askUserForGameDirectory()
        if gameDirectory != None:
            self.gameDirectory = gameDirectory
            lib.game_dir_handling.saveGameDirectory(gameDirectory)
            print("Changed game directory to '%s'" % gameDirectory)
            self._updateGameDirectoryLabel()
            self.startLocalVersionFetcher()

    def onQuitPressed(self):
        self.quit()

    def runOnTkThread(self, target):
        self.taskQueue.put(target)

def _fetchLocalVersion(gameDirectory, callback):
    callback(lib.version_fetching.getInstalledVersionId(gameDirectory))

root=None
isRootHidden=True

def init():
    global root
    root = tkinter.Tk()
    root.withdraw()

def askUserForDirectory(title):
    return tkinter.filedialog.askdirectory(title=title)

def askYesOrNo(title, message):
    return tkinter.messagebox.askyesno(title=title, message=message)

GAME_EXECUTABLE="/usr/bin/leafpad"

def runLauncherDialog(gameDirectory, title):
    global root,isRootHidden
    if isRootHidden:
        root.wm_deiconify()

    root.title(title)
    app = Application(gameDirectory, master=root)
    app.mainloop()
    if not app.launchGame:
        return None
    print(lib.game_paths.determineGameExecutablePath(app.gameDirectory))
    return GAME_EXECUTABLE
