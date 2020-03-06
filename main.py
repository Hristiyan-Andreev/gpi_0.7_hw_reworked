#!/usr/bin/env python
import sys
import time
import importlib
# import RPi.GPIO as GPIO

from s_av_ctrl import StreamAvailController as StreamAvailCtrl
from reloader import Reloader
from state_manager import StateManager

# sys.path.append('/home/pi/config')
import config as cf


# Set-up state manager
stater = StateManager(cf.LAST_EXIT_FILE, cf.STATE_FILE)

# Make a new dict with GPIs as Keys and (class)StreamAvailCtrl as values
# Check wether last exit was from reload and load state if necessary
gpi_event_dict = {}
if stater.is_last_exit_from_reload() is True:
    gpi_cue_state = stater.load_gpi_state()

    for gpi, id in cf.gpi2stream.items():
        gpi_event_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip,\
            in_cue = gpi_cue_state[gpi])

elif stater.is_last_exit_from_reload() is False:
    for gpi, id in cf.gpi2stream.items():
        gpi_event_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip)
   
# Set-up reloader on file changes

reload_thread = Reloader(cf.WATCHED_FILES, linux=True,\
     before_reload= stater.save_gpi_state, gpi_event_dict = gpi_event_dict)
reload_thread.start()


# Setup GPIO inputs/outputs
    #Use Board pin numbering - etc. (12) in pinout command
# GPIO.setmode(GPIO.BCM)
#     #Setup GPIOs as inputs with PULL-UP
# for GPI in list(cf.gpi2stream):
#     GPIO.setup( GPI, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# # Tie callbacks to events

# for GPI in list(cf.gpi2stream):
#     GPIO.add_event_detect( GPI, GPIO.BOTH, callback = gpi_event_dict[GPI].\
#         start_stop_avail , bouncetime = 20)


if __name__ == '__main__':
    try:
        while(True):
            pass
    except KeyboardInterrupt:
        # GPIO.cleanup()
        pass