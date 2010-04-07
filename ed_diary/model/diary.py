import logging
log = logging.getLogger(__name__)

from ed_diary.model.entry import Entry
import datetime
import os


HOME=os.environ.get('HOME') or '/home/user/'
CONFIG_DIR=os.path.join(HOME, '.eddiary')
DIARY_FILE=os.path.join(CONFIG_DIR, 'diary.txt')
DIARY_FILE2=os.path.join(CONFIG_DIR, 'diary-save.txt')

WELCOME="""
Hello to "Every Day Diary". An utility for you to store a not each day.

To continue just press Right Arrow.
"""

class Diary(object):
    """Represents a Diary. Diary has a list of entries.
    """
    def __init__(self):
        self.entries = []


    def last_entry(self):
        if self.entries:
            return self.entries[len(self.entries)-1]


    def new_entry(self):
        self.entries.append(Entry())


    def import_me(self):
        log.debug('import_me')
        self.entries = []

        file, first_time = self.get_file_from_disk()
        for entry in self.parse_file(file):
            self.entries.append(entry)
        file.close()

        if not self.entries:
            self.entries.append(Entry(WELCOME))
        log.debug('/import_me')
        return self


    def save_me(self):
        file = self.get_file_from_disk(name=DIARY_FILE2, mode='w')

        for entry in self.entries:
            file.write(entry.to_file())
            file.write('n\n')
        file.close()

        
        

    def get_file_from_disk(self, filename=DIARY_FILE, mode='r'):
        first_time = False
        if not os.path.exists(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)
            first_time = True

        if not os.path.exists(filename):
            file = open(filename, 'w')
            file.close()
            first_time = True

        return open(filename, mode), first_time
        

    def parse_file(self, file):
        def parse_date(line):
            line = line.strip(': ;-')
            for format in ['%Y.%m.%d', '%Y:%m:%d', '%Y:%m', '%Y.%m']:
                try:
                    return datetime.datetime.strptime(line, format)
                except Exception, e:
                    pass
            return line

        def represents_date(line):
            if line and line[0].isdigit() and len(line)>=1:
                date = parse_date(line)
                return True, date
            else:
                return False, None


        lines = file.read()
        lines = lines.split('\n')
        when = None
        text = []

        for line in lines:
            is_date, _ = represents_date(line)
            if is_date:

                if text:
                    #flush, cause new entry started
                    yield Entry('\n'.join(text).strip('\n'), when=when)
                    text = []
                    when = _


                elif not text:
                    #new entry starting
                    when = _

            elif not is_date:
                text.append(line.rstrip())
            
