import tkinter
import tkinter.filedialog
import tkinter.messagebox

class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self._createWidgets() 
        self.launchGame = False

    def _createWidgets(self):
        self.quit_button = tkinter.Button(self) 
        self.quit_button["text"] = "Quit"
        self.quit_button["command"] = self.onQuitPressed;
        self.quit_button.pack(side="left")

        self.launch_button = tkinter.Button(self) 
        self.launch_button["text"] = "Launch"
        self.launch_button["command"] = self.onLaunchPressed;
        self.launch_button.pack(side="left")

    def onLaunchPressed(self):
        self.launchGame = True
        self.quit()

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

def runLauncherDialog(title):
    global root,isRootHidden
    if isRootHidden:
        root.wm_deiconify()

    root.title(title)
    app = Application(root)
    app.mainloop()
    return app.launchGame
