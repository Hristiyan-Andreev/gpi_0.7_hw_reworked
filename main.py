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

# Start cue on Falling edge and Stop Cue on Rising edge
def start_stop_avail(gpi):
    # Start measuring the reaction time between getting GPIO input and getting response from Elemental server
    reaction_time.start_measure()

    global splice_counter                   # Use for counting splices
    edge = GPIO.input(gpi)                  # Read if rising or falling edge
    stream = gpi_stream_dict[gpi]           # Make a copy of the dict object, for better perfomance
    
    print("1. {} Event detcted".format(edge))
    print("2. Stream is in cue: {}".format(stream.in_cue))
              
    # Falling edge detected and Stream is NOT in Cue => Start cue
    if not edge and not stream.in_cue:
        response = stream.start_cue(elemental_api.start_cue)
        # print(response)
        
        reaction_time.end_measure()
        splice_counter += 1
        print('Splice count:{}\n'.format(splice_counter))
        reaction_time.print_measure()
        

        gpi_stream_dict[gpi].update_info(stream)    # Update the actual object in the stream dict
        #time.sleep(cf.wait_time)                    # Sleeps the thread for all GPIO inputs - not good

    # Rising edge detected and Stream is in Cue => Stop cue
    elif edge and stream.in_cue:        
        response = stream.stop_cue(elemental_api.stop_cue)
        # print(response)
        
        reaction_time.end_measure()
        reaction_time.print_measure()        
        
        gpi_stream_dict[gpi].update_info(stream)    # Update the actual object in the stream dict       
        #time.sleep(cf.wait_time)                    # Sleeps the thread for all GPIO inputs - not good
        

# Tie callbacks to events
for GPI in list(cf.gpi2stream):
    #GPIO.add_event_detect( GPI, GPIO.BOTH, callback = start_stop_avail, bouncetime = cf.wait_time*1000)
    GPIO.add_event_detect( GPI, GPIO.BOTH, callback = start_stop_avail)

@app.route('/')
def index():
    return "Working"

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')     
    except KeyboardInterrupt:
        GPIO.cleanup()