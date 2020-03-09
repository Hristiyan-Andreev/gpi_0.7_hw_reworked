import os
import sys
from os.path import getmtime
import threading as th
import time
import logging as log

class Reloader(th.Thread):
    def __init__(self, files_to_watch, gpi_event_dict = None, check_interval = 2, linux = True,\
                before_reload = None):
        '''
        @files_to_watch: Files watched for changes list of strings - e.g.\
             ['config.json','file.py']
        @check_interval: Time in seconds in between file change checks
        @linux: True if called on linux, false if called on windows
        '''
        th.Thread.__init__(self, name='watch_and_reload_thread', daemon=True)
        self.files = files_to_watch
        self.start_up_edit_times = [(f, getmtime(f)) for f in self.files]
        self.check_interval = check_interval
        self.linux = linux
        self.file = file
        self.logger = self.setup_logger()
        if before_reload:
            self.before_reload_func = before_reload
            self.before_reload_dict = gpi_event_dict

    def setup_logger(self):
        path = os.path.join('/','var','log')
        filename = '{}/{}'.format(path,'reloader.log')

        file_handler = log.FileHandler(filename)
        file_handler.setLevel(log.DEBUG)
        file_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        logger = log.getLogger(__name__)
        logger.addHandler(file_handler)
        logger.setLevel(log.DEBUG)

        return logger

    def run(self):
        while True:
            time.sleep(self.check_interval)
            # Check whether a watched file has changed.
            for f, mtime in self.start_up_edit_times:
                if getmtime(f) != mtime:
                    # One of the files has changed, so restart the script.
                    self.logger.info('Change detected in {} --> Restarting'.format(f))
                    if self.linux is True:
                    # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
                        try:
                            if self.before_reload_func:
                                self.before_reload_func(self.before_reload_dict)
                        except AttributeError:
                            print('No pre reload command given')

                        # print(sys.executable, sys.argv)
                        os.execl(sys.executable, sys.executable, *sys.argv)
                        pass

                    elif self.linux is False:
                    # When running the script via `python daemon.py` (e.g. Windows), use
                        try:
                            if self.before_reload_func:
                                self.before_reload_func(self.before_reload_dict)
                        except AttributeError:
                            print('No pre reload command given')

                        # print(sys.executable, sys.argv)
                        os.execv(sys.executable, ['python3'] + sys.argv)
        