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
        window.set_app_menu(self.create_menu())
        return window


    def fill_main_area(self, window):
        self.ui_entry_date = gtk.Label("date...")
        self.ui_entry_date.set_alignment(0, 0)

        self.ui_entry_text = gtk.TextView()
        self.ui_entry_text.set_property('wrap-mode', gtk.WRAP_WORD_CHAR)

        #self.ui_entry_text.get_buffer().connect('changed', lambda text_buffer: self.controller.text_changed('changed', text_buffer))
        #self.ui_entry_text.get_buffer().connect('modified-changed', lambda text_buffer: self.controller.text_changed('modified-changed', text_buffer))

        #not working :(
        #self.ui_entry_text = hildon.TextView()
        #self.ui_entry_text.set_placeholder(self.controller.current_entry.text)

        right_a = lambda: gtk.Alignment(0, 1, 0, 0)
        left_a = lambda: gtk.Alignment(1, 0, 0, 0)

        date_labels = right_a()

        hbox = gtk.HBox(False, 5);
        hbox.add(gtk.Label('Date: '))
        hbox.add(self.ui_entry_date)

        vbox = gtk.VBox(False);
        vbox.pack_start(date_labels, expand=False, fill=False, padding=0)
        vbox.pack_start(self.ui_entry_text, expand=True, fill=True, padding=0)

        date_labels.add(hbox)
        window.add(vbox)


    def create_menu(self):
        menu = hildon.AppMenu()
        button = hildon.GtkButton(gtk.HILDON_SIZE_AUTO)
        button.set_label("About")
        button.connect("clicked", self.controller.menu_about, None)
        menu.append(button)
        menu.show_all()
        return menu

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
        #buffer = self.ui_entry_text.get_buffer()
        buffer = gtk.TextBuffer()
        self.ui_entry_text.set_buffer(buffer)
        buffer.set_text(entry.text)
        buffer.connect('changed', lambda b: self.controller.text_changed('changed', b))

        self.window.set_title(entry.when_for_ui())


    def show_entry(self):
        self._update_labels(self.controller.current_entry)


    def reload(self):
        self.show_entry()

