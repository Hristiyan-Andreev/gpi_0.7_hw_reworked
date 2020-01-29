import sys
import time
from threading import Timer
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


# GPI to Stream class with more information
class GpiStream: 
    
    def __init__(self, id):
        self.stream_id = id
        self.in_cue = False
        # self.channel_locked = False
        
    def __str__(self):
        return "GPI: {} str_id: {} in_cue: {}".format(self.gpi_input, self.stream_id, self.in_cue)
        
    def update_info(self, stream):
        self.in_cue = stream.in_cue
        
    def start_cue(self, api_start_cue):
        response = api_start_cue(self.stream_id)
        print("3. Starting cue")
        self.in_cue = True
        return response
        
    def stop_cue(self, api_stop_cue):
        response = api_stop_cue(self.stream_id)
        print("3. Stopping cue")
        self.in_cue = False
        return response

 