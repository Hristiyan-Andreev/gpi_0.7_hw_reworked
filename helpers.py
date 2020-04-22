# import sys
import time
from datetime import datetime as dt

# sys.path.append('/home/pi/config')
import config as cf
import os
import logging as log


# datetime object containing current date and time
now = dt.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y %H:%M:%S")


# Time measurement class
class TimeMeasure():
    start_time = 0
    end_time = 0

    def __init__(self):
        self.start_time = time.time()
        self.end_time = time.time()

    def start_measure(self):
        self.start_time = time.time()

    def end_measure(self):
        self.end_time = time.time() - self.start_time

    def print_measure(self, msg = "Time measured"):
        print('{}: {}'.format(msg,str(self.end_time)))
        # print(msg + str(self.end_time))

def setup_main_logger():
    path = os.path.join('/','var','log')
    filename = '{}/{}'.format(path,'main_{}.log'.format(dt_string))

    file_handler = log.FileHandler(filename)
    file_handler.setLevel(log.DEBUG)
    file_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    logger = log.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(log.DEBUG)

    return logger
