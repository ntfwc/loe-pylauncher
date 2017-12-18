import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def init():
    pass

def askUserForDirectory(title):
    dialog = Gtk.FileChooserDialog(title, None, Gtk.FileChooserAction.SELECT_FOLDER, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.set_default_response(Gtk.ResponseType.OK)

    dialog.run()
    dialog.destroy()

    while Gtk.events_pending():
        Gtk.main_iteration()
