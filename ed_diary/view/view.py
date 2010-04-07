import logging
log = logging.getLogger(__name__)

import gtk
import hildon


from ed_diary.view.window_main import WindowMain



class View(object):

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.window_main = WindowMain(root, self, controller)

        program = hildon.Program.get_instance()

        program.add_window(self.window_main.window)
        self.window_main.window.show_all()

        #program.set_common_toolbar(common_toolbar)
        #program.set_common_app_menu(common_menu)

        program.set_can_hibernate(True)



    def start(self):
        log.debug('started')
        self.window_main.reload()
        #self.window_main.text_entry.grab_focus()
        gtk.main()
        




        



