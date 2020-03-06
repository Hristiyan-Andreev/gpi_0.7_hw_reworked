#!/usr/bin/env python
import sys
import time
import importlib
# import RPi.GPIO as GPIO

from s_av_ctrl import StreamAvailController as StreamAvailCtrl
from reloader import Reloader

# sys.path.append('/home/pi/config')
import config as cf

# Set-up reloader on file changes
WATCHED_FILES = ['config.json']
reload_thread = Reloader(WATCHED_FILES, linux=True)
reload_thread.start()

# Make a new dict with GPIs as Keys and (class)StreamAvailCtrl as values
gpi_stream_dict = {}
for gpi, id in cf.gpi2stream.items():
    gpi_stream_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip)


# Setup GPIO inputs/outputs
    #Use Board pin numbering - etc. (12) in pinout command
# GPIO.setmode(GPIO.BCM)
#     #Setup GPIOs as inputs with PULL-UP
# for GPI in list(cf.gpi2stream):
#     GPIO.setup( GPI, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Tie callbacks to events

# for GPI in list(cf.gpi2stream):
#     GPIO.add_event_detect( GPI, GPIO.BOTH, callback = gpi_stream_dict[GPI].\
#         start_stop_avail , bouncetime = 20)


if __name__ == '__main__':
    try:
        while(True):
            pass
    except KeyboardInterrupt:
        # GPIO.cleanup()
        pass