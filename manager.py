import os
import subprocess as subp
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
def get_proc_pid(name):
    return list(map(int,subp.check_output(["pidof", "-c", name]).split()))

def get_arg_pid(argument):
   return list(map(int,subp.check_output(["pgrep", "-f", argument]).split()))

def is_main_running():
    #Check if main program is running
    
    python_pids = get_proc_pid('python3')
    try:
        main_py_pids = get_arg_pid('main.py')
    except Exception as e:
        print(e)


#-- Test pgrep
# this_pid = os.getpid()
# print(this_pid)

# print(python_pids)
# print(main_py_pids)

# python_main_py_pid = set(python_pids).intersection(main_py_pids)
# print(python_main_py_pid)

is_main_running()


while(True):
    pass

# -- Start the main program from this process -- 
# inp = input("Start the bloody program!")
# process = subp.Popen(['python3','main.py'], stdout=subp.PIPE)
# print(process.communicate())
