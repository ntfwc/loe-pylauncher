dialogLib=None

def init():
    global dialogLib
    import lib.tk_dialog as dialogLib
    dialogLib.init()

def askUserForDirectory(title):
    return dialogLib.askUserForDirectory(title)

def askYesOrNo(title, message):
    return dialogLib.askYesOrNo(title, message)

def runLauncherDialog(gameDirectory, title):
    return dialogLib.runLauncherDialog(gameDirectory, title)
