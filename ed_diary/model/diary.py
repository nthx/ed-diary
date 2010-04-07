import logging
log = logging.getLogger(__name__)

from ed_diary.model.entry import Entry
import os


HOME=os.environ.get('HOME') or '/home/user/'
CONFIG_DIR=os.path.join(HOME, '.eddiary')
DIARY_FILE=os.path.join(CONFIG_DIR, 'diary.txt')

WELCOME="""
Hello to "Every Day Diary". An utility for you to store a not each day.

To continue just press Right Arrow.
"""

class Diary(object):
    """Represents a Diary. Diary has a list of entries.
    """
    def __init__(self):
        self.entries = []


    def import_me(self):
        self.entries = []

        file, first_time = self.get_file_from_disk()
        for entry in self.parse_file(file):
            self.entries.append(entry)
        file.close()

        if not self.entries:
            self.entries.append(Entry(WELCOME))
        return self
        
        

    def get_file_from_disk(self):
        first_time = False
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
            first_time = True

        if not os.path.exists(DIARY_FILE):
            file = open(DIARY_FILE, 'w')
            file.close()
            first_time = True

        return open(DIARY_FILE, 'r'), first_time
        

    def parse_file(self, file):
        content = file.read()
        lines = content.split('\n\n')

        log.debug('%s entries' % len(lines))

        for line in lines:
            line = line.strip().strip('\n')
            when, text = self.parse_entry(line)
            yield Entry(text, when=when)


    def parse_entry(self, line):
        return '', line

