import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Application(Gtk.Window):
    def __init__(self, gameDirectory):
        super().__init__()
        self.connect("delete-event", Gtk.main_quit)
        self.gameDirectory = gameDirectory

        self._createWidgets()

    def _createWidgets(self):
        self.rootBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.labelBox.set_homogeneous(False)
        self.rootBox.pack_start(self.labelBox, True, True, 0)

        self.gameDirectoryLabel =  Gtk.Label("Some label")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.labelBox.pack_start(self.gameDirectoryLabel, True, True, 0)

        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.rootBox.pack_start(self.buttonBox, True, True, 0)

        self._addButton("Quit", self.onQuitClicked)

        self.add(self.rootBox)

    def _addButton(self, text, command):
        button = Gtk.Button.new_with_label("Quit")
        button.connect("clicked", command)
        self.buttonBox.pack_start(button, True, True, 0)
        return button

    def onQuitClicked(self, button):
        Gtk.main_quit()

def init():
    pass

def askUserForDirectory(title):
    dialog = Gtk.FileChooserDialog(title, None, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.set_default_response(Gtk.ResponseType.OK)

    result = None
    if dialog.run() == Gtk.ResponseType.OK:
        result = dialog.get_filename()

    dialog.destroy()
    __process_remaining_events()

    return result

def askYesOrNo(title, message):
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, message_format=message)
    dialog.set_title(title)

    response = dialog.run()
    dialog.destroy()
    __process_remaining_events()

    return response == Gtk.ResponseType.YES

def displayError(title, message):
    dialog = Gtk.MessageDialog(parent=None, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=message)
    dialog.set_title(title)

    dialog.run()
    dialog.destroy()
    __process_remaining_events()

def __process_remaining_events():
    while Gtk.events_pending():
        Gtk.main_iteration()

def runLauncherDialog(gameDirectory, title):
    app = Application(gameDirectory)
    app.show_all()
    Gtk.main()
    return None
