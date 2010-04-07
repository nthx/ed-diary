import logging
log = logging.getLogger(__name__)

from ed_diary.model.entry import Entry
import os



class Diary(object):
    """Represents a Diary. Diary has a list of entries.
    """
    def __init__(self):
        self.entries = []


    def import_me(self):
        self.entries = []
        self.entries.append(Entry('abcdef'))
        self.entries.append(Entry('123456\nXYZ'))
        return self
        
        
