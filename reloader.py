import os
import sys
from os.path import getmtime
import threading as th
import time
import logging as log

class WatchDogReload(th.Thread):
    def __init__(self, files_to_watch, gpi_pair_dict = None, check_interval = 2, linux = True,\
                before_reload = None):
        '''
        @files_to_watch: Files watched for changes list of strings - e.g.\
             ['config.json','file.py']
        @check_interval: Time in seconds in between file change checks
        @linux: True if called on linux, false if called on windows
        '''
        #TODO: Attach a logger
        th.Thread.__init__(self, name='watch_and_reload_thread', daemon=True)
        self.files = files_to_watch
        self.start_up_edit_times = [(f, getmtime(f)) for f in self.files]
        self.check_interval = check_interval
        self.linux = linux
        if before_reload:
            self.before_reload_func = before_reload
            self.before_reload_dict = gpi_pair_dict

    def run(self):
        while True:
            time.sleep(self.check_interval)
            print('Checking files...')
            # Check whether a watched file has changed.
            for f, mtime in self.start_up_edit_times:
                if getmtime(f) != mtime:
                    # One of the files has changed, so restart the script.
                    print('--> restarting')
                    if self.linux is True:
                    # When running the script via `./daemon.py` (e.g. Linux/Mac OS), use
                        # if self.before_reload_func:
                        #     before_reload_func(before_reload_args)
                        os.execv(__file__, sys.argv)
                        pass

                    elif self.linux is False:
                        try:
                            if self.before_reload_func:
                                self.before_reload_func(self.before_reload_dict)
                        except AttributeError:
                            print('No pre reload command given')
                    # When running the script via `python daemon.py` (e.g. Windows), use
                        os.execv(sys.executable, ['python'] + sys.argv)
        