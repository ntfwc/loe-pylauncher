dialogLib=None

def init():
    global dialogLib
    import lib.tk_dialog as dialogLib
    dialogLib.init()

def askUserForDirectory():
    return dialogLib.askUserForDirectory()

def runLauncherDialog(title):
    return dialogLib.runLauncherDialog(title)
