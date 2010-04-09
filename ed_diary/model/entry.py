import logging
log = logging.getLogger(__name__)

import datetime
import os


FILE_DATE_FORMAT = '%Y-%m-%d'
UI_DATE_FORMAT = '%Y, %h %d'



class Entry(object):
    """Represents one of Diary's entries
    """

    POLYMORPHIC_WHEN_FOR_UI = {}
    POLYMORPHIC_WHEN_FOR_UI[type('')] = lambda self: self.when_for_ui_for_str
    POLYMORPHIC_WHEN_FOR_UI[type(datetime.datetime.now())] = lambda self: self.when_for_ui_for_datetime


    def __init__(self, text='', when=datetime.datetime.now()):
        self.text = text
        self.when = when


    def when_for_ui_for_str(self, for_file=False):
        return str(self.when)


    def when_for_ui_for_datetime(self, for_file=False):
        if for_file:
            return self.when.strftime(FILE_DATE_FORMAT)
        else:
            return self.when.strftime(UI_DATE_FORMAT)


    def when_for_ui(self, for_file=False):
        if not self.when:
            self.when = ''

        #Tricky Python polymorphism
        fn = self.POLYMORPHIC_WHEN_FOR_UI[type(self.when)]
        return fn(self)(for_file=for_file)

    
    def update(self, text):
        self.text = text
        return True


    def is_not_empty(self):
        return self.text and len(self.text.strip()) >= 0


    def is_empty(self):
        return not self.is_not_empty()


    def to_file(self):
        return '%s\n%s\n' % (self.when_for_ui(for_file=True), self.text)


    def __str__(self):
        return '%s: %s' % (self.when, self.text)

    __repr__ = __str__

