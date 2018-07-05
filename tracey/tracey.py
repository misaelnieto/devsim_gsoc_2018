#!/usr/bin/env python3
# coding=utf8
import sys
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import  Gio, GLib, Gtk, GdkPixbuf

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Maximize</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

WINDOW_TITLE = 'Tracey - Devsim structure viewer'


class TraceyAppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup logo, title and size
        self.props.title = WINDOW_TITLE
        self.props.default_width = 640
        self.props.default_height = 400
        self.set_icon_from_file('tracey.svg')

        # Now setup the header bar
        hb = Gtk.HeaderBar()
        hb.props.show_close_button = True
        hb.props.title = WINDOW_TITLE
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        button = Gtk.Button('Open')
        button.connect("clicked", self.on_open_clicked)
        box.add(button)
        hb.pack_start(box)
        # self.add(Gtk.TextView())
        self.set_titlebar(hb)

        # This stuff is for the gnome application menu
        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful(
            "maximize",
            None,
            GLib.Variant.new_boolean(False)
        )
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect(
            "notify::is-maximized",
            lambda obj, pspec: max_action.set_state(GLib.Variant.new_boolean(obj.props.is_maximized))
        )

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()

    def on_open_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            "Please choose a file",
            self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()

class TraceyApp(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.devsim.tracey",
                                 flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE)
        # Hook-up command line
        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = TraceyAppWindow(application=self, title=WINDOW_TITLE)

        self.window.show_all()
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        logo = GdkPixbuf.Pixbuf.new_from_file_at_size('tracey.svg', 128, 128)
        about_dialog.props.logo = logo
        about_dialog.props.program_name = "Tracey"
        about_dialog.props.version = "0.0"
        about_dialog.props.authors = ["Noe Nieto <nnieto@noenieto.com>"]
        about_dialog.props.comments = "A plotting tool for DevSim"
        about_dialog.props.copyright = "Copyright © 2018 Noe Nieto"
        about_dialog.props.license = "<Include the lcense here>"
        about_dialog.props.website = "https://devsim.org/"
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

if __name__ == '__main__':
    app = TraceyApp()
    app.run(sys.argv)
