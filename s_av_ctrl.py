import threading as td
# import RPi.GPIO as GPIO
import datetime as dt
import time

from helpers import TimeMeasure
import elemental_api_class as liveapi

class StreamAvailController: 
    
    def __init__(self, gpi_trigger, event_id, elemental_ip, lock_interval = 3, in_cue = False):
        self.gpi_trigger = gpi_trigger
        self.event_id = event_id
        self.elemental_api = liveapi.Elemental_api(elemental_ip)
        self.lock_interval = lock_interval
        self.in_cue = in_cue

        self.stream_locked = False
        self.splice_counter = 0
        self.interrupt_counter = 0
        self.reaction_time = TimeMeasure()

    def __str__(self):
        return "GPI: {} str_id: {} in_cue: {}".format(self.gpi_input, self.stream_id, self.in_cue)

    def event_detected(self):
        # Edge double checking to avoid false positives
        edge_before = GPIO.input(self.gpi_trigger)
        time.sleep(0.003)
        edge_after = GPIO.input(self.gpi_trigger)

        # If two edges are different -> measure third time
        if edge_before != edge_after:
            time.sleep(0.001)
            edge = GPIO.input(self.gpi_trigger)

        elif edge_before == edge_after:
            time.sleep(0.001)     # Added for determinisim between the two cases
            edge = edge_before

        
        self.reaction_time.start_measure()
        self.interrupt_counter += 1

        print('--------------------------------------------\n')
        print("1.{} / {} Event detcted / Number: {}".format(dt.datetime.now(), edge, self.interrupt_counter))
        print("2. Stream is in cue: {}".format(self.in_cue))

        self.start_avail() if edge else self.stop_avail()

        return 0


    def start_avail(self):

        try:
            if self.in_cue:
                raise Exception("Stream ({}) is already in avail".format(self.event_id))
                return 1

            if self.stream_locked:
                raise Exception("Stream ({}) is locked".format(self.event_id))
                return 1

            response = self.elemental_api.start_cue(self.stream_id)
            if response.status_code != 200:
                raise Exception("Elemental server error: {}".format(response.status_code))
                return 1

            self.in_cue = True
            self.lock_stream()
            
            self.reaction_time.end_measure()
            self.splice_counter += 1
            print('3. AD STARTED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
            print(response.text)
            self.reaction_time.print_measure()
            print('--------------------------------------------\n')

            return response        

    def stop_avail(self):
        try:
            if not self.in_cue:
                raise Exception("Stream ({}) is not in avail".format(self.event_id))
                return 1

            if self.stream_locked:
                raise Exception("Stream ({}) is locked".format(self.event_id))
                return 1

            response = self.elemental_api.stop_cue(self.stream_id)
            if response.status_code != 200:
                raise Exception("Elemental server error: {}".format(response.status_code))
                return 1

        self.in_cue = False
        self.lock_stream()

        print('3. AD STOPPED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
        print(response.text)
        self.reaction_time.print_measure()       
        print('--------------------------------------------\n')

        return response
    
 
    def lock_stream(self):
        self.stream_locked = True
        unlock_timer = td.Timer(self.lock_interval, self.unlock_stream)
        unlock_timer.start()


    def unlock_stream (self):
        self.stream_locked = False

        # If stream was locked on entering in an avail (GPIO -> 1)
        if self.in_cue:
            # If GPIO input is still 1 -> do nothing // If GPIO went to 1 -> stop cue
            # return 1 if GPIO.input(self.gpi_trigger) else self.stop_cue()
            pass
          
        # Or stream was locked on exiing from an avail (GPIO -> 0)
        elif not self.in_cue:
            # If GPIO input is still 0 -> do nothing // if GPIO went to 1 -> start cue
            # return 1 if not GPIO.input(self.gpi_trigger) else self.start_cue()
            pass
