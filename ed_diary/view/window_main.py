import logging
log = logging.getLogger(__name__)

import gobject
import gtk
import hildon



class WindowMain(object):

    def __init__(self, root, view, controller):
        self.root = root
        self.view = view
        self.controller = controller

        self.ui_entry_date = None
        self.ui_entry_text = None

        self.window = self.build()


    def build(self):
        log.debug('building main..')

        window = hildon.StackableWindow()
        window.connect("destroy", self.controller.app_quit)

        self.fill_main_area(window)

        window.add_toolbar(self.create_navigation_toolbar())
        return window


    def fill_main_area(self, window):
        self.ui_entry_date = gtk.Label("date...")
        self.ui_entry_date.set_alignment(0, 0)

        self.ui_entry_text = gtk.TextView()
        self.ui_entry_text.get_buffer().set_text(self.controller.current_entry.text)

        x = """
        align = gtk.Alignment(0, 1, 0, 0)
        vbox = gtk.VBox(False)
        vbox.pack_start(self.ui_entry_date, False, False, 0)
        vbox.pack_start(self.ui_entry_text, False, False, 0)
        align.add(vbox)
        window.add(align)
        """

        y="""
        """
        halign = gtk.Alignment(1, 0, 0, 0);
        valign = gtk.Alignment(0, 1, 0, 0);
        hbox = gtk.HBox(False);
        vbox = gtk.VBox(False);


        hbox.add(self.ui_entry_date)
        vbox.add(self.ui_entry_text)

        halign.add(hbox)

        vbox.pack_start(valign, False, False, 0)
        vbox.pack_start(halign, False, False, 0)
        #vbox.add(halign)
        window.add(vbox)




    def create_navigation_toolbar(self):
        toolbar = gtk.Toolbar()

        self.toolbar_prev = gtk.ToolButton(
            gtk.image_new_from_stock(gtk.STOCK_GO_BACK,
            gtk.ICON_SIZE_LARGE_TOOLBAR),
            "Back")
        toolbar.insert(self.toolbar_prev, 0)

        self.toolbar_next = gtk.ToolButton(
            gtk.image_new_from_stock(gtk.STOCK_GO_FORWARD,
            gtk.ICON_SIZE_LARGE_TOOLBAR),
            "Forward")
        toolbar.insert(self.toolbar_next, 1)

        self.toolbar_prev.connect("clicked", lambda x: self.controller.load_prev_entry())
        self.toolbar_next.connect("clicked", lambda x: self.controller.load_next_entry())
        return toolbar


    def _update_labels(self, entry):
        self.ui_entry_date.set_label(entry.when_for_ui())
        self.ui_entry_text.get_buffer().set_text(entry.text)
        self.window.set_title(entry.when_for_ui())


    def show_entry(self):
        entry = self.controller.current_entry
        log.debug(entry)

        self._update_labels(entry)


    def reload(self):
        self.show_entry()

