import logging, sys
log = logging.getLogger(__name__)


import gtk
import hildon


class Controller(object):

    def __init__(self, root):
        self.root = root
        self.view = None #view setup later

        self.current_entry = self.root.diary.last_entry()
        self.any_entry_modified = False


    def store_current_entry(self, entry):
        self.current_entry = entry


    def app_quit(self, widget, data=None):
        self.save_if_needed()
        gtk.main_quit()


    def text_changed(self, signal_name, text_buffer):
        #log.debug("text_changed")
        current_entry = self.current_entry
        text = text_buffer.get_property('text')
        updated = current_entry.update(text)
        if updated:
            self.any_entry_modified = True


    def entry_clicked(self, treeview, path, view_column):
        index = path[0]
        self.store_current_entry(self.root.current_entries[index])
        self.view.window_main.show_entry()


    def load_prev_entry(self):
        self.save_if_needed()
        if not self.current_entry in self.root.current_entries:
            return

        index = self.root.current_entries.index(self.current_entry)
        if index > 0 and len(self.root.current_entries):
            self.store_current_entry(self.root.current_entries[index-1])
            self.view.window_main.show_entry()


    def load_next_entry(self):
        self.save_if_needed()
        def valid_index(index):
            return index < len(self.root.current_entries) - 1


        if not self.current_entry in self.root.current_entries:
            return

        index = self.root.current_entries.index(self.current_entry)

        if not valid_index(index):
            if self.current_entry.is_not_empty():
                self.root.new_entry()

        if valid_index(index):
            self.store_current_entry(self.root.current_entries[index+1])
            self.view.window_main.show_entry()


    def save_if_needed(self):
        if self.any_entry_modified:
            self.any_entry_modified = False
            self.root.diary.save_me()


    def menu_about(self, button, param):
        log.debug("menu_about")
        

