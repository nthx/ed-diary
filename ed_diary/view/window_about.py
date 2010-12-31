
import logging
log = logging.getLogger(__name__)

import gobject
import gtk
import hildon


ABOUT = """
"Every Day Diary". An utility for you to store a not each day.
Written in Python by Tomasz Nazar <tomasz.nazar@aspectized.com>

It's so simple:
*) Start the app
*) You can see your latest entry
*) Right arrow to add today's entry
*) Close
*) Your entries are automatically stored when you exist the app


Your Diary:
*) is stored inside /home/user/.eddiary/diary.txt file
*) is a simple, long file with entries represented by a single line with
date (2009/08/17) and further text lines.
"""


class WindowAbout(object):

    def __init__(self):
        pass


    def build_and_show(self):
        log.debug('building main..')

        window = hildon.StackableWindow()
        window.set_title('About Ed Diary')
        pannable_area = hildon.PannableArea()

        about = gtk.Label(ABOUT)
        pannable_area.add_with_viewport(about)

        vbox = gtk.VBox(False);
        vbox.pack_start(pannable_area, expand=True, fill=True, padding=0)

        window.add(vbox)
        window.show_all()


