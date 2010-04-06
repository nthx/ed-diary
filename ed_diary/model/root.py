import logging
log = logging.getLogger(__name__)

import os

from ed_diary.util.storage import load_diary, store_diary


class Root(object):
    """Just contains all objects (data) used by the app
    """
    def __init__(self):
        self.all_entries = []
        self.current_entries = [] #filtered view to all_entries


    def build_data(self):
        log.debug('building data..')

        self.all_entries = load_diary()
        self.current_entries = self.all_entries[:]


