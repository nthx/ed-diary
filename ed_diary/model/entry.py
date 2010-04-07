import logging
log = logging.getLogger(__name__)

import datetime
import os


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class Entry(object):
    """Represents one of Diary's entries
    """
    def __init__(self, text):
        self.text = text
        self.when = datetime.datetime.utcnow()


    def when_for_ui(self):
        return self.when and self.when.strftime(DATE_FORMAT) or ''

    def __str__(self):
        return '%s: %s' % (self.when, self.text)

    __repr__ = __str__
