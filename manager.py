import os
import sys
import subprocess as subp
import loggers as lg
import time
import click as cl
from os.path import getmtime
import PyInquirer as pyq


AVAIL_MAIN_FILE = 'main.py'
# import PyInquirer as pyq

# TODO: Master script to
# 4) monitor (health check) the main script
# 5) Menu

# Used universally through the program as "back one step" flag
EXIT_FLAG = 123

# Dicts of menu options - to avoid using strings in the whole program
mm_choices = {
    'ss_script': 'Start/Stop/Restart main avail script',
    'en_dis_auto': 'Enable/Disable autostart',
    'show_log': 'Show current log',
    'back': 'Exit the program'
}

ss_options = {
    'start': 'Start the main avail script',
    'stop': 'Stop the main avail script',
    'restart': 'Restart the script',
    'back': 'Back to main menu'
}

autostart_options = {
    'enable': 'Enable main script autostart',
    'disable': 'Disable main scritp autostart',
    'back': 'Back to main menu'
}

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

    return
    

def stop_avail_script():
    is_running = is_avail_main_running()

    if is_running is False:
        control_log.info('Ad avail script {} is not running'.format(AVAIL_MAIN_FILE))
        return 1

    main_proc_pid = get_main_proc_pid()
    subp.check_output(["kill", str(main_proc_pid)])
    

    control_log.info('Ad avail script {} with PID: {} was terminated'.format(AVAIL_MAIN_FILE, main_proc_pid))

    return 0


def restart_avail_script():
    stop_avail_script()
    start_avail_script()

    return 0


def read_main_log():
    main_log_file = lg.get_logger_fname('main')
    last_save_time = getmtime(main_log_file)
    print('\nPress CTRL+C to Exit')
    time.sleep(3)
    with open(main_log_file, 'r') as log_file:
        lines = log_file.readlines()
        for line in lines:
            print(line, end=" ")
        line_count = len(lines)


    while(True):
        try:
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
        except KeyboardInterrupt as e:
            break
    
    return 0


def enable_avaiL_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()
        bash_file.write('#!/bin/sh\n')
        bash_file.write('cd /Projects/gpi_0.7_hw_reworked/\n')
        bash_file.write('python3 {} &'.format(AVAIL_MAIN_FILE))

    control_log.info('Main avail script autostart enabled')

    return 0


def disable_avail_startup():
    with open('autostart.sh', 'w') as bash_file:
        bash_file.seek(0)
        bash_file.truncate()

    control_log.info('Main avail script autostart disabled')
    return 0

# ------ Menu functions --------------------------------
def main_menu():
    main_menu_promt = {
        'type': 'list',
        'name': 'main_choice',
        'message': 'Choose an option\n',
        'choices': [v for k,v in mm_choices.items()]
    }


    while(True):
        print('\n')
        mm_answers = pyq.prompt(main_menu_promt)

        if mm_answers['main_choice'] is mm_choices['back']:
            break
        
        elif mm_answers['main_choice'] is mm_choices['ss_script']:
            ss_menu()

        elif mm_answers['main_choice'] is mm_choices['en_dis_auto']:
            autostart_menu()

        elif mm_answers['main_choice'] is mm_choices['show_log']:
            read_main_log()


def ss_menu():
    ss_menu_promt = {
        'type': 'list',
        'name': 'start_stop',
        'message': '\nChoose an option\n',
        'choices': [v for k,v in ss_options.items()]
    }

    while (True):
        print('\n')
        ss_answers = pyq.prompt(ss_menu_promt)

        if ss_answers['start_stop'] is ss_options['back']:
            break

        elif ss_answers['start_stop'] is ss_options['start']:
            start_avail_script()

        elif ss_answers['start_stop'] is ss_options['stop']:
            stop_avail_script()

        elif ss_answers['start_stop'] is ss_options['restart']:
            restart_avail_script()


def autostart_menu():
    autostart_menu_promt = {
        'type': 'list',
        'name': 'enable_disable',
        'message': '\nChoose an option\n',
        'choices': [v for k,v in autostart_options.items()]
    }

    while (True):
        print('\n')
        autostart_answers = pyq.prompt(autostart_menu_promt)

        if autostart_answers['enable_disable'] is autostart_options['back']:
            break

        elif autostart_answers['enable_disable'] is autostart_options['enable']:
            enable_avaiL_startup()

        elif autostart_answers['enable_disable'] is autostart_options['disable']:
            disable_avail_startup()


# inp = input("Start the bloody program!")
# start_avail_script()

# inp = input("Stop the bloody program!")
# stop_avail_script()

# inp = input("Read logging file")
# read_main_log()

# inp = input("Enable autostart")
# enable_avaiL_startup()

# inp = input("Disable autostart")
# disable_avail_startup()

try:
    main_menu()
except KeyboardInterrupt:
    print('Will miss you')
finally:
    print('We are done!')

