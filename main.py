#!/usr/bin/env python
import sys
import time
import importlib
import RPi.GPIO as GPIO

import elemental_api_class as liveapi
from s_av_ctrl import StreamAvailController as StreamAvailCtrl
from reloader import Reloader
from state_manager import StateManager
# from helpers import setup_logger
# sys.path.append('/home/pi/config')
import loggers as lg
import config as cf


# main_log = lg.setup_logger('main_logger','main')
main_log = lg.get_main_logger()
main_log.info('Starting Ad Avail Controller ver. 0.7')
stater = StateManager(cf.LAST_EXIT_FILE, cf.STATE_FILE)

def check_elemental_connection():
    global main_log
    live_api = liveapi.Elemental_api(cf.elemental_ip)
    try:
        response = live_api.list_live_events()
        if response.status_code != 200:
                raise Exception("Elemental server error: {}".format(response.status_code))
    except Exception as e:
        main_log.error('Error: {}'.format(e))


# Set-up state manager

# Make a new dict with GPIs as Keys and (class)StreamAvailCtrl as values
# Check wether last exit was from reload and load state if necessary
gpi_event_dict = {}
if stater.is_last_exit_from_reload() is True:
    gpi_cue_state = stater.load_gpi_state()
    main_log.info('Last exit: Reload')
    
    for gpi, id in cf.gpi2stream.items():
        gpi_event_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip,\
            in_cue = gpi_cue_state[gpi])

elif stater.is_last_exit_from_reload() is False:
    for gpi, id in cf.gpi2stream.items():
        gpi_event_dict[gpi] = StreamAvailCtrl(gpi, id, cf.elemental_ip, lock_interval=cf.min_av_dur)


main_log.info('State loaded')
main_log.info(gpi_event_dict['12'])
# Set-up reloader on file changes

reload_thread = Reloader(cf.WATCHED_FILES, linux=True,\
    before_reload= stater.save_gpi_state, gpi_event_dict = gpi_event_dict)
reload_thread.start()
main_log.info('Reloading enabled')

# Setup GPIO inputs/outputs
#     Use Board pin numbering - etc. (12) in pinout command
GPIO.setmode(GPIO.BCM)
#Setup GPIOs as inputs with PULL-UP
for gpi,id in cf.gpi2stream.items():
    print(gpi)
    GPIO.setup( int(gpi), GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Tie callbacks to events

for gpi,id in cf.gpi2stream.items():
    GPIO.add_event_detect( int(gpi), GPIO.BOTH, callback = gpi_event_dict[gpi].\
        start_stop_avail , bouncetime = 20)

# check_elemental_connection()



if __name__ == '__main__':
    try:
        while(True):
            gpi_event_dict['21'].in_cue = True
            main_log.info("Running")
            time.sleep(10)
            pass
    except KeyboardInterrupt:
        main_log.info('Exiting on keyboard interrupt\n')
        stater.save_last_exit(last_exit_state='Exit')
        pass