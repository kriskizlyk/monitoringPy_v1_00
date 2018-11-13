import os, gi
import threading
import time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib, GObject
from database.admin import DataBase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIEWS_DIR = os.path.join(BASE_DIR, 'views')

class Window(Gtk.Window, GObject.GObject):
    def __init__(self, name, handler):
        window_name = name
        path = os.path.join(VIEWS_DIR, 'glade')
        gladefile = path + '/' + window_name + '.glade'

        # Create a GTK Window Object
        builder = Gtk.Builder()

        # Link all the GTK objects to a glade file.
        builder.add_from_file(gladefile)

        # Create a database of all the glade widgets.
        DataBase.create_widget_database(builder.get_objects())

        # Link window to the windows handler
        builder.connect_signals(handler)

        # Add css styling from my custom file.
        css = Gtk.CssProvider()
        css.load_from_path(VIEWS_DIR + '/glade/css/custom.css')

        context = Gtk.StyleContext()
        context.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Get the GTKWindow ID from the glade file and show window.
        window = builder.get_object(window_name)

        # Show the window.make
        window.show_all()

        # Add a Label Update using the built in GObject Thread.
        GObject.timeout_add(100, self.label_refresh)

    def label_refresh(self):
        DataBase.set_value("date_time", time.strftime("%H:%M"))
        DataBase.refresh_tag_database()
        return True