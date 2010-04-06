import logging
log = logging.getLogger(__name__)

import datetime
import os



class Entry(object):
    """Represents one of Diary's entries
    """
    def __init__(self, text):
        self.text = text
        self.when = datetime.datetime.utcnow()


