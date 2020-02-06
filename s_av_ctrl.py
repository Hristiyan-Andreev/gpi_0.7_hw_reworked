from threading import Timer
import RPi.GPIO as GPIO

from helpers import TimeMeasure


class StreamAvailController: 
    
    def __init__(self, id, elemental_api):
        self.stream_id = id
        self.in_cue = False
        self.splice_counter = 0
        self.interrupt_counter = 0
        self.elemental_api = elemental_api
        self.reaction_time = TimeMeasure()
        # self.channel_locked = False
        
    def __str__(self):
        return "GPI: {} str_id: {} in_cue: {}".format(self.gpi_input, self.stream_id, self.in_cue)
        
    def update_info(self, stream):
        self.in_cue = stream.in_cue
        
    def start_cue(self):
        response = self.elemental_api.start_cue(self.stream_id)
        print("3. Starting cue")
        self.in_cue = True
        return response
        
    def stop_cue(self):
        response = self.elemental_api.stop_cue(self.stream_id)
        print("3. Stopping cue")
        self.in_cue = False
        return response

    def start_stop_avail(self, gpi_triggered):
        edge = GPIO.input(gpi_triggered)        # Read if rising or falling edge
        self.interrupt_counter += 1
        self.reaction_time.start_measure()

        print('--------------------------------------------\n')
        print("1. {} Event detcted / Number: {}".format(edge,self.interrupt_counter))
        print("2. Stream is in cue: {}".format(self.in_cue))

        # Falling edge detected and Stream is NOT in Cue => Start cue
        if not edge and not self.in_cue:
            response = self.start_cue()
            self.reaction_time.end_measure()
            self.splice_counter += 1

            print('4. AD STARTED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
            # print(response.text)     
            self.reaction_time.print_measure()
            print('--------------------------------------------\n')

        # Rising edge detected and Stream is in Cue => Stop cue
        elif edge and self.in_cue:
            response = self.stop_cue()
            self.reaction_time.end_measure()
            
            print('4. AD STOPPED: Splice count:{} / Event Num: {}\n'.format(self.splice_counter, self.interrupt_counter))
            # print(response.text)
            self.reaction_time.print_measure()       
            print('--------------------------------------------\n')