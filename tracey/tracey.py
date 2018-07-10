#!/usr/bin/env python3
# coding=utf8
import sys
from string import ascii_lowercase
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import  Gio, GLib, Gtk, GdkPixbuf
from parser import DevsimData


WINDOW_TITLE = 'Tracey - Devsim structure viewer'
TRACEY_LOGO = 'tracey.svg'
COLUMN_TITLES = 'xyz' + ascii_lowercase[:-3][::-1]


class Workspace(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

        # TreeView for device and subsections
        self.devices_model = Gtk.TreeStore(str)
        self.devices_view = Gtk.TreeView(self.devices_model)
        self.devices_view.set_headers_visible(True)
        renderer = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Device (Resistor)', renderer, text=0)
        self.devices_view.append_column(col)
        self.devices_view.props.activate_on_single_click = True
        self.devices_view.props.enable_tree_lines = True
        self.devices_view.connect('row-activated', self.load_datagrid)

        # Background
        self.background = Gtk.Image.new_from_file(TRACEY_LOGO)

        # Finally, configure the pane
        self.pane = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        self.pack_start(
            self.pane,
            expand=True,
            fill=True,
            padding=0
        )
        scroll = Gtk.ScrolledWindow()
        scroll.add(self.devices_view)
        self.pane.add1(scroll)
        self.pane.add2(self.background)

        self.data_map = {}

    def load_data(self, filename):
        self.data = DevsimData(filename)
        self.load_sections()

    def load_datagrid(self, tree_widget, tree_path, tree_column):
        if str(tree_path) in self.data_map:
            datum = self.data_map[str(tree_path)]
            # How many columns do we need?
            n_columns = len(datum[0])

            # Data Grid
            model = Gtk.ListStore(*[str] * (n_columns))
            view = Gtk.TreeView(model)
            for n in range(n_columns):
                renderer = Gtk.CellRendererText()
                col = Gtk.TreeViewColumn(str, renderer, text=n)
                col.set_title(COLUMN_TITLES[n])
                view.append_column(col)
            self.pane.remove(self.pane.get_child2())
            scroll = Gtk.ScrolledWindow()
            scroll.add(view)
            self.pane.add2(scroll)

            # populate model
            for r in datum:
                model.append([str(c) for c in r])
            self.show_all()

    def register_datamap(self, t_iter, datum):
        self.data_map[
            self.devices_model.get_path(t_iter).to_string()
        ] = datum

    def load_sections(self):
        self.devices_view.get_column(0).set_title(self.data.name)
        coords_iter = self.devices_model.append(None, ["Coordinates"])
        self.register_datamap(coords_iter, self.data.coordinates)
        # Regions
        regions_iter = self.devices_model.append(None, ["Regions"])
        for rname, rdata in self.data.regions.items():
            region_iter = self.devices_model.append(regions_iter, ['{} ({})'.format(rname, rdata['material'])])
            self.devices_model.append(region_iter, ["Nodes"])
            self.register_datamap(region_iter, self.data.regions[rname]['nodes'])
            nss_iter = self.devices_model.append(region_iter, ["Node solutions"])
            for sname in rdata['node_solutions']:
                ns = self.devices_model.append(nss_iter, [sname])
                self.register_datamap(ns, self.data.regions[rname]['node_solutions'][sname])
            self.devices_model.append(region_iter, ["Edges"])
            ess_iter = self.devices_model.append(region_iter, ["Edge solutions"])
            for sname in rdata['edge_solutions']:
                self.devices_model.append(ess_iter, [sname])
                self.register_datamap(ns, self.data.regions[rname]['edge_solutions'][sname])
        contacts = self.devices_model.append(None, ["Contacts"])


class TraceyAppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup logo, title and size
        self.props.title = WINDOW_TITLE
        self.props.default_width = 640
        self.props.default_height = 400
        self.set_icon_from_file(TRACEY_LOGO)

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
        self.set_titlebar(hb)

        # Workspace
        self.wkspace = None
        self.bg_image = Gtk.Image.new_from_file(TRACEY_LOGO)
        self.add(self.bg_image)

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
            if self.wkspace is None:
                self.remove(self.bg_image)
                self.wkspace = Workspace()
                self.add(self.wkspace)
            self.wkspace.load_data(dialog.get_filename())
            self.show_all()
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

        builder = Gtk.Builder.new_from_string(open('system_menu.ui', 'r').read(), -1)
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
        logo = GdkPixbuf.Pixbuf.new_from_file_at_size(TRACEY_LOGO, 128, 128)
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
