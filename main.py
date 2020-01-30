import sys
import time
import RPi.GPIO as GPIO
from flask import Flask
from helpers import TimeMeasure, GpiStream
import elemental_api_class as liveapi


# sys.path.append('/home/pi/config')
import config as cf

reaction_time = TimeMeasure()
splice_counter = 0

# Configure the web app (needed only for autorestart)
app = Flask(__name__)
app.config.from_object(cf.FlaskConfig)

# Make a new dict with GPIs as Keys and (class)GpiStreams as values
gpi_stream_dict = {}
for gpi, id in cf.gpi2stream.items():
    gpi_stream_dict[gpi] = GpiStream(id)

# Set-up Elemental API class
elemental_api = liveapi.Elemental_api(cf.elemental_ip)
elemental_api.gen_cue_part_url()


# Setup GPIO inputs/outputs
    #Use Board pin numbering - etc. (12) in pinout command
GPIO.setmode(GPIO.BCM)
    #Setup GPIOs as inputs with PULL-UP
for GPI in list(cf.gpi2stream):
    GPIO.setup( GPI, GPIO.IN, pull_up_down=GPIO.PUD_UP )


# Define callbacks

# When falling edge detected -> Start ad avail
def start_avail(gpi):
    global splice_counter
    reaction_time.start_measure()
    stream = gpi_stream_dict[gpi]           # Make a copy of the dict object, for better perfomance
    print('--------------------------------------------\n')
    print('1. Rising edge detected\n')

    # Check if the stream is already in a cue and return if so
    if stream.in_cue:
        print('2. NO ACTION: Stream is already in cue\n')
        return 1
    
    response = stream.start_cue(elemental_api.start_cue)
    print(response.text)
    reaction_time.end_measure()


    #TODO: Check the status code of the response    
    splice_counter += 1
    print('2. AD STARTED: Splice count:{}\n'.format(splice_counter))
    reaction_time.print_measure()    
    print('--------------------------------------------\n')

    gpi_stream_dict[gpi].update_info(stream)    # Update the actual object in the stream dict    
    

# When rising edge detected -> Stop ad avail
def stop_avail(gpi):
    global splice_counter
    reaction_time.start_measure()
    stream = gpi_stream_dict[gpi]           # Make a copy of the dict object, for better perfomance

    if stream.in_cue is False:
        print('2. NO ACTION: Stream is not in cue\n')
        return 1

    response = stream.stop_cue(elemental_api.stop_cue)    
    reaction_time.end_measure()

    print('2. AD STOPPED: Splice count:{}\n'.format(splice_counter))
    print(response.text)
    reaction_time.print_measure()        
    print('--------------------------------------------\n')
    
    gpi_stream_dict[gpi].update_info(stream)    # Update the actual object in the stream dict       
    

# Tie callbacks to events
for GPI in list(cf.gpi2stream):
    # GPIO.add_event_detect( GPI, GPIO.BOTH, callback = start_stop_avail, bouncetime = cf.wait_time*1000)
    # GPIO.add_event_detect( GPI, GPIO.BOTH, callback = start_stop_avail)
    GPIO.add_event_detect( GPI, GPIO.FALLING, callback = start_avail)
    GPIO.add_event_detect( GPI, GPIO.RISING, callback = stop_avail)

@app.route('/')
def index():
    return "Working"

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')     
    except KeyboardInterrupt:
        GPIO.cleanup()