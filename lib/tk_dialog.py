import lib.game_dir_handling
import lib.game_paths
import lib.version_fetching

import tkinter
import tkinter.filedialog
import tkinter.messagebox
import threading
from queue import Queue

TASK_QUEUE_SIZE = 10
class Application(tkinter.Frame):
    def __init__(self, gameDirectory, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self._createWidgets() 
        self.launchGame = False
        self.gameDirectory = gameDirectory

        self.taskQueue = Queue(TASK_QUEUE_SIZE)
        self.master.after(200, self.runPeriodicProcessing)

        self.startLocalVersionFetcher()

    def _createWidgets(self):
        self.quit_button = self._addButton("Quit", self.onQuitPressed)
        self.change_game_dir_button = self._addButton("Change game directory", self.onChangeGameDirectory)
        self.launch_button = self._addButton("Launch", self.onLaunchPressed)

    def _addButton(self, text, command):
        button = tkinter.Button(self) 
        button["text"] = text
        button["command"] = command;
        button.pack(side="left")
        return button

    def startLocalVersionFetcher(self):
        thread = threading.Thread(target=_fetchLocalVersion, args=(self.gameDirectory,self.localVersionFetcherCallback))
        thread.daemon = True
        thread.start()

    def localVersionFetcherCallback(self, version):
        def tkTask():
            print(threading.currentThread())
            print(version)
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
