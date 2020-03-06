# import sys
import time
# from threading import Timer
# import elemental_api_class as liveapi

# sys.path.append('/home/pi/config')
import config as cf

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

