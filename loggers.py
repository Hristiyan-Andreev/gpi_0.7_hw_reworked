from datetime import datetime as dt
import logging as log
import os


def get_timestamp():
    now = dt.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    return dt_string

def get_formatted_f_handler(filename):

    file_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    file_handler = log.FileHandler(filename)
    file_handler.setLevel(log.DEBUG)
    file_handler.setFormatter(file_format)
    
    return file_handler

def get_formatted_s_handler():

    console_format = log.Formatter('%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    console_handler = log.StreamHandler()
    console_handler.setLevel(log.DEBUG)
    console_handler.setFormatter(console_format)

    return console_handler


def setup_logger(filename = None):
    dt_string = get_timestamp()
    path = os.path.join('/','var','log')
    if filename:
        full_filename = '{}/{}'.format(path,'{}_{}.log'.format(filename,dt_string))
        file_handler = get_formatted_f_handler(full_filename)

    console_handler = get_formatted_s_handler()

    logger = log.getLogger(__name__)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(log.DEBUG)

    return logger
