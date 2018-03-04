import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GObject

from lib.constants import (GAME_DIRECTORY_LABEL_PREFIX,
                           LOCAL_VERSION_LABEL_PREFIX,
                           LOCAL_VERSION_LABEL_CHECKING,
                           LOCAL_VERSION_LABEL_CHECK_FAILED,
                           AVAILABLE_VERSION_LABEL_PREFIX,
                           AVAILABLE_VERSION_LABEL_CHECKING,
                           AVAILABLE_VERSION_LABEL_CHECK_FAILED,
                           QUIT_BUTTON_TEXT,
                           CHANGE_GAME_DIR_BUTTON_TEXT,
                           STATUS_SAME_POSTFIX,
                           STATUS_NEW_POSTFIX)

import lib.game_dir_handling
import lib.version_fetching

import threading

class Application(Gtk.Window):
    def __init__(self, gameDirectory):
        super().__init__()
        self.connect("delete-event", Gtk.main_quit)
        self.gameDirectory = gameDirectory
        self.localVersion = None
        self.availableVersion = None

        self._createWidgets()

        self._startLocalVersionFetcher()

    def _createWidgets(self):
        self.rootBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.labelBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.labelBox.set_homogeneous(False)
        self.rootBox.pack_start(self.labelBox, True, True, 0)

        self.gameDirectoryLabel = self._addLabel()
        self._updateGameDirectoryLabel()

        self.localVersionLabel = self._addLabel()
        self._updateLocalVersionLabel()

        self.availableVersionLabel = self._addLabel()
        self._updateAvailableVersionLabel()

        self.buttonBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.rootBox.pack_start(self.buttonBox, True, True, 0)

        self._addButton(QUIT_BUTTON_TEXT, self.onQuitClicked)
        self._addButton(CHANGE_GAME_DIR_BUTTON_TEXT, self.onChangeGameDirectoryClicked)

        self.add(self.rootBox)

    def _addButton(self, text, command):
        button = Gtk.Button.new_with_label(text)
        button.connect("clicked", command)
        self.buttonBox.pack_start(button, True, True, 0)
        return button

    def _addLabel(self):
        label =  Gtk.Label()
        label.set_justify(Gtk.Justification.LEFT)
        self.labelBox.pack_start(label, True, True, 0)
        return label

    def _updateGameDirectoryLabel(self):
        self.gameDirectoryLabel.set_text(GAME_DIRECTORY_LABEL_PREFIX + '"' + self.gameDirectory + '"')

    def _updateLocalVersionLabel(self):
        version = self.localVersion if self.localVersion != None else ""
        self.localVersionLabel.set_text(LOCAL_VERSION_LABEL_PREFIX + version)

    def _updateAvailableVersionLabel(self):
        version = self.availableVersion if self.availableVersion != None else ""
        postfix = ""
        if self.availableVersion != None and self.localVersion != None:
            postfix = STATUS_SAME_POSTFIX if self.availableVersion == self.localVersion else STATUS_NEW_POSTFIX

        self.availableVersionLabel.set_text(AVAILABLE_VERSION_LABEL_PREFIX + version + postfix)

    def _startLocalVersionFetcher(self):
        self.localVersionLabel.set_text(LOCAL_VERSION_LABEL_CHECKING)
        thread = threading.Thread(target=_fetchLocalVersion, args=(self.gameDirectory,self._localVersionFetcherCallback))
        thread.daemon = True
        thread.start()

    def _localVersionFetcherCallback(self, version):
        def gtkTask():
            self.localVersion = version
            if (version == None):
                self.localVersionLabel.set_text(LOCAL_VERSION_LABEL_CHECK_FAILED)
            else:
                self._updateLocalVersionLabel()
                if self.availableVersion != None:
                    self._updateAvailableVersionLabel()
        GObject.idle_add(gtkTask)

    def onChangeGameDirectoryClicked(self, button):
        gameDirectory = lib.game_dir_handling.askUserForGameDirectory()
        if gameDirectory != None:
            self.gameDirectory = gameDirectory
            lib.game_dir_handling.saveGameDirectory(gameDirectory)
            print("Changed game directory to '%s'" % gameDirectory)
            self._updateGameDirectoryLabel()
            self._startLocalVersionFetcher()

    def onQuitClicked(self, button):
        Gtk.main_quit()

def _fetchLocalVersion(gameDirectory, callback):
    callback(lib.version_fetching.getInstalledVersionId(gameDirectory))

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
