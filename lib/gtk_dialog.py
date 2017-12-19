import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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

