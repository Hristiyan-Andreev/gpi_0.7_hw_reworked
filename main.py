import sys
import time
import RPi.GPIO as GPIO

from flask import Flask
from s_av_ctrl import StreamAvailController as StreamAvailCtrl
import elemental_api_class as liveapi


# sys.path.append('/home/pi/config')
import config as cf

# reaction_time = TimeMeasure()
splice_counter = 0

# Configure the web app (needed only for autorestart)
app = Flask(__name__)
app.config.from_object(cf.FlaskConfig)

# Set-up Elemental API class
elemental_api = liveapi.Elemental_api(cf.elemental_ip)
elemental_api.gen_cue_part_url()

# Make a new dict with GPIs as Keys and (class)StreamAvailCtrl as values
gpi_stream_dict = {}
for gpi, id in cf.gpi2stream.items():
    gpi_stream_dict[gpi] = StreamAvailCtrl(id, elemental_api)


# Setup GPIO inputs/outputs
    #Use Board pin numbering - etc. (12) in pinout command
GPIO.setmode(GPIO.BCM)
    #Setup GPIOs as inputs with PULL-UP
for GPI in list(cf.gpi2stream):
    GPIO.setup( GPI, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Tie callbacks to events
for GPI in list(cf.gpi2stream):
    #GPIO.add_event_detect( GPI, GPIO.BOTH, callback = start_stop_avail, bouncetime = cf.wait_time*1000)
    GPIO.add_event_detect( GPI, GPIO.BOTH, callback = gpi_stream_dict[GPI].start_stop_avail , bouncetime = 20)

@app.route('/')
def index():
    return "Working"

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')     
    except KeyboardInterrupt:
        GPIO.cleanup()