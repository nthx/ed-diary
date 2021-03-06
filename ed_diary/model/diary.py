import logging
log = logging.getLogger(__name__)

from ed_diary.model.entry import Entry
import ed_diary.lib.simplejson as sjson
import datetime
import os
import shutil


HOME=os.environ.get('HOME') or '/home/user/'
CONFIG_DIR=os.path.join(HOME, '.eddiary')
DIARY_FILE=os.path.join(CONFIG_DIR, 'diary.txt')
DIARY_FILE_TMP=os.path.join(CONFIG_DIR, 'diary-save.txt')

DIARY_FILE_FOR_IPAD=os.path.join(CONFIG_DIR, 'diary-ipad.txt')
DIARY_FILE_TMP_FOR_IPAD=os.path.join(CONFIG_DIR, 'diary-save-ipad.txt')

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


    def add_entry(self, entry):
        if entry.is_not_empty():
            self.entries.append(entry)


    def import_me(self):
        log.debug('import_me')
        self.entries = []

        file, first_time = self.get_file_from_disk()
        for entry in self.parse_file(file):
            self.add_entry(entry)
        file.close()
        log.debug('%s entries imported' % len(self.entries))

        if not self.entries:
            self.entries.append(Entry(WELCOME))
        log.debug('/import_me')
        return self


    def save_me(self):
        log.debug('saving..')
        file, _ = self.get_file_from_disk(filename=DIARY_FILE_TMP, mode='w')
        file_ipad, _ = self.get_file_from_disk(filename=DIARY_FILE_TMP_FOR_IPAD, mode='w')
        json_diary = []

        for entry in self.entries:
            if entry.is_empty():
                continue
            file.write(entry.to_file())
            file.write('\n\n')
            json_diary.append(entry.as_json())

        file_ipad.write(sjson.dumps(json_diary, ensure_ascii = False, indent=4, sort_keys=True))


        file.close()
        shutil.move(DIARY_FILE_TMP, DIARY_FILE)
        shutil.move(DIARY_FILE_TMP_FOR_IPAD, DIARY_FILE_FOR_IPAD)
        log.debug('saved..')
        
        

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
            for format in ['%Y.%m.%d', '%Y:%m:%d', '%Y-%m-%d', '%Y:%m', '%Y.%m', '%Y-%m']:
                try:
                    return datetime.datetime.strptime(line, format)
                except Exception, e:
                    pass
            return line

        def represents_date(line):
            if line and line[0].isdigit() and len(line)>=4:
                date = parse_date(line)
                return True, date
            else:
                return False, None


        lines = file.read()
        lines = lines.split('\n')

        when = None
        text = []
        last_line = None

        for line in lines:
            is_date, _ = represents_date(line)

            if is_date and last_line:
                is_date = False #dont treat as date, when no blank line above a date

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
            last_line = line
            

        #and last entry
        if text:
            yield Entry('\n'.join(text).strip('\n'), when=when)
