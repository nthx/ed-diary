import logging
log = logging.getLogger(__name__)

import os



class Diary(object):
    """Represents a Diary. Diary has a list of entries.
    """
    def __init__(self):
        self.entries = []


