import logging
log = logging.getLogger(__name__)

import datetime
import os


#DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y, %h %d'



class Entry(object):
    """Represents one of Diary's entries
    """

    POLYMORPHIC_WHEN_FOR_UI = {}
    POLYMORPHIC_WHEN_FOR_UI[type('')] = lambda self: self.when_for_ui_for_str
    POLYMORPHIC_WHEN_FOR_UI[type(datetime.datetime.utcnow())] = lambda self: self.when_for_ui_for_datetime


    def __init__(self, text='', when=datetime.datetime.utcnow()):
        self.text = text
        self.when = when


    def when_for_ui_for_str(self):
        return str(self.when)


    def when_for_ui_for_datetime(self):
        return self.when.strftime(DATE_FORMAT)


    def when_for_ui(self):
        if not self.when:
            self.when = ''

        #Tricky Python polymorphism
        fn = self.POLYMORPHIC_WHEN_FOR_UI[type(self.when)]
        return fn(self)()

    
    def is_not_empty(self):
        return self.text and len(self.text.strip()) >= 0


    def to_file(self):
        return '%s\n%s\n' % (self.when_for_ui(), self.text)


    def __str__(self):
        return '%s: %s' % (self.when, self.text)

    __repr__ = __str__

