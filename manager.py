import os
import sys
import subprocess as subp
import loggers as lg
import time
import click as cl
from os.path import getmtime
import pyinquirer as pyq


AVAIL_MAIN_FILE = 'main.py'
# import PyInquirer as pyq

# TODO: Master script to
# 2) enable/disable autostart
# 3) Show output and logs
# 4) monitor (health check) the main script

control_log = lg.setup_logger('control_log', 'controller')

def get_proc_pid(name):
    return list(map(int,subp.check_output(["pidof", "-c", name]).split()))

def get_arg_pid(argument):
   return list(map(int,subp.check_output(["pgrep", "-f", argument]).split()))

def get_main_proc_pid():
    python_pids = get_proc_pid('python3')

    try:
        main_py_pids = get_arg_pid(AVAIL_MAIN_FILE)
    except subp.CalledProcessError as no_main_error:
        control_log.info('{} is not running'.format(AVAIL_MAIN_FILE))
        return 1
    else:
        python_main_py_pid = set(python_pids).intersection(main_py_pids)
        return python_main_py_pid.pop()
    

def is_avail_main_running():
    #Check if main program is running
    
    python_pids = get_proc_pid('python3')
    try:
        main_py_pids = get_arg_pid(AVAIL_MAIN_FILE)
    except subp.CalledProcessError as no_main_error:
        control_log.info('{} is not running'.format(AVAIL_MAIN_FILE))
        main_file_found = False
        return False
    else:
        main_file_found = True
    
    if main_file_found is True:
        python_main_py_pid = set(python_pids).intersection(main_py_pids)

        if python_main_py_pid:
            python_main_py_pid = python_main_py_pid.pop()
            control_log.info("{} pid is {}".format(AVAIL_MAIN_FILE, python_main_py_pid))
            return True
        else:
            control_log.info('{} python process is not running'.format(AVAIL_MAIN_FILE))
            return False


def start_avail_script():
    #Start the main avail script
    is_running = is_avail_main_running()
    
    if is_running is True:
        control_log.info('Ad avail script {} is already running'.format(AVAIL_MAIN_FILE))
        return 1
    
    os.system('sh run.sh')
    

def stop_avail_script():
    is_running = is_avail_main_running()

    if is_running is False:
        control_log.info('Ad avail script {} is not running'.format(AVAIL_MAIN_FILE))
        return 1

    main_proc_pid = get_main_proc_pid()
    subp.check_output(["kill", str(main_proc_pid)])
    

    control_log.info('Ad avail script {} with PID: {} was terminated'.format(AVAIL_MAIN_FILE, main_proc_pid))


def restart_avail_script():
    stop_avail_script()
    start_avail_script()


def read_main_log():
    main_log_file = lg.get_logger_fname('main')
    last_save_time = getmtime(main_log_file)
    with open(main_log_file, 'r') as log_file:
        lines = log_file.readlines()
        for line in lines:
            print(line, end=" ")
        line_count = len(lines)


    while(True):
        save_time = getmtime(main_log_file)

        if last_save_time != save_time:
            with open(main_log_file) as log_file:
                lines = log_file.readlines()
            new_lines = lines[line_count:]
            for line in new_lines:
                print(line, end=" ")

            line_count = len(lines)
            last_save_time = save_time
        time.sleep(1)


def enable_avaiL_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()
        bash_file.write('python3 {} &'.format(AVAIL_MAIN_FILE))

    control_log.info('Main avail script autostart enabled')

def disable_avail_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()

    control_log.info('Main avail script autostart disabled')



# inp = input("Start the bloody program!")
# start_avail_script()

# inp = input("Stop the bloody program!")
# stop_avail_script()

# inp = input("Read logging file")
# read_main_log()

inp = input("Enable autostart")
enable_avaiL_startup()

# inp = input("Disable autostart")
# disable_avail_startup()

while(True):
    print('Running')
    time.sleep(5)
    pass

