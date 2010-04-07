import logging
log = logging.getLogger(__name__)

import os

from ed_diary.model.diary import Diary


class Root(object):
    """Just contains all objects (data) used by the app
    """
    def __init__(self):
        self.diary = Diary().import_me()
        self.current_entries = [] #filtered view to all_entries


    def build_data(self):
        log.debug('building data..')

        self.current_entries = self.diary.entries[:]


