import threading as td
import RPi.GPIO as GPIO
import datetime as dt
import time

from helpers import TimeMeasure


class StreamAvailController: 
    
    def __init__(self, gpio, id, elemental_api):
        self.gpi_trigger = gpio
        self.stream_id = id
        self.in_cue = False
        self.stream_locked = False
        self.lock_interval = 3
        self.splice_counter = 0
        self.interrupt_counter = 0
        self.elemental_api = elemental_api
        self.reaction_time = TimeMeasure()


    def __str__(self):
        return "GPI: {} str_id: {} in_cue: {}".format(self.gpi_input, self.stream_id, self.in_cue)
        
    def update_info(self, stream):
        self.in_cue = stream.in_cue
        
    def start_cue(self):
        if self.stream_locked:
            return 1
        response = self.elemental_api.start_cue(self.stream_id)
        self.lock_stream()
        print("3. Starting cue")
        self.in_cue = True
        return response
        
    def stop_cue(self):
        if self.stream_locked:
            return 1
        response = self.elemental_api.stop_cue(self.stream_id)
        print("3. Stopping cue")
        self.in_cue = False
        return response

    # def event_detected(self, gpi_trig):
    #     ed = GPIO.input(gpi_trig)        # Read if rising or falling edge
    #     # start_stop_av = lambda gpi_triggered=gpi_trig, edge=ed: self.start_stop_avail(gpi_triggered, edge)
    #     td.Thread(target=start_stop_av).start()


    def start_stop_avail(self, gpi_triggered):
        # time.sleep(0.001)
        edge = GPIO.input(gpi_triggered)        # Read if rising or falling edge
        self.reaction_time.start_measure()
        self.interrupt_counter += 1

        print('--------------------------------------------\n')
        print("1.{} / {} Event detcted / Number: {}".format(dt.datetime.now(), edge, self.interrupt_counter))
        print("2. Stream is in cue: {}".format(self.in_cue))

        # Falling edge detected and Stream is NOT in Cue => Start cue
        if not edge and not self.in_cue:
            response = self.start_cue()
            if response is 1:
                print('Stream is locked!')

                return 0

            self.reaction_time.end_measure()
            self.splice_counter += 1

            print('4. AD STARTED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
            print(response.text)
            self.reaction_time.print_measure()
            print('--------------------------------------------\n')

            return 0

        # Rising edge detected and Stream is in Cue => Stop cue
        elif edge and self.in_cue:
            response = self.stop_cue()
            self.reaction_time.end_measure()
            if response is 1:
                print('Stream is locked!')
                return 0
            
            print('4. AD STOPPED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
            print(response.text)
            self.reaction_time.print_measure()       
            print('--------------------------------------------\n')

            return 0

        return 0

    def lock_stream(self):
        self.stream_locked = True
        unlock_timer = td.Timer(self.lock_interval, self.unlock_stream)
        unlock_timer.start()

    def unlock_stream (self):
        self.stream_locked = False

        # If GPIO input is still 0 -> return
        if not GPIO.input(self.gpi_trigger):
            return 0

        # If GPIO input went to 1 -> stop cue
        response = self.stop_cue()
