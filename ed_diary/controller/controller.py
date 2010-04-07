import logging, sys
log = logging.getLogger(__name__)


import gtk
import hildon


class Controller(object):

    def __init__(self, root):
        self.root = root
        self.view = None #view setup later

        self.current_entry = self.root.diary.last_entry()


    def store_current_entry(self, entry):
        self.current_entry = entry


    def app_quit(self, widget, data=None):
        gtk.main_quit()


    def entry_clicked(self, treeview, path, view_column):
        index = path[0]
        self.store_current_entry(self.root.current_entries[index])
        self.view.window_main.show_entry()


    def load_prev_entry(self):
        if not self.current_entry in self.root.current_entries:
            return

        index = self.root.current_entries.index(self.current_entry)
        if index > 0 and len(self.root.current_entries):
            self.store_current_entry(self.root.current_entries[index-1])
            self.view.window_main.show_entry()


    def load_next_entry(self):
        if not self.current_entry in self.root.current_entries:
            return

        index = self.root.current_entries.index(self.current_entry)
        if index < len(self.root.current_entries) - 1:
            self.store_current_entry(self.root.current_entries[index+1])
            self.view.window_main.show_entry()


