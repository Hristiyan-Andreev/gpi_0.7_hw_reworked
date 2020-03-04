import sys
# sys.modules.clear()
import time
import importlib
import RPi.GPIO as GPIO
import threading as td

from s_av_ctrl import StreamAvailController as StreamAvailCtrl


# sys.path.append('/home/pi/config')
import config as cf

# Set-up Elemental API class

# elemental_api.gen_cue_part_url()

# Make a new dict with GPIs as Keys and (class)StreamAvailCtrl as values
gpi_stream_dict = {}
for gpi, id in cf.gpi2stream.items():
    gpi_stream_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip)


# Setup GPIO inputs/outputs
    #Use Board pin numbering - etc. (12) in pinout command
GPIO.setmode(GPIO.BCM)
    #Setup GPIOs as inputs with PULL-UP
for GPI in list(cf.gpi2stream):
    GPIO.setup( GPI, GPIO.IN, pull_up_down=GPIO.PUD_UP)

locker = td.Lock()
# Tie callbacks to events

for GPI in list(cf.gpi2stream):
    GPIO.add_event_detect( GPI, GPIO.BOTH, callback = gpi_stream_dict[GPI].start_stop_avail , bouncetime = 20)


if __name__ == '__main__':
    try:
        while(True):
            pass
    except KeyboardInterrupt:
        GPIO.cleanup()