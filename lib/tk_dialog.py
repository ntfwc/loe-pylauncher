import lib.game_dir_handling
import lib.game_paths

import tkinter
import tkinter.filedialog
import tkinter.messagebox

class Application(tkinter.Frame):
    def __init__(self, gameDirectory, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self._createWidgets() 
        self.launchGame = False
        self.gameDirectory = gameDirectory

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


    def onLaunchPressed(self):
        self.launchGame = True
        self.quit()

    def onChangeGameDirectory(self):
        gameDirectory = lib.game_dir_handling.askUserForGameDirectory()
        if gameDirectory != None:
            self.gameDirectory = gameDirectory
            lib.game_dir_handling.saveGameDirectory(gameDirectory)
            print("Changed game directory to '%s'" % gameDirectory)

    def onQuitPressed(self):
        self.quit()

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
