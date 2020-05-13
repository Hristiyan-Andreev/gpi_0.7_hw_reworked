import os
import sys
import subprocess as subp
import loggers as lg
import time

AVAIL_MAIN_FILE = 'main.py'
# import click as cl
# import PyInquirer as pyq

# TODO: Master script to 
# 1) start/stop/restart the main.py
# 2) enable/disable autostart
# 3) Show output and logs
# 4) monitor (health check) the main script

# def check_status_main():
#     this_pid = os.getpid()
#     python_pids = get_pid('python3')
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
    #Check if the program is running
    is_running = is_avail_main_running()
    
    if is_running is True:
        control_log.info('Ad avail script {} is already running'.format(AVAIL_MAIN_FILE))
        return 1
    
    # process = subp.Popen(['python3',AVAIL_MAIN_FILE, '&'], stdout=subp.PIPE)
    # subp.check_output(["python3", AVAIL_MAIN_FILE, '&'])
    # control_log.info('Ad avail {} started with PID: {}'.format(AVAIL_MAIN_FILE, process.pid))

    # print(sys.executable)
    os.execl(sys.executable, sys.executable, 'main.py')
    # control_log.info('Ad avail {} started with PID: {}'.format(AVAIL_MAIN_FILE))
    

def stop_avail_script():
    is_running = is_avail_main_running()

    if is_running is False:
        control_log.info('Ad avail script {} is not running'.format(AVAIL_MAIN_FILE))
        return 1

    main_proc_pid = get_main_proc_pid()
    subp.check_output(["kill", str(main_proc_pid)])
    

    control_log.info('Ad avail script {} with PID: {} was terminated'.format(AVAIL_MAIN_FILE, main_proc_pid))


# is_avail_main_running()
inp = input("Start the bloody program!")
start_avail_script()

# inp = input("Stop the bloody program!")
# stop_avail_script()



while(True):
    print('Running')
    time.sleep(5)
    pass

# -- Start the main program from this process -- 
# inp = input("Start the bloody program!")
# process = subp.Popen(['python3','main.py'], stdout=subp.PIPE)
# print(process.communicate())
